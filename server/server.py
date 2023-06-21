from flask import Flask, request

from docker_manager import DockerManager


app = Flask(__name__)
manager = DockerManager()


@app.route('/job', methods=['POST'])
def handle_client_request():
    data = request.get_json()
    return manager.handle_request(data)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, threaded=True)
