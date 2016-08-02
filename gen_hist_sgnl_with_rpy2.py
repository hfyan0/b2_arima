import sys
import ConfigParser
from datetime import datetime
import math
from b2_arima_common import B2_rpy_arima


if len(sys.argv) == 1:
    print "Usage: python ... [config.ini] [symbol]"
    sys.exit(0)

configfile = sys.argv[1]
symbol = sys.argv[2]
print symbol

###################################################
# config
###################################################
config = ConfigParser.ConfigParser()
config.read(configfile)
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
# get historical price data
###################################################
(py_ls_date_full, py_ls_ln_avgpx_full) = b2_rpy_arima.get_hist_price_data(symbol)

###################################################
outfile_coef = open(CoefFolder+"/"+symbol+".csv", "w")
outfile_fcast = open(ForecastFolder+"/"+symbol+".csv", "w")

###################################################
# loop through historical data
###################################################
for how_many_days_bk in range(1,len(py_ls_date_full)):

    for barintvl in range(1,MaxBarInterval+1):

        for barintvlshift in range(0,barintvl):

            (py_fit_coef, fc_pxreturn_1d) = b2_rpy_arima.calc_forecast(py_ls_date_full, py_ls_ln_avgpx_full, how_many_days_bk, barintvl, barintvlshift)

            if py_fit_coef is None or fc_pxreturn_1d is None:
                continue

            outfile_coef.write(str(py_ls_date_full[-how_many_days_bk]))
            outfile_coef.write(",")
            outfile_coef.write(symbol)
            outfile_coef.write(",")
            outfile_coef.write(str(how_many_days_bk))
            outfile_coef.write(",")
            outfile_coef.write(str(barintvl))
            outfile_coef.write(",")
            outfile_coef.write(str(barintvlshift))
            outfile_coef.write(",")
            outfile_coef.write(",".join(map(lambda x: str(x), py_fit_coef)))
            outfile_coef.write("\n")

            outfile_fcast.write(str(py_ls_date_full[-how_many_days_bk]))
            outfile_fcast.write(",")
            outfile_fcast.write(symbol)
            outfile_fcast.write(",")
            outfile_fcast.write(str(how_many_days_bk))
            outfile_fcast.write(",")
            outfile_fcast.write(str(barintvl))
            outfile_fcast.write(",")
            outfile_fcast.write(str(barintvlshift))
            outfile_fcast.write(",")
            outfile_fcast.write(str(fc_pxreturn_1d))
            outfile_fcast.write("\n")


outfile_coef.close()
outfile_fcast.close()
