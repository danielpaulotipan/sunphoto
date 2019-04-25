import RPi.GPIO as GPIO
from pysolar.solar import *
import datetime
import pytz
from dateutil import tz
import Adafruit_ADS1x15
werstern = pytz.timezone('Asia/Manila')
# Initial Value
from time import sleep
import sys, tty, termios, time
import time

DIRalt = 20
STEPalt = 21
DIRazi = 19
STEPazi = 26
CW = 0
CCW = 1

delay = 0.002

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIRalt, GPIO.OUT)
GPIO.setup(STEPalt, GPIO.OUT)
GPIO.setup(DIRazi, GPIO.OUT)
GPIO.setup(STEPazi, GPIO.OUT)

adcqpd = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

GAIN = 2/3

qpd_step_count = 5 #1 step is equal to .05 degree

# ====================================================== Program Start / Manual Alignment


def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

while True:
	char = getch()

	if(char == "d"):
		print("D/Right")
		GPIO.output(DIRazi,CW)
		for x in range(5):
			#print (x)
			GPIO.output(STEPazi, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPazi, GPIO.LOW)
			time.sleep(delay)

	if(char == "a"):
		print("A/Left")
		GPIO.output(DIRazi,CCW)
		for x in range(5):
			#print (x)
			GPIO.output(STEPazi, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPazi, GPIO.LOW)
			time.sleep(delay)

	if(char == "w"):
		print("W/Up")
		GPIO.output(DIRalt,CCW)
		for x in range(5):
			#print (x)
			GPIO.output(STEPalt, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPalt, GPIO.LOW)
			time.sleep(delay)

	if(char == "s"):
		print("S/Down")
		GPIO.output(DIRalt,CW)
		for x in range(5):
 			#print (x)
 			GPIO.output(STEPalt, GPIO.HIGH)
 			time.sleep(delay)
 			GPIO.output(STEPalt, GPIO.LOW)
 			time.sleep(delay)


	if(char == "x"):
		print("Aligned")


		#Get position values of Sun and Machine
		# Get / Update Date and Time
		date = datetime.datetime.now(pytz.utc)


		# Get Sun's Current Azimuth position
		sun_cur_azi_pos = get_azimuth(14.5653, 120.9929, date) # Pysolar module
		sun_cur_azi_pos = round(sun_cur_azi_pos,1)
		print("Sun's current azimuth = " + str(sun_cur_azi_pos))



		# Get the Sun's Current Altitude position
		sun_cur_alt_pos = get_altitude(14.5653, 120.9929, date) # Pysolar module
		sun_cur_alt_pos = round(sun_cur_alt_pos,1)
		print("Sun's current altitude = " + str(sun_cur_alt_pos))

		# Machine Position 
		mach_cur_azi_pos = sun_cur_azi_pos 
		print("Machine's current azimuth = " + str(sun_cur_azi_pos))

		mach_cur_alt_pos = sun_cur_alt_pos
		print("Machine's current altitude = " + str(sun_cur_alt_pos))

		# Check values
		break
		time.sleep(5)

while True:

	values = [0]*4
	values[0] = adcqpd.read_adc(0, gain=GAIN)
	values[1] = adcqpd.read_adc(1, gain=GAIN)
	LRQ = (values[0] * 0.1875)/1000
	UDQ = (values[1] * 0.1875)/1000

       # print voltage
#-----------------Azimuth------------------#
	azizero = 1.930

	if LRQ >azizero:
		GPIO.output(DIRazi,CCW)
		for x in range(qpd_step_count):
			print (x)
			GPIO.output(STEPazi, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPazi,GPIO.LOW)
			time.sleep(delay)

		time.sleep(1)

	elif LRQ < azizero:
		GPIO.output(DIRazi,CW)
		print ("ccw")
		for x in range(qpd_step_count):
			print (x)
			GPIO.output(STEPazi, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPazi,GPIO.LOW)
			time.sleep(delay)
		time.sleep(1)

#-----------------Altitude------------------#
	altzero = 1.013

	if UDQ > altzero:
		GPIO.output(DIRalt,CW)
		for x in range(qpd_step_count):
			print (x)
			GPIO.output(STEPalt, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPalt,GPIO.LOW)
			time.sleep(delay)


		time.sleep(1)

	elif UDQ < altzero:
		GPIO.output(DIRalt,CCW)
		print ("ccw")
		for x in range(qpd_step_count):
			print (x)
			GPIO.output(STEPalt, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPalt,GPIO.LOW)
			time.sleep(delay)
		sleep(.5)



		time.sleep(1)

GPIO.cleanup()
