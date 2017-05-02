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
import numpy as np
from numpy import binary_repr
import math


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

def fetch_raw_new(master,start,end):
    '''Fetches data via Modbus. Can only take 123 floating point numbers at once.'''
    # it is necessary that the number of ports is even
    number_of_ports = end - start + 1
    if number_of_ports % 2: 
        number_of_ports += 1
    # data format is float
    data_format = '>' + number_of_ports // 2 * 'f'
    #print('start: {}, end: {}, number of ports: {}, data format: {}'.format(start,end,number_of_ports,data_format))
    raw_data = master.execute(1, cst.READ_HOLDING_REGISTERS, start, number_of_ports, 0, data_format)
    return raw_data

def fetch_data_dataframe(dataframe,ports,master):
    '''Fetches data by port-series from Modbus and stores it converted in
    seperat DataFrame.'''
    start_time = dt.datetime.now()
    for i in ports.index:
        n = 0
        delta = ports.at[i,'end'] - ports.at[i,'start']
        data = ()
        #print('delta: ' + str(delta))
        if delta < 123:
            start = ports.at[i,'start']
            end = ports.at[i,'end']
            data = data + fetch_raw_new(master,start,end)
        else:
            x = math.ceil(delta/122)
            for k in range(x):
                start =  ports.at[i,'start'] + k*122
                if k < x-1:
                    end = start + 121
                else:
                    end = ports.at[i,'end']
                data = data + fetch_raw_new(master,start,end)
        if ports.at[i,'range'] == 2:
            for n,m in enumerate(range(ports.at[i,'start'],ports.at[i,'end']+1,ports.at[i,'range'])):
                dataframe[m] = np.round(data[n],4)
                #print('port: {}, value: {}, index: {}'.format(m,data[n:n+1],n))

    end_time = dt.datetime.now()
    timedelta = end_time - start_time
    #print (timedelta)
    return dataframe


def convert_to_float(data):
    '''Converts floating point number (IEEE 754) into normal float.'''
    sign = 1 if data[0] < 32768 else -1
    exponent = ((data[0] % 2**15) >> 7) - 127
    high0 = data[0] % 128 * 2**16
    low0 = data[1]
    mantisse = (high0 + low0) % 2**23
    return round(sign * (1.0 + mantisse / 2**23) * 2**exponent, 4)

def convert_to_float2(data):
    highbyte = binary_repr(data[0],16)
    lowbyte = binary_repr(data[1],16)
    totalbyte = highbyte + lowbyte
    # handle sign
    sign = int(totalbyte[0])
    if sign == 0:
        sign = 1
    else:
        sign = -1
    # handle exponent
    exponent = int(totalbyte[1:9],2) - 127
    # handle fraction
    fraction = totalbyte[9:]
    mantisse = 0
    for i in range(len(fraction)):
        mantisse += int(fraction[i]) * 2**-i
    # create float
    value = sign * (1 + mantisse) * 2 ** exponent
    return value


