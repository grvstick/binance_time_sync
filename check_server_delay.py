import time
import json
from traceback import print_exc

from loguru import logger
import requests

TIME_SAMPLES = 10

while True:
    time.sleep(1)
    url = "https://api.binance.com/api/v3/time"
    req_start_time = time.time() * 1_000
    try:
        server_time = json.loads(requests.get(url).content)["serverTime"]
    except Exception:
        print_exc()
        continue
    req_end_time = time.time() * 1_000
    
    server_vs_pc = round(server_time - req_start_time)
    round_trip_latency = round(req_end_time - req_start_time)
    real_time_difference = round(server_time - (req_start_time + round_trip_latency / 2))

    
    logger.info(f"\n{server_vs_pc = }ms\n{round_trip_latency = }ms\n{real_time_difference = }ms")