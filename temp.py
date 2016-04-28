#!/usr/bin/env python
##############################################################################
import os, subprocess, sys, time, datetime
import MySQLdb as mydb
from time import sleep, gmtime, strftime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

##############################################################################
Version = "0.3"
MySQL_Host = "10.128.2.252"
MySQL_User = "homepi"
MySQL_Pass = "raspberry!"
MySQL_DB = "homepi"
##############################################################################
def GetTemps():
	# id,inside,outside,humidy_in,humidy_out
	query = ("SELECT * FROM `homepi`.`tempzone` order by `date_time` desc limit 1;")
	return DBQuery(1,query)
##############################################################################
def GetSensorInZone(ZoneID):
	query = ("SELECT `ident` FROM `homepi`.`sensors` WHERE `zone_id`='%s';" % ZoneID)
	row = DBQuery(0,query)
	return row[0]
##############################################################################
def GetConfig(ConfigName):
	query = ("SELECT `data` FROM `homepi`.`config` WHERE `name`='%s';" % ConfigName)
	row = DBQuery(0,query)
	return row[0]
##############################################################################
def DBQuery(Type,Query):
        global MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB

        DB_Connected = False
        while not DB_Connected:
                #db = mydb.connect(MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB)
                try:
                        db = mydb.connect(MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB)
                        cur = mydb.cursors.Cursor(db)
                        DB_Connected = True
                except Exception, e:
                        ExceptionHand(e,"DBQuery | Unable to connect! Retrying!")
                        DB_Connected= False
                        time.sleep(120)
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
        except Exception, e:
                ExceptionHand(e,"DBQuery | %s." % (Query))
                results = False
                pass

        if results == None:
                logging("Database Query Failed! | %s." % (Query))
                results = False
        cur.close()
        return results
##############################################################################

def dbinit():
	global MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB
	global db
	try:
		db = mydb.connect(MySQL_Host, MySQL_User, MySQL_Pass, MySQL_DB)
		cur = mydb.cursors.Cursor(db)
		cur.execute("SET SESSION tx_isolation='READ-COMMITTED';")
		cur.execute("SELECT VERSION()")
		row = cur.fetchone()
		ver = str(row[0])
		logging("Config: Connected to MySQL Server at %s, version %s " % (MySQL_Host, ver))
	except mydb.Error, e:
		print "Error dbinit | %d: %s" % (e.args[0],e.args[1])	
		cur.close()
		return False
		
	return True
##############################################################################
def logging(Message):
	#Stdout to shell
	print strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), ":", Message
	#logging events to database
	HostName = "homepi-2"
	query = ('INSERT INTO `homepi`.`logging` (`board`, `message`) VALUES ("%s", "%s");' % (HostName, Message))
	DBQuery(2,query)
	return
##############################################################################	
def ExceptionHand(error,called_from):
	print "Error %s | %s." % (called_from,error)
	if (error.args[0] == 2013) or (error.args[0] == 2006):
		DataBaseReady = False
		while not DataBaseReady:
			print "Attempting to reconnect to database..."
			sleep(1)
			DataBaseReady = dbinit()
		print "Success! Connected to MySQL Server at %s." % MySQL_Host
	return
##############################################################################		
def temp_raw(sensor_id):
	temp_sensor = ('/sys/bus/w1/devices/%s/w1_slave' % sensor_id)
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines
##############################################################################	
def read_temp(sensor_id):
    lines = temp_raw(sensor_id)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw(sensor_id)

    temp_output = lines[1].find('t=')
	
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
##############################################################################			
def record_temp(zone_id,temp_c):
	query = ("INSERT `homepi`.`tempzone` (`temp`,`zone_id`) VALUES(%s,%s);" % (temp_c,zone_id))
	return DBQuery(2,query)
##############################################################################	
def C2F(c):
    return c * 9/5 + 32
##############################################################################
def GetMinute():
	return strftime("%M", time.localtime(time.time()))
##############################################################################
def GetHour():
	return strftime("%H", time.localtime(time.time()))
##############################################################################


##############################################################################
# Main Loop
##############################################################################		
def Main():	
	print ("##############################################################")
	print ("HomePi Temp Node Version %s | 2015-12-27 Robert Dunmire III" % Version)
	print ("##############################################################")
	
	logging("HomePi Temp Node Startup.")
	should_stop = False
	db = False	
	OutsideZone = int(GetConfig("outside_zone"))
	OutsideTemp = 0
	InsideZone = int(GetConfig("inside_zone"))
	InsideTemp = 0
	logging("Config: using outside zone %s." % OutsideZone)
	logging("Config: using inside zone %s." % InsideZone)
	logging("Config: outsize zone device %s." % GetSensorInZone(OutsideZone))
	logging("Config: inside zone device %s." % GetSensorInZone(InsideZone))
	TempInterval = int(GetConfig("temp_interval"))
	lastminute = int(GetMinute())
	lasthour = 0
	hour = int(GetHour())
	logging("Config: polling temperature every %s seconds." % TempInterval)
	logging("########### Starting Main() Events Loop! ###########")
	try:
		#####################	
		while not should_stop:
				OutsideTemp = read_temp(GetSensorInZone(OutsideZone))
				record_temp(OutsideZone,OutsideTemp)
				time.sleep(0.25)
				InsideTemp = read_temp(GetSensorInZone(InsideZone))
				record_temp(InsideZone,InsideTemp)
				hour = int(GetHour())
				if int(hour) != int(lasthour):
					lasthour = int(hour)
					logging("Outside tempature is now: %s C, %s F." % (OutsideTemp,C2F(OutsideTemp)))
					logging("Inside tempature is now: %s C, %s F." % (InsideTemp,C2F(InsideTemp)))
				time.sleep(TempInterval)
				
		#####################			
	except KeyboardInterrupt:
		logging("Quit: Stopping Main()")
		print("HomePi: Exiting...")
		pass
	else:
		pass

	print("HomePi Temp Node: Quit!")
	sys.exit()
	return
		
##############################################################################
if __name__ == "__main__":
	Main()
##############################################################################