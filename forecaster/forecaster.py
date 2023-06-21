from flask import Flask
import random

app = Flask(__name__)


@app.route('/predict/<container_id>', methods=['POST'])
def handle_client_request(container_id):
    # todo
    return [[[str(random.uniform(0.0001, 0.0002))]]]


if __name__ == '__main__':
    app.run(host='localhost', port=12345, threaded=True)
