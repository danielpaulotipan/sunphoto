#IMPORT MODULES
from time import sleep
import RPi.GPIO as GPIO
from pysolar.solar import *
import datetime
import pytz
from dateutil import tz

# Pysolar Values
werstern = pytz.timezone('Asia/Manila')
date = datetime.datetime.now(pytz.utc)

# Initial Value
DIR = 20
STEP = 21
CW = 0
CCW = 1
MVA= 10 * 20        # Number of degrees * number of steps for 1 degree
alt_lsp = -10      # Alt Limit Switch Position (degrees) 
step_count = 7200   # SPR
delay=.005          #.005

# Set GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(16,GPIO.IN)

#--------------------------------------- Finding Limit Switch

GPIO.output(DIR,CW)
for x in range(step_count):
	print (x)
	GPIO.output(STEP, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP,GPIO.LOW)
	sleep(delay)

	if (GPIO.input(16)):
		print("Button Pressed")
		break
sleep(.5)

#------------------------------------- Limit Switch Pressed

GPIO.output(DIR,CCW)
print("moving away from limit switch")
sleep(1)
for x in range(MVA):
	print (x)
	GPIO.output(STEP, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP,GPIO.LOW)
	sleep(delay)

#------------------------------------ Machine and Sun Position Determine

alt_mpos = alt_lsp + 10        # 10 because we move away from the limit switch position
alt_mpos = round(alt_mpos,1)
print("Machine's current altitude position = " + str(alt_mpos))

sun_cur_alt_pos = get_altitude(14.5653, 120.9929, date) # Pysolar module
sun_cur_alt_pos = round(sun_cur_alt_pos,1)
print("Sun's current altitude position = " + str(sun_cur_alt_pos))

sleep(5)

#----------------------------------- Move Machine to Current Sun Position

alt_mach_no_steps = (sun_cur_alt_pos - alt_mpos)*20         # Number of Steps to move to the Current Sun Position
#azi_mach_no_steps = round(azi_mach_no_steps,1)

GPIO.output(DIR,CCW)
for x in range(int(alt_mach_no_steps)):
        print (x)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP,GPIO.LOW)
        sleep(delay)

#---------------------------------- Update Machine Current Position

alt_mpos = sun_cur_alt_pos
print("Machine's current altitude position = " + str(alt_mpos))
print("Sun's current altitude position = " + str(sun_cur_alt_pos))

sleep(30)
print("--------------------------------------------------------------------")

date = datetime.datetime.now(pytz.utc)

sun_cur_alt_pos = get_altitude(14.5653, 120.9929, date) # Pysolar module
sun_cur_alt_pos = round(sun_cur_alt_pos,1)
print("Sun's current altitude position = " + str(sun_cur_alt_pos))

sleep(5)
print("Moving Machine...")
#----------------------------------- Move Machine to Current Sun Position

alt_mach_no_steps = (sun_cur_alt_pos - alt_mpos)*20         # Number of Steps to move to the Current Sun Position
#azi_mach_no_steps = round(azi_mach_no_steps,1)
print(alt_mach_no_steps)

GPIO.output(DIR,CCW)
for x in range(abs(int(alt_mach_no_steps))):
        print (x)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP,GPIO.LOW)
        sleep(delay)

#---------------------------------- Update Machine Current Position

alt_mpos = sun_cur_alt_pos
print("Machine's current altitude position = " + str(alt_mpos))
print("Sun's current altitude position = " + str(sun_cur_alt_pos))


GPIO.cleanup()


