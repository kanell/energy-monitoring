#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 12:16:42 2016

@author: Felix
"""

import pandas as pd
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import json
import datetime as dt
import os
import numpy as np
import math


jsonpath    = 'jsonfiles'
IP          = '129.69.176.123'
os.makedirs(jsonpath, exist_ok=True)


def read_port_csv():
    '''Reads Confic-Ports-CSV-File and sets adresses as Index (Adress_DF).\n
    The DataFrame Ports_DF is later used to fetch the data-tuple via Modbus TCP/IP.
    The Start, End and Range parameter is used to set the start, lenght and steprange
    in each tulpe.'''
    Adress_DF = pd.read_csv( 'Port.csv')    
    Ports_DF = pd.DataFrame(columns = ['Start','End','Range']).apply(int)
    Start = Adress_DF.at[0,'Adresse']
    for i in Adress_DF.index:
        try:
            if i+1 == len(Adress_DF):
                Range_Num = Adress_DF.at[i,'Adresse']-Adress_DF.at[i-1,'Adresse']
                Row = pd.DataFrame(data = [[Start,Adress_DF.at[i,'Adresse'],Range_Num]],columns = ['Start','End','Range'])
                Ports_DF = pd.concat([Ports_DF,Row])
                Start = Adress_DF.at[i,'Adresse']
            elif (Adress_DF.at[i,'Adresse']-Adress_DF.at[i-1,'Adresse']) == (Adress_DF.at[i+1,'Adresse']-Adress_DF.at[i,'Adresse']):
                pass
            else:
                if Start == Adress_DF.at[i,'Adresse']:
                    pass
                else:
                    Range_Num = Adress_DF.at[i,'Adresse']-Adress_DF.at[i-1,'Adresse']
                    Row = pd.DataFrame(data = [[Start,Adress_DF.at[i,'Adresse'],Range_Num]],columns = ['Start','End','Range'])
                    Ports_DF = pd.concat([Ports_DF,Row])
                    Start = Adress_DF.at[i+1,'Adresse']
        except KeyError:
            pass
    Ports_DF = Ports_DF.set_index(np.arange(0,(len(Ports_DF))))
    Ports_DF = Ports_DF.astype(int)
    Adress_DF = Adress_DF.set_index('Adresse')
    Adress_DF['Data'] = pd.Series(np.NaN, index=Adress_DF.index).astype(object)
    return Adress_DF, Ports_DF


def connection(IP):
    '''Connect to Janitza via Modbus'''
    master = modbus_tcp.TcpMaster(host = IP)
    master.set_timeout(5)    
    return master


def fetch_raw(master,Start):
    '''Fetches data via Modbus. Can only take 123 floating point numbers at once.'''
    Raw_Data = master.execute(1, cst.READ_HOLDING_REGISTERS,Start, 123)
    return Raw_Data


def fetch_data_dataframe(Adress_DF,Ports_DF,master):
    '''Fetches data by port-series from Modbus and stores it converted in 
    seperat DataFrame.'''
    Start_time = dt.datetime.now()
    Data_DF = pd.DataFrame(Adress_DF['Data'])
    for i in Ports_DF.index:
        data = ()
        n = 0
        Delta = Ports_DF.at[i,'End'] - Ports_DF.at[i,'Start']
        if Delta < 123:
            Start = Ports_DF.at[i,'Start']
            data = data + fetch_raw(master,Start)
            for m in range(Ports_DF.at[i,'Start'],Ports_DF.at[i,'End']+1,2):
                Data_DF.at[m,'Data'] = convert_to_float(data[n:n+2])
                n += Ports_DF.at[i,'Range']
        else:
            X = math.ceil(Delta/123)
            for k in range(0,X):
                Start =  Ports_DF.at[i,'Start']+k*124
                data = data + fetch_raw(master,Start)
            if Ports_DF.at[i,'Range'] == 2:
                for m in range(Ports_DF.at[i,'Start'],Ports_DF.at[i,'End']+1,2):
                    Data_DF.at[m,'Data'] = convert_to_float(data[n:n+2])
                    n += Ports_DF.at[i,'Range']
                

    End_time = dt.datetime.now()
    TimeDelta = End_time - Start_time
    print (TimeDelta)
    return Data_DF


def fetch_data_dict(Adress_DF,Ports_DF,master):
    '''Fetches data by port-series from Modbus and stores it converted in 
    seperat dict.'''
    Start_time = dt.datetime.now()
    Data_dict = Adress_DF['Data'].to_dict()    
    for i in Ports_DF.index:
        data = ()
        n = 0
        Delta = Ports_DF.at[i,'End'] - Ports_DF.at[i,'Start']
        if Delta < 123:
            Start = Ports_DF.at[i,'Start']
            data = data + fetch_raw(master,Start)
            for m in range(Ports_DF.at[i,'Start'],Ports_DF.at[i,'End']+1,2):
                Data_dict[m] = convert_to_float(data[n:n+2])
                n += Ports_DF.at[i,'Range']
        else:
            X = math.ceil(Delta/123)
            for k in range(0,X):
                Start =  Ports_DF.at[i,'Start']+k*124
                data = data + fetch_raw(master,Start)
            if Ports_DF.at[i,'Range'] == 2:
                for m in range(Ports_DF.at[i,'Start'],Ports_DF.at[i,'End']+1,2):
                    Data_dict[m] = convert_to_float(data[n:n+2])
                    n += Ports_DF.at[i,'Range']
    
    End_time = dt.datetime.now()
    TimeDelta = End_time - Start_time
    print (TimeDelta)
    return Data_dict

    
def convert_to_float(data):
    '''Converts floating point number (IEEE 754) into normal float.'''
    sign = 1 if data[0] < 32768 else -1
    exponent = ((data[0] % 2**15) >> 7) - 127
    high0 = data[0] % 128 * 2**16
    low0 = data[1]
    mantisse = (high0 + low0) % 2**23    
    return round(sign * (1.0 + mantisse / 2**23) * 2**exponent, 4)

