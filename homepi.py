#!/usr/bin/env python
##############################################################################
import os, sys, time, datetime, argparse, math, decimal, re
import threading, random, subprocess, string
import cgi, urllib2, json, alsaaudio
import MySQLdb as mydb
import pifacecommon, pifacedigitalio
import pifacedigitalio.version as pfdioV
import pifacecommon.version as pfcV
import smtplib
from email.mime.text import	MIMEText
from os import curdir, sep, path
from subprocess import Popen
from time import sleep, gmtime, strftime
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
##############################################################################
Version = "0.4.1"
MySQL_Host = "10.128.2.252"
MySQL_User = "homepi"
MySQL_Pass = "raspberry!"
MySQL_DB = "homepi"
LOG_FILE = "/var/log/homepi.log"
STDOUT_SHELL = False
DEBUG_LOG = False
DB_ERROR = False
##############################################################################
class HTTP_Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			#send HTTP 200 response code to client
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()        	  
			#['', 'request', '0', 'off', '7', '', '']
			#parse data string with PiFace Board/Pin values
			datastring = str(self.path).split("/")
			if datastring[1] == "request":
				PiFace_Board  = int(datastring[2])
				status = datastring[3]
				status = string.lower(status)
				PiFace_Pin = int(datastring[4])
				if PiFace_Board != "":
					if status == "on":
						pifacedigitalio.digital_write(PiFace_Pin, 1, PiFace_Board)
					elif status == "off":
						pifacedigitalio.digital_write(PiFace_Pin, 0, PiFace_Board)
			elif datastring[1] == "quit":
				status = "quit"
		
		except IOError:
			self.send_error(404,'File Not Found: ' + self.path)
##############################################################################
def HTTP_Server():
	HTTP_Port = int(GetConfig("http_port"))
	logging("Thread: Starting thread for HTTP server on tcp port %s." % (HTTP_Port))
	#Start HTTP server to serve requests from web frontend
	try:
		srv = HTTPServer(('', HTTP_Port), HTTP_Handler)
	except BaseException, e:
		ExceptionHand(e,"HTTP_Server")
		return
	should_stop = False
	while not should_stop:
		srv.handle_request()
		should_stop = homepi_running()
	srv.socket.close()
	logging("Quit: Stopping thread for HTTP server on tcp port %s." % (HTTP_Port))
	return
##############################################################################
def homepi_running():
	global should_stop
	return should_stop
##############################################################################	
def C2F(c):
    return c * 9/5 + 32
##############################################################################
def thermostat_control(furnace_value):
	global FuranceRunning, Furnace_Pin, Furnace_Board, Furnace_ID
	OnOff = {0:'off',1:'on'}
	pifacedigitalio.digital_write(Furnace_Pin, furnace_value, Furnace_Board)
	if DEBUG_LOG:
		logging("Action: Thermostat output on pin %s is set to %s." % (Furnace_Pin, OnOff[int(furnace_value)]))
	query = ("UPDATE `homepi`.`piface` SET `status`=%d WHERE `id`=%d;" % (furnace_value, Furnace_ID))
	DBQuery(2,query)
	FuranceRunning = bool(furnace_value)
	logging("Action: FuranceRunning has been set to %s." % (FuranceRunning))
	return
##############################################################################
def set_thermostat(temp):
	query = ("UPDATE `homepi`.`config` SET `data`=%d WHERE `name`='thermostat_temp';" % (temp))
	return DBQuery(2,query)
##############################################################################
def thermostat_check():
	global OnValue, OffValue
	global FuranceRunning, Furance_ID, Thermostat_Temp
	
	#get current outside and inside temperature
	temp_inside = GetTemp(GetConfig("inside_zone"))
	temp_outside = GetTemp(GetConfig("outside_zone"))
	
	
	if temp_outside > 66 and FuranceRunning:
		logging("Info: Outside temperature is too high to run furnace!")
		thermostat_control(OffValue)
		return
				
	thermostat_onat = int(GetConfig("thermostat_temp"))
	temp_limit_upper = int(GetConfig("thermostat_limit_upper"))
	thermostat_limit_lower = int(GetConfig("thermostat_limit_lower"))
	
	if thermostat_onat > temp_limit_upper:
		thermostat_onat = temp_limit_upper
		set_thermostat(temp_limit_upper)
	elif thermostat_onat < thermostat_limit_lower:
		thermostat_onat = thermostat_limit_lower
		set_thermostat(thermostat_limit_lower)
		
	thermostat_offat = (thermostat_onat + 1)
		
	if Thermostat_Temp != thermostat_onat:
		Thermostat_Temp = thermostat_onat
		logging("Config: Thermostat is set at %s F." % (Thermostat_Temp))	
		
	#if inside temp is < setting then turn on
	if temp_inside < thermostat_onat and not FuranceRunning:
		thermostat_control(OnValue)
		logging("Info: The current temperature inside is %s F, outside %s F." % (temp_inside,temp_outside))
	elif temp_inside >= thermostat_offat and FuranceRunning:
		thermostat_control(OffValue)
		logging("Info: The current temperature inside is %s F, outside %s F." % (temp_inside,temp_outside))	
	return
