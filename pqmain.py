# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:53:13 2016

@author: malte
"""

import pqdb
import get_data_janitza as gd
import numpy as np
import time
import cProfile
import pstats
import datetime as dt
import json
import os
import analyse as ana

# init
ipaddr = '129.69.176.123'
timedelta = 2 # seconds
tablename = 'pqdata'
max_time = 0
min_time = 1000

# create folders
paths = ['temp', 'temp/jsons', 'temp/csv']
for path in paths:
    os.makedirs(os.path.join(path), exist_ok=True)

profile = True
if profile is True:
    profiling = cProfile.Profile()
    profiling.enable()

# database config
db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}

try:
    # read ports from csv
    print('Get addresses from csv file')
    dataframe, ports, addresses = gd.read_port_csv()
    
    # create datadict
    datadict = {}
    
    # create database table
    db_table_config = {}
    for index in dataframe.index:
        db_table_config['port_'+str(index)] = 'float'
    db_table_config['frequency_10s'] = 'float'
    
    # connect to janitza
    print('Connect to Janitza', end='\r')
    pqid = gd.connection(ipaddr)
    print('Connected to Janitza')
    
    # connect to database
    print('Connect to postgres database', end='\r')
    db = pqdb.connect_to_db(db_config)
    print('Connected to postgres database')
    
    # create table in  database if not already created
    if not 'public.'+tablename in db.get_tables():
        pqdb.create_db_table(db,tablename,db_table_config)
        
    timestamp = int(dt.datetime.now().timestamp())
    
    while True:
        time1 = time.time()
        # get data from janitza
        pq_data = gd.fetch_data_dataframe(dataframe, ports, pqid)
        
        # send data to analysis func
        frequency_10s, status_dict = ana.analyse(pq_data)
        
        # create dict for database insert
        for addr in pq_data.index:
            datadict['port_'+str(addr)] = pq_data[addr]
        
        # add primary key to every dict and frequency 10s
        datadict['timestamp'] = timestamp
        datadict['frequency_10s'] = frequency_10s

        # insert data in database
        db.insert(tablename,datadict)

        # create data json
        with open('temp/jsons/alldata.json','w') as f:
            f.write(json.dumps(datadict))
        
        time2 = time.time()
        min_time = min(min_time,time2-time1)
        max_time = max(max_time,time2-time1)
        print('loop duration time| current: {:6.4f} sec.\t| max: {:6.4f} sec.\t| min: {:6.4f} sec.'.format(time2-time1,max_time,min_time), end='\r')
        # try to get data every 1 second
        if time2-time1 <= timedelta:
            timestamp += timedelta
            time.sleep(timedelta-time1+time2) 
        else:
            timestamp += 2*timedelta
            time.sleep(2*timedelta-time1+time2)

except KeyboardInterrupt:
    print('\nCTRL-C KeyboardInterrupt is active')
except:
    import traceback
    print(traceback.format_exc())
    raise
finally:
    # stop profiling if started
    if profile is True:
        profiling.disable()
        ps = pstats.Stats(profiling)
        ps.strip_dirs()
        ps.sort_stats('cumtime')
        ps.dump_stats('profiling_pqmain.pstat')
    
