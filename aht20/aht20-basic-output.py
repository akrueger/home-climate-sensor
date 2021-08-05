import time
import math
import os
import board
import adafruit_ahtx0

# --------- Settings ---------
USE_METRIC = os.environ.get("USE_METRIC", "FALSE")
TEMPERATURE_OFFSET = float(os.environ.get("TEMPERATURE_OFFSET", 0))
HUMIDITY_OFFSET = float(os.environ.get("HUMIDITY_OFFSET", 0))
# ---------------------------------

# Uses board.SCL and board.SDA
i2c = board.I2C()
aht20 = adafruit_ahtx0.AHTx0(i2c)

# Sensor needs a moment to gather initial readings
time.sleep(1)

temperature_c = aht20.temperature + TEMPERATURE_OFFSET
humidity = aht20.relative_humidity + HUMIDITY_OFFSET

# Magnus formula for dew point
b = 17.62
c = 243.12
gamma = (b * temperature_c / (c + temperature_c)) + math.log(humidity / 100)
dew_point = (c * gamma) / (b - gamma)

if USE_METRIC.lower() == "true":
    print("Temperature(C)", temperature_c)
else:
    temperature_f = format(temperature_c * 9.0 / 5.0 + 32.0, ".2f")
    print("Temperature(F)", temperature_f)

humidity = format(humidity, ".2f")
print("Humidity(%)", humidity)
print("Dew Point(%)", dew_point)
