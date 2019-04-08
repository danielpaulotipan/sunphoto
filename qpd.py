import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

Azi_Dir = 20
Azi_Step = 21

Alt_Dir = 19 
Alt_Step = 16

CW =1
CCW = 0
SPR= 7200
zero =1.755 #1.755  #volts (center of QPD)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Azi_Dir, GPIO.OUT)
GPIO.setup(Azi_Step, GPIO.OUT)
GPIO.setup(Alt_Dir, GPIO.OUT)
GPIO.setup(Alt_Step, GPIO.OUT)

adcqpd = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)


GAIN = 2/3

step_count = 20 #7200 steps / 360 degrees
delay=.005  #.005 
while True:
	values = [0]*4
	values[0] = adcqpd.read_adc(0, gain=GAIN)
	values[1] = adcqpd.read_adc(1, gain=GAIN)
        LRQ = (values[0] * 0.1875)/1000
        UDQ = (values[1] * 0.1875)/1000

       # print voltage
#-----------------Azimuth------------------#
	if LRQ > zero:
		GPIO.output(Azi_Dir,CW)
		for x in range(step_count):
			print (x)
			GPIO.output(Azi_Step, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(Azi_Step,GPIO.LOW)
			time.sleep(delay)

#	sleep(.5)

	elif LRQ < zero:
		GPIO.output(Azi_Dir,CCW)
		print "ccw"
		for x in range(step_count):
			print (x)
	      		GPIO.output(Azi_Step, GPIO.HIGH)
	        	time.sleep(delay)
	        	GPIO.output(Azi_Step,GPIO.LOW)
	        	time.sleep(delay)

#-----------------Altitude------------------#
        if UDQ > zero:
                GPIO.output(Alt_Dir,CW)
                for x in range(step_count):
                        print (x)
                        GPIO.output(Alt_Step, GPIO.HIGH)
                        time.sleep(delay)
                        GPIO.output(Alt_Step,GPIO.LOW)
                        time.sleep(delay)

#       sleep(.5)

        elif UDQ < zero:
                GPIO.output(Alt_Dir,CCW)
                print "ccw"
                for x in range(step_count):
                        print (x)
                        GPIO.output(Alt_Step, GPIO.HIGH)
                        time.sleep(delay)
                        GPIO.output(Alt_Step,GPIO.LOW)
                        time.sleep(delay)

	time.sleep(.1)

GPIO.cleanup()


