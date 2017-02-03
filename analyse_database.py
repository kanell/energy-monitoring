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
'''wöchentlicher Abstand?'''

#   1 weak in seconds 
week_s = 604800
    
db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}
#   connection to database
db = pqdb.connect_to_db(db_config)
    
def analyse_database_frequency(starttime, endtime):
#   Analyses historical Data: frequency
    rule = 'frequency_10s between {} and {} and timestamp between {} and {}'.format(49.5,50,5,starttime,endtime) 
    data_frequency_1 = pqdb.get_data(db, tablename, 'frequency_10s', rule)
    '''her muss noch der jeweilige Zeitstempel selected werden.''' 
    data_frequency_time = pqdb.get_data(db, tablename, 'timestamp', rule)
    
    analysisdict = {}
    analysisdict = 
    
#   Duration of exceeding limits in seconds
    frequency_critical_s = len(data_frequency_1)

    if frequency_critical_s/week_s < 0.005 :
        frequency1_weekly = "okay"
    else:
        frequency1_weekly = "bad"

    rule2 = 'frequency_10s < {}'.format(47.5) 
    '''weitere Regel wird noch eingefügt'''
    data_frequency_2 = pqdb.get_data(db, tablename, 'frequency_10s', rule2 ) 
    '''hier muss noch der jeweilige Zeitstempel selected werden.'''      
    
    if data_frequency_2 == None :
        frequency2_weekly = "okay"
    else:        
        frequency2_weekly = "bad" 
    
    return data_frequency_1, data_frequency_2, frequency1_weekly, frequency2_weekly
    
def analyse_database_voltage(starttime, endtime):
#   Analyses historical Data: voltage        
    rule3 = 'port_1728 < {}'.format(207) 
    rule4 = 'port_1730 < {}'.format(207) 
    rule5 = 'port_1732 < {}'.format(207) 
    '''weitere Regeln werden noch eingefügt: > 253'''

    data_voltage_L1 = pqdb.get_data(db, tablename, 'port_1728', rule3 )    
    data_voltage_L2 = pqdb.get_data(db, tablename, 'port_1730', rule4 )  
    data_voltage_L3 = pqdb.get_data(db, tablename, 'port_1732', rule5 )    
    '''hier müssen noch die jeweiligen Zeitstempel selected werden.''' 
        
#   Duration of exceeding limits in seconds
    voltageL1_critical_s = len(data_voltage_L1)
    if voltageL1_critical_s/week_s < 0.05 :
        voltage_weekly_L1 = "okay"
    else:
        voltage_weekly_L1 = "bad"   
        
    voltageL2_critical_s = len(data_voltage_L2)
    if voltageL2_critical_s/week_s < 0.05 :
        voltage_weekly_L2 = "okay"
    else:
        voltage_weekly_L2 = "bad"   

    voltageL3_critical_s = len(data_voltage_L3)
    if voltageL3_critical_s/week_s < 0.05 :
        voltage_weekly_L3 = "okay"
    else:
        voltage_weekly_L3 = "bad"   
        
    return voltage_weekly_L1, voltage_weekly_L2, voltage_weekly_L3
    
    return data_voltage_L1, data_voltage_L2, data_voltage_L3, 
    voltage_weekly_L1, voltage_weekly_L2, voltage_weekly_L3