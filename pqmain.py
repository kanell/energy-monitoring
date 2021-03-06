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
import analyse_database as ana_db

# processes
def get_data(queue, dataframe, ports, pqid, control_flag):
    # ignore signals from main process
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # init
    max_time = 0
    min_time = 1000
    timestamp = int(dt.datetime.now().timestamp())

    try:
        starttime = dt.datetime.now().timestamp()
        while control_flag.value == 0:
            # get data from janitza
            pq_data = gd.fetch_data_dataframe(dataframe, ports, pqid)

            # put in queue
            queue.put((pq_data, timestamp))

            endtime = time.time()
            min_time = min(min_time,endtime-starttime)
            max_time = max(max_time,endtime-starttime)
            #print('modbus loop duration time| current: {:6.4f} sec.\t| max: {:6.4f} sec.\t| min: {:6.4f} sec.'.format(time2-time1,max_time,min_time), end='\r')
            # try to get data every 1 second
            if endtime - starttime <= timedelta:
                timestamp += timedelta
                time.sleep(timedelta-(endtime-starttime))
                starttime += timedelta
            else:
                add_seconds = (endtime - starttime) // timedelta
                timestamp += timedelta + add_seconds
                time.sleep((timedelta + add_seconds) - (endtime - starttime))
                starttime += (timedelta + add_seconds)
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
                try:
                    db.insert(tablename,datadict)
                except:
                    pass

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

def update_analyse_database(control_flag):
    # ignore signals from main process
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    old_day = dt.datetime.now().day
    try:
        while control_flag.value == 0:
            # update analyse_database files for each new day
            timestamp = dt.datetime.now()
            day_now = timestamp.day
            # check if it is a new day
            if day_now != old_day:
                ana_db.analyse_database_voltage()
                ana_db.analyse_database_frequency()
                ana_db.analyse_database_THD_U()
                # as long as there is no current
#               ana_db.analyse_database_THD_I()
                # create heatplot every day
                start = dt.datetime.fromtimestamp(timestamp.timestamp()-(60*60*24)).strftime('%m/%d/%Y')
                end = dt.datetime.fromtimestamp(timestamp.timestamp()).strftime('%m/%d/%Y')
                datasize = 10000
                ana.heatplot_data(start, end, datasize)
                old_day = day_now
            else:
                # process can sleep
                time.sleep(1)
    except:
        control_flag.value = 1

        import traceback
        print(traceback.format_exc())
        raise
    finally:
        # close process
        pass

def write_csv(csvdict, basefolder, csvsize):
    if csvdict['csvdata'].shape[0] < csvsize:
        csvdict['csvdata'] = np.append(csvdict['csvdata'],np.array([csvdict['newdata']]),axis=0)
    else:
        csvdict['csvdata'] = np.roll(csvdict['csvdata'],-1,axis=0)
        csvdict['csvdata'][-1] = csvdict['newdata']
    #print(csvdict['csvdata'])
    np.savetxt(os.path.join(basefolder,'temp/csv/'+str(csvdict['filename'])+'.csv'),csvdict['csvdata'],delimiter=',',newline='\n',header=csvdict['header'], comments='')
    return csvdict

# init
ipaddr = '129.69.176.123'
timedelta = 1 # seconds
max_time = 0
min_time = 1000
control_flag = Value('i',0)

# ports for live data
live_ports = [800,808,810,812,860,862,864,884,886,888,868,870,872,876,878,880,836,838,840,908,910,912]
harmonics_u_ports = []
harmonics_i_ports = []
for index in np.arange(0,80,2):
    harmonics_u_ports.append([1000+index,1080+index,1160+index])
    harmonics_i_ports.append([1480+index,1560+index,1640+index])
#print(harmonics_u_ports)

live_harmonics_u = np.zeros((len(harmonics_u_ports)-1,4))
live_harmonics_i = np.zeros((len(harmonics_i_ports)-1,4))

