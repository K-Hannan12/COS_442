import requests
import time
import random

while True:
    random_number = random.uniform(0.5, 1.5)
    time.sleep(random_number)
    try:
        response_from_worker = requests.get("http://worker:5000/")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to worker: {e}")
    