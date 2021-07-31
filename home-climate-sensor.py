import time
import math
import board
from adafruit_bme280 import basic as adafruit_bme280
from ISStreamer.Streamer import Streamer

# --------- Settings ---------
SENSOR_NAME = "os.environ.get('SENSOR_NAME')"
BUCKET_NAME = "os.environ.get('INITIAL_STATE_BUCKET_NAME')"
BUCKET_KEY = "os.environ.get('INITIAL_STATE_BUCKET_KEY')"
ACCESS_KEY = "os.environ.get('INITIAL_STATE_ACCESS_KEY')"
MINUTES_BETWEEN_READS = 5
METRIC_UNITS = False
# ---------------------------------

# Uses board.SCL and board.SDA
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

streamer = Streamer(
    bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY
)

# Sensor needs a moment to gather initial readings
time.sleep(1)

while True:
    try:
        temperature_c = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure

        # Magnus formula for dew point
        b = 17.62
        c = 243.12
        gamma = (b * temperature_c / (c + temperature_c)) + math.log(humidity / 100)
        dew_point = (c * gamma) / (b - gamma)

    except RuntimeError:
        print("RuntimeError, trying again...")
        continue

    if METRIC_UNITS:
        streamer.log(SENSOR_NAME + " Temperature(C)", temperature_c)
    else:
        temperature_f = format(temperature_c * 9.0 / 5.0 + 32.0, ".2f")
        streamer.log(SENSOR_NAME + " Temperature(F)", temperature_f)
        humidity = format(humidity, ".2f")
        streamer.log(SENSOR_NAME + " Humidity(%)", humidity)
        streamer.log(SENSOR_NAME + " Dew Point(%)", dew_point)
        streamer.flush()
        time.sleep(60 * MINUTES_BETWEEN_READS)
