#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 12:16:42 2016

@author: Felix
"""

import pandas as pd
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
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
    addresses = pd.read_csv('port.csv')['Adresse']
    ports = pd.DataFrame(columns = ['start','end','range']).astype(int)
    start = addresses[0]
    for i in addresses.index:
        try:
            if i == addresses.size - 1:
                range_num = addresses[i] - addresses[i-1]
                row = pd.DataFrame(data = [[start,addresses[i],range_num]], columns = ['start','end','range'])
                ports = ports.append(row)
                start = addresses[i]
            elif (addresses[i] - addresses[i-1]) == (addresses[i+1]-addresses[i]):
                pass
            else:
                if start == addresses[i]:
                    pass
                else:
                    range_num = addresses[i] - addresses[i-1]
                    row = pd.DataFrame(data = [[start,addresses[i],range_num]], columns = ['start','end','range'])
                    ports = ports.append(row)
                    start = addresses[i+1]
        except KeyError:
            pass
    ports = ports.set_index(np.arange(ports.index.size))
    dataframe = pd.Series(np.NaN, index=addresses, name='data').astype(float)
    return dataframe, ports, addresses


def connection(IP):
    '''Connect to Janitza via Modbus'''
    master = modbus_tcp.TcpMaster(host = IP)
    master.set_timeout(5)
    return master


def fetch_raw(master,start):
    '''Fetches data via Modbus. Can only take 123 floating point numbers at once.'''
    raw_data = master.execute(1, cst.READ_HOLDING_REGISTERS,start, 123)
    return raw_data

def fetch_raw_new(master,port):
    '''Fetches data via Modbus. Can only take 123 floating point numbers at once.'''
    raw_data = master.execute(1, cst.READ_HOLDING_REGISTERS,port, 1)
    return raw_data

def fetch_data_dataframe(dataframe,ports,master):
    '''Fetches data by port-series from Modbus and stores it converted in
    seperat DataFrame.'''
    start_time = dt.datetime.now()
    for i in ports.index:
        data = ()
        n = 0
        delta = ports.at[i,'end'] - ports.at[i,'start']
        if delta < 123:
            start = ports.at[i,'start']
            data = data + fetch_raw(master,start)
        else:
            x = math.ceil(delta/123)
            for k in range(x):
                start =  ports.at[i,'start']+k*124
                data = data + fetch_raw(master,start)
        if ports.at[i,'range'] == 2:
            for m in range(ports.at[i,'start'],ports.at[i,'end']+1,ports.at[i,'range']):
                dataframe[m] = convert_to_float(data[n:n+2])
                n += ports.at[i,'range']

    end_time = dt.datetime.now()
    timedelta = end_time - start_time
    print (timedelta)
    return dataframe


def convert_to_float(data):
    '''Converts floating point number (IEEE 754) into normal float.'''
    sign = 1 if data[0] < 32768 else -1
    exponent = ((data[0] % 2**15) >> 7) - 127
    high0 = data[0] % 128 * 2**16
    low0 = data[1]
    mantisse = (high0 + low0) % 2**23
    return round(sign * (1.0 + mantisse / 2**23) * 2**exponent, 4)