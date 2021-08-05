import time
import math
import os
import board
import adafruit_tmp117
from ISStreamer.Streamer import Streamer

# --------- Settings ---------
DEVICE_NAME = os.environ.get("BALENA_DEVICE_NAME_AT_INIT")
BUCKET_NAME = os.environ.get("INITIAL_STATE_BUCKET_NAME")
BUCKET_KEY = os.environ.get("INITIAL_STATE_BUCKET_KEY")
ACCESS_KEY = os.environ.get("INITIAL_STATE_ACCESS_KEY")
MINUTES_BETWEEN_READS = float(os.environ.get("MINUTES_BETWEEN_READS", 5))
USE_METRIC = os.environ.get("USE_METRIC")
TEMPERATURE_OFFSET = float(os.environ.get("TEMPERATURE_OFFSET", 0))
# ---------------------------------

# Uses board.SCL and board.SDA
i2c = board.I2C()
tmp117 = adafruit_tmp117.TMP117(i2c)

streamer = Streamer(
    bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY
)

# Sensor needs a moment to gather initial readings
time.sleep(1)

while True:
    try:
        temperature_c = tmp117.temperature + TEMPERATURE_OFFSET

    except RuntimeError:
        print("RuntimeError, trying again...")
        continue

    if USE_METRIC.lower() == "true":
        streamer.log(DEVICE_NAME + " Temperature(C)", temperature_c)
    else:
        temperature_f = format(temperature_c * 9.0 / 5.0 + 32.0, ".2f")
        streamer.log(DEVICE_NAME + " Temperature(F)", temperature_f)

    streamer.flush()
    time.sleep(60 * MINUTES_BETWEEN_READS)
