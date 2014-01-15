#!/usr/bin/python
# Filename: Local.py
# Support for ProjectCuracao
# MiloCreek JS MiloCreek
# Version 2.0  11/4/2013
#
# Local Execute Objects for RasPiConnect  
# to add Execute objects, modify this file 
#
#
#
# RasPiConnectServer interface constants

REMOTE_WEBVIEW_UITYPE = 1
ACTION_BUTTON_UITYPE = 16
FEEDBACK_ACTION_BUTTON_UITYPE = 17
SINGLE_LED_DISPLAY_UITYPE = 32
SPEEDOMETER_UITYPE = 64
VOLTMETER_UITYPE = 128
BARMETER_UITYPE = 129
SERVER_STATUS_UITYPE = 256
PICTURE_REMOTE_WEBVIEW_UITYPE = 512
LABEL_UITYPE = 1024
FM_BLINK_LED_UITYPE = 2048
TEXT_DISPLAY_UITYPE = 4096
TOGGLE_SWITCH_UITYPE = 33
SEND_TEXT_UITYPE = 34
SOUND_ALARM_UITYPE = 35


# system imports
import sys
import subprocess
import time
import RPi.GPIO as GPIO
import math
import re

# from ProjectCuracao
sys.path.append('/home/pi/ProjectCuracao/main/hardware')
sys.path.append('/home/pi/ProjectCuracao/main/actions')
sys.path.append('/home/pi/ProjectCuracao/main/util')
sys.path.append('/home/pi/ProjectCuracao/main/datacollect')
sys.path.append('/home/pi/ProjectCuracao/main/config')

import useCamera
import hardwareactions
import util
import getArduinoLog

# Check for user imports
try:
	import conflocal as conf
except ImportError:
	import conf


# end of Project Curacao files

import MySQLdb as mdb

from luxmeter import Luxmeter
from Subfact_ina219 import INA219

from Adafruit_ADS1x15 import ADS1x15
from Adafruit_BMP085 import * 
# RasPiConnectImports

import Config
import Validate
import BuildResponse 

