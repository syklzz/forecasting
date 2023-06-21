import docker
import docker.errors
import requests
import threading
import concurrent.futures


class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.max_cpu_usage = 0.05
        self.min_cpu_usage = 0.02
        self.max_containers = 5
        self.active_containers = 3
        self.selected_container = 0
        self.lock = threading.Lock()
        self.worker_url = 'http://localhost:{}'
        self.worker_base_port = 9000
        self.forecaster_url = 'http://localhost:12345/predict/{}'
        self.update_active_containers()

    def handle_request(self, data):
        with self.lock:
            if self.selected_container > self.active_containers:
                self.selected_container = 0
            selected_container = self.selected_container
            self.selected_container = (selected_container + 1) % self.active_containers

        print(f'Request was redirected to worker_{selected_container}.')
        return requests.post(self.worker_url.format(self.worker_base_port + selected_container), json=data).text

    def get_current_cpu_usage(self, containers):
        result = []
        for container_id in containers:
            container = self.client.containers.get(f'worker_{container_id}')
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            system_cpu_usage = stats['cpu_stats']['system_cpu_usage']
            result.append((cpu_usage / system_cpu_usage) * 100)
        return result

    def send_request_to_forecaster(self, container_id):
        container = self.client.containers.get(f'worker_{container_id}')
        url = self.forecaster_url.format(container.id)
        return float(requests.get(url).text)

    def get_future_cpu_usage(self, containers):
        result = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.send_request_to_forecaster, container_id) for container_id in containers]
            for future in concurrent.futures.as_completed(futures):
                result.append(future.result())
        return result

    def get_active_containers(self):
        containers = [i for i in range(self.active_containers)]
        future_cpu_usage = self.get_future_cpu_usage(containers)
        current_cpu_usage = self.get_current_cpu_usage(containers)
        overloaded_containers = sum(future_cpu_usage[i] > 2 * current_cpu_usage[i] for i in range(self.active_containers))
        inactive_containers = sum(2 * future_cpu_usage[i] < current_cpu_usage[i] for i in range(self.active_containers))
        active_containers = self.active_containers + overloaded_containers - inactive_containers
        return max(1, min(active_containers, self.max_containers))

    def update_active_containers(self):
        threading.Timer(10.0, self.update_active_containers).start()
        active_containers = self.get_active_containers()
        with self.lock:
            self.active_containers = active_containers
            print(f'Number of active containers: {self.active_containers}.')
