#candels table:

import datetime
import numpy as np
from numpy.core.numeric import NaN
from numpy.core.records import array
import pytz
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# importamos el módulo pandas para mostrar los datos obtenidos en forma de recuadro

pd.set_option('display.max_columns', 500) # cuántas columnas mostramos
pd.set_option('display.width', 1500)      # anchura máx. del recuadro para la muestra
# importamos el módulo pytz para trabajar con el huso horario TC, para que no se aplique el desplazamiento del huso horario local
utc_from = datetime.datetime(2021,1,1)
utc_to=datetime.datetime.today()
print(utc_to)
# establecemos la conexión con el terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# establecemos el huso horario en UTC
#timezone = pytz.timezone("Europe/Vienna")
# creamos el objeto datetime en el huso horario U020 en el huso horario UTC

rates=mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_H1, utc_from, utc_to)
ticks = mt5.copy_ticks_range("EURUSD", utc_from,utc_to, mt5.COPY_TICKS_ALL)
print("Ticks received:",len(ticks))
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()

# creamos un DataFrame de los datos obtenidos
rates_frame = pd.DataFrame(rates)
# convertimos la hora en segundos al formato datetime
#rates_frame.set_index("time")
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
# create DataFrame out of the obtained data
ticks_frame = pd.DataFrame(ticks)
# convert time in seconds into the datetime format
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')


##find the asian hour:
###create new colum called session
# ( if the 00:00<=datetime(time atribute) and datetime(time atribute)<=)
#Extraer tick y candels

print("last candel:\n",rates_frame.iloc[-1,:])
print("last tick:\n",ticks_frame.iloc[-1,:])
rates_frame=rates_frame[rates_frame["time"]>=datetime.datetime(2021,1,4)]
ticks_frame=ticks_frame[ticks_frame["time"]>=datetime.datetime(2021,1,4)]
print("DATA START AT ",str(datetime.datetime(2021,1,4)))
print(rates_frame.head(25))
#lets create and see how one day sample will look like
rates_sample_1= rates_frame[rates_frame["time"]<datetime.datetime(2021,1,5)]
ticks_sample_1=ticks_frame[ticks_frame["time"]<datetime.datetime(2021,1,5)]
#rates_frame.to_excel("EUROUSD_candels.xlsx")
print("Rates sample 1\n",rates_sample_1)
print("Ticks sample 1\n",ticks_sample_1)
#from the dayly sampple we need to find the H.H and the lowest low for the first 7 hours of the day
asian_setion_dt=rates_sample_1[rates_sample_1["time"]<datetime.datetime(2021,1,4,8)]
ticks_post_Asetion_dt=ticks_sample_1[ticks_sample_1["time"]>=datetime.datetime(2021,1,4,7)]
print("Asian setion candels:\n",asian_setion_dt)
print("Post asian setion ticks:\n",ticks_post_Asetion_dt)