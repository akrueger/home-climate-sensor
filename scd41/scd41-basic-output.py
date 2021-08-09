import time
import math
import os
import board
import adafruit_scd4x

# --------- Settings ---------
USE_METRIC = os.environ.get("USE_METRIC", "FALSE")
MINUTES_BETWEEN_READS = float(os.environ.get("MINUTES_BETWEEN_READS", 0.08))
TEMPERATURE_OFFSET = float(os.environ.get("TEMPERATURE_OFFSET", 0))
HUMIDITY_OFFSET = float(os.environ.get("HUMIDITY_OFFSET", 0))
# ---------------------------------

# Uses board.SCL and board.SDA
i2c = board.I2C()
scd41 = adafruit_scd4x.SCD4X(i2c)

print("Altitude(m)", scd41.altitude)
# Set altitude to Austin, TX
scd41.altitude = 280
print("New Altitude(m)", scd41.altitude)

# scd41.set_ambient_pressure(1015)

# Sensor needs a moment to gather initial readings
scd41.start_periodic_measurement()
print("Waiting for first measurement....")

while True:
    if scd41.data_ready:
        co2 = scd41.CO2
        temperature_c = scd41.temperature + TEMPERATURE_OFFSET
        humidity = scd41.relative_humidity + HUMIDITY_OFFSET

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

        print("CO2: %d ppm" % co2)
        print("Humidity(%)", humidity)
        print("Dew Point(%)", dew_point)
    time.sleep(60 * MINUTES_BETWEEN_READS)
