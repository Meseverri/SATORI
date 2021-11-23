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

def timestamps_to_datetime(series,id):
    timestames=[]
    Dict={"year":[0,4],
    "month":[5,7],
    "day":[8,10],
    "time":11}
    if id!="time":
        flt1=Dict[id][0]
        flt2=Dict[id][1]
        for i in series:
            
            timestames.append(int(str(i)[flt1:flt2]))
    else:
        flt1=Dict[id]
        for i in series:    
            timestames.append(str(i)[flt1:])
    return timestames

# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# importamos el módulo pandas para mostrar los datos obtenidos en forma de recuadro

pd.set_option('display.max_columns', 500) # cuántas columnas mostramos
pd.set_option('display.width', 1500)      # anchura máx. del recuadro para la muestra
# importamos el módulo pytz para trabajar con el huso horario TC, para que no se aplique el desplazamiento del huso horario local
utc_from = datetime.datetime.today()
 
# establecemos la conexión con el terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# establecemos el huso horario en UTC
timezone = pytz.timezone("Europe/Vienna")
# creamos el objeto datetime en el huso horario U020 en el huso horario UTC
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, utc_from, 10000)
 
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()

# creamos un DataFrame de los datos obtenidos
rates_frame = pd.DataFrame(rates)
# convertimos la hora en segundos al formato datetime
#rates_frame.set_index("time")
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')



            rates_frame.insert(0,"year",timestamps_to_datetime(rates_frame['time'],"year"))
            rates_frame.insert(1,"month",timestamps_to_datetime(rates_frame['time'],"month"))
            rates_frame.insert(2,"day",timestamps_to_datetime(rates_frame['time'],"day"))
            rates_frame.insert(3,"weekday",rates_frame["time"].dt.dayofyear)

            rates_frame["time"]=timestamps_to_datetime(rates_frame['time'],"time")
            rates_frame.set_index(["year","month","day","time","weekday"])

print(rates_frame.groupby(["year","month","day","time"]))
    

print(rates_frame.head)
rates_frame.to_excel("EUROUSD_candels.xlsx")