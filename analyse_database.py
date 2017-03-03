# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:55:29 2017

@author: Paul-G
"""

import pqdb
import numpy as np
import datetime
import json
import time
tablename = 'pqdata'
    
db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}
             
#   connection to database
db = pqdb.connect_to_db(db_config)
    
def analyse_database_frequency():
#   Analyses historical Data: frequency (+/- 1%)
    rule = 'frequency_10s between {} and {}'.format(47,49.5) 
    data_frequency_critical_1 = pqdb.get_data(db, tablename, 'frequency_10s', rule)
    timestamp_frequency_1 = pqdb.get_data(db, tablename, 'timestamp', rule)
    
    rule = 'frequency_10s between {} and {}'.format(50.5,52) 
    data_frequency_critical_2 = pqdb.get_data(db, tablename, 'frequency_10s', rule)
    timestamp_frequency_2 = pqdb.get_data(db, tablename, 'timestamp', rule)
    
    data_frequency_critical = data_frequency_critical_1 + data_frequency_critical_2
    timestamp_frequency_float = timestamp_frequency_1 + timestamp_frequency_2
    
# Transform float time in time "yyy-mm-dd hh:mm:ss"
    timestamp_frequency_critical = []
    i = 0
    while i < len(timestamp_frequency_float):
        timestamp_frequency_critical.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_frequency_float[i])))
        i += 1

# Save Data as JS conform JSON file    
    try:
        if timestamp_frequency_critical != []:
            frequency_critical_JS = []
            i = 0
            while i < len(timestamp_frequency_critical):
                frequency_critical_JS.append({"timestamp": timestamp_frequency_critical[i], "value": data_frequency_critical[i],"deviation": (data_frequency_critical[i]-50)/50*100})
                i += 1
            with open("frequency_critical.json","w") as out_file:
                out_file.write(json.dumps(frequency_critical_JS))
    except KeyError:
        pass

#   Analyses historical Data: frequency (+ 4% / -6%)
    rule2 = 'frequency_10s not between {} and {}'.format(47,52) 
    data_frequency_bad = pqdb.get_data(db, tablename, 'frequency_10s', rule2 )    
    timestamp_frequency_float = pqdb.get_data(db, tablename, 'timestamp', rule)
    
# Transform float time in time "yyy-mm-dd hh:mm:ss"    
    timestamp_frequency_bad = []
    i = 0
    while i < len(timestamp_frequency_float):
        timestamp_frequency_bad.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_frequency_float[i])))
        i += 1

# Save Data as JS conform JSON file    
    try:
        if timestamp_frequency_bad != []:
            frequency_bad_JS = []
            i = 0
            while i < len(timestamp_frequency_bad):
                frequency_bad_JS.append({"timestamp": timestamp_frequency_bad[i], "value": data_frequency_bad[i],"deviation": (data_frequency_bad[i]-50)/50*100})
                i += 1
            with open("frequency_bad.json","w") as out_file:
                out_file.write(json.dumps(frequency_bad_JS))
    except KeyError:
        pass
    
def analyse_database_voltage():
#   Analyses historical Data: voltage        
    rule_L1 = 'port_1728 not between {} and {}'.format(242, 253) 
    rule_L2 = 'port_1730 not between {} and {}'.format(242, 253) 
    rule_L3 = 'port_1732 not between {} and {}'.format(242, 253) 

# Get data and timestamps from database
    data_voltage_L1 = pqdb.get_data(db, tablename, 'port_1728', rule_L1 ) 
    timestamp_voltage_L1_float = pqdb.get_data(db, tablename, 'timestamp', rule_L1)

# Transform float time in time "yyy-mm-dd hh:mm:ss"    
    timestamp_voltage_L1 = []
    i = 0
    while i < len(timestamp_voltage_L1_float):
        timestamp_voltage_L1.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_voltage_L1_float[i])))
        i += 1
        
# Save Data as JS conform JSON file        
    try:
        if timestamp_voltage_L1 != []:
            voltage_L1_JS = []
            i = 0
            while i < len(timestamp_voltage_L1):
                voltage_L1_JS.append({"timestamp": timestamp_voltage_L1[i], "value": data_voltage_L1[i],"deviation": (data_voltage_L1[i]-230)/230*100})
                i += 1
            with open("voltage_L1.json","w") as out_file:
                out_file.write(json.dumps(voltage_L1_JS))
    except KeyError:
        pass
        
# Get data and timestamps from database    
    data_voltage_L2 = pqdb.get_data(db, tablename, 'port_1730', rule_L2 )  
    timestamp_voltage_L2_float = pqdb.get_data(db, tablename, 'timestamp', rule_L2)
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_voltage_L2 = []
    i = 0
    while i < len(timestamp_voltage_L2_float):
        timestamp_voltage_L2.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_voltage_L2_float[i])))
        i += 1

# Save Data as JS conform JSON file        
    try:
        if timestamp_voltage_L2 != []:
            voltage_L2_JS = []
            i = 0
            while i < len(timestamp_voltage_L2):
                voltage_L2_JS.append({"timestamp": timestamp_voltage_L2[i], "value": data_voltage_L2[i],"deviation": (data_voltage_L2[i]-230)/230*100})
                i += 1
            with open("voltage_L2.json","w") as out_file:
                out_file.write(json.dumps(voltage_L2_JS))
    except KeyError:
        pass
        
# Get data and timestamps from database
    data_voltage_L3 = pqdb.get_data(db, tablename, 'port_1732', rule_L3 ) 
    timestamp_voltage_L3_float = pqdb.get_data(db, tablename, 'timestamp', rule_L3)
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_voltage_L3 = []
    i = 0
    while i < len(timestamp_voltage_L3_float):
        timestamp_voltage_L3.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_voltage_L3_float[i])))
        i += 1

# Save Data as JS conform JSON file        
    try:
        if timestamp_voltage_L3 != []:
            voltage_L3_JS = []
            i = 0
            while i < len(timestamp_voltage_L3):
                voltage_L3_JS.append({"timestamp": timestamp_voltage_L3[i], "value": data_voltage_L3[i],"deviation": (data_voltage_L3[i]-230)/230*100})
                i += 1
            with open("voltage_L3.json","w") as out_file:
                out_file.write(json.dumps(voltage_L3_JS))
    except KeyError:
        pass

def analyse_database_THD_U():
#   Analyses historical Data: THD 
    data_THD_L1 = pqdb.get_data(db, tablename, 'port_2236', 'port_2236 > 8') 
    timestamp_THD_L1 = pqdb.get_data(db, tablename, 'timestamp', 'port_2236 > 8')
    
    data_THD_L2 = pqdb.get_data(db, tablename, 'port_2238', 'port_2238 > 8') 
    timestamp_THD_L2 = pqdb.get_data(db, tablename, 'timestamp', 'port_2238 > 8')

    data_THD_L3 = pqdb.get_data(db, tablename, 'port_2238', 'port_2238 > 8') 
    timestamp_THD_L3 = pqdb.get_data(db, tablename, 'timestamp', 'port_2238 > 8')    
    
    data_THD_L1_dict = {'THD_L1_data:': data_THD_L1,
                            'THD_L1_timestamp': timestamp_THD_L1}
                            
    data_THD_L2_dict =  {'THD_L2_data:': data_THD_L2,
                            'THD_L2_timestamp': timestamp_THD_L2}
    
    data_THD_L3_dict = {'THD_L3_data:': data_THD_L3,
                            'THD_L3_timestamp': timestamp_THD_L3}    
    
    return data_THD_L1_dict, data_THD_L2_dict, data_THD_L3_dict
    
#def analyse_database_THD_I()
    