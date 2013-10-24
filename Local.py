#!/usr/bin/python
# Filename: Local.py
# Support for ProjectCuracao
# MiloCreek JS MiloCreek
# Version 1.0  9/7/2013
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


# system imports
import sys
import subprocess
import time
import RPi.GPIO as GPIO
import math
import re

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
        	print("objectServerID = %s" % objectServerID)
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

			GPIO.setup(22, GPIO.OUT)
			GPIO.output(22, False)
			time.sleep(0.5)
			GPIO.output(22, True)

	
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

               		lowername = objectName.lower()


                	if (lowername == "display voltages"):

                        	responseData = "display currents" 
                        	responseData = responseData.title()


                		f = open("./local/GraphSelect.txt", "w")
                		f.write(lowername)
                		f.close()


                	elif (lowername == "display currents"):

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

               		lowername = objectName.lower()


                	if (lowername == "turn fan on"):

				GPIO.setup(18, GPIO.OUT)
				GPIO.output(18, True)
                		f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "w")
                		f.write("1")
                		f.close()

	
                        	responseData = "turn fan off" 
                        	responseData = responseData.title()


                	elif (lowername == "turn fan off"):
				
				GPIO.setup(18, GPIO.OUT)
				GPIO.output(18, False)
                		f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "w")
                		f.write("0")
                		f.close()

                        	responseData = "turn fan on" 
                        	responseData = responseData.title()


			 # defaults to fan on (meaning fan is off)
                	else:
                        	lowername = "turn fan on" 
				GPIO.setup(18, GPIO.OUT)
				GPIO.output(18, False)

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
			
			# Using resistances and trip points from LiPo Pro v0.9 	
			# all voltages after split compared to 2.5V 
			percenthigh = 10
			percentlow = 0


			print "voltage = %3.3f" % voltage
			print "low = %3.3f" %(voltage * 359.7/536.6) 
			print "next = %3.3f" %(voltage * 355/536.6)
			print "next = %3.3f" %(voltage * 345/536.6)
			print "high = %3.3f" %(voltage * 330.7/536.6)
			
			if ((voltage * 359.7/536.6) > 2.5):
				percenthigh = 30
				percentlow = 10
			if ((voltage * 355/536.6) > 2.5):
				percenthigh = 60
				percentlow = 30
			if ((voltage * 345/536.6) > 2.5):
				percenthigh = 90
				percentlow = 60
			if ((voltage * 330.7/536.6) > 2.5):
				percenthigh = 100
				percentlow = 90

			print "percenthigh = %i percentlow=%i" % (percenthigh, percentlow)
			
			BatteryPackSize = 6000 #mAh size of batteries		
			
			mAhLeft = 6000 *(((percenthigh + percentlow)/2.0)/100.0)
			myString = "%i-%i%%/~%imAh" % (percentlow, percenthigh, int(mAhLeft))

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



	# object Type match
	if (objectType == BARMETER_UITYPE):

		if (Config.debug()):
			print "BARMETER_UITYPE of %s found" % objectServerID


		#M-10 is Pi Voltage
		if (objectServerID == "BR-10"):	

        	        #check for validate request
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()

                        	return outgoingXMLData

                        ina41 = INA219(0x41)
                        voltage = ina41.getBusVoltage_V()

                        # Using resistances and trip points from LiPo Pro v0.9
                        # all voltages after split compared to 2.5V
                        percenthigh = 10
                        percentlow = 0

                        print "voltage = %3.3f" % voltage
                        print "low = %3.3f" %(voltage * 359.7/536.6) 
                        print "next = %3.3f" %(voltage * 355/536.6)
                        print "next = %3.3f" %(voltage * 345/536.6)
                        print "high = %3.3f" %(voltage * 330.7/536.6)
                        
                        if ((voltage * 359.7/536.6) > 2.5):
                                percenthigh = 30
                                percentlow = 10
                        if ((voltage * 355/536.6) > 2.5):
                                percenthigh = 60
                                percentlow = 30
                        if ((voltage * 345/536.6) > 2.5):
                                percenthigh = 90
                                percentlow = 60
                        if ((voltage * 330.7/536.6) > 2.5):
                                percenthigh = 100
                                percentlow = 90



                        responseData = "%s" % ( percenthigh/10.0 )

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
                	responseData += "<BR>Picture<BR>"

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
                	responseData += "<BR>Picture<BR>"

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
                        responseData += "<BR>Picture<BR>"

                        responseData +="</body>"

                        responseData += "</html>"


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



	else:
		return ""
	# returning a zero length string tells the server that you have not matched 
	# the object and server 
	return ""

