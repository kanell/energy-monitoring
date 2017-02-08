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
    
def analyse_database_frequency():
#   Analyses historical Data: frequency
    rule = 'frequency_10s between {} and {}'.format(47.5,49.5) 
    data_frequency_critical_1 = pqdb.get_data(db, tablename, 'frequency_10s', rule)
    timestamp_frequency_1 = pqdb.get_data(db, tablename, 'timestamp', rule)
    
    rule = 'frequency_10s between {} and {}'.format(50.5,52) 
    data_frequency_critical_2 = pqdb.get_data(db, tablename, 'frequency_10s', rule)
    timestamp_frequency_2 = pqdb.get_data(db, tablename, 'timestamp', rule)
    
    data_frequency_critical = data_frequency_critical_1 + data_frequency_critical_2
    timestamp_frequency = timestamp_frequency_1 + timestamp_frequency_2
    
#    timestamps_frequency = []
#    for i in timestamp_frequency:
#        timestamps_frequency.append = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_frequency[i]))
#    
    frequency_critical_dict = {'frequency_data': data_frequency_critical,
                               'frequency_timestamp': timestamp_frequency}
    
#   Duration of exceeding limits in seconds
#    frequency_critical_s = len(data_frequency_critcal)
#
#    if frequency_critical_s/week_s < 0.005 :
#        frequency1_weekly = "okay"
#    else:
#        frequency1_weekly = "bad"

    rule2 = 'frequency_10s not between {} and {}'.format(47.5,52) 
    data_frequency_bad = pqdb.get_data(db, tablename, 'frequency_10s', rule2 )    
    timestamp_frequency_bad = pqdb.get_data(db, tablename, 'timestamp', rule)
    
    frequency_bad_dict = {'frequency_data': data_frequency_bad,
                          'frequency_timestamp': timestamp_frequency_bad}
                          
#    if data_frequency_bad == None :
#        frequency2_weekly = "okay"
#    else:        
#        frequency2_weekly = "bad" 
    
    return frequency_critical_dict, frequency_bad_dict
    
def analyse_database_voltage():
#   Analyses historical Data: voltage        
    rule_L1 = 'port_1728 not between {} and {}'.format(207, 200) 
    rule_L2 = 'port_1730 not between {} and {}'.format(207, 200) 
    rule_L3 = 'port_1732 not between {} and {}'.format(207, 200) 

    data_voltage_L1 = pqdb.get_data(db, tablename, 'port_1728', rule_L1 ) 
    timestamp_voltage_L1 = pqdb.get_data(db, tablename, 'timestamp', rule_L1)
    
    data_voltage_L2 = pqdb.get_data(db, tablename, 'port_1730', rule_L2 )  
    timestamp_voltage_L2 = pqdb.get_data(db, tablename, 'timestamp', rule_L2)
    
    data_voltage_L3 = pqdb.get_data(db, tablename, 'port_1732', rule_L3 ) 
    timestamp_voltage_L3 = pqdb.get_data(db, tablename, 'timestamp', rule_L3)
    
    data_voltage_L1_dict = {'voltage_L1_data:': data_voltage_L1,
                            'voltage_L1_timestamp': timestamp_voltage_L1}
                            
    data_voltage_L2_dict =  {'voltage_L2_data:': data_voltage_L2,
                            'voltage_L2_timestamp': timestamp_voltage_L2}
    
    data_voltage_L3_dict = {'voltage_L3_data:': data_voltage_L3,
                            'voltage_L3_timestamp': timestamp_voltage_L3}
        
#   Duration of exceeding limits in seconds
#    voltageL1_critical_s = len(data_voltage_L1)
#    if voltageL1_critical_s/week_s < 0.05 :
#        voltage_weekly_L1 = "okay"
#    else:
#        voltage_weekly_L1 = "bad"   
#        
#    voltageL2_critical_s = len(data_voltage_L2)
#    if voltageL2_critical_s/week_s < 0.05 :
#        voltage_weekly_L2 = "okay"
#    else:
#        voltage_weekly_L2 = "bad"   
#
#    voltageL3_critical_s = len(data_voltage_L3)
#    if voltageL3_critical_s/week_s < 0.05 :
#        voltage_weekly_L3 = "okay"
#    else:
#        voltage_weekly_L3 = "bad"   
        
    return data_voltage_L1_dict, data_voltage_L2_dict, data_voltage_L3_dict