import logging
import os
from redis import Redis
import requests
import time
from flask import Flask
import threading
import random

app = Flask(__name__)

DEBUG = os.environ.get("DEBUG", "").lower().startswith("y")

log = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)


redis = Redis("redis")


def get_random_bytes():
    r = requests.get("http://rng/32")
    return r.content


def hash_bytes(data):
    r = requests.post("http://hasher/",
                      data=data,
                      headers={"Content-Type": "application/octet-stream"})
    hex_hash = r.text
    return hex_hash


def work_loop(interval=1):
    deadline = 0
    loops_done = 0
    global flag
        
    while True:
        # If flag is true then it will sleep
        if flag:
            random_sleep = random.randint(1,5)
            log.info(f'Sleeping for {random_sleep} seconds')
            time.sleep(random_sleep)
            flag = False
        if time.time() > deadline:
            log.info("{} more units of work done, updating hash counter"
                     .format(loops_done))
            redis.incrby("hashes", loops_done)
            loops_done = 0
            deadline = time.time() + interval
        work_once()
        loops_done += 1


def work_once():
    log.debug("Doing one unit of work")
    time.sleep(0.1)
    random_bytes = get_random_bytes()
    hex_hash = hash_bytes(random_bytes)
    if not hex_hash.startswith('0'):
        log.debug("No coin found")
        return
    log.info("Coin found: {}...".format(hex_hash[:8]))
    created = redis.hset("wallet", hex_hash, random_bytes)
    if not created:
        log.info("We already had that coin")

#Global flag
flag = False

# This is the worker thread
def work():
    while True:
            try:
                work_loop()
            except:
                log.exception("In work loop:")
                log.error("Waiting 10s and restarting.")
                time.sleep(10)


# This is the route that co-worker will call
@app.route('/')
def getFlagFromWorker():
    global flag
    flag = True
    return "OK"


if __name__ == "__main__":
    threading.Thread(target=work).start()
    app.run(host='0.0.0.0',port=5000, threaded=True)


