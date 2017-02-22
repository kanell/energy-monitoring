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
from multiprocessing import Process, Queue, Value
import signal

# processes
def get_data(queue, dataframe, ports, pqid, control_flag):
    # ignore signals from main process
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    # init
    max_time = 0
    min_time = 1000
    timestamp = int(dt.datetime.now().timestamp())
    
    try:
        while control_flag.value == 0:
            time1 = time.time()

            # get data from janitza
            pq_data = gd.fetch_data_dataframe(dataframe, ports, pqid)
            
            # put in queue
            queue.put((pq_data, timestamp))

            time2 = time.time()
            min_time = min(min_time,time2-time1)
            max_time = max(max_time,time2-time1)
            print('modbus loop duration time| current: {:6.4f} sec.\t| max: {:6.4f} sec.\t| min: {:6.4f} sec.'.format(time2-time1,max_time,min_time), end='\r')
            # try to get data every 1 second
            if time2-time1 <= timedelta:
                timestamp += 2*timedelta
                time.sleep(timedelta-(time2-time1))
            else:
                timestamp += 2*timedelta
                time.sleep(2*timedelta-(time2-time1))
    except:
        control_flag.value = 1
        
        import traceback
        print(traceback.format_exc())
        raise
    finally:
        # check if queue is empty
        while queue.qsize() != 0:
            queue.get()
            
def put_data(queue, db, tablename, control_flag):
    # ignore signals from main process
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # init
    max_time = 0
    min_time = 1000

    try:
        while control_flag.value == 0:
            if queue.qsize() == 0:
                time.sleep(0.2)
            else:
                time1 = time.time()
                
                # get dict from queue
                datadict = queue.get()
                
                # insert data in database
                db.insert(tablename,datadict)

                time2 = time.time()
                min_time = min(min_time,time2-time1)
                max_time = max(max_time,time2-time1)
                #print('database loop duration time| current: {:6.4f} sec.\t| max: {:6.4f} sec.\t| min: {:6.4f} sec.'.format(time2-time1,max_time,min_time), end='\r')
    except:
        control_flag.value = 1
        
        import traceback
        print(traceback.format_exc())
        raise
    finally:
        # check if queue is empty
        while queue.qsize() != 0:
            queue.get()
            
# init
ipaddr = '129.69.176.123'
timedelta = 2 # seconds
tablename = 'pqdata'
max_time = 0
min_time = 1000
control_flag = Value('i',0)
# queues
mbqueue = Queue()
dbqueue = Queue()

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
        
    # Start processes
    args = (mbqueue, dataframe, ports, pqid, control_flag)
    mbprocess = Process(target=get_data, args=args)
    mbprocess.start()
    print('Started modbus process')
    args = (dbqueue, db, tablename, control_flag)
    dbprocess = Process(target=put_data, args=args)
    dbprocess.start()
    print('Started database process')
        
    timestamp = int(dt.datetime.now().timestamp())
    
    while control_flag.value == 0:
        if mbqueue.qsize() == 0:
            time.sleep(0.2)
        else:
            time1 = time.time()
            
            # get data from mbqueue
            pq_data, timestamp = mbqueue.get()
            
            # send data to analysis func
            frequency_10s, status_dict = ana.analyse(pq_data)
            
            # create dict for database insert
            for addr in pq_data.index:
                datadict['port_'+str(addr)] = pq_data[addr]
            
            # add primary key to every dict and frequency 10s
            datadict['timestamp'] = timestamp
            datadict['frequency_10s'] = frequency_10s
    
            # insert data in dbqueue
            dbqueue.put(datadict)
    
            # create data json
            with open('temp/jsons/alldata.json','w') as f:
                f.write(json.dumps(datadict))
            
            time2 = time.time()
            min_time = min(min_time,time2-time1)
            max_time = max(max_time,time2-time1)
            #print('main loop duration time| current: {:6.4f} sec.\t| max: {:6.4f} sec.\t| min: {:6.4f} sec.'.format(time2-time1,max_time,min_time), end='\r')

except KeyboardInterrupt:        
    control_flag.value = 1
        
    print('\nCTRL-C KeyboardInterrupt is active')
except:
    control_flag.value = 1
        
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
        
    mbprocess.join()
    dbprocess.join()
    
    print('finished measurement')
    