def ExecuteUserObjects(objectType, element):

	# Example Objects

	# fetch information from XML for use in user elements

	#objectServerID is the RasPiConnect ID from the RasPiConnect App

       # find the interface object type
        objectServerID = element.find("./OBJECTSERVERID").text
        objectID = element.find("./OBJECTID").text
        objectName = element.find("./OBJECTNAME").text
        objectFlags = element.find("./OBJECTFLAGS").text


        if (Config.debug()):
        	print("Local objectServerID = %s" % objectServerID)
	# 
	# check to see if this is a Validate request
	#
        validate = Validate.checkForValidate(element)

        if (Config.debug()):
        	print "VALIDATE=%s" % validate

        
	# Build the header for the response

	outgoingXMLData = BuildResponse.buildHeader(element)


	# objects are split up by object types by Interface Constants
	#
	#
	#
	# search for matches to object Type 

	# object Type match
	if (objectType == ACTION_BUTTON_UITYPE):

		if (Config.debug()):
			print "ACTION_BUTTON_UTYPE of %s found" % objectServerID

		# B-2 - flash an LED on the Pi, located on GPIO 25  
		if (objectServerID == "B-2"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(22, GPIO.OUT)
			GPIO.output(22, False)
			time.sleep(0.5)
			GPIO.output(22, True)

	
			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData
		
		# B-3 - take normal picture (with shutter control) 
		if (objectServerID == "B-3"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(22, GPIO.OUT)
			GPIO.output(22, False)
			time.sleep(0.5)
			GPIO.output(22, True)

			useCamera.takeSinglePicture("RasPiConnect - takeSinglePicture", 0.0)
	
			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-4 - do time lapse
		if (objectServerID == "B-4"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(22, GPIO.OUT)
			GPIO.output(22, False)
			time.sleep(0.5)
			GPIO.output(22, True)

	
			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-5 - Open Shutter 
		if (objectServerID == "B-5"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(22, GPIO.OUT)
			GPIO.output(22, False)
			time.sleep(0.5)
			GPIO.output(22, True)
			
			hardwareactions.openshutter()	
	
			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-6 -  take picture without shutters 
		if (objectServerID == "B-6"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(22, GPIO.OUT)
			GPIO.output(22, False)
			time.sleep(0.5)
			GPIO.output(22, True)

			useCamera.takePicture("RasPiConnect Picture Only")
	
			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-7 - Close Shutter 
		if (objectServerID == "B-7"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(22, GPIO.OUT)
			GPIO.output(22, False)
			time.sleep(0.5)
			GPIO.output(22, True)

			hardwareactions.closeshutter()	
	
			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData
	
		# B-8 - Display High and Lows 
		if (objectServerID == "B-8"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


			print "set W-16 state B-8"
                        f = open("./local/SumPageGraphSelect.txt", "w")
                        f.write("display hi/low")
                        f.close()

			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-9 - Display Daily High and Lows 
		if (objectServerID == "B-9"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


			print "set W-16 state B-9"
                        f = open("./local/SumPageGraphSelect.txt", "w")
                        f.write("daily hi/low")
                        f.close()

			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData
	
		# B-10 -  System Logs
		if (objectServerID == "B-10"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


			print "set W-16 state B-10"
                        f = open("./local/SumPageGraphSelect.txt", "w")
                        f.write("System Logs")
                        f.close()

			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-11 -  Trigger Alarm SU-1 
		if (objectServerID == "B-11"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			#format =    titletext, alarmtext, alarmstate, soundvalue, how often in seconds, how many times
                        f = open("/home/pi/ProjectCuracao/main/state/SU-1.txt", "w")
                        f.write("Low Battery, Pi Low,YES, 1005, 1, 10")
                        f.close()

			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-12 -  Clear Alarm SU-1 
		if (objectServerID == "B-12"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


                        f = open("/home/pi/ProjectCuracao/main/state/SU-1.txt", "w")
			#format =    titletext, alarmtext, alarmstate, soundvalue, how often in seconds, how many times
                        f.write("Timeouts, Arduino, NO, 1005, 1, 10")
                        f.close()

			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData
	
		# B-13 -  Trigger Alarm SU-2 
		if (objectServerID == "B-13"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


			#format =    titletext, alarmtext, alarmstate, soundvalue, how often in seconds, how many times
                        f = open("/home/pi/ProjectCuracao/main/state/SU-2.txt", "w")
                        f.write("alarm 2, Reason2-1,YES, 1005, 1, 10")
                        f.close()

			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-14 -  Clear Alarm SU-2 
		if (objectServerID == "B-14"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


			#format =    titletext, alarmtext, alarmstate, soundvalue, how often in seconds, how many times
                        f = open("/home/pi/ProjectCuracao/main/state/SU-2.txt", "w")
                        f.write("alarm 2, Reason2-1,NO, 1005, 1, 10")
                        f.close()

			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-15 -  Send current picture to email in config file
		if (objectServerID == "B-15"):	
			if (Config.debug()):
				print "ACTION_BUTTON_UTYPE of %s executing" % objectServerID
			 

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


			util.sendEmail("Current Picture", "Current Picture from ProjectCuracao", "Sent from PC Pi", conf.notifyAddress, conf.fromAddress, "/home/pi/RasPiConnectServer/static/picamera.jpg");


			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# B-16 -  Send current picture to email in config file
		if (objectServerID == "B-16"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData


			#getArduinoLog.getArduinoLog("RasPi", 1)


			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData
	
	
	# object Type match
	if (objectType == FEEDBACK_ACTION_BUTTON_UITYPE):

		if (Config.debug()):
			print "FEEDBACK_ACTION_BUTTON_UTYPE of %s found" % objectServerID

		
		# FB-11 - change the graph display 
		if (objectServerID == "FB-11"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute

               		responseData = "XXX"

			if (objectName is None):
				objectName = "XXX"
               		lowername = objectName.lower()


                	if (lowername == "display voltages"):

                        	responseData = "display currents" 
                        	responseData = responseData.title()


                		f = open("./local/GraphSelect.txt", "w")
                		f.write(lowername)
                		f.close()


                	elif (lowername == "display currents"):

                        	responseData = "display solar/wind" 
                        	responseData = responseData.title()

                		f = open("./local/GraphSelect.txt", "w")
                		f.write(lowername)
                		f.close()

                	elif (lowername == "display solar/wind"):

                        	responseData = "display voltages" 
                        	responseData = responseData.title()

                		f = open("./local/GraphSelect.txt", "w")
                		f.write(lowername)
                		f.close()

			# defaults to display currents 
                	else:
                        	lowername = "display currents" 
                		f = open("./local/GraphSelect.txt", "w")
                		f.write(lowername)
                		f.close()

                        	responseData = "display voltages" 
                        	responseData = lowername.title()

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData
		
		# FB-12 - turn on GPIO 18 (fan) 
		if (objectServerID == "FB-12"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute

               		responseData = "XXX"
			if (objectName is None):
				objectName = "XXX"

               		lowername = objectName.lower()

			GPIO.setmode(GPIO.BOARD)

                	if (lowername == "turn fan on"):

				GPIO.setup(18, GPIO.OUT)
				GPIO.output(18, True)
				time.sleep(0.3)
				GPIO.output(18, False)

                		f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "w")
                		f.write("1")
                		f.close()

	
                        	responseData = "turn fan off" 
                        	responseData = responseData.title()


                	elif (lowername == "turn fan off"):
				
				GPIO.setup(15, GPIO.OUT)
				GPIO.output(15, True)
				time.sleep(0.3)
				GPIO.output(15, False)
                		f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "w")
                		f.write("0")
                		f.close()

                        	responseData = "turn fan on" 
                        	responseData = responseData.title()


			 # defaults to fan on (meaning fan is off)
                	else:
                        	lowername = "turn fan on" 
				GPIO.setup(15, GPIO.OUT)
				GPIO.output(15, True)
				time.sleep(0.3)
				GPIO.output(15, False)
                		f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "w")
                		f.write("0")
                		f.close()

                        	responseData = lowername.title()

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData



                # FB-13 - change environmental graph 
                if (objectServerID == "FB-13"):

                        #check for validate request
                        # validate allows RasPiConnect to verify this object is here
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()
                                return outgoingXMLData

                        # not validate request, so execute

                        responseData = "XXX"

			if (objectName is None):
				objectName = "XXX"
                        lowername = objectName.lower()


                        if (lowername == "display lum/fan/bar"):

                                responseData = "display temp/hum"
                                responseData = responseData.title()


                                f = open("./local/EGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()


                        elif (lowername == "display temp/hum"):

                                responseData = "display lum/fan/bar"
                                responseData = responseData.title()

                                f = open("./local/EGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        # defaults to display currents
                        else:
                                lowername = "display temp/hum"
                                f = open("./local/EGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                                responseData = "display lum/fan/bar"
                                responseData = lowername.title()


                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # FB-14 - change Arduino 
                if (objectServerID == "FB-14"):

                        #check for validate request
                        # validate allows RasPiConnect to verify this object is here
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()
                                return outgoingXMLData

                        # not validate request, so execute

                        responseData = "XXX"

			if (objectName is None):
				objectName = "XXX"
                        lowername = objectName.lower()


                        if (lowername == "display currents"):

                                responseData = "display voltages"
                                responseData = responseData.title()


                                f = open("./local/AGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()


                        elif (lowername == "display voltages"):

                                responseData = "display currents"
                                responseData = responseData.title()

                                f = open("./local/AGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        # defaults to display currents
                        else:
                                lowername = "display currents"
                                f = open("./local/AGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                                responseData = "display voltages"
                                responseData = lowername.title()


                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

	
                # FB-15 - summary page complex graph chart 
                if (objectServerID == "FB-15"):

                        #check for validate request
                        # validate allows RasPiConnect to verify this object is here
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()
                                return outgoingXMLData

                        # not validate request, so execute


                        responseData = "pi power volts"

			if (objectName is None):
				objectName = "pi power volts"
                        lowername = objectName.lower()


                        if (lowername == "env temp/hum"):

                                responseData = "env lum/fan/bar"
                                responseData = responseData.title()


                        	f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()


                        elif (lowername == "env lum/fan/bar"):

                                responseData = "pi power volts"
                                responseData = responseData.title()

                                f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        elif (lowername == "pi power volts"):

                                responseData = "pi power currents"
                                responseData = responseData.title()

                                f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        elif (lowername == "pi power currents"):

                                responseData = "pi system stats"
                                responseData = responseData.title()

                                f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        elif (lowername == "pi system stats"):

                                responseData = "watchdog volts"
                                responseData = responseData.title()

                                f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        elif (lowername == "watchdog volts"):

                                responseData = "watchdog currents"
                                responseData = responseData.title()

                                f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        elif (lowername == "watchdog currents"):

                                responseData = "env temp/hum" 
                                responseData = responseData.title()

                                f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                        # defaults to display currents
                        else:
                                
				f = open("./local/SumPageGraphSelect.txt", "w")
                                f.write(lowername)
                                f.close()

                                responseData = "env temp/hum" 
                                responseData = lowername.title()


                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

	
	# object Type match

                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

	
	# object Type match
	# object Type match
	if (objectType == TEXT_DISPLAY_UITYPE):

		if (Config.debug()):
			print "ACTION_BUTTON_UTYPE of %s found" % objectServerID


		#LT-10 is Power into Pi	
		if (objectServerID == "LT-10"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

			ina40 = INA219(0x40)
			current = ina40.getCurrent_mA()
			voltage = ina40.getBusVoltage_V()
			power =  (current * voltage) / 1000.0
			myString = "%3.0fmA/%3.2fW" % (current, power)

			responseData = "%s, %s, %s" % (myString, myString,"Power into Pi")

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#LT-11 is Power from Battery
		if (objectServerID == "LT-11"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

			ina41 = INA219(0x41)
			current = ina41.getCurrent_mA()
			voltage = ina41.getBusVoltage_V()
			power =  (current * voltage) / 1000.0
			myString = "%3.0fmA/%3.2fW" % (current, power)

			responseData = "%s, %s, %s" % (myString, myString,"Power from Battery")

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#LT-12 is Power from Solar
		if (objectServerID == "LT-12"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
	

			ina44 = INA219(0x44)
			current = ina44.getCurrent_mA()
			voltage = ina44.getBusVoltage_V()
			
			if (current < 0):
				current = 0
			power =  (current * voltage) / 1000.0
			myString = "%3.0fmA/%3.2fW" % (current, power)

			responseData = "%s, %s, %s" % (myString, myString,"Power from Solar")

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData



		#LT-13 is % Battery left 
		if (objectServerID == "LT-13"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
	

			ina41 = INA219(0x41)
			voltage = ina41.getBusVoltage_V()
			

			percent = util.returnPercentLeftInBattery(voltage, 4.226)

			
			BatteryPackSize = 6000 #mAh size of batteries		
			
			mAhLeft = BatteryPackSize *(percent/100.0)
			myString = "%i%%~%imAh" % (percent, int(mAhLeft))

			responseData = "%s, %s, %s" % (myString, myString,"Battery Remaining")

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData



		#LT-14 is % power efficiency 
		if (objectServerID == "LT-14"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
	

			ina40 = INA219(0x40)
			ina41 = INA219(0x41)
			ina44 = INA219(0x44)
			current40 = ina40.getCurrent_mA() # pi
			current41 = ina41.getCurrent_mA() # battery
			current44 = ina44.getCurrent_mA() # solar
	
			shunt44 = ina44.getShuntVoltage_mV()
			print "44 shunt Voltage =", shunt44
			voltage40 = ina40.getBusVoltage_V()
			voltage41 = ina41.getBusVoltage_V()
			voltage44 = ina44.getBusVoltage_V()
		
			powerEfficiency = (current40*voltage40/(current41*voltage41+current44*voltage44))*100

		        # if power Efficiency < 0, then must be plugged in so add 500ma @ 5V
        		if (powerEfficiency < 0.0):
                		powerEfficiency = (current40*voltage40/(current41*voltage41+current44*voltage44+5.0*500.0))*100



			responseData = "%3.1f%%, %3.1f%%, %s" % (powerEfficiency, powerEfficiency,"Power Efficiency")

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData


		#LT-15 is Battery Temperature and CPU temperature
		if (objectServerID == "LT-15"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
			
 			toggleTemp = 0	

			try:
                		f = open("./local/TempFlip.txt", "r")
                		tempString = f.read()
                		f.close()
				toggleTemp = int(tempString)
				print "read toggleTemp=%i" % toggleTemp

			except IOError as e:
				toggleTemp = 0
				print "I/O error({0}): {1}".format(e.errno, e.strerror)


			print "toggleTemp=%i" % toggleTemp

			if (toggleTemp == 0):


				
				inputnumber=0
				ADS1015 = 0x00  # 12-bit ADC
				ADS1115 = 0x01  # 16-bit ADC

				# Initialise the ADC using the default mode (use default I2C address)
				# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
				adc = ADS1x15(ic=ADS1015)


			        #/ resistance at 25 degrees C
        			THERMISTORNOMINAL = 10000
        			#/ temp. for nominal resistance (almost always 25 C)
        			TEMPERATURENOMINAL = 25
        			#/ how many samples to take and average, more takes longer
        			#/ but is more 'smooth'
        			NUMSAMPLES = 5
        			#/ The beta coefficient of the thermistor (usually 3000-4000)
        			BCOEFFICIENT  = 3950
        			#/ the value of the 'other' resistor
        			SERIESRESISTOR = 10000
			
        			samples = []
			
			
        			# take N samples in a row, with a slight delay
        			for i in range(NUMSAMPLES):
                			samples.append(adc.readADCSingleEnded(inputnumber, 4096, 250))
                			time.sleep(0.100)

        			# average all the samples out
        			average = 0;
        			for i in range(NUMSAMPLES):
                			average = average + samples[i]

        			average = average/NUMSAMPLES

        			print("Average analog reading: %3.3f "% average)

        			# convert the value to resistance
				if (average == 0):
					average = 1.0
        			average = (4096 / average) - 1
        			average = SERIESRESISTOR / average

        			print("Thermistor resistance: %5.3f " % average)



        			steinhart = 0.0
        			steinhart = average / THERMISTORNOMINAL     #/ (R/Ro)
        			steinhart = math.log(steinhart)                  #/ ln(R/Ro)
        			steinhart = steinhart/BCOEFFICIENT                   #/ 1/B * ln(R/Ro)
        			steinhart = steinhart + 1.0 / (TEMPERATURENOMINAL + 273.15) #/ + (1/To)
        			steinhart = 1.0 / steinhart;                 #/ Invert
        			steinhart = steinhart - 273.15;                         #/ convert to C

        			steinhart = steinhart - 7.59 # compared to thermometer
        			print("Temperature: %2.4f *C " % steinhart)
        			temperature = steinhart



				responseData = "%3.1fC, %3.1fC, %s" % (temperature, temperature,"Battery Temperature")
			elif (toggleTemp == 1): 

            			output = subprocess.check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
                		FMOutput = float(output)/1000.0
                		responseData = "%3.2fC, %3.2fC, %s" % (FMOutput, FMOutput,"CPU Temperature")
	
			else:
				temperature = 0.0
				responseData = "%3.1fC, %3.1fC, %s" % (temperature, temperature,"Undefined Temp")

			toggleTemp = toggleTemp+1

			if (toggleTemp > 1):
				toggleTemp = 0 

                	f = open("./local/TempFlip.txt", "w")
                	f.write( str(toggleTemp))
                	f.close()
			print "toggleTemp=%i" % toggleTemp


	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

                #LT-16 is number of samples in environmental table 
                if (objectServerID == "LT-16"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData


			sampleCount = 0

		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT COUNT(*) FROM environmentaldata"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				sampleCount = result[0]

        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

                        responseData = "%i, %i, %s" % (sampleCount, sampleCount,"Total Sample Count")


                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData



		#LT-17 is Power into Arduino
		
		if (objectServerID == "LT-17"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT ArInputVoltage, ArInputCurrent FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]
				current = result[1]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db


			power =  (current * voltage) / 1000.0
			myString = "%3.0fmA/%3.2fW" % (current, power)

			responseData = "%s, %s, %s" % (myString, myString,"Power into Arduino")

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#LT-18 is Power from Battery Arduino
		if (objectServerID == "LT-18"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT BatteryOutputVoltage, BatteryOutputCurrent FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]
				current = result[1]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

			power =  (current * voltage) / 1000.0
			myString = "%3.0fmA/%3.2fW" % (current, power)

			responseData = "%s, %s, %s" % (myString, myString,"Power from Battery")

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#LT-19 is Power from Solar Arduino
		if (objectServerID == "LT-19"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
	
		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT SolarOutputVoltage, SolarOutputCurrent FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]
				current = result[1]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db


			if (current < 0):
				current = 0
			power =  (current * voltage) / 1000.0
			myString = "%3.0fmA/%3.2fW" % (current, power)

			responseData = "%s, %s, %s" % (myString, myString,"Power from Solar")

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData



		#LT-20 is % Battery left  Arduino
		if (objectServerID == "LT-20"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
	
		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT BatteryOutputVoltage FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db


			

			percent = util.returnPercentLeftInBattery(voltage, 4.04)

			
			BatteryPackSize = 6000 #mAh size of batteries		
			
			mAhLeft = BatteryPackSize *(percent/100.0)
			myString = "%i%%/~%imAh" % (percent, int(mAhLeft))

			responseData = "%s, %s, %s" % (myString, myString,"Battery Remaining")

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData



		#LT-21 is % power efficiency for Arduino
		if (objectServerID == "LT-21"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
	

			#current40 = ina40.getCurrent_mA() # pi
			#current41 = ina41.getCurrent_mA() # battery
			#current44 = ina44.getCurrent_mA() # solar

			ArVoltage = 0.0
			ArCurrent = 0.0
			BatVoltage = 0.0
			BatCurrent = 0.0
			SolVoltage = 0.0
			SolCurrent = 0.0

		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT ArInputVoltage, ArInputCurrent, BatteryOutputVoltage, BatteryOutputCurrent, SolarOutputVoltage, SolarOutputCurrent FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()

				ArVoltage = result[0]
				ArCurrent = result[1]
	
				BatVoltage = result[2]
				BatCurrent = result[3]
	
				SolVoltage = result[4]
				SolCurrent = result[5]
	
        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db
		
			powerEfficiency = (ArVoltage*ArCurrent/(BatVoltage*BatCurrent+SolVoltage*SolCurrent))*100

		        # if power Efficiency < 0, then must be plugged in so add 500ma @ 5V
        		if (powerEfficiency < 0.0):
				powerEfficiency = (ArVoltage*ArCurrent/(BatVoltage*BatCurrent+SolVoltage*SolCurrent+5.0*500))*100



			responseData = "%3.1f%%, %3.1f%%, %s" % (powerEfficiency, powerEfficiency,"Power Efficiency")

	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData


		#LT-22 is Battery Temperature 
		if (objectServerID == "LT-22"):	

                	#check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
	
                        	return outgoingXMLData
			

		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT BatteryTemperature FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				temperature = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db


			responseData = "%3.1fC, %3.1fC, %s" % (temperature, temperature,"Battery Temperature")


	
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData



	# object Type match
	if (objectType == VOLTMETER_UITYPE):

		if (Config.debug()):
			print "VOLTMETER_UITYPE of %s found" % objectServerID


		#M-10 is Pi Voltage
		if (objectServerID == "M-10"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

			ina40 = INA219(0x40)
			voltage = ina40.getBusVoltage_V()
			responseData = "%3.2f" % voltage
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData


		if (objectServerID == "M-11"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

			ina41 = INA219(0x41)
			voltage = ina41.getBusVoltage_V()
			responseData = "%3.2f" % voltage
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		if (objectServerID == "M-12"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

			ina44 = INA219(0x44)
			voltage = ina44.getBusVoltage_V()
			responseData = "%3.2f" % voltage
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#BMP085 Barometric Pressure
		if (objectServerID == "M-13"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData
                        # Initialise the BMP085 and use STANDARD mode (default value)
                        # bmp = BMP085(0x77, debug=True)
                        # bmp = BMP085(0x77)

                        # To specify a different operating mode, uncomment one of the following:
                        # bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
                        # bmp = BMP085(0x77, 1)  # STANDARD Mode
                        # bmp = BMP085(0x77, 2)  # HIRES Mode
                        bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode




                        try:
                                pressure = bmp.readPressure()
                                pressureData = "%.2f hPa" % (pressure / 100.0)

                        except IOError as e:
                                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                        except:
                                print "Unexpected error:", sys.exc_info()[0]
                                raise

			responseData = "%3.2f" % (pressure / 100.0)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#BMP085 Inside Temperature 
		if (objectServerID == "M-14"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

                        # Initialise the BMP085 and use STANDARD mode (default value)
                        # bmp = BMP085(0x77, debug=True)
                        # bmp = BMP085(0x77)

                        # To specify a different operating mode, uncomment one of the following:
                        # bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
                        # bmp = BMP085(0x77, 1)  # STANDARD Mode
                        # bmp = BMP085(0x77, 2)  # HIRES Mode
                        bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode


                        try:
                                temp = bmp.readTemperature()


                        except IOError as e:
                                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                        except:
                                print "Unexpected error:", sys.exc_info()[0]
                                raise


			responseData = "%3.2f" % temp
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData


                #luxmeter (brightness)
                if (objectServerID == "M-15"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData



                        try:
				oLuxmeter=Luxmeter()

				myLux = oLuxmeter.getLux()
                        except IOError as e:
                                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                        except:
                                print "Unexpected error:", sys.exc_info()[0]
                                raise


                        responseData = "%3.1f" % myLux
                        print "%s = %s" % (objectServerID, responseData)

                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData
		
                #DHT-11 (to be DHT-22 in the full system)
                if (objectServerID == "M-16"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData


			humidity = 0

			# we change to reading from database because this takes too long from DHT for RasPi


		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT InsideHumidity FROM environmentaldata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				humidity = result[0]

        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db


                        responseData = "%3.1f" % humidity 
                        print "%s = %s" % (objectServerID, responseData)

                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

		# Arduino page

                # Arduino Voltage
                if (objectServerID == "M-17"):

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT ArInputVoltage FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

			responseData = "%3.2f" % voltage

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData


		# Arduino Battery Voltage
		if (objectServerID == "M-18"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

			
		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT BatteryOutputVoltage FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

			responseData = "%3.2f" % voltage

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# Arduino Solar Cell
		if (objectServerID == "M-19"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData
		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT SolarOutputVoltage FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

			responseData = "%3.2f" % voltage
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# Outside Temperature 
		if (objectServerID == "M-20"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData
		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT OutsideTemperature FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				temperature = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

			responseData = "%3.2f" % temperature
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		# Outside Humidity
		if (objectServerID == "M-21"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData
		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT OutsideHumidity FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				humidity = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

			responseData = "%3.2f" % humidity
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#  M-22 show servo location
		if (objectServerID == "M-22"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

			servoValue = hardwareactions.readCameraServo()
			responseData = "%4.1f" % servoValue
			print "%s = %s" % (objectServerID, responseData)

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData


	# object Type match
	if (objectType == BARMETER_UITYPE):

		if (Config.debug()):
			print "BARMETER_UITYPE of %s found" % objectServerID


		#BR-10 is Pi Battery 
		if (objectServerID == "BR-10"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

                        ina41 = INA219(0x41)
                        voltage = ina41.getBusVoltage_V()

			
			

			percent = util.returnPercentLeftInBattery(voltage, 4.226)

			

                        responseData = "%s" % ( percent/10.0 )

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#BR-11 is Arduino Battery 
		if (objectServerID == "BR-11"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData
		        try:
                		print("trying database")
                		db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                		cursor = db.cursor()


				query = "SELECT BatteryOutputVoltage FROM batterywatchdogdata ORDER BY ID DESC LIMIT 1"
                		cursor.execute(query)
                		result = cursor.fetchone()
				print result
				voltage = result[0]


        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db



			percent = util.returnPercentLeftInBattery(voltage, 4.04) 


                        responseData = "%s" % ( percent/10.0 )

                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData




	# object Type match
	if (objectType == PICTURE_REMOTE_WEBVIEW_UITYPE):

		if (Config.debug()):
			print "PICTURE_REMOTE_WEBVIEW_UITYPE of %s found" % objectServerID


		#M-10 is Pi Voltage
		if (objectServerID == "W-10"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

            		# normal response requested



			lowername = "display currents"

			try:
                		f = open("./local/GraphSelect.txt", "r")
                		tempString = f.read()
                		f.close()
				lowername = tempString 		

			except IOError as e:
				print "I/O error({0}): {1}".format(e.errno, e.strerror)

                
			print "lowername=", lowername	
			if (lowername == "display currents"):

				imageName = "systempower.png"

			elif (lowername == "display voltages"):

				imageName = "systemvoltages.png"

			elif (lowername == "display solar/wind"):

				imageName = "solarwindgraph.png"

			else:
				imageName = "systempower.png"



              	 	responseData = "<html><head>"
                	responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
                	responseData += "</head>"
	
                	responseData += "<body><img src=\""
                	responseData += Config.localURL()
                	responseData += "static/"
                	responseData += imageName
                	responseData += "\" type=\"jpg\" width=\"800\" height=\"300\">"

                	responseData +="</body>"
	
                	responseData += "</html>"


                	outgoingXMLData += BuildResponse.buildResponse(responseData)


      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

		#W-11 is Pi System Status 
		if (objectServerID == "W-11"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

            		# normal response requested



			imageName = "systemstatistics.png"



              	 	responseData = "<html><head>"
                	responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
                	responseData += "</head>"
	
                	responseData += "<body><img src=\""
                	responseData += Config.localURL()
                	responseData += "static/"
                	responseData += imageName
                	responseData += "\" type=\"jpg\" width=\"800\" height=\"300\">"

                	responseData +="</body>"
	
                	responseData += "</html>"


                	outgoingXMLData += BuildResponse.buildResponse(responseData)


      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData

                #W-12 is Environmental graph
                if (objectServerID == "W-12"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData

                        # normal response requested



                        lowername = "display temp/hum"

                        try:
                                f = open("./local/EGraphSelect.txt", "r")
                                tempString = f.read()
                                f.close()
                                lowername = tempString

                        except IOError as e:
                                print "I/O error({0}): {1}".format(e.errno, e.strerror)


                        print "lowername=", lowername
                        if (lowername == "display lum/fan/bar"):

				imageName = "environmentalgraph2.png"

                        elif (lowername == "display temp/hum"):

				imageName = "environmentalgraph.png"

                        else:
				imageName = "environmentalgraph.png"



                        responseData = "<html><head>"
                        responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
                        responseData += "</head>"

                        responseData += "<body><img src=\""
                        responseData += Config.localURL()
                        responseData += "static/"
                        responseData += imageName
                        responseData += "\" type=\"jpg\" width=\"585\" height=\"300\">"

                        responseData +="</body>"

                        responseData += "</html>"


                        outgoingXMLData += BuildResponse.buildResponse(responseData)


                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                #W-15 is latest pi camera picture
                if (objectServerID == "W-15"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData

                        # normal response requested

			imageName = "picamera.jpg"


                        responseData = "<html><head>"
                        responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
                        responseData += "</head>"

                        responseData += "<body><img src=\""
                        responseData += Config.localURL()
                        responseData += "static/"
                        responseData += imageName
                        responseData += "\" type=\"jpg\" width=\"585\" height=\"300\">"

                        responseData +="</body>"

                        responseData += "</html>"


                        outgoingXMLData += BuildResponse.buildResponse(responseData)


                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

	if (objectType == REMOTE_WEBVIEW_UITYPE):

		if (Config.debug()):
			print "REMOTE_WEBVIEW_UITYPE of %s found" % objectServerID



                #W-13 is Arduino Current and Voltage
                if (objectServerID == "W-13"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData

                        # normal response requested



                        lowername = "display currents"

                        try:
                                f = open("./local/AGraphSelect.txt", "r")
                                tempString = f.read()
                                f.close()
                                lowername = tempString

                        except IOError as e:
                                print "I/O error({0}): {1}".format(e.errno, e.strerror)


                        print "lowername=", lowername
                        if (lowername == "display currents"):

				imageName = "batterywatchdogcurrent.png"

                        elif (lowername == "display voltages"):

				imageName = "batterywatchdogvoltage.png"

                        else:
				imageName = "batterywatchdogcurrent.png"



                        responseData = "<html><head>"
                        responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
                        responseData += "</head>"

                        responseData += "<body><img src=\""
                        responseData += Config.localURL()
                        responseData += "static/"
                        responseData += imageName
                        responseData += "\" type=\"jpg\" width=\"585\" height=\"300\">"

                        responseData +="</body>"

                        responseData += "</html>"


                        outgoingXMLData += BuildResponse.buildResponse(responseData)


                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                #W-14 is Arduino Log 
                if (objectServerID == "W-14"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData



                        # normal response requested

                        responseData = "<html><head>"
                        responseData += "<title></title><style>body,html,iframe{margin:10;padding:0;}</style>"
                        responseData += "</head>"

                        responseData += "<body style=font-family:'Helvetica Neue';font-size:10pt;>"
			responseData += "<!--INSERTArduinoLOGS-->"
                        responseData +="</body>"

                        responseData += "</html>"


		        try:
                		print("trying database")
               			db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
	
               			cursor = db.cursor()


				query = "SELECT TimeStamp, Level, Source, Message FROM systemlog WHERE Source ='Ardinuo BatteryWatchDog' ORDER BY TimeStamp DESC LIMIT 20"
                		cursor.execute(query)

				rows = cursor.fetchall()
				CRITICAL=50
				ERROR=40
				WARNING=30
				INFO=20
				DEBUG=10
				NOTSET=0


				line = "Last 20 Arduino Watchdog Log Entries<BR>\n<!--INSERTArduinoLOGS-->"	
				responseData = responseData.replace("<!--INSERTArduinoLOGS-->", line)	
				for row in rows:
					level = row[1]	
					levelName = "NONE"
					if (level == DEBUG):
						levelName = "DEBUG"
					if (level == INFO):
						levelName = "INFO"
					if (level == WARNING):
						levelName = "WARNING"
					if (level == ERROR):
						levelName = "ERROR"
					if (level == CRITICAL):
						levelName = "CRITICAL"

					logline = "%s:%s:%s" % (row[0], levelName, row[3] )
					line = logline+"<BR>\n<!--INSERTArduinoLOGS-->"	
					responseData = responseData.replace("<!--INSERTArduinoLOGS-->", line)	

        		except mdb.Error, e:
		
                		print "Error %d: %s" % (e.args[0],e.args[1])

        		finally:
		
                		cursor.close()
                		db.close()
		
                		del cursor
                		del db

                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData


                #W-16 is many things, but first high / low temp
                if (objectServerID == "W-16"):

                        #check for validate request
                        if (validate == "YES"):
                                outgoingXMLData += Validate.buildValidateResponse("YES")
                                outgoingXMLData += BuildResponse.buildFooter()

                                return outgoingXMLData

			print "executing W-16"
       			try:

                        	f = open("./local/SumPageGraphSelect.txt", "r")
                		graphName = f.read()
                		f.close()
       			except IOError as e:
               			graphName = "display hi/low"

			graphName = graphName.lower()
			responseData = ""

			print "executing ", graphName

			if (graphName == "display hi/low"):
				# generate low-high data

			
				# calculate high and lows
				# high and low inside temperatures
				# high and low outside temperatures
				# high and low barometric pressure
				# high and low air speed
	
				
		        	try:
                			print("trying database")
                			db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
			
                			cursor = db.cursor()
	
					# temperature
					query = "SELECT TimeStamp, InsideTemperature FROM environmentaldata ORDER BY InsideTemperature ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowInsideTemperatureTimeStamp = result[0]
					lowInsideTemperature = result[1]
	
					query = "SELECT TimeStamp, InsideTemperature FROM environmentaldata ORDER BY InsideTemperature DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highInsideTemperatureTimeStamp = result[0]
					highInsideTemperature = result[1]
	
					query = "SELECT TimeStamp, OutsideTemperature FROM environmentaldata ORDER BY OutsideTemperature ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowOutsideTemperatureTimeStamp = result[0]
					lowOutsideTemperature = result[1]
	
					query = "SELECT TimeStamp, OutsideTemperature FROM environmentaldata ORDER BY OutsideTemperature DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highOutsideTemperatureTimeStamp = result[0]
					highOutsideTemperature = result[1]
	
					# humidity
					query = "SELECT TimeStamp, InsideHumidity FROM environmentaldata ORDER BY InsideHumidity ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowInsideHumidityTimeStamp = result[0]
					lowInsideHumidity = result[1]
	
					query = "SELECT TimeStamp, InsideHumidity FROM environmentaldata ORDER BY InsideHumidity DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highInsideHumidityTimeStamp = result[0]
					highInsideHumidity = result[1]
	
					query = "SELECT TimeStamp, OutsideHumidity FROM environmentaldata ORDER BY OutsideHumidity ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowOutsideHumidityTimeStamp = result[0]
					lowOutsideHumidity = result[1]
	
					query = "SELECT TimeStamp, OutsideHumidity FROM environmentaldata ORDER BY OutsideHumidity DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highOutsideHumidityTimeStamp = result[0]
					highOutsideHumidity = result[1]
	
					# barometric pressure
					query = "SELECT TimeStamp, BarometricPressure FROM environmentaldata ORDER BY BarometricPressure ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowBarometricPressureTimeStamp = result[0]
					lowBarometricPressure = result[1]
	
					query = "SELECT TimeStamp, BarometricPressure FROM environmentaldata ORDER BY BarometricPressure DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highBarometricPressureTimeStamp = result[0]
					highBarometricPressure = result[1]
	
	
	
	
					# airspeed
					query = "SELECT TimeStamp, AirSpeed FROM environmentaldata ORDER BY AirSpeed ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowAirSpeedTimeStamp = result[0]
					lowAirSpeed = result[1]
	
					query = "SELECT TimeStamp, AirSpeed FROM environmentaldata ORDER BY AirSpeed DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highAirSpeedTimeStamp = result[0]
					highAirSpeed = result[1]
	
        			except mdb.Error, e:
			
                			print "Error %d: %s" % (e.args[0],e.args[1])
	
					lowInsideTemperatureTimeStamp = ""
					lowInsideTemperature = 0.0
	
					highInsideTemperatureTimeStamp = ""
					highInsideTemperature = 0.0
	
					lowOutsideTemperatureTimeStamp = ""
					lowOutsideTemperature = 0.0
	
					highOutsideTemperatureTimeStamp = ""
					highOutsideTemperature = 0.0
	
					lowInsideHumidityTimeStamp = ""
					lowInsideHumidity = 0.0
	
					highInsideHumidityTimeStamp = ""
					highInsideHumidity = 0.0
	
					lowOutsideHumidityTimeStamp = ""
					lowOutsideHumidity = 0.0
	
					highOutsideHumidityTimeStamp = ""
					highOutsideHumidity = 0.0
	
					lowBarometricPressureTimeStamp = ""
					lowBarometricPressure = 0.0
	
					highBarometricPressureTimeStamp = ""
					highBarometricPressure = 0.0

					lowAirSpeedTimeStamp = ""
					lowAirSpeed = 0.0
	
					highAirSpeedTimeStamp = ""
					highAirSpeed = 0.0
	
        			finally:
			
                			cursor.close()
                			db.close()
			
                			del cursor
                			del db
	
	
				print "lowInsideTemperature = %3.2f DateTime=%s" % (lowInsideTemperature, lowInsideTemperatureTimeStamp)
				print "highInsideTemperature = %3.2f DateTime=%s" % (highInsideTemperature, highInsideTemperatureTimeStamp)
				print "lowOutsideTemperature = %3.2f DateTime=%s" % (lowOutsideTemperature, lowOutsideTemperatureTimeStamp)
				print "highOutsideTemperature = %3.2f DateTime=%s" % (highOutsideTemperature, highOutsideTemperatureTimeStamp)
				print
	
				print "lowInsideHumidity = %3.2f DateTime=%s" % (lowInsideHumidity, lowInsideHumidityTimeStamp)
				print "highInsideHumidity = %3.2f DateTime=%s" % (highInsideHumidity, highInsideHumidityTimeStamp)
				print "lowOutsideHumidity = %3.2f DateTime=%s" % (lowOutsideHumidity, lowOutsideHumidityTimeStamp)
				print "highOutsideHumidity = %3.2f DateTime=%s" % (highOutsideHumidity, highOutsideHumidityTimeStamp)
				print
	
				print "lowBarometricPressure = %3.2f DateTime=%s" % (lowBarometricPressure, lowBarometricPressureTimeStamp)
				print "highBarometricPressure = %3.2f DateTime=%s" % (highBarometricPressure, highBarometricPressureTimeStamp)
				print
	
				print "lowAirSpeed = %3.2f DateTime=%s" % (lowAirSpeed, lowAirSpeedTimeStamp)
				print "highAirSpeed = %3.2f DateTime=%s" % (highAirSpeed, highAirSpeedTimeStamp)
				print
				# read an HTML template into aw string		
	
				responseData = ""
				with open ("./Templates/W-16-HL.html", "r") as myfile:
    					responseData += myfile.read().replace('\n', '')
		
				title = "Environmental All Time High and Lows (UTC Time)"	
				responseData = responseData.replace("HLTITLE", title)	
				# now replace the OTH, OTTSH, etc with the right data
				responseData = responseData.replace("OTH", str(highOutsideTemperature))	
				responseData = responseData.replace("OTTSH", str(highOutsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("OTL", str(lowOutsideTemperature))
				responseData = responseData.replace("OTTSL", str(lowOutsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("ITH", str(highInsideTemperature))	
				responseData = responseData.replace("ITTSH", str(highInsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("ITL", str(lowInsideTemperature))
				responseData = responseData.replace("ITTSL", str(lowInsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("OHH", str(highOutsideHumidity))	
				responseData = responseData.replace("OHTSH", str(highOutsideHumidityTimeStamp))	
	
				responseData = responseData.replace("OHL", str(lowOutsideHumidity))	
				responseData = responseData.replace("OHTSL", str(lowOutsideHumidityTimeStamp))	
	
				responseData = responseData.replace("IHH", str(highInsideHumidity)	)
				responseData = responseData.replace("IHTSH", str(highInsideHumidityTimeStamp))	
	
				responseData = responseData.replace("IHL", str(lowInsideHumidity)	)
				responseData = responseData.replace("IHTSL", str(lowInsideHumidityTimeStamp))	
	
				responseData = responseData.replace("BPTH", str(highBarometricPressure)	)
				responseData = responseData.replace("BPTTSH", str(highBarometricPressureTimeStamp))	
	
				responseData = responseData.replace("BPTL", str(lowBarometricPressure)	)
				responseData = responseData.replace("BPTTSL", str(lowBarometricPressureTimeStamp))	
				
				responseData = responseData.replace("WSTH", str(highAirSpeed)	)
				responseData = responseData.replace("WSTTSH", str(highAirSpeedTimeStamp))	
	
				responseData = responseData.replace("WSTL", str(lowAirSpeed)	)
				responseData = responseData.replace("WSTTSL", str(lowAirSpeedTimeStamp))	
	

			if (graphName == "daily hi/low"):
				# generate low-high data

			
				# calculate high and lows
				# high and low inside temperatures
				# high and low outside temperatures
				# high and low barometric pressure
				# high and low air speed
	
				
		        	try:
                			print("trying database")
                			db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
			
                			cursor = db.cursor()
					#SELECT TIMESTAMP, InsideTemperature FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY InsideTemperature ASC 
					# temperature
					query = "SELECT TimeStamp, InsideTemperature FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY InsideTemperature ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowInsideTemperatureTimeStamp = result[0]
					lowInsideTemperature = result[1]
	
					query = "SELECT TimeStamp, InsideTemperature FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY InsideTemperature DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highInsideTemperatureTimeStamp = result[0]
					highInsideTemperature = result[1]

					query = "SELECT TimeStamp, OutsideTemperature FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY OutsideTemperature ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowOutsideTemperatureTimeStamp = result[0]
					lowOutsideTemperature = result[1]
	
					query = "SELECT TimeStamp, OutsideTemperature FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY OutsideTemperature DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highOutsideTemperatureTimeStamp = result[0]
					highOutsideTemperature = result[1]
	
					# humidity
					query = "SELECT TimeStamp, InsideHumidity FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY InsideHumidity ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowInsideHumidityTimeStamp = result[0]
					lowInsideHumidity = result[1]
	
					query = "SELECT TimeStamp, InsideHumidity FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY InsideHumidity DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highInsideHumidityTimeStamp = result[0]
					highInsideHumidity = result[1]
	
					query = "SELECT TimeStamp, OutsideHumidity FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY OutsideHumidity ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowOutsideHumidityTimeStamp = result[0]
					lowOutsideHumidity = result[1]
	
					query = "SELECT TimeStamp, OutsideHumidity FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY OutsideHumidity DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highOutsideHumidityTimeStamp = result[0]
					highOutsideHumidity = result[1]
	
					# barometric pressure
					query = "SELECT TimeStamp, BarometricPressure FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY BarometricPressure ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowBarometricPressureTimeStamp = result[0]
					lowBarometricPressure = result[1]
	
					query = "SELECT TimeStamp, BarometricPressure FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY BarometricPressure DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highBarometricPressureTimeStamp = result[0]
					highBarometricPressure = result[1]
	
	
	
	
					# airspeed
					query = "SELECT TimeStamp, AirSpeed FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY AirSpeed ASC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					lowAirSpeedTimeStamp = result[0]
					lowAirSpeed = result[1]
	
					query = "SELECT TimeStamp, AirSpeed FROM environmentaldata WHERE DATE_ADD(CURDATE( ) , INTERVAL - 4 HOUR) < TIMESTAMP ORDER BY AirSpeed DESC LIMIT 1"
                			cursor.execute(query)
                			result = cursor.fetchone()
					highAirSpeedTimeStamp = result[0]
					highAirSpeed = result[1]
	
        			except mdb.Error, e:
			
                			print "Error %d: %s" % (e.args[0],e.args[1])
	
					lowInsideTemperatureTimeStamp = ""
					lowInsideTemperature = 0.0
	
					highInsideTemperatureTimeStamp = ""
					highInsideTemperature = 0.0
	
					lowOutsideTemperatureTimeStamp = ""
					lowOutsideTemperature = 0.0
	
					highOutsideTemperatureTimeStamp = ""
					highOutsideTemperature = 0.0
	
					lowInsideHumidityTimeStamp = ""
					lowInsideHumidity = 0.0
	
					highInsideHumidityTimeStamp = ""
					highInsideHumidity = 0.0
	
					lowOutsideHumidityTimeStamp = ""
					lowOutsideHumidity = 0.0
	
					highOutsideHumidityTimeStamp = ""
					highOutsideHumidity = 0.0
	
					lowBarometricPressureTimeStamp = ""
					lowBarometricPressure = 0.0
	
					highBarometricPressureTimeStamp = ""
					highBarometricPressure = 0.0

					lowAirSpeedTimeStamp = ""
					lowAirSpeed = 0.0
	
					highAirSpeedTimeStamp = ""
					highAirSpeed = 0.0
	
        			finally:
			
                			cursor.close()
                			db.close()
			
                			del cursor
                			del db
	
	
				print "lowInsideTemperature = %3.2f DateTime=%s" % (lowInsideTemperature, lowInsideTemperatureTimeStamp)
				print "highInsideTemperature = %3.2f DateTime=%s" % (highInsideTemperature, highInsideTemperatureTimeStamp)
				print "lowOutsideTemperature = %3.2f DateTime=%s" % (lowOutsideTemperature, lowOutsideTemperatureTimeStamp)
				print "highOutsideTemperature = %3.2f DateTime=%s" % (highOutsideTemperature, highOutsideTemperatureTimeStamp)
				print
	
				print "lowInsideHumidity = %3.2f DateTime=%s" % (lowInsideHumidity, lowInsideHumidityTimeStamp)
				print "highInsideHumidity = %3.2f DateTime=%s" % (highInsideHumidity, highInsideHumidityTimeStamp)
				print "lowOutsideHumidity = %3.2f DateTime=%s" % (lowOutsideHumidity, lowOutsideHumidityTimeStamp)
				print "highOutsideHumidity = %3.2f DateTime=%s" % (highOutsideHumidity, highOutsideHumidityTimeStamp)
				print
	
				print "lowBarometricPressure = %3.2f DateTime=%s" % (lowBarometricPressure, lowBarometricPressureTimeStamp)
				print "highBarometricPressure = %3.2f DateTime=%s" % (highBarometricPressure, highBarometricPressureTimeStamp)
				print
	
				print "lowAirSpeed = %3.2f DateTime=%s" % (lowAirSpeed, lowAirSpeedTimeStamp)
				print "highAirSpeed = %3.2f DateTime=%s" % (highAirSpeed, highAirSpeedTimeStamp)
				print
				# read an HTML template into aw string		
	
				responseData = ""
				with open ("./Templates/W-16-HL.html", "r") as myfile:
    					responseData += myfile.read().replace('\n', '')
		
	
				title = "Environmental Daily High and Lows (UTC Time - Curacao Day)"	
				responseData = responseData.replace("HLTITLE", title)	
				# now replace the OTH, OTTSH, etc with the right data
				responseData = responseData.replace("OTH", str(highOutsideTemperature))	
				responseData = responseData.replace("OTTSH", str(highOutsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("OTL", str(lowOutsideTemperature))
				responseData = responseData.replace("OTTSL", str(lowOutsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("ITH", str(highInsideTemperature))	
				responseData = responseData.replace("ITTSH", str(highInsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("ITL", str(lowInsideTemperature))
				responseData = responseData.replace("ITTSL", str(lowInsideTemperatureTimeStamp))	
	
				responseData = responseData.replace("OHH", str(highOutsideHumidity))	
				responseData = responseData.replace("OHTSH", str(highOutsideHumidityTimeStamp))	
	
				responseData = responseData.replace("OHL", str(lowOutsideHumidity))	
				responseData = responseData.replace("OHTSL", str(lowOutsideHumidityTimeStamp))	
	
				responseData = responseData.replace("IHH", str(highInsideHumidity)	)
				responseData = responseData.replace("IHTSH", str(highInsideHumidityTimeStamp))	
	
				responseData = responseData.replace("IHL", str(lowInsideHumidity)	)
				responseData = responseData.replace("IHTSL", str(lowInsideHumidityTimeStamp))	
	
				responseData = responseData.replace("BPTH", str(highBarometricPressure)	)
				responseData = responseData.replace("BPTTSH", str(highBarometricPressureTimeStamp))	
	
				responseData = responseData.replace("BPTL", str(lowBarometricPressure)	)
				responseData = responseData.replace("BPTTSL", str(lowBarometricPressureTimeStamp))	
				
				responseData = responseData.replace("WSTH", str(highAirSpeed)	)
				responseData = responseData.replace("WSTTSH", str(highAirSpeedTimeStamp))	
	
				responseData = responseData.replace("WSTL", str(lowAirSpeed)	)
				responseData = responseData.replace("WSTTSL", str(lowAirSpeedTimeStamp))	
	

			if (graphName == "system logs"):

				# grab the system logs
				with open ("./Templates/W-16-SL.html", "r") as myfile:
    					responseData += myfile.read().replace('\n', '')
		
		        	try:
                			print("trying database")
                			db = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');
		
                			cursor = db.cursor()


					query = "SELECT TimeStamp, Level, Source, Message FROM systemlog WHERE Source != 'Ardinuo BatteryWatchDog' ORDER BY ID DESC LIMIT 20"
                			cursor.execute(query)

					rows = cursor.fetchall()
					CRITICAL=50
					ERROR=40
					WARNING=30
					INFO=20
					DEBUG=10
					NOTSET=0

					for row in rows:
						level = row[1]	
						levelName = "NONE"
						if (level == DEBUG):
							levelName = "DEBUG"
						if (level == INFO):
							levelName = "INFO"
						if (level == WARNING):
							levelName = "WARNING"
						if (level == ERROR):
							levelName = "ERROR"
						if (level == CRITICAL):
							levelName = "CRITICAL"

						logline = "%s:%s:%s:%s" % (row[0], levelName, row[2], row[3] )
						line = logline+"<BR>\n<!--INSERTLOGS-->"	

						responseData = responseData.replace("<!--INSERTLOGS-->", line)	


					query = "SELECT TimeStamp, Level, Source, Message FROM systemlog WHERE Source ='Ardinuo BatteryWatchDog' ORDER BY TimeStamp DESC LIMIT 20"
                			cursor.execute(query)

					rows = cursor.fetchall()

					line = "<BR>Last 20 Arduino Watchdog Log Entries<BR>\n<!--INSERTArduinoLOGS-->"	
					responseData = responseData.replace("<!--INSERTArduinoLOGS-->", line)	
					for row in rows:
						level = row[1]	
						levelName = "NONE"
						if (level == DEBUG):
							levelName = "DEBUG"
						if (level == INFO):
							levelName = "INFO"
						if (level == WARNING):
							levelName = "WARNING"
						if (level == ERROR):
							levelName = "ERROR"
						if (level == CRITICAL):
							levelName = "CRITICAL"

						logline = "%s:%s:%s:%s" % (row[0], levelName, row[2], row[3] )
						line = logline+"<BR>\n<!--INSERTArduinoLOGS-->"	
						responseData = responseData.replace("<!--INSERTArduinoLOGS-->", line)	

        			except mdb.Error, e:
		
                			print "Error %d: %s" % (e.args[0],e.args[1])

        			finally:
		
                			cursor.close()
                			db.close()
			
                			del cursor
                			del db

			#if responseData length is zero then we have a graph to do	
			if (len(responseData) == 0):
                       		if (graphName == "env temp/hum"):
					imageName = "environmentalgraph.png"

                       		elif (graphName == "env lum/fan/bar"):
					imageName = "environmentalgraph2.png"

                       		elif (graphName == "pi power volts"):
					imageName = "systemvoltages.png"
	

                       		elif (graphName == "pi power currents"):
					imageName = "systempower.png"


                       		elif (graphName == "pi system stats"):
					imageName = "systemstatistics.png"


                       		elif (graphName == "watchdog volts"):
					imageName = "batterywatchdogvoltage.png"


                       		elif (graphName == "watchdog currents"):
					imageName = "batterywatchdogcurrent.png"
			
				else:
					imageName = "systemstatistics.png"



              	 		responseData = "<html><head>"
                		responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
                		responseData += "</head>"
		
                		responseData += "<body><img src=\""
                		responseData += Config.localURL()
                		responseData += "static/"
                		responseData += imageName
                		responseData += "\" type=\"jpg\" width=\"675\" height=\"296\">"
	
                		responseData +="</body>"
		
                		responseData += "</html>"

			

			# now finish it up
	
                        outgoingXMLData += BuildResponse.buildResponse(responseData)
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

	# object Type match
	if (objectType == SINGLE_LED_DISPLAY_UITYPE):
		if (Config.debug()):
			print "SINGLE_LED_DISPLAY_UITYPE of %s found" % objectServerID





	        # L-10 sends back the current state of the Fan 
       		if (objectServerID == "L-10"):

               		#check for validate request
               		if (validate == "YES"):
                       		outgoingXMLData += Validate.buildValidateResponse("YES")
                       		outgoingXMLData += BuildResponse.buildFooter()
	
                       		return outgoingXMLData

			# read from fan state file
       			try:
               			f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "r")
               			tempString = f.read()
               			f.close()
               			fanstate = int(tempString)
       			except IOError as e:
               			fanstate = 0


			if (fanstate == 0):
				ledoutput = 5	
			else:
				ledoutput = 2
	
	                responseData = "%i" % ledoutput


               		outgoingXMLData += BuildResponse.buildResponse(responseData)
                        
			outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

	        # L-11 shutter state 
       		if (objectServerID == "L-11"):

               		#check for validate request
               		if (validate == "YES"):
                       		outgoingXMLData += Validate.buildValidateResponse("YES")
                       		outgoingXMLData += BuildResponse.buildFooter()
	
                       		return outgoingXMLData

			servoValue = hardwareactions.readCameraServo()

			# assume in middle (Green, yellow, red)
			ledoutput = 6 # Yellow		

			if (servoValue < 1100):
				print "shutter open"
				ledoutput = 2
			
			if (servoValue > 1650):
				print "shutter open"
				ledoutput = 5
	
	                responseData = "%i" % ledoutput


               		outgoingXMLData += BuildResponse.buildResponse(responseData)
                        
			outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

	# object Type match
	if (objectType == SOUND_ALARM_UITYPE):
		if (Config.debug()):
			print "SOUND_ALARM_UITYPE of %s found" % objectServerID

	        # SU-1 Alarm 1
       		if (objectServerID == "SU-1"):

               		#check for validate request
               		if (validate == "YES"):
                       		outgoingXMLData += Validate.buildValidateResponse("YES")
                       		outgoingXMLData += BuildResponse.buildFooter()
	
                       		return outgoingXMLData



			try:
                        	f = open("/home/pi/ProjectCuracao/main/state/SU-1.txt", "r")
                		responseData = f.read()
                		f.close()

			except IOError as e:
				toggleTemp = 0
				print "I/O error({0}): {1}".format(e.errno, e.strerror)
				responseData = ""



               		outgoingXMLData += BuildResponse.buildResponse(responseData)
			outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData
	        
		# SU-2 Alarm 2
       		if (objectServerID == "SU-2"):

               		#check for validate request
               		if (validate == "YES"):
                       		outgoingXMLData += Validate.buildValidateResponse("YES")
                       		outgoingXMLData += BuildResponse.buildFooter()
	
                       		return outgoingXMLData




			try:
                        	f = open("/home/pi/ProjectCuracao/main/state/SU-2.txt", "r")
                		responseData = f.read()
                		f.close()

			except IOError as e:
				toggleTemp = 0
				print "I/O error({0}): {1}".format(e.errno, e.strerror)
				responseData = ""



               		outgoingXMLData += BuildResponse.buildResponse(responseData)
			outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

	else:
		return ""
	# returning a zero length string tells the server that you have not matched 
	# the object and server 
	return ""

