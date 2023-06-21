import requests
import threading


def send_request():
    url = "http://localhost:8000/job"
    request_data = [
        {'iterations': 5, 'size': 100},
        {'iterations': 2, 'size': 1000},
        {'iterations': 3, 'size': 3000}
    ]

    print(f'Request: {request_data}')
    response = requests.post(url, json=request_data)
    print(f'Response: {response.text}')


if __name__ == '__main__':
    print('Client started.')

    threads = []

    for _ in range(5):
        thread = threading.Thread(target=send_request)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
