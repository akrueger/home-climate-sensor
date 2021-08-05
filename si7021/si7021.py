import time
import math
import os
from busio import I2C
from board import SCL, SDA
import adafruit_si7021
from ISStreamer.Streamer import Streamer

# --------- Settings ---------
DEVICE_NAME = os.environ.get("BALENA_DEVICE_NAME_AT_INIT")
BUCKET_NAME = os.environ.get("INITIAL_STATE_BUCKET_NAME")
BUCKET_KEY = os.environ.get("INITIAL_STATE_BUCKET_KEY")
ACCESS_KEY = os.environ.get("INITIAL_STATE_ACCESS_KEY")
MINUTES_BETWEEN_READS = float(os.environ.get("MINUTES_BETWEEN_READS", 5))
USE_METRIC = os.environ.get("USE_METRIC")
TEMPERATURE_OFFSET = float(os.environ.get("TEMPERATURE_OFFSET", 0))
HUMIDITY_OFFSET = float(os.environ.get("HUMIDITY_OFFSET", 0))
# ---------------------------------

# Uses board.SCL and board.SDA
i2c = I2C(SCL, SDA)
si7021 = adafruit_si7021.SI7021(i2c)

streamer = Streamer(
    bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY
)

# Sensor needs a moment to gather initial readings
time.sleep(1)

while True:
    try:
        temperature_c = si7021.temperature + TEMPERATURE_OFFSET
        humidity = si7021.relative_humidity + HUMIDITY_OFFSET

        # Magnus formula for dew point
        b = 17.62
        c = 243.12
        gamma = (b * temperature_c / (c + temperature_c)) + math.log(humidity / 100)
        dew_point = (c * gamma) / (b - gamma)

    except RuntimeError:
        print("RuntimeError, trying again...")
        continue

    if USE_METRIC.lower() == "true":
        streamer.log(DEVICE_NAME + " Temperature(C)", temperature_c)
    else:
        temperature_f = format(temperature_c * 9.0 / 5.0 + 32.0, ".2f")
        streamer.log(DEVICE_NAME + " Temperature(F)", temperature_f)

    humidity = format(humidity, ".2f")
    streamer.log(DEVICE_NAME + " Humidity(%)", humidity)
    # streamer.log(DEVICE_NAME + " Dew Point(%)", dew_point)
    streamer.flush()
    time.sleep(60 * MINUTES_BETWEEN_READS)