##############################################################################
def GetTemp(zone_id):
	ZoneTemp = 0
	query = ("SELECT `temp` FROM `homepi`.`tempzone` WHERE `zone_id`=%s order by `date_time` desc limit 1;" % zone_id)
	rows = DBQuery(1,query)
	if not (rows):
		logging("Error: GetTemp | %s." % query)
		return
		
	for row in rows:
		ZoneTemp = int(row[0])
		
	if GetConfig("temp_mode") == "F":
		ZoneTemp = C2F(int(row[0]))
		
	return ZoneTemp
##############################################################################
def ReadTempSensor(SensorNumber):
	# DS18B20 Temperature Sensor
	
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'
	
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
		equals_pos = lines[1].find('t=')
		
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0

	return temp_c
############################################################################## 
def event_interrupt(event):
	Pin_Value = pifacedigitalio.digital_read(event.pin_num, event.chip.hardware_addr)
	logging("Event Interrupt: Board: %d Pin: %d Value: %d Direction: %d" % (event.chip.hardware_addr,event.pin_num,Pin_Value,event.direction))
	event_process(int(event.chip.hardware_addr),int(event.pin_num),Pin_Value)
	return
##############################################################################	
def event_process(PiFace_Board,PiFace_Pin,Pin_Value):
	query = ("SELECT * FROM `homepi`.`piface` WHERE (`enabled`=1 AND `output`=0 AND `pin`=%d AND `board`=%d);" % (PiFace_Pin, PiFace_Board))
	rows = DBQuery(1,query)
	if not (rows):
		logging("Error: event_interrupt | %s." % query)
		return
	
	for row in rows:
		PiFace_ID = int(row[0])
		Zone_Number = int(row[4])
		Input_Name = row[6]
		Default_Value = int(row[9])
		Zone_Name = GetZoneName(Zone_Number)
		
	logging("Input: #%s-%s %s zone #%s event. | Board: %s Pin: %s." % (PiFace_ID, Input_Name, Zone_Name, Zone_Number, PiFace_Board, PiFace_Pin))
	query = ("SELECT * FROM `homepi`.`input_action` WHERE `piface_id`=%d;" % (PiFace_ID))
	rows = DBQuery(1,query)
	if not (rows):
		logging("Error: event_interrupt | %s." % query)
		return
		
	for row in rows:
		Output_ID = int(row[3])
		Output_Value = int(row[4])
	
		if row[2] == 1:
			#Action is On/Off output
			device_control(int(Output_ID),int(Output_Value),True)
		
		elif row[2] == 2:	
			#Action changes zone
			MotionInZone(int(Zone_Number))
			
		elif row[2] == 3:	
			#Speak Data
			SpeakData(int(row[4]),Zone_Number)
					
	return
