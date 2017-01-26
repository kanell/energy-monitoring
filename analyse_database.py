# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:55:29 2017

@author: Paul-G
"""

import pqdb
import numpy as np
import datetime
tablename = 'pqdata'

starttime = datetime.datetime(2017,1,24,14,00,00,000000).timestamp()
endtime = datetime.datetime(2017,1,24,15,00,00,000000).timestamp()

def analyse_database(starttime, endtime):
    '''Analyses live Data: frequency, voltage'''
    
    db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}
    
    db = pqdb.connect_to_db(db_config)
    
    rule = 'port_800 < {}'.format(49.5) 
    '''weitere Regel wird noch eingefügt'''
    data = pqdb.get_data(db, tablename, 'port_800', rule )

    frequency_critical_s = len(data)*10
    year_s = 31536000

    if frequency_critical_s/year_s < 0.005 :
        frequency1_average_year = "okay"
    else:
        frequency1_average_year = "bad"

    rule = 'port_800 < {}'.format(47.5) 
    '''weitere Regel wird noch eingefügt'''
    data = pqdb.get_data(db, tablename, 'port_800', rule )       
    
    if data == None :
        frequency2_average_year = "okay"
    else:        
        frequency2_average_year = "bad" 
    
    return data, frequency_critical_s, frequency1_average_year, frequency2_average_year