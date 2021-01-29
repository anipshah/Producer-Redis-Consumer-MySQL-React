from rq import Queue
from redis import Redis
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import json
import schedule
from typing import List
import os


def next_number():
    """
    Function to get next sequence number starting from 0
    """
    msg_n: int = 0
    while True:
        msg_n += 1
        yield msg_n


def produce(message_numbers: List[int], host: str):
    """
    Job function to run a job of sending 10 post requests
    :param: message_numbers: List[int]: list of message numbers
    :param: host: str: host url of consumer
    """

    consumer_url = f"{host}/send"

    headers = {'content-type': 'application/json'}
    session = requests.session()

    def send(session, consumer_url, payload, headers):
        """
        Function to do a post request
        """
        if payload:
            response = session.post(consumer_url, json.dumps(payload), headers=headers)

            if response.status_code == 200:
                return response.json()['message_no']
        else:
            print("Payload is empty.")

    # thread pool to send post request in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for i in message_numbers:
            sender_time = datetime.now()
            payload = {'message_no': i, 'transmission_time': sender_time.strftime("%Y-%m-%d %H:%M:%S.%f")}
            futures.append(executor.submit(send, session, consumer_url, payload, headers))
        # get result from the parallel tasks
        for future in as_completed(futures):
            print(f"sent message: {future.result()}")


if __name__ == '__main__':
    import main

    message_number = next_number()
    # Redis connection
    redis_host: str = os.environ['REDIS_HOST']
    redis_port: int = int(os.environ['REDIS_PORT'])
    redis_conn = Redis(host=redis_host, port=redis_port)
    host: str = os.environ['CONSUMER_HOST_URL']

    queue_name: str = os.environ['QUEUE_NAME']
    # initialize redis queue
    q = Queue(queue_name, connection=redis_conn)


    def message_job():
        """
        Function for starting a producer job
        """

        message_numbers = []
        # generate next 10 message numbers
        for i in range(0, 10):
            message_numbers.append(next(message_number))
        # add job into queue
        job = q.enqueue(main.produce, message_numbers, host)
        print(f"submitted job id: {job.id}")


    # schedule every 1 second
    schedule.every(1).seconds.do(message_job)
    while True:
        schedule.run_pending()
        time.sleep(0.5)