# configdicts for csv file
csvsize = 600 # sec.
filenames = ['voltage','current','power','frequency']
valuenumber = [4,4,4,2]
headers = ['timestamp,u1,u2,u3','timestamp,i1,i2,i3','timestamp,p1,p2,p3','timestamp,frequency']
csvports = [[808,810,812],[860,862,864],[868,870,872],[800]]
csvdictlist = []
for index, filename in enumerate(filenames):
    csvdictlist.append({'filename':filename,
                        'header':headers[index],
                        'newdata': np.empty(len(csvports[index])+1),
                        'csvdata': np.empty((0,len(csvports[index])+1))
                        })

# queues
mbqueue = Queue()
dbqueue = Queue()

# create folders
basefolder = 'Website'
paths = ['temp', 'temp/json', 'temp/csv']
for path in paths:
    os.makedirs(os.path.join(basefolder,path), exist_ok=True)
os.makedirs('logs', exist_ok=True)

profile = True
if profile is True:
    profiling = cProfile.Profile()
    profiling.enable()

# database config
with open('db_config.json', 'r') as f:
    db_config = json.loads(f.read())
tablename = db_config['tablename']

try:
    # read ports from csv
    print('Get addresses from csv file')
    dataframe, ports, addresses = gd.read_port_csv()

    # create datadict
    datadict = {}
    livedatadict = {}

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
    args = (control_flag,)
    anadbprocess = Process(target=update_analyse_database, args=args)
    anadbprocess.start()
    print('Started analyse database process')

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

            # create dict for database insert and showing on website
            for addr in pq_data.index:
                if addr in live_ports:
                    livedatadict['port_'+str(addr)] = pq_data[addr]
                datadict['port_'+str(addr)] = pq_data[addr]

            # add primary key to every dict and frequency 10s
            datadict['timestamp'] = timestamp
            datadict['frequency_10s'] = frequency_10s

            # insert data in dbqueue
            dbqueue.put(datadict)

            # create data json
            with open(os.path.join(basefolder,'temp/json/alldata.json'),'w') as f:
                f.write(json.dumps(datadict))
            with open(os.path.join(basefolder,'temp/json/livedata.json'), 'w') as f:
                f.write(json.dumps(livedatadict))
            with open(os.path.join(basefolder,'temp/json/liveanalyse.json'), 'w') as f:
                f.write(json.dumps(status_dict))

            # create csv files
            for index, csvdata in enumerate(csvdictlist):
                csvdata['newdata'][0] = timestamp
                csvdata['newdata'][1:] = pq_data[csvports[index]]
                csvdictlist[index] = write_csv(csvdata,basefolder, csvsize)

	    # create csv file for harmonics
            for index, ports in enumerate(harmonics_u_ports[1:]):
                live_harmonics_u[index,0] = index + 2
                live_harmonics_u[index,1] = np.round(datadict['port_'+str(ports[0])] / datadict['port_'+str(harmonics_u_ports[0][0])] * 100, 4)
                live_harmonics_u[index,2] = np.round(datadict['port_'+str(ports[1])] / datadict['port_'+str(harmonics_u_ports[0][1])] * 100, 4)
                live_harmonics_u[index,3] = np.round(datadict['port_'+str(ports[2])] / datadict['port_'+str(harmonics_u_ports[0][2])] * 100, 4)
            np.savetxt(os.path.join(basefolder,'temp/csv/harmonics_u.csv'),live_harmonics_u,delimiter=',',newline='\n',header='number,u1,u2,u3', comments='')
            for index, ports in enumerate(harmonics_i_ports[1:]):
                live_harmonics_i[index,0] = index + 2
                live_harmonics_i[index,1] = np.round(datadict['port_'+str(ports[0])],4)
                live_harmonics_i[index,2] = np.round(datadict['port_'+str(ports[1])],4)
                live_harmonics_i[index,3] = np.round(datadict['port_'+str(ports[2])],4)
            np.savetxt(os.path.join(basefolder,'temp/csv/harmonics_i.csv'),live_harmonics_i,delimiter=',',newline='\n',header='number,i1,i2,i3', comments='')

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
    anadbprocess.join()

    print('finished measurement')
