import sys
import ConfigParser
from datetime import datetime, date
import math
import zmq
import time

if len(sys.argv) == 1:
    print "Usage: python ... [config.ini]"
    sys.exit(0)

configfile = sys.argv[1]

###################################################
# config
###################################################
config = ConfigParser.ConfigParser()
config.read(configfile)
ServerPort     = int(config.get("ARIMA", "ServerPort"    ))
TrainingPeriod = int(config.get("ARIMA", "TrainingPeriod"))
MaxBarInterval = int(config.get("ARIMA", "MaxBarInterval"))
PriceFolder    =     config.get("ARIMA", "PriceFolder"   )
CoefFolder     =     config.get("ARIMA", "CoefFolder"    )
ForecastFolder =     config.get("ARIMA", "ForecastFolder")

###################################################
# zmq
###################################################
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:%s" % ServerPort)

while True:
    socket.send('2016-06-02,AGG,1,2,3,4')
    print socket.recv()
    time.sleep(1)
