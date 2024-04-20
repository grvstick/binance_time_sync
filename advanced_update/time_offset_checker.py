import time
import json
from pathlib import Path
from traceback import print_exc

from loguru import logger
import requests

TIME_SAMPLES = 10
OFFSET_DIR = "./time_offset"
Path(OFFSET_DIR).mkdir(exist_ok=True)

while True:
    samples: list[float] = []

    while len(samples) < TIME_SAMPLES:
        time.sleep(2)
        url = "https://api.binance.com/api/v1/time"
        start_time = time.time() * 1_000_000
        try:
            server_time = json.loads(requests.get(url).content)["serverTime"] * 1000
        except Exception:
            print_exc()
            continue
        end_time = time.time() * 1_000_000

        round_trip_latency = start_time - end_time
        server_time_latency = server_time - start_time
        expected_offset_us = (server_time_latency - round_trip_latency / 2)

        logger.debug(f"{expected_offset_us = }")
        samples.append(expected_offset_us)

    current_offset = int(sum(samples)//TIME_SAMPLES)
    logger.info(f"{current_offset = }")
    
    new_offset_path = Path(OFFSET_DIR).joinpath(f"{start_time}_{current_offset}.t_offset")
    
    with open(new_offset_path, "w") as fp:
        fp.write("New offset record")
    
    offset_file_list = sorted(Path(OFFSET_DIR).glob("*.t_offset"))

    if len(offset_file_list) > 10:
        offset_file_list[0].unlink()
        

    # print(int(t)-result["serverTime"]) 