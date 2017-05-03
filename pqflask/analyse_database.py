# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:55:29 2017

@author: Paul-G
"""

import pqdb
import json
import time
import os
import numpy as np
import datetime as dt

with open('../db_config.json','r') as f:
    db_config = json.loads(f.read())

basefolder = '../Website/temp/json'
tablename = db_config['tablename'] 


def analyse_database_frequency():
    db = pqdb.connect_to_db(db_config)
#   Analyses historical Data: frequency (+/- 1%)
    rule = 'frequency_10s between {} and {}'.format(47,49.5)
    data_frequency_critical_1 = round(pqdb.get_data(db, tablename, 'frequency_10s', rule), 4)
    timestamp_frequency_1 = pqdb.get_data(db, tablename, 'timestamp', rule)

    rule = 'frequency_10s between {} and {}'.format(50.5,52)
    data_frequency_critical_2 = round(pqdb.get_data(db, tablename, 'frequency_10s', rule), 4)
    timestamp_frequency_2 = pqdb.get_data(db, tablename, 'timestamp', rule)

    data_frequency_critical = data_frequency_critical_1 + data_frequency_critical_2
    timestamp_frequency_float = timestamp_frequency_1 + timestamp_frequency_2

# Transform float time in time "yyy-mm-dd hh:mm:ss"
    timestamp_frequency_critical = []
    i = 0
    while i < len(timestamp_frequency_float):
        timestamp_frequency_critical.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_frequency_float[i])))
        i += 1

# Save Data as json conform javascript file    
    try:
        if timestamp_frequency_critical != []:
            frequency_critical_JS = []
            i = 0
            while i < len(timestamp_frequency_critical):
                frequency_critical_JS.append({"timestamp": timestamp_frequency_critical[i], "value": data_frequency_critical[i],"deviation": (data_frequency_critical[i]-50)/50*100})
                i += 1
            with open(os.path.join(basefolder, "frequency_critical.json"),"w") as out_file:
                out_file.write(json.dumps(frequency_critical_JS))
    except KeyError:
        pass

#   Analyses historical Data: frequency (+ 4% / -6%)
    rule2 = 'frequency_10s not between {} and {}'.format(47,52)
    data_frequency_bad = round(pqdb.get_data(db, tablename, 'frequency_10s', rule2), 4)
    timestamp_frequency_float = pqdb.get_data(db, tablename, 'timestamp', rule)

# Transform float time in time "yyy-mm-dd hh:mm:ss"
    timestamp_frequency_bad = []
    i = 0
    while i < len(timestamp_frequency_float):
        timestamp_frequency_bad.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_frequency_float[i])))
        i += 1

# Save Data as json conform javascript file    
    try:
        if timestamp_frequency_bad != []:
            frequency_bad_JS = []
            i = 0
            while i < len(timestamp_frequency_bad):
                frequency_bad_JS.append({"timestamp": timestamp_frequency_bad[i], "value": data_frequency_bad[i],"deviation": (data_frequency_bad[i]-50)/50*100})
                i += 1
            with open(os.path.join(basefolder, "frequency_bad.json"),"w") as out_file:
                out_file.write(json.dumps(frequency_bad_JS))
    except KeyError:
        pass
  
    
def analyse_database_voltage():
    db = pqdb.connect_to_db(db_config)
#   Analyses historical Data: voltage        
    rule_L1 = 'port_1728 not between {} and {}'.format(233, 253) 
    rule_L2 = 'port_1730 not between {} and {}'.format(207, 253) 
    rule_L3 = 'port_1732 not between {} and {}'.format(207, 253)

# Get data and timestamps from database
    t1 = time.time()
    data_voltage_L1 = round(pqdb.get_data(db, tablename, 'port_1728', rule_L1 ), 4)
    t2 = time.time()
    timestamp_voltage_L1_float = pqdb.get_data(db, tablename, 'timestamp', rule_L1)
    t3 = time.time()
    print('t2-t1: {} s, t3-t2: {} s'.format(t2-t1,t3-t2))

# Transform float time in time "yyy-mm-dd hh:mm:ss"
    timestamp_voltage_L1 = []
    i = 0
    while i < len(timestamp_voltage_L1_float):
        timestamp_voltage_L1.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_voltage_L1_float[i])))
        i += 1
        
# Save Data as json conform javascript file       
    try:
        if timestamp_voltage_L1 != []:
            voltage_L1_JS = []
            i = 0
            while i < len(timestamp_voltage_L1):
                voltage_L1_JS.append({"timestamp": timestamp_voltage_L1[i], "value": data_voltage_L1[i],"deviation": (data_voltage_L1[i]-230)/230*100})
                i += 1
            with open(os.path.join(basefolder, "voltage_L1.json"),"w") as out_file:
                out_file.write(json.dumps(voltage_L1_JS))
    except KeyError:
        pass

# Get data and timestamps from database
    data_voltage_L2 = round(pqdb.get_data(db, tablename, 'port_1730', rule_L2 ),4)
    timestamp_voltage_L2_float = pqdb.get_data(db, tablename, 'timestamp', rule_L2)

# Transform float time in time "yyy-mm-dd hh:mm:ss"
    timestamp_voltage_L2 = []
    i = 0
    while i < len(timestamp_voltage_L2_float):
        timestamp_voltage_L2.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_voltage_L2_float[i])))
        i += 1

# Save Data as json conform javascript file        
    try:
        if timestamp_voltage_L2 != []:
            voltage_L2_JS = []
            i = 0
            while i < len(timestamp_voltage_L2):
                voltage_L2_JS.append({"timestamp": timestamp_voltage_L2[i], "value": data_voltage_L2[i],"deviation": (data_voltage_L2[i]-230)/230*100})
                i += 1
            with open(os.path.join(basefolder, "voltage_L2.json"),"w") as out_file:
                out_file.write(json.dumps(voltage_L2_JS))
    except KeyError:
        pass

# Get data and timestamps from database
    data_voltage_L3 = round(pqdb.get_data(db, tablename, 'port_1732', rule_L3 ), 4)
    timestamp_voltage_L3_float = pqdb.get_data(db, tablename, 'timestamp', rule_L3)

# Transform float time in time "yyy-mm-dd hh:mm:ss"
    timestamp_voltage_L3 = []
    i = 0
    while i < len(timestamp_voltage_L3_float):
        timestamp_voltage_L3.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_voltage_L3_float[i])))
        i += 1

# Save Data as json conform javascript file        
    try:
        if timestamp_voltage_L3 != []:
            voltage_L3_JS = []
            i = 0
            while i < len(timestamp_voltage_L3):
                voltage_L3_JS.append({"timestamp": timestamp_voltage_L3[i], "value": data_voltage_L3[i],"deviation": (data_voltage_L3[i]-230)/230*100})
                i += 1
            with open(os.path.join(basefolder, "voltage_L3.json"),"w") as out_file:
                out_file.write(json.dumps(voltage_L3_JS))
    except KeyError:
        pass

    
def analyse_database_THD_U():  
    db = pqdb.connect_to_db(db_config)
# Get data and timestamps from database
    data_THD_U_L1 = round(pqdb.get_data(db, tablename, 'port_2236', 'port_2236 > 8'), 2)
    timestamp_THD_U_L1_float = pqdb.get_data(db, tablename, 'timestamp', 'port_2236 > 8')
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_THD_U_L1 = []
    i = 0
    while i < len(timestamp_THD_U_L1_float):
        timestamp_THD_U_L1.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_THD_U_L1_float[i])))
        i += 1    
        
# Save Data as json conform javascript file        
    try:
        if timestamp_THD_U_L1 != []:
            THD_U_L1_JS = []
            i = 0
            while i < len(timestamp_THD_U_L1):
                THD_U_L1_JS.append({"timestamp": timestamp_THD_U_L1[i], "value": data_THD_U_L1[i],"deviation": data_THD_U_L1[i]})
                i += 1
            with open(os.path.join(basefolder, "THD_U_L1.json"),"w") as out_file:
                out_file.write(json.dumps(THD_U_L1_JS))
    except KeyError:
        pass    
    
# Get data and timestamps from database    
    data_THD_U_L2 = round(pqdb.get_data(db, tablename, 'port_2238', 'port_2238 > 8'), 2) 
    timestamp_THD_U_L2_float = pqdb.get_data(db, tablename, 'timestamp', 'port_2238 > 8')
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_THD_U_L2 = []
    i = 0
    while i < len(timestamp_THD_U_L2_float):
        timestamp_THD_U_L2.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_THD_U_L2_float[i])))
        i += 1    
        
# Save Data as json conform javascript file        
    try:
        if timestamp_THD_U_L2 != []:
            THD_U_L2_JS = []
            i = 0
            while i < len(timestamp_THD_U_L2):
                THD_U_L2_JS.append({"timestamp": timestamp_THD_U_L2[i], "value": data_THD_U_L2[i],"deviation": data_THD_U_L2[i]})
                i += 1
            with open(os.path.join(basefolder, "THD_U_L2.json"),"w") as out_file:
                out_file.write(json.dumps(THD_U_L2_JS))
    except KeyError:
        pass    

# Get data and timestamps from database
    data_THD_U_L3 = round(pqdb.get_data(db, tablename, 'port_2238', 'port_2238 > 8'), 2) 
    timestamp_THD_U_L3_float = pqdb.get_data(db, tablename, 'timestamp', 'port_2238 > 8')    
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_THD_U_L3 = []
    i = 0
    while i < len(timestamp_THD_U_L3_float):
        timestamp_THD_U_L3.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_THD_U_L3_float[i])))
        i += 1    
        
# Save Data as json conform javascript file        
    try:
        if timestamp_THD_U_L3 != []:
            THD_U_L3_JS = []
            i = 0
            while i < len(timestamp_THD_U_L3):
                THD_U_L3_JS.append({"timestamp": timestamp_THD_U_L3[i], "value": data_THD_U_L3[i],"deviation": data_THD_U_L3[i]})
                i += 1
            with open(os.path.join(basefolder, "THD_U_L3.json"),"w") as out_file:
                out_file.write(json.dumps(THD_U_L3_JS))
    except KeyError:
        pass        
    
    
def analyse_database_THD_I():
    db = pqdb.connect_to_db(db_config)
# Get data and timestamps from database  
    data_THD_I_L1 = round(pqdb.get_data(db, tablename, 'port_2548', 'port_2548 > 8'), 2) 
    timestamp_THD_I_L1_float = pqdb.get_data(db, tablename, 'timestamp', 'port_2548 > 8')
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_THD_I_L1 = []
    i = 0
    while i < len(timestamp_THD_I_L1_float):
        timestamp_THD_I_L1.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_THD_I_L1_float[i])))
        i += 1    
        
# Save Data as json conform javascript file        
    try:
        if timestamp_THD_I_L1 != []:
            THD_I_L1_JS = []
            i = 0
            while i < len(timestamp_THD_I_L1):
                THD_I_L1_JS.append({"timestamp": timestamp_THD_I_L1[i], "value": data_THD_I_L1[i],"deviation": data_THD_I_L1[i]})
                i += 1
            with open(os.path.join(basefolder, "THD_I_L1.json"),"w") as out_file:
                out_file.write(json.dumps(THD_I_L1_JS))
    except KeyError:
        pass       
       
# Get data and timestamps from database    
    data_THD_I_L2 = round(pqdb.get_data(db, tablename, 'port_2238', 'port_2238 > 8'), 2) 
    timestamp_THD_L2_float = pqdb.get_data(db, tablename, 'timestamp', 'port_2238 > 8')
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_THD_I_L2 = []
    i = 0
    while i < len(timestamp_THD_L2_float):
        timestamp_THD_I_L2.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_THD_L2_float[i])))
        i += 1    
        
# Save Data as json conform javascript file        
    try:
        if timestamp_THD_I_L2 != []:
            THD_I_L2_JS = []
            i = 0
            while i < len(timestamp_THD_I_L2):
                THD_I_L2_JS.append({"timestamp": timestamp_THD_I_L2[i], "value": data_THD_I_L2[i],"deviation": data_THD_I_L2[i]})
                i += 1
            with open(os.path.join(basefolder, "THD_I_L2.json"),"w") as out_file:
                out_file.write(json.dumps(THD_I_L2_JS))
    except KeyError:
        pass 
    

# Get data and timestamps from database
    data_THD_I_L3 = round(pqdb.get_data(db, tablename, 'port_2238', 'port_2238 > 8'), 2) 
    timestamp_THD_L3_float = pqdb.get_data(db, tablename, 'timestamp', 'port_2238 > 8')    
    
# Transform float time in time "yyy-mm-dd hh:mm:ss" 
    timestamp_THD_I_L3 = []
    i = 0
    while i < len(timestamp_THD_L3_float):
        timestamp_THD_I_L3.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_THD_L3_float[i])))
        i += 1    
        
# Save Data as json conform javascript file        
    try:
        if timestamp_THD_I_L3 != []:
            THD_I_L3_JS = []
            i = 0
            while i < len(timestamp_THD_I_L2):
                THD_I_L3_JS.append({"timestamp": timestamp_THD_I_L3[i], "value": data_THD_I_L3[i],"deviation": data_THD_I_L3[i]})
                i += 1
            with open(os.path.join(basefolder, "THD_I_L3.json"),"w") as out_file:
                out_file.write(json.dumps(THD_I_L3_JS))
    except KeyError:
        pass 