##############################################################################
def device_control(PiFace_ID,Pin_Value,AutoOff):
	global LightsOff
	OnOff = {0:'off',1:'on'}
	row = GetDevicebyID(PiFace_ID)
	if (row):
		PiFace_ID = int(row[0])
		PiFace_Board = int(row[1])
		PiFace_Pin = int(row[2])
		PiFace_Status = int(row[3])
		Zone_Number = int(row[4])
		PiFace_Name = str(row[6])
	else:
		logging("Error: Invalid PiFace GetDevicebyID data at device_control.")
		return
	
	if int(PiFace_Status) != int(Pin_Value):
		pifacedigitalio.digital_write(PiFace_Pin, int(Pin_Value), PiFace_Board)
		Zone_Name = GetZoneName(Zone_Number)
		logging("Output: %d-%s %s has been set to %s. | Board: %s Pin: %s."  % (PiFace_ID, PiFace_Name, Zone_Name, OnOff[int(Pin_Value)], PiFace_Board, PiFace_Pin))
		query = ("UPDATE `homepi`.`piface` SET `status`=%d WHERE `id`=%d;" % (Pin_Value, PiFace_ID))
		DBQuery(2,query)
		
		#if device is a light then turn off in X mins
		if (int(PiFace_Status) == 0) and AutoOff:
			dt = datetime.timedelta(minutes=LightsOff)
			EventTime = datetime.datetime.now() + dt
			query = ("INSERT INTO `homepi`.`event_action` (`piface_id`, `value`, `datetime`) VALUES (%d, 0, '%s');" % (PiFace_ID, EventTime))
			DBQuery(2,query)
			logging("Action: %s %s will be set to off in %s minutes." % (PiFace_Name, Zone_Name, LightsOff))
		return 
		
	elif bool(PiFace_Status) and AutoOff:
		#Update Auto Off time
		#logging("Update AutoOff PiFace_ID=%d" % PiFace_ID)
		query = ("SELECT * FROM `homepi`.`event_action` WHERE `datetime` > now() AND `piface_id`=%d LIMIT 1;" % PiFace_ID)
		rows = DBQuery(1,query)
		if not (rows):
			return
		for row in rows:
			Mod_ID = int(row[0])
			dt = datetime.timedelta(minutes=LightsOff)
			EventTime = datetime.datetime.now() + dt
			query = ("UPDATE `homepi`.`event_action` SET `datetime`='%s' WHERE `id`=%d;" % (EventTime, Mod_ID))
			DBQuery(2,query)
				
	return
##############################################################################	
def event_check():
	#select database for timed events that are due
	event_start = datetime.datetime.now()
	dt = datetime.timedelta (seconds=60)
	event_end = event_start + dt
	if DEBUG_LOG:
		logging("Checking events between %s and %s" % (event_start, event_end))
	query = ("SELECT DISTINCT * FROM `homepi`.`event_action` WHERE `datetime` BETWEEN '%s' AND '%s' LIMIT 4;" % (event_start,  event_end))
	rows = DBQuery(1,query)
	if (rows):
		for row in rows:
			PiFace_ID = int(row[1])
			Pin_Value = int(row[2])
			logging("Event Action: PiFace_ID=%d Pin_Value=%d" % (PiFace_ID,Pin_Value))
			device_control(PiFace_ID,Pin_Value,True)
	return
##############################################################################
def zone_check():
	ModeID = int(GetHouseMode())
	#If Mode is Away check for occupied zones
	if ModeID == 1:
		query = ('SELECT * FROM `homepi`.`zones` WHERE `occupied`=1 AND `type` > 0;')
		rows = DBQuery(1,query)
		if (rows):
			for row in rows:
				SetMode(2)
				break
			
	#select database for timed events that are due
	event_start = datetime.datetime.now()
	dt = datetime.timedelta (seconds=60)
	event_end = event_start + dt
	query = ('SELECT * FROM `homepi`.`zone_action` WHERE `time_stamp` BETWEEN "%s" AND "%s";' % (event_start, event_end))
	rows = DBQuery(1,query)
	
	if not (rows):
		return
	for row in rows:
		Action_Type = int(row[2])
		Zone_ID = int(row[1])
		
		if int(row[2]) == 1:
			#Occupied zone expired
			query = ("UPDATE `homepi`.`zones` SET `occupied`=0 WHERE `id`=%d;" % (Zone_ID))
			DBQuery(2,query)
			logging("Action: Zone %s has been set to unoccupied." % GetZoneName(Zone_ID))
			
		elif int(row[2]) == 2:
			#All Lights Off
			logging("Action: Turning off all lights in zone %s." % GetZoneName(Zone_ID))
			# TODO 
	
	return
##############################################################################
def ZoneOccupied(Zone_ID):
	query = ("SELECT * FROM `homepi`.`zones` WHERE `id`=%d;" % Zone_ID)
	rows = DBQuery(1,query)
	for row in rows:
		return bool(row[3])
	return False
##############################################################################
def MotionInZone(Zone_ID):
	query = ("SELECT * FROM `homepi`.`zones` WHERE `id`=%d;" % Zone_ID)
	rows = DBQuery(1,query)
	if not (rows):
		logging("ERROR: failed to select zone!")
		return
		
	for row in rows:
		Zone_Occupied = bool(row[3])
		Zone_Type = int(row[2])
		Zone_Name = str(row[1])
		
	ModeID = int(GetHouseMode())
	
	#House Mode is 
	if ModeID == 1:
		#If away then set occupied
		if not Zone_Occupied: 
			SetOccupied(Zone_ID)
		
	elif ModeID == 2:
		#If Occupied check zone occupied
		if not Zone_Occupied: 
			SetOccupied(Zone_ID)
		else:
			ExtendOccupied(Zone_ID)
		
	elif ModeID == 3:
		#If night then be quiet!
		if not Zone_Occupied: 
			SetOccupied(Zone_ID)
		
	elif ModeID == 4:
		#If security armed then send alerts!
		if Zone_Type > 0:
			#Send email/text message
			TimeNow = strftime("%H:%M", time.localtime(time.time()))
			Body = "Alarm has been raised at %s due to sensor in %s zone." % (TimeNow,Zone_Name)
			SendMessage(Body,"HomePi Alarm")
			logging("Alert: Sending email!")
			
			if not Zone_Occupied: 
				SetOccupied(Zone_ID)
		
	return
