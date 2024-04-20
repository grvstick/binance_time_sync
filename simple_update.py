import time
import binance

def update_time_offset(client: binance.Client):
    res = client.get_server_time()
    client.timestamp_offset = res['serverTime'] - int(time.time() * 1000)

client = binance.Client(api_key="my_api_key", private_key="my_private_key")
update_time_offset()

