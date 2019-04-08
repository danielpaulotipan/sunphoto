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
zero=1.755 ###

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


#---------------------------------------------------- Finding Limit Switch ------------------------------------#

#-------------------------------- Azimuth
GPIO.output(DIRazi,CCW)
for x in range(step_count):
	print (x)
	GPIO.output(STEPazi, GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(STEPazi, GPIO.LOW)
	time.sleep(delay)

	if (GPIO.input(16)):
		print("Azimuth = 0")
		break
time.sleep(.5)

GPIO.output(DIRazi,CW)
print("Moving away from Azimuth limit switch")
time.sleep(1)
for x in range(MVA):
        print (x)
        GPIO.output(STEPazi, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEPazi,GPIO.LOW)
        time.sleep(delay)
azi_mpos= 10.0
print("Azimuth current position = 10")

#------------------------------ Altitude
GPIO.output(DIRalt,CW)
for x in range(step_count):
	print (x)
	GPIO.output(STEPalt, GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(STEPalt, GPIO.LOW)
	time.sleep(delay)

	if (GPIO.input(16)):
		print("Altitude = -10")
		break
time.sleep(.5)

#----------------------------------- Altitude
GPIO.output(DIRalt,CCW)
print("Moving away from Altitude limit switch")
time.sleep(1)
for x in range(MVA):
	print (x)
	GPIO.output(STEPalt, GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(STEPalt, GPIO.LOW)
	time.sleep(delay)

print("Altitude current position = 0") 
alt_mpos= -20.0

#------------------------------------ Machine and Sun Position Determine ----------------------------------------#
#----------------------- First movement

#Get position values of Sun and Machine
# Get / Update Date and Time
date = datetime.datetime.now(pytz.utc)

# Get the Machine's Current Azimuth position
azi_mpos = round(azi_mpos,1)
print("Machine's current azimuth position = " + str(azi_mpos))

# Get Sun's Current Azimuth position
sun_cur_azi_pos = get_azimuth(14.5653, 120.9929, date) # Pysolar module
sun_cur_azi_pos = round(sun_cur_azi_pos,1)
print("Sun's current azimuth position = " + str(sun_cur_azi_pos))


# Get the Machine's Current Altitude position
alt_mpos = round(alt_mpos,1)
print("Machine's current altitude position = " + str(alt_mpos))

# Get the Sun's Current Altitude position
sun_cur_alt_pos = get_altitude(14.5653, 120.9929, date) # Pysolar module
sun_cur_alt_pos = round(sun_cur_alt_pos,1)
print("Sun's current altitude position = " + str(sun_cur_alt_pos))

# Check values
time.sleep(5)

#-------------- Move Machine to Current Sun Position
azi_mach_no_steps = (sun_cur_azi_pos - azi_mpos)*20         # Number of Steps to move to the Current Sun Position
GPIO.output(DIRazi,CW)
for x in range(int(azi_mach_no_steps)):
	print (x)
	GPIO.output(STEPazi, GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(STEPazi,GPIO.LOW)
	time.sleep(delay)

altdiff = sun_cur_alt_pos - alt_mpos

alt_mach_no_steps = altdiff*20         # Number of Steps to move to the Current Sun Position

if altdiff < 0:

	GPIO.output(DIRalt,CW)
	for x in range(abs(int(alt_mach_no_steps))):
		print (x)
		GPIO.output(STEPalt, GPIO.HIGH)
		time.sleep(delay)
		GPIO.output(STEPalt,GPIO.LOW)
		time.sleep(delay)
elif altdiff > 0:

	GPIO.output(DIRalt,CCW)
	for x in range(abs(int(alt_mach_no_steps))):
		print (x)
		GPIO.output(STEPalt, GPIO.HIGH)
		time.sleep(delay)
		GPIO.output(STEPalt,GPIO.LOW)
		time.sleep(delay)



#------------ Update Machine Current Position
azi_mpos = sun_cur_azi_pos
print("Machine's current azimuth position = " + str(azi_mpos))
print("Sun's current azimuth position = " + str(sun_cur_azi_pos))

alt_mpos = sun_cur_alt_pos
print("Machine's current altitude position = " + str(alt_mpos))
print("Sun's current altitude position = " + str(sun_cur_alt_pos))

print("start of loop")

#======================start of while loop=========================#

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
		azi_mpos= azi_mpos + (qpd_step_count * 0.05)
		print("Machine's current azimuth position = " + str(azi_mpos))

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
		azi_mpos= azi_mpos - (qpd_step_count * 0.05)
		print("Machine's current azimuth position = " + str(azi_mpos))
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
		alt_mpos= alt_mpos + (qpd_step_count * 0.05)
		print("Machine's current altitude position = " + str(alt_mpos))


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
		alt_mpos= alt_mpos - (qpd_step_count * 0.05)
		print("Machine's current altitude position = " + str(alt_mpos))
		sleep(.5)



		time.sleep(1)

GPIO.cleanup()