##############################################################################
def SetOccupied(Zone_ID):
	global LightsOff
	time_now = strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	query = ("UPDATE `homepi`.`zones` SET `occupied`='1', `occupied_time`='%s' WHERE `id`=%d;" % (time_now, Zone_ID))
	DBQuery(2,query)
	
	dt = datetime.timedelta(minutes=LightsOff)
	EventTime = datetime.datetime.now() + dt
	query = ("INSERT INTO `homepi`.`zone_action` (`zone_id`, `action_type`, `action_value`, `time_stamp`) VALUES (%d, 1, 0, '%s');" % (Zone_ID, EventTime))
	DBQuery(2,query)	
		
	logging("Zone: %s has been set to occupied and will expire in %s mins." % (GetZoneName(Zone_ID), LightsOff))
	return
##############################################################################
def ExtendOccupied(Zone_ID):
	query = ("SELECT * FROM `homepi`.`zone_action` WHERE `time_stamp` > now() AND `zone_id`=%d;" % Zone_ID)
	rows = DBQuery(1,query)
	if not (rows):
		return False
	for row in rows:
		Mod_ID = int(row[0])
		dt = datetime.timedelta(minutes=LightsOff)
		EventTime = datetime.datetime.now() + dt
		query = ("UPDATE `homepi`.`zone_action` SET `time_stamp`='%s' WHERE `id`=%d;" % (EventTime,Mod_ID))
		DBQuery(2,query)
		time_now = strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		query = ("UPDATE `homepi`.`zones` SET `occupied`='1', `occupied_time`='%s' WHERE `id`=%d;" % (time_now, Zone_ID))
		DBQuery(2,query)
	return True
##############################################################################
def SetOccupiedZones(SetType):
	SetData = SetType.split("/")
	SetID = int(SetData[0])
	SetValue = int(SetData[1])
	if SetID == 0:
		#Reset all zones to value
		query = ("UPDATE `homepi`.`zones` SET `occupied`=0 WHERE `occupied`=1;")	
	if SetID > 0:
		#Reset only this type zones to value
		time_now = strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		query = ("UPDATE `homepi`.`zones` SET `occupied`=%d, `occupied_time`='%s' WHERE `type`=%d;" % (SetValue,time_now,SetID))	
	DBQuery(2,query)
	logging("Action: Set zone type %s to occupied %s." % (SetID,bool(SetValue)))	
	return
##############################################################################
def GetZoneName(Zone_ID):
	Zone_Name = "Unknown"
	query = ("SELECT `id`,`name` FROM `homepi`.`zones` WHERE `id`=%d;" % Zone_ID)
	row = DBQuery(0,query)
	if not (row):
		logging("ERROR: Failed to GetZoneName!")
		return 
	return str(row[1])
##############################################################################
def SetMode(SetMode):
	query = ("UPDATE `homepi`.`config` SET `data`=%d WHERE `name`='mode';" % SetMode)
	return DBQuery(2,query)
##############################################################################
def GetHouseMode():
	query = ("SELECT `id`,`data` FROM `homepi`.`config` WHERE `name`='mode';")
	row = DBQuery(0,query)
	if not (row):
		logging("ERROR: Failed to get house mode!")
		return 0
	return int(row[1])
##############################################################################
def ModeCheck():
	global Mode
	ModeID = int(GetHouseMode())
	if Mode != ModeID:
		Mode = ModeID
		query = ("SELECT `id`,`name` FROM `homepi`.`modes` WHERE `id`=%d;" % Mode)
		row = DBQuery(0,query)
		HouseMode = row[1]
		logging("Action: House mode has been set to %s." % HouseMode)
		if Mode == 1:
			VolumeLevel = GetConfig("vol1")
		elif Mode == 2:
			VolumeLevel = GetConfig("vol2")
		elif Mode == 3:
			VolumeLevel = GetConfig("vol3")
		else:
			VolumeLevel = 0
		SetVolume(VolumeLevel)
		#Speak("House mode has been set to %s." % HouseMode)
	return
