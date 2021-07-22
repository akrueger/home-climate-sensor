import time
import math
import board
from adafruit_bme280 import basic as adafruit_bme280

# Uses board.SCL and board.SDA
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

temp = bme280.temperature
humid = bme280.humidity
pressure = bme280.pressure

# Magnus formula
b = 17.62
c = 243.12
gamma = (b * temp / (c + temp)) + math.log(humid / 100)
dew_point = (c * gamma) / (b - gamma)

# Sensor needs a moment to gather initial readings
time.sleep(1)

print("\nTemperature: %0.1f C" % temp)
print("\nHumidity: %0.1f %%" % humid)
print("\nDew Point: %0.1f %%" % dew_point)
print("\nPressure: %0.1f hPa" % pressure)