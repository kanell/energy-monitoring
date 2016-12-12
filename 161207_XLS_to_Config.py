#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 12:47:25 2016

@author: felixstoeckmann
"""

import pandas as pd

path = '/FILEPATH'

def Read_XLSX():
    '''Reads compled XLSX-file with all available ports and information.'''
    filename = path + 'Janitza-Manual-UMG96RM-Modbus-adress-list.xlsx'
    DF_Ports = pd.read_excel(filename)
    
    return DF_Ports


def Merge(adresses,DF_Ports):
    '''Merges List of Data-Adresses with Port-DataFrame.\n
    Set Port-Adress = DataFrame.index. Portnumer is set to Variable-ID.'''
    New_File = pd.DataFrame()
    for i in adresses:
        New_File = New_File.append(DF_Ports[DF_Ports['Adresse'] == i])
    New_File['Adresse'] = New_File['Adresse'].apply(int)
    New_File['Abk'] = pd.Series('NaN', index=New_File.index)
    New_File = New_File.set_index('Adresse')
    return New_File