##############################################################################
def ScheduledTask():
	Today = datetime.datetime.today().weekday()
	week = {0:'M',1:'T',2:'W',3:'R',4:'F',5:'S',6:'N'}
	TaskTime = strftime("%H:%M:00", time.localtime(time.time()))
	query = ("SELECT * FROM `homepi`.`scheduled_task` WHERE `enabled`=1 AND `start`='%s' AND `%s`=1;" % (TaskTime, week[Today]))
	rows = DBQuery(1,query)
	if (rows):
		for row in rows:
			TaskName = row[1]
			TaskType = int(row[2])
			TaskData = row[3]
			logging("Running Task: %s at %s." % (TaskName,TaskTime))
			do_task(TaskType,TaskData)
	return
##############################################################################
def do_task(TaskType,TaskData):

	if TaskType == 1:
		#Data changes piface outputs
		data = TaskData.split("/")
		device_control(int(data[0]),int(data[1]),False)
		
	elif TaskType == 2:
		#Data is shell code
		# TODO santize command
		subprocess.call(TaskData, shell=True)
		
	elif TaskType == 3:
		#Set Thermostat to Data
		set_thermostat(int(TaskData))
			
	elif TaskType == 4:
		#Set House Mode
		SetMode(int(TaskData))
		
	elif TaskType == 5:
		#Set Zone Occupied Status
		SetOccupiedZones(TaskData)
		
	elif TaskType == 6:
		#AM/PM Greeting and Weather
		SpeakTime = strftime("%I %M %p", time.localtime(time.time()))
				
		if int(GetHour()) < 12:
			Speak("Good Morning. Today is %s." % (datetime.date.today().strftime("%A, %B %d")))
		else:
			Speak("Good Evening.")
			
		Speak("The time is now %s." % (SpeakTime.lstrip('0')))
		Forecast = GetForcast(TaskData)
		if (Forecast):
			Speak("The weather forecast is %s." % FixForcast(Forecast))

		OutsideTemp = GetTemp(GetConfig("outside_zone"))
		Speak("The conditions outside are %s with a temperature of %s degrees." % (GetForcast(9),OutsideTemp))
		
	elif TaskType == 7:
		#Get Sun Rise and Set 
		UpdateSunRiseSet()
		
	elif TaskType == 8:
		#Speak Data
		Speak(TaskData)
		
	return
##############################################################################
def hour_check():
	InsideTemp = GetTemp(GetConfig("inside_zone"))
	OutsideTemp = GetTemp(GetConfig("outside_zone"))
		
	ModeID = int(GetHouseMode())
	
	if ModeID == 2:
		SpeakTime = strftime("%I %p", time.localtime(time.time()))
		Speak("The time is now %s ." % (SpeakTime.lstrip('0')))
		Speak("The conditions outside are %s with a temperature of %s degrees." % (GetForcast(9),OutsideTemp))
	else:
		TimeNow = strftime("%H:%M", time.localtime(time.time()))
		logging("The time is now %s. The temperature is %s F inside, %s F outside." % (TimeNow,InsideTemp,OutsideTemp))
	
	if ModeID == 2:
		query = ('SELECT * FROM `homepi`.`zones` WHERE `occupied`=1 AND `type` > 0;')
		rows = DBQuery(1,query)
		if not (rows):
			SetMode(1)
	return
##############################################################################
def Speak(SpeakText):
	global Speaking
	while (Speaking):
		sleep(0.2)
	logging("Speaking: %s" % SpeakText)
	#parameter: rate, volume, pitch, range, punctuation, capitals, wordgap
	#espeak -v mb-en1 -s 140 "Hello, this is my voice" --stdout |aplay
	Speaking = True
	os.system('espeak -v mb-us3 -s 140 "{0}" --stdout |aplay > /dev/null 2>&1'.format(SpeakText)) 
	sleep(0.25)
	Speaking = False
	return
##############################################################################	
def SpeakData(SpeakID,ZoneID):
	if ZoneOccupied(ZoneID):
		return
	query = ("SELECT * FROM `homepi`.`speak` WHERE `id`=%d;" % (SpeakID))
	rows = DBQuery(1,query)
	if (rows):
		for row in rows:
			Speak(row[1])
	return
##############################################################################	
def SetVolume(VolumeLevel):  
	alsaaudio.Mixer('PCM').setvolume(int(VolumeLevel))
	logging("Config: Volume level %s%%." % VolumeLevel)
	return
