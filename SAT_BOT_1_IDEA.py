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

rates=mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M10, utc_from, utc_to)
ticks =mt5.copy_ticks_range("EURUSD", utc_from,utc_to, mt5.COPY_TICKS_ALL)
print("Ticks received:",len(ticks))
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()
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

"""print("last candel:\n",rates_frame.iloc[-1,:])
print("last tick:\n",ticks_frame.iloc[-1,:])"""
ticks_frame=ticks_frame.drop(["last","volume","time_msc","flags","volume_real"],axis=1)
rates_frame=rates_frame[rates_frame["time"]>=datetime.datetime(2021,1,4)]
ticks_frame=ticks_frame[ticks_frame["time"]>=datetime.datetime(2021,1,4)]
print("DATA START AT ",str(ticks_frame.iloc[0,0]))

#lets create and see how one day sample will look like
rates_sample_1= rates_frame[rates_frame["time"]<datetime.datetime(2021,1,5)]
ticks_sample_1=ticks_frame[ticks_frame["time"]<datetime.datetime(2021,1,5)]
print("Rates sample 1\n",rates_sample_1)
print("Ticks sample 1\n",ticks_sample_1)
#from the daily sample we need to find the H.H and the lowest low for the first 7 hours of the day
asian_setion_dt=rates_sample_1[rates_sample_1["time"]<=datetime.datetime(2021,1,4,8)]
P0=asian_setion_dt["low"].min()
P1=asian_setion_dt["high"].max()
#tick variables for 7:00 -9:00
ticks_post_Asetion_dt=ticks_sample_1[ticks_sample_1["time"]>=datetime.datetime(2021,1,4,7)][ticks_sample_1["time"]<=datetime.datetime(2021,1,4,9)]
print("Asian setion candels:\n",asian_setion_dt)
print("Asian setion structure:\n",[asian_setion_dt["low"].min(),asian_setion_dt["high"].max(),asian_setion_dt["high"].max()-asian_setion_dt["low"].min()])

ticks_post_Asetion_dt["range indicator bid"]=Afin_indicator(P0,P1,ticks_post_Asetion_dt["bid"])
ticks_post_Asetion_dt["range indicator ask"]=Afin_indicator(P0,P1,ticks_post_Asetion_dt["ask"])
print("Post asian setion ticks size:\n",ticks_post_Asetion_dt)
print("How many times the price was out of range in the next 2 hours after ")
print("L BOS:",len(ticks_post_Asetion_dt[ticks_post_Asetion_dt["range indicator bid"]<=0].index))
print("H BOS:",len(ticks_post_Asetion_dt[ticks_post_Asetion_dt["range indicator ask"]>=1].index))
#Highest 
print(ticks_post_Asetion_dt[ticks_post_Asetion_dt["range indicator ask"]>=1].max())

print("in or out")
print("bid")
count=0
for i in range_list(ticks_post_Asetion_dt["range indicator bid"].tolist()):
    
    if i=="high breakout":
        print(i,count)
        count+=1
    elif i=="low breakout":
        print(i,count)
        count+=1
    else:
        count+=1
count=0
print("ask")
for i in range_list(ticks_post_Asetion_dt["range indicator ask"].tolist()):
    
    if i=="high breakout":
        print(i,count)
        count+=1
    elif i=="low breakout":
        print(i,count)
        count+=1
    else:
        
        count+=1





with pd.ExcelWriter("EUROUSD_ticks_sample_1.xlsx") as writer:  
    ticks_post_Asetion_dt.to_excel(writer, sheet_name='Tick sample 1')
    rates_sample_1.to_excel(writer, sheet_name='Candels sample')

