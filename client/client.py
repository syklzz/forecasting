import requests


def send_request(request_data):
    url = "http://localhost:8000"

    print(f'Request: {request_data}')
    response = requests.post(url, json=request_data)
    print(f'Response: {response.text}')


if __name__ == '__main__':
    print('Client started.')

    data = {'iterations': 503406033}
    send_request(data)
