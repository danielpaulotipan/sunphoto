import time
import RPi.GPIO as GPIO
from pysolar.solar import *
import datetime
import pytz
from dateutil import tz
import Adafruit_ADS1x15
werstern = pytz.timezone('Asia/Manila')
# Initial Value

DIRalt = 20
STEPalt = 21
alt_lsp = -10       # Alt Limit Switch Position (degrees)

DIRazi = 19
STEPazi = 26
azi_lsp = 0.00      # Azi Limit Switch Position (degrees)


CW = 0
CCW = 1
MVA= 10 * 20        # Number of degrees * number of steps for 1 degree
step_count = 7200   # SPR
delay=.002          #.005

# Set GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIRalt, GPIO.OUT)
GPIO.setup(STEPalt, GPIO.OUT)
GPIO.setup(DIRazi, GPIO.OUT)
GPIO.setup(STEPazi, GPIO.OUT)
GPIO.setup(16,GPIO.IN)

adcqpd = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)


GAIN = 2/3

qpd_step_count = 1 #1 step is equal to .05 degree



#======================start of while loop=========================#

while True:
	values = [0]*4

	values[0] = adcqpd.read_adc(0, gain=GAIN)
	SUM= (values[0] * 0.1875)/1000   #sum

	values[1] = adcqpd.read_adc(1, gain=GAIN)
	UDQ= (values[1] * 0.1875)/1000   #alt


	values[2] = adcqpd.read_adc(2, gain=GAIN)
	LRQ = (values[2] * 0.1875)/1000

#-----------------Azimuth------------------#
	if SUM > 0.5:
		print (LRQ)
		azizero = 1.9

		if LRQ >azizero:
			GPIO.output(DIRazi,CCW)
			print("ccw")
			for x in range(qpd_step_count):
#				print (x)
				GPIO.output(STEPazi, GPIO.HIGH)
				time.sleep(delay)
				GPIO.output(STEPazi,GPIO.LOW)
				time.sleep(delay)
#		azi_mpos= azi_mpos + (qpd_step_count * 0.05)
#		print("Machine's current azimuth position = " + str(azi_mpos))

#		time.sleep(1)

		elif LRQ < azizero:
			GPIO.output(DIRazi,CW)
			print ("cw")
			for x in range(qpd_step_count):
#				print (x)
				GPIO.output(STEPazi, GPIO.HIGH)
				time.sleep(delay)
				GPIO.output(STEPazi,GPIO.LOW)
				time.sleep(delay)
#		azi_mpos= azi_mpos - (qpd_step_count * 0.05)
#		print("Machine's current azimuth position = " + str(azi_mpos))
#		time.sleep(1)

#-----------------Altitude------------------#
		altzero = 1.9
#		print (UDQ)
		if UDQ > altzero:
			GPIO.output(DIRalt,CW)
			print ("cw")
			for x in range(qpd_step_count):
				print (x)
				GPIO.output(STEPalt, GPIO.HIGH)
				time.sleep(delay)
				GPIO.output(STEPalt,GPIO.LOW)
				time.sleep(delay)
#		alt_mpos= alt_mpos + (qpd_step_count * 0.05)
#		print("Machine's current altitude position = " + str(alt_mpos))
#
#
#		time.sleep(1)
#
		elif UDQ < altzero:
			GPIO.output(DIRalt,CCW)
			print ("ccw")
			for x in range(qpd_step_count):
				print (x)
				GPIO.output(STEPalt, GPIO.HIGH)
				time.sleep(delay)
				GPIO.output(STEPalt,GPIO.LOW)
				time.sleep(delay)
#		alt_mpos= alt_mpos - (qpd_step_count * 0.05)
#		print("Machine's current altitude position = " + str(alt_mpos))
#		sleep(.5)

		time.sleep(.25)

	elif SUM <= 0.5:
		time.sleep(1)
		print("CLOUDY")		 
GPIO.cleanup()


