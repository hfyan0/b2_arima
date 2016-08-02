import zmq
import random
import time
import sys
import ConfigParser
from datetime import datetime, date
import math
from b2_arima_common import B2_rpy_arima


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
# obj
###################################################
b2_rpy_arima = B2_rpy_arima(configfile)

###################################################
# load previous forecasts
###################################################

print "Start loading previous forecasts"
b2_rpy_arima.load_prev_forecasts()
print "Finished loading previous forecasts"

###################################################
# zmq
###################################################
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % ServerPort)

while True:
    message = socket.recv()
    msg_csv = message.split(",")
    if len(msg_csv) < 6:
        continue
    dt = datetime.strptime(msg_csv[0],"%Y-%m-%d").date()
    sym = msg_csv[1]
    o = msg_csv[2]
    h = msg_csv[3]
    l = msg_csv[4]
    c = msg_csv[5]

    socket.send(str(b2_rpy_arima.get_prev_forecast(dt,sym)))

