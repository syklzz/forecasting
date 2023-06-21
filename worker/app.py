from flask import Flask, request
import numpy as np
from numpy.linalg import LinAlgError

app = Flask(__name__)


def handle_request(data):
    for job in data:
        iterations, matrix_size = job['iterations'], job['size']
        for i in range(iterations):
            try:
                np.linalg.inv(np.random.randint(-10, 10, size=(matrix_size, matrix_size)))
            except LinAlgError:
                return 'Error: singular matrix'
    return 'Success'


@app.route('/', methods=['POST'])
def handle_client_request():
    data = request.get_json()
    return handle_request(data)


if __name__ == "__main__":
    app.run(threaded=True)