##############################################################################	
def GetForcast(Period):
	global wunderground_api_key, wunderground_location
	Forecast = "Error!"
	openurl = "http://api.wunderground.com/api/%s/forecast/q/%s.json" % (wunderground_api_key,wunderground_location)
	try:
		wurl = urllib2.urlopen(openurl)
		json_string = wurl.read()
		if not (json_string):
			return Forecast		
		parsed_json = json.loads(json_string)
	except BaseException, e:
		ExceptionHand(e,"GetForcast")
		return Forecast	
	if int(Period) < 9:
		for data in parsed_json['forecast']['txt_forecast']['forecastday']:
			if int(Period) == int(data['period']):
				Forecast = data['fcttext']
				break
	else:
		Period = (int(Period) - 8)
		for data in parsed_json['forecast']['simpleforecast']['forecastday']:
			if int(Period) == int(data['period']):
				Forecast = data['conditions']
				break
	wurl.close()
	return Forecast
##############################################################################
def FixForcast(Forcast):
	#Format words for speech 
	dict = {
		'in.':'inches',
		'F ':' degrees ',
		'F. ':' degrees. ',
		' mph':' miles per hour',
		' N ':' north ',
		' S ':' south ',
		' W ':' west ',
		' E ':' east ',
		' NNW':' north, north west',
		' NNE':' north, north east',
		' SSW':' south, south west',
		' SSE':' south, south east',
		' NE':' north east',
		' NW':' north west',
		' SW':' south west',
		' SE':' south east'
		}
	for word in dict:
		Forcast = Forcast.replace(word, dict[word])
	return Forcast
##############################################################################
def UpdateSunRiseSet():
	global wunderground_api_key, wunderground_location
	openurl = "http://api.wunderground.com/api/%s/astronomy/q/%s.json" % (wunderground_api_key,wunderground_location)
	logging("Update: Downloading Sun Rise/Sun Set for today using location %s." % (wunderground_location))
	try:
		wurl = urllib2.urlopen(openurl)
		json_string = wurl.read()
		if not json_string:
			logging("Error: UpdateSunRiseSet | Invalid json string.")
			return	
	except BaseException, e:
		ExceptionHand(e,"UpdateSunRiseSet")
		return 
	
	parsed_json = json.loads(json_string)
	
	h = int(parsed_json['sun_phase']['sunrise']['hour'])
	m = int(parsed_json['sun_phase']['sunrise']['minute'])
	SunRise = "%02d:%02d:00" % (h,m)

	h = int(parsed_json['sun_phase']['sunset']['hour'])
	m = int(parsed_json['sun_phase']['sunset']['minute'])
	SunSet = "%02d:%02d:00" % (h,m)
		
	wurl.close()
	query = ("UPDATE `homepi`.`config` SET `data`='%s' WHERE `name`='sunrise';" % SunRise)
	DBQuery(2,query)
	query = ("UPDATE `homepi`.`config` SET `data`='%s' WHERE `name`='sunset';" % SunSet)
	DBQuery(2,query)
	logging("Config: Updated sunrise/sunset to %s/%s." % (SunRise, SunSet))
	
	query = ('SELECT `id`, `sun_time`, `sun_mod` FROM `homepi`.`scheduled_task` WHERE `sun_time` > 0;')
	rows = DBQuery(1,query)
	if not (rows):
		return
	for row in rows:
		sun_mod = str(row[2]).split(":")
		if row[1] == 1:
			SetTime = datetime.datetime(*time.strptime(SunRise,"%H:%M:%S")[:6]) + datetime.timedelta(hours=int(sun_mod[0]),minutes=int(sun_mod[1]))
		else:
			SetTime = datetime.datetime(*time.strptime(SunSet,"%H:%M:%S")[:6]) + datetime.timedelta(hours=int(sun_mod[0]),minutes=int(sun_mod[1]))
		
		UpdateTime = "%02d:%02d:%02d" % (SetTime.hour, SetTime.minute, SetTime.second)
		query = ("UPDATE homepi.scheduled_task SET start='%s' WHERE id=%d" % (UpdateTime,int(row[0])))
		DBQuery(2,query)
			
	return
##############################################################################	
def CheckUsers():
	# TODO: Events that change user and home status
	return
##############################################################################
def GetConfig(ConfigName):
	query = ("SELECT `data` FROM `homepi`.`config` WHERE `name`='%s';" % ConfigName)
	row = DBQuery(0,query)
	return row[0]
