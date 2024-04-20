# time_offset_checker.py should be running on background

from pathlib import Path


import binance


OFFSET_DIR = "./time_offset"

def get_latest_offset():
    offset_files = sorted(Path(OFFSET_DIR).glob("*.t_offset"))
    if not offset_files:
        print("time offset not ready!!")
        return 0
    
    return int(offset_files[-1].stem.split("_")[-1]) // 1000



latest_offset = get_latest_offset()
print(f"{latest_offset = }")


client = binance.Client(api_key="my_api_key", private_key="my_private_key")
#update client timestamp offset as needed
client.timestamp_offset = latest_offset
