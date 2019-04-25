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
delay = 0.002

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIRalt, GPIO.OUT)
GPIO.setup(STEPalt, GPIO.OUT)
GPIO.setup(DIRazi, GPIO.OUT)
GPIO.setup(STEPazi, GPIO.OUT)

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
		GPIO.output(DIRazi,1)
		for x in range(20):
                        #print (x)
			GPIO.output(STEPazi, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPazi, GPIO.LOW)
			time.sleep(delay)

		

	if(char == "a"):
		print("A/Left")
		GPIO.output(DIRazi,0)
		for x in range(20):
			#print (x)
			GPIO.output(STEPazi, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPazi, GPIO.LOW)
			time.sleep(delay)


	if(char == "w"):
		print("W/Up")
		GPIO.output(DIRalt,1)
		for x in range(20):
			#print (x)
			GPIO.output(STEPalt, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(STEPalt, GPIO.LOW)
			time.sleep(delay)

	if(char == "s"):
		print("S/Down")
		GPIO.output(DIRalt,0)
		for x in range(20):
 			#print (x)
 			GPIO.output(STEPalt, GPIO.HIGH)
 			time.sleep(delay)
 			GPIO.output(STEPalt, GPIO.LOW)
 			time.sleep(delay)



	if(char == "x"):
		print("Program exit")
		break

