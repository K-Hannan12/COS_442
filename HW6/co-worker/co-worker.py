import requests
import time
import random
import logging
import os


DEBUG = os.environ.get("DEBUG", "").lower().startswith("y")

log = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

def co_work_loop():
    while True:
        random_number = random.uniform(0.5, 1.5)
        time.sleep(random_number)
        try:
            response_from_worker = requests.get("http://worker:5000/")
            log.info(f"Response from worker: {response_from_worker.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to worker: {e}")


co_work_loop()
