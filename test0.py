#!/usr/bin/python
# Test file for reading and sending values to AT&T M2X

APIKEY = '6b3221d6f7e1e3d9828acd73502ae0b4'
DEVICEID = '51b5e0bee3a7584252b324a55b9e1785'

import time
import Adafruit_BMP.BMP085 as BMP085
from m2x.client import M2XClient
import RPi.GPIO as GPIO
import logging

sample_rate = 300.0 # in seconds as float
isRunningLED = 17
logging.basicConfig(filename='test0.log',level=logging.WARNING)
s_bmp085 = BMP085.BMP085()
s_bmp085 = BMP085.BMP085(busnum=1)
m2xclient = M2XClient(key=APIKEY)
device = m2xclient.device(DEVICEID)
stream_f = device.streams()[0]
stream_mb = device.streams()[1]
GPIO.setmode(GPIO.BCM)
GPIO.setup(isRunningLED, GPIO.OUT)

def DelayUntilNextPeriod(Period_Length):
	offset = time.time() % float(Period_Length)
	return Period_Length - offset

#main
GPIO.output(isRunningLED, 1)
print 'Running. Waiting for next {0} second mark.'.format(sample_rate)

try:
	for i in range(0,1727):
		time.sleep(DelayUntilNextPeriod(sample_rate))
		print '{0}: Timestamp: {1}'.format(i, time.asctime(time.localtime(time.time())))
		temp = s_bmp085.read_temperature()
		f = ((temp * 1.8) + 32)
		f = round(f, 1)
		pressure = s_bmp085.read_pressure()
		mb = pressure * 0.01
		print 'Temp ({0}) written as {1}'.format(temp, f)
		stream_f.add_value(f)
		#time.sleep(1)
		print 'Pressure ({0}) written as {1}'.format(pressure, mb)
		stream_mb.add_value(mb)
		alt_m = s_bmp085.read_altitude()
		print 'Altitude ({0:0.4f} m; {1:0.2f} ft) not written'.format(alt_m, alt_m * 3.2808)
		i += 1
except:
	logging.warning(sys.exc_info()[0])


finally:
	GPIO.cleanup()
