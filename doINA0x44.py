import sys
import time


# from ProjectCuracao
sys.path.append('/home/pi/ProjectCuracao/main/hardware')
sys.path.append('/home/pi/ProjectCuracao/main/actions')
sys.path.append('/home/pi/ProjectCuracao/main/util')
sys.path.append('/home/pi/ProjectCuracao/main/datacollect')
sys.path.append('/home/pi/ProjectCuracao/main/config')
sys.path.append('/home/pi/ProjectCuracao/main/state')

from Subfact_ina219 import INA219



while True:
	ina44 = INA219(0x44)
	voltage = ina44.getBusVoltage_V()
	responseData = "%3.2f" % voltage
	print "voltage = %s " % (responseData)
	time.sleep(2.000)
		
