#!/usr/bin/python
# Test file for reading and sending values to AT&T M2X

APIKEY = '6b3221d6f7e1e3d9828acd73502ae0b4'
DEVICEID = '51b5e0bee3a7584252b324a55b9e1785'

import time
import Adafruit_BMP.BMP085 as BMP085
from m2x.client import M2XClient

sample_rate = 60.0 # in seconds as float
s_bmp085 = BMP085.BMP085()
s_bmp085 = BMP085.BMP085(busnum=1)
m2xclient = M2XClient(key=APIKEY)
device = m2xclient.device(DEVICEID)
stream_f = device.streams()[0]
stream_mb = device.streams()[1]

def DelayUntilNextPeriod(Period_Length):
	offset = time.time() % float(Period_Length)
	return Period_Length - offset

#main
print 'Running. Waiting for {0} second mark.'.format(sample_rate)
for i in range(0,9):
	time.sleep(DelayUntilNextPeriod(sample_rate))
	print 'Timestamp: {0}'.format(time.asctime(time.localtime(time.time())))
	temp = s_bmp085.read_temperature()
	f = ((temp * 1.8) + 32)
	f = float(format(f, '.1f'))
	pressure = s_bmp085.read_pressure()
	mb = pressure * 0.01
	print 'Temp ({0}) written as {1}'.format(temp, f)
	stream_f.add_value(f)
	print 'Pressure ({0}) written as {1}'.format(pressure, mb)
	stream_mb.add_value(mb)
	i += 1

