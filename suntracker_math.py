#IMPORT MODULES
from time import sleep
import RPi.GPIO as GPIO
from pysolar.solar import *
import datetime
import pytz
from dateutil import tz

# Pysolar Values
werstern = pytz.timezone('Asia/Manila')

# Initial Value

DIRalt = 20
STEPalt = 21
alt_lsp = -10       # Alt Limit Switch Position (degrees)

DIRazi = xx                                                              
STEPazi = xx                                                              
azi_lsp = 0.00      # Azi Limit Switch Position (degrees)

CW = 0
CCW = 1
MVA= 10 * 20        # Number of degrees * number of steps for 1 degree
step_count = 7200   # SPR
delay=.005          #.005

# Set GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(16,GPIO.IN)                                                  

#---------------------------------------------------- Finding Limit Switch ------------------------------------#

#-------------------------------- Azimuth
GPIO.output(DIRazi,CCW)
for x in range(step_count):
	print (x)
	GPIO.output(STEPazi, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEPazi, GPIO.LOW)
	sleep(delay)

	if (GPIO.input(16)):
		print("Azimuth = 0")
		break
sleep(.5)

GPIO.output(DIR,CW)
print("Moving away from Azimuth limit switch")
sleep(1)
for x in range(MVA):
        print (x)
        GPIO.output(STEPazi, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEPazi,GPIO.LOW)
        sleep(delay)

print("Azimuth current position = 10")

#------------------------------ Altitude
GPIO.output(DIRalt,CW)
for x in range(step_count):
        print (x)
        GPIO.output(STEPalt, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEPalt, GPIO.LOW)
        sleep(delay)

        if (GPIO.input(x)):                 
		print("Altitude = 0")
                break
sleep(.5)

#----------------------------------- Altitude
GPIO.output(DIR,CCW)
print("Moving away from Altitude limit switch")
sleep(1)
for x in range(MVA):
        print (x)
        GPIO.output(STEPalt, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEPalt, GPIO.LOW)
        sleep(delay)

print("Altitude current position = 0")

#------------------------------------ Machine and Sun Position Determine ----------------------------------------#
#----------------------- First movement

#Get position values of Sun and Machine
# Get / Update Date and Time
date = datetime.datetime.now(pytz.utc)

# Get the Machine's Current Azimuth position
azi_mpos = azi_lsp + 10        # 10 because we move away from the limit switch position
azi_mpos = round(azi_mpos,1)
print("Machine's current azimuth position = " + str(azi_mpos))

# Get Sun's Current Azimuth position
sun_cur_azi_pos = get_azimuth(14.5653, 120.9929, date) # Pysolar module
sun_cur_azi_pos = round(sun_cur_azi_pos,1)
print("Sun's current azimuth position = " + str(sun_cur_azi_pos))


# Get the Machine's Current Altitude position
alt_mpos = alt_lsp + 10        # 10 because we move away from the limit switch position
alt_mpos = round(alt_mpos,1)
print("Machine's current altitude position = " + str(alt_mpos))

# Get the Sun's Current Altitude position
sun_cur_alt_pos = get_altitude(14.5653, 120.9929, date) # Pysolar module
sun_cur_alt_pos = round(sun_cur_alt_pos,1)
print("Sun's current altitude position = " + str(sun_cur_alt_pos))

# Check values
sleep(5)

#-------------- Move Machine to Current Sun Position
azi_mach_no_steps = (sun_cur_azi_pos - azi_mpos)*20         # Number of Steps to move to the Current Sun Position
GPIO.output(DIRazi,CW)
for x in range(int(azi_mach_no_steps)):
	print (x)
	GPIO.output(STEPazi, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEPazi,GPIO.LOW)
	sleep(delay)

alt_mach_no_steps = (sun_cur_alt_pos - alt_mpos)*20         # Number of Steps to move to the Current Sun Position
GPIO.output(DIRalt,CW)
for x in range(int(alt_mach_no_steps)):
	print (x)
	GPIO.output(STEPalt, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEPalt,GPIO.LOW)
                        sleep(delay)

#------------ Update Machine Current Position
azi_mpos = sun_cur_azi_pos
print("Machine's current azimuth position = " + str(azi_mpos))
print("Sun's current azimuth position = " + str(sun_cur_azi_pos))

alt_mpos = sun_cur_alt_pos
print("Machine's current altitude position = " + str(alt_mpos))
print("Sun's current altitude position = " + str(sun_cur_alt_pos))


#---------------------------- Start at 00:00 time
while True:
	now = datetime.datetime.now()
	time.sleep(60 - now.second - now.microsecond / 1e6)
	print(datetime.datetime.now())
	t_end = time.time() + 28

	while time.time() < t_end:

#-------------- Get position values of Sun and Machine
		# Get / Update Date and Time
		date = datetime.datetime.now(pytz.utc)

		# Get Sun's Current Azimuth position
		sun_cur_azi_pos = get_azimuth(14.5653, 120.9929, date) # Pysolar module
		sun_cur_azi_pos = round(sun_cur_azi_pos,1)
		print("Sun's current azimuth position = " + str(sun_cur_azi_pos))


		# Get the Sun's Current Altitude position
                sun_cur_alt_pos = get_altitude(14.5653, 120.9929, date) # Pysolar module
                sun_cur_alt_pos = round(sun_cur_alt_pos,1)
                print("Sun's current altitude position = " + str(sun_cur_alt_pos))

		# Check values
		sleep(5)

#-------------- Move Machine to Current Sun Position
		azi_mach_no_steps = (sun_cur_azi_pos - azi_mpos)*20         # Number of Steps to move to the Current Sun Position
		GPIO.output(DIRazi,CW)
		for x in range(int(azi_mach_no_steps)):
        		print (x)
        		GPIO.output(STEPazi, GPIO.HIGH)
        		sleep(delay)
        		GPIO.output(STEPazi,GPIO.LOW)
        		sleep(delay)

		alt_mach_no_steps = (sun_cur_alt_pos - alt_mpos)*20         # Number of Steps to move to the Current Sun Position
                GPIO.output(DIRalt,CW)
                for x in range(int(alt_mach_no_steps)):
                        print (x)
                        GPIO.output(STEPalt, GPIO.HIGH)
                        sleep(delay)
                        GPIO.output(STEPalt,GPIO.LOW)
                        sleep(delay)

#------------ Update Machine Current Position

		azi_mpos = sun_cur_azi_pos
		print("Machine's current azimuth position = " + str(azi_mpos))
		print("Sun's current azimuth position = " + str(sun_cur_azi_pos))

		alt_mpos = sun_cur_alt_pos
                print("Machine's current altitude position = " + str(alt_mpos))
                print("Sun's current altitude position = " + str(sun_cur_alt_pos))
