import docker
import docker.errors
import requests
import threading


class DockerManager:
    def __init__(self, containers_count):
        self.client = docker.from_env()
        self.active_containers_count = 0
        self.selected_container = 0
        self.containers_state = [threading.Semaphore()] * containers_count
        self.lock = threading.Lock()
        self.url = 'http://localhost:{}/2015-03-31/functions/function/invocations'
        self.base_port = 9000
        self.update_active_containers(1)

    def start_container(self, container_name):
        try:
            self.client.containers.get(container_name).start()
            print(f'Container {container_name} started successfully. '
                  f'Number of running containers: {self.active_containers_count}.')
        except docker.errors.NotFound:
            print(f'Container {container_name} not found.')
        except docker.errors.APIError as e:
            print(f'Failed to start container {container_name}: {e}')

    def stop_container(self, container_name):
        try:
            self.client.containers.get(container_name).stop()
            print(f'Container {container_name} stopped successfully. '
                  f'Number of running containers: {self.active_containers_count}.')
        except docker.errors.NotFound:
            print(f'Container {container_name} not found.')
        except docker.errors.APIError as e:
            print(f'Failed to stop container {container_name}: {e}')

    def handle_request(self, data):
        with self.lock:
            if self.active_containers_count == 0:
                return 'There are no running containers.'
            if self.selected_container > self.active_containers_count:
                self.selected_container = 0
            selected_container = self.selected_container
            self.selected_container = (selected_container + 1) % self.active_containers_count
            self.containers_state[selected_container].acquire()

        print(f'Request was redirected to lambda_{selected_container}.')
        data['container_index'] = selected_container
        response = requests.post(self.url.format(self.base_port + selected_container), json=data).text
        self.containers_state[selected_container].release()

        return response

    def update_active_containers(self, active_containers):
        if self.active_containers_count < active_containers:
            for i in range(self.active_containers_count, active_containers):
                with self.lock:
                    self.active_containers_count += 1
                    self.start_container(f'lambda_{i}')
        elif self.active_containers_count > active_containers:
            for i in range(self.active_containers_count - 1, active_containers - 1, -1):
                with self.lock:
                    self.active_containers_count -= 1
                with self.containers_state[i]:
                    self.stop_container(f'lambda_{i}')
