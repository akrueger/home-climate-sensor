import time
import math
import os
import board
import adafruit_tmp117

# --------- Settings ---------
USE_METRIC = os.environ.get("USE_METRIC", "FALSE")
TEMPERATURE_OFFSET = float(os.environ.get("TEMPERATURE_OFFSET", 0))
# ---------------------------------

# Uses board.SCL and board.SDA
i2c = board.I2C()
tmp117 = adafruit_tmp117.TMP117(i2c)

# Sensor needs a moment to gather initial readings
time.sleep(1)

temperature_c = tmp117.temperature + TEMPERATURE_OFFSET

if USE_METRIC.lower() == "true":
    print("Temperature(C)", temperature_c)
else:
    temperature_f = format(temperature_c * 9.0 / 5.0 + 32.0, ".2f")
    print("Temperature(F)", temperature_f)
