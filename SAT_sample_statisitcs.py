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
utc_from = datetime.datetime(2021,1,4)
utc_to=datetime.datetime.today()
print(utc_to)
# establecemos la conexión con el terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# establecemos el huso horario en UTC
#timezone = pytz.timezone("Europe/Vienna")
# creamos el objeto datetime en el huso horario U020 en el huso horario UTC

rates=mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M10, utc_from, utc_to)
ticks =mt5.copy_ticks_range("EURUSD", utc_from,utc_to, mt5.COPY_TICKS_ALL)
print("Ticks received:",len(ticks))
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()
utc_rnow=datetime.datetime.today()
print("time taken",utc_rnow-utc_to)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
ticks_frame = pd.DataFrame(ticks)
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
ticks_frame=ticks_frame.drop(["last","volume","time_msc","flags","volume_real"],axis=1)
#gets the highs and lows of the atian setion
def sampleLoop(candelsdf,hourStart=0,hourfinish=7):
    time_list=candelsdf["time"].tolist()
    startdate=time_list[0]
    delta=datetime.timedelta(1)
    HL_list=[]
    for i in time_list:
        print(i)
    return startdate+delta


def Afin_indicator(PO,P1,P):
    #PO is min, P1 max
    Len=P1-P0
    return(P-P0)/Len

#esta funcion nos permitira saber si pd series del range indicator a roto por primera vez
def first_BO(serie):
    default=False
    return default

#esta funcion regresa un booleano si el indicador esta fuera del rago
def range(Aind):
    if Aind>0 and Aind<1:
        return "inside range"
    elif Aind<=0:
        return "low breakout"
    elif Aind>=1:
        return "high breakout"
        
def range_list(Ainds):
    l=[]
    for i in Ainds:
        l.append(range(i))

    return l

print(sampleLoop(rates_frame))
print(rates_frame.head())
# mostramos los datos sobre el paquete MetaTrader5