##############################################################################
def GetDevicebyID(PiFace_ID):
	query = ("SELECT * FROM `homepi`.`piface` WHERE `id`=%d;" % PiFace_ID)	
	return DBQuery(0,query)
##############################################################################
def DBQuery(Type,Query):
	global MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB
	retry_seconds = 30
	DB_Connected = False
	while not DB_Connected:
		try:
			db = mydb.connect(MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB)
			cur = mydb.cursors.Cursor(db)
			DB_Connected = True
		except BaseException, e:
			ExceptionHand(e,"DBQuery | Unable to connect to database %s. Retrying againin %d seconds!" % (MySQL_DB,retry_seconds))
			DB_Connected= False
			time.sleep(retry_seconds)
			pass

	try:
		cur.execute(Query)
		if Type == 0:
				results = cur.fetchone()
		elif Type == 1:
				results = cur.fetchall()
		elif Type == 2:
				db.commit()
				results = True
		cur.close()
		
	except BaseException, e:
		ExceptionHand(e,"DBQuery | %s." % (Query))
		results = False
		pass

	if results == None:
		logging("Database Query Failed! | %s." % (Query))
		results = False
	return results
##############################################################################
def dbinit():
	global MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB
	global DB_ERROR, db
	try:
		db = mydb.connect(MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB)
		cur = mydb.cursors.Cursor(db)
		cur.execute("SET SESSION tx_isolation='READ-COMMITTED';")
		cur.execute("SELECT VERSION()")
		row = cur.fetchone()
		ver = str(row[0])
		logging("Config: Connected to MySQL Server at %s, version %s " % (MySQL_Host, ver))
	except mydb.Error, e:
		DB_ERROR = True
		logging("Error dbinit | %d: %s" % (e.args[0],e.args[1]))
		cur.close()
		return False
	return True
##############################################################################
def logging(Message):
	global STDOUT_SHELL, LOG_FILE, DB_ERROR
	
	LOG_TEXT = "%s : %s" % (strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), Message)
	
	if STDOUT_SHELL:
		#Stdout to shell
		print strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), ":", Message
	
	#Write to logfile
	try:
		target = open(LOG_FILE, 'a')
		target.truncate()
		target.write(LOG_TEXT)
		target.write("\n")
		target.close()
	except BaseException, e:
		ExceptionHand(e,"Log Write | %s." % (LOG_FILE))
		pass
		
	if not DB_ERROR:
		#logging events to database
		HostName = "homepi"
		query = ('INSERT INTO `homepi`.`logging` (`board`, `message`) VALUES ("%s", "%s");' % (HostName, Message))
		DBQuery(2,query)
	return
##############################################################################	
def ExceptionHand(error,called_from):
	global DB_ERROR
	DB_ERROR = True
	logging("Error: %s  %s %s." % (called_from,sys.exc_info()[0],error))
	if not (error.args):
		return
	if (error.args[0] == 2013) or (error.args[0] == 2006):
		DataBaseReady = False
		while not DataBaseReady:
			sleep(1)
			DataBaseReady = dbinit()
		DB_ERROR = False
		logging("Success! Connected to MySQL Server at %s." % MySQL_Host)
	return
##############################################################################
def GetMinute():
	return strftime("%M", time.localtime(time.time()))
##############################################################################
def GetHour():
	return strftime("%H", time.localtime(time.time()))
##############################################################################
def SendMessage(Body,Subject):
	# create the email
	message = '""%s""' % Body
	msg	= MIMEText(message)
	msg['Subject'] = Subject
	msg['From'] = 'HomePi <homepi@rd3solutions.com>'
	msg['To'] = 'rob@rd3solutions.com'
	# send the email
	s = smtplib.SMTP('mail.rd3solutions.com')
	#s.login('username', 'password')
	s.sendmail
	s.quit()
	return
