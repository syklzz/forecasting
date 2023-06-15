from datetime import datetime

storage = []


def handler(event, context):
    iterations = event['iterations']
    container_index = event['container_index']

    start_time = datetime.now()
    total = task(iterations)
    end_time = datetime.now()

    record = (container_index, start_time, end_time)
    storage.append(record)  # todo save in database

    return total


def task(iterations):
    total = 0
    for i in range(iterations):
        total = (total + i) % 100
    return total
