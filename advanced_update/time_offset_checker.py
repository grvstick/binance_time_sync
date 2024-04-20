import time
import json
from pathlib import Path
from traceback import print_exc

from loguru import logger
import requests

TIME_SAMPLES = 10
OFFSET_DIR = "./time_offset"
Path(OFFSET_DIR).mkdir(exist_ok=True)


def record_offset_to_file(current_offset_ms: int):
    new_offset_path = Path(OFFSET_DIR).joinpath(f"{time()}_{current_offset_ms}.t_offset")
    
    with open(new_offset_path, "w") as fp:
        fp.write("New offset record")
    
    offset_file_list = sorted(Path(OFFSET_DIR).glob("*.t_offset"))

    if len(offset_file_list) > 10:
        offset_file_list[0].unlink()
        

while True:
    samples: list[float] = []

    while len(samples) < TIME_SAMPLES:
        time.sleep(1)
        url = "https://api.binance.com/api/v3/time"
        req_start_time = time.time() * 1_000
        try:
            server_time = json.loads(requests.get(url).content)["serverTime"]
        except Exception:
            print_exc()
            continue
        req_end_time = time.time() * 1_000
        # logger.info(f"{server_time = }")

        request_delay = (req_end_time - req_start_time) / 2
        offset = round(server_time - req_start_time)
        # account for request delay if you want absolute precision
        # offset = round(server_time - req_start_time + request_delay)

        samples.append(offset)

    current_offset = round(sum(samples)/TIME_SAMPLES)
    logger.info(f"{current_offset = }")
    record_offset_to_file()