##############################################################################
# Main 
##############################################################################
def Main():
	global Version, should_stop, HTTP_Port, db, Today
	global FuranceRunning, Thermostat_Temp, LightsOff, DELAY, Mode
	global Furnace_Pin, Furnace_Board, Furnace_ID
	global pfd, PiFace_Boards, PiFace_Inputs
	global Speaking, OnValue, OffValue
	global wunderground_api_key, wunderground_location
	if DEBUG_LOG:
		print ("HomePi Version %s | 2013-10-19 Robert Dunmire III" % Version)
		print ("HomePi Startup.")
	Today = datetime.datetime.today().weekday()
	OnOff = {0:'off',1:'on'}
	OnValue = 1
	OffValue = 0
	Mode = 0
	should_stop = False
	Speaking = False
	db = False	
	logging("HomePi Startup.")
	logging("##############################################################")
	logging("HomePi Version %s | 2013-10-19 - 2016-05-28 Robert Dunmire III" % Version)
	logging("##############################################################")
	logging("Config: Attempting to init database connection.")
	query = ("SELECT piface.id, piface.board, piface.pin, piface.status FROM piface INNER JOIN devices ON piface.device=devices.id WHERE devices.name = 'thermostat';")	
	row = DBQuery(0,query)
	#Thermostat
	Furnace_Pin = int(row[2])
	Furnace_Board = int(row[1])
	Furnace_ID = int(row[0])
	FuranceRunning = bool(row[3])
	
	Thermostat_Temp = GetConfig("thermostat_temp")
	LightsOff = int(GetConfig("LightsOff"))
	DELAY = int(GetConfig("Delay"))	
	logging("Config: Poll delay = %d sec; Lights off delay = %d min." % (LightsOff,DELAY))
	
	wunderground_api_key = GetConfig("wunderground_api_key")
	wunderground_location = GetConfig("wunderground_location")
	
	logging("Config: pifacedigitalio version = %s" % pfdioV.__version__)
	logging("Config: pifacecommon version = %s " % pfcV.__version__)
	
	# GPIOB is the input ports. Set up interrupts
	PiFace_Boards = 1
	PiFace_Inputs = 8
	###
	for PiFace_Number in range(PiFace_Boards):
		pifacedigitalio.init(PiFace_Number)
		logging("Config: Init PiFace Board %s." % PiFace_Number)
		pfd = pifacedigitalio.PiFaceDigital(hardware_addr=PiFace_Number)
		listener = pifacedigitalio.InputEventListener(chip=pfd)
		for i in range(PiFace_Inputs):
			query = ("SELECT * FROM homepi.piface WHERE output=0 AND board=%d AND pin=%d;" % (PiFace_Number,i))
			row = DBQuery(0,query)
			PiFace_Name = str(row[6])
			if bool(row[9]):
				#Device is NC pifacedigitalio.IODIR_FALLING_EDGE pifacecommon.interrupts.IODIR_OFF
				listener.register(i, pifacedigitalio.IODIR_RISING_EDGE, event_interrupt, settle_time=0.1)
				logging("Config: PiFace Board %s, Input %s-%s is NC." % (PiFace_Number,i,PiFace_Name))
			else:
				#Device is NO IODIR_FALLING_EDGE
				listener.register(i, pifacedigitalio.IODIR_FALLING_EDGE, event_interrupt, settle_time=0.1)
				logging("Config: PiFace Board %s, Input %s-%s is NO." % (PiFace_Number,i,PiFace_Name))
			pifacedigitalio.digital_write_pullup(i, 1, hardware_addr=PiFace_Number)
	###	
	logging("Thread: Starting listener for %d interrupts!" % (int(PiFace_Boards * PiFace_Inputs)))
	sleep(0.2)
	listener.activate()
	
	#HTTP Server tcp port 8888
	http_thread = threading.Thread(name='http_server', target=HTTP_Server)
	http_thread.start()
	sleep(0.2)
	
	thermostat_control(OffValue)
	UpdateSunRiseSet()
	SetOccupiedZones("0/0")
	ModeCheck()
	logging("########### Starting Main() Events Loop! ###########")
	lastminute = int(GetMinute())
	lasthour = int(GetHour())
	hour = lasthour
	try:
		#####################
		while not should_stop:
			minute = int(GetMinute())
			if int(minute) != int(lastminute):
				lastminute = int(minute)
				ScheduledTask()
				event_check()
				zone_check()
				ModeCheck()
				CheckUsers()
				hour = int(GetHour())
			if int(hour) != int(lasthour):
				lasthour = int(hour)
				hour_check()
				LightsOff = int(GetConfig("LightsOff"))
				DELAY = int(GetConfig("Delay"))
			thermostat_check()
			sleep(DELAY)
		#####################
		
	except KeyboardInterrupt:
		logging("Quit: Stopping Main()")
		print("HomePi: Exiting...")
		pass
	else:
		pass
		
	try:	
		listener.deactivate()
		pifacedigitalio.deinit()
	except:
		pass
		
	should_stop = True	
	closeurl = urllib2.urlopen("http://127.0.0.1:8888/quit/0/").read()
	threading.Event()
	http_thread.join()
	print("HomePi: Quit!")
	sys.exit()
	return
##############################################################################
if __name__ == "__main__":
	Main()
##############################################################################
