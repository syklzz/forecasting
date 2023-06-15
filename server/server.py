from flask import Flask, request

from docker_manager import DockerManager


app = Flask(__name__)
manager = DockerManager(5)


@app.route('/', methods=['POST'])
def handle_client_request():
    data = request.get_json()
    return manager.handle_request(data)


@app.route('/lambda', methods=['POST'])
def handle_forecaster_request():
    data = request.get_json()
    manager.update_active_containers(data['active_containers'])
    return 'Success'


if __name__ == '__main__':
    app.run(host='localhost', port=8000, threaded=True)
