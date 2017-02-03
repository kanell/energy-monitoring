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

# init
ipaddr = '129.69.176.123'
timedelta = 1 # seconds
tablename = 'pqdata'
max_dictsize = 1000

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
    dataframe, ports, addresses = gd.read_port_csv()
    
    # create datadict
    datadictlist = []
    dataframesize = dataframe.size
    while dataframesize > max_dictsize:
        datadictlist.append({})
        dataframesize -= max_dictsize
    datadictlist.append({})
    
    # create database table
    db_table_config = {}
    for index in dataframe.index:
        db_table_config['port_'+str(index)] = 'float'
    
    # connect to janitza
    pqid = gd.connection(ipaddr)
    
    # connect to database
    db = pqdb.connect_to_db(db_config)
    # create table in  database if not already created
    if not 'public.'+tablename in db.get_tables():
        pqdb.create_db_table(db,tablename,db_table_config)
        
    timestamp = int(dt.datetime.now().timestamp())
    
    while True:
        time1 = time.time()
        # get data from janitza
        pq_data = gd.fetch_data_dataframe(dataframe, ports, pqid)
        
        # create dict for database insert
        index = 0
        for i,addr in enumerate(pq_data.index):
            if (i - max_dictsize*index) >= max_dictsize:
                index += 1
            datadictlist[index]['port_'+str(addr)] = pq_data[addr]
        
        # add primary key to every dict
        timestamp += 1
        for datadict in datadictlist:
            datadict['timestamp'] = timestamp

        # insert data in database
        db.insert(tablename,{'timestamp':timestamp})
        for index, datadict in enumerate(datadictlist):
                db.update(tablename,datadict)
                # create data json
                with open('temp/jsons/alldata.json','w') as f:
                    f.write(json.dumps(datadict))
        
    
        time2 = time.time()
        
        # try to get data every 1 second
        if time2-time1 < timedelta:
            time.sleep(timedelta-time2+time1) 
        else:
            print('getting data from janitza takes to long')

except KeyboardInterrupt:
    print('CTRL-C KeyboardInterrupt is active')
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
    