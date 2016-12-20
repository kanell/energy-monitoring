# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:53:13 2016

@author: malte
"""

import pqdb
import get_data_janitza as gd
import numpy as np
import time

# init
ipaddr = '129.69.176.123'
timedelta = 1 # seconds
tablename = 'pqdata'

# database config
db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}

# read ports from csv
addresses, ports = gd.read_port_csv()

# create database table
db_table_config = {}
for index in addresses.index:
    db_table_config[str(index)] = 'float'

# connect to janitza
pqid = gd.connection(ipaddr)

# connect to database
db = pqdb.connect_to_db(db_config)
# create table in  database if not already created
if not 'public.'+tablename in db.get_tables():
    pqdb.create_db_table(db,tablename,db_table_config)

while True:
    time1 = time.time()
    # get data from janitza
    pq_data = gd.fetch_data_dict(addresses, ports, pqid)
    # insert data in database
    db.insert(tablename,pq_data)
    time2 = time.time()
    
    # try to get data every 1 second
    if time2-time1 < timedelta:
        time.sleep(timedelta-time2+time1) 
    else:
        print('getting data from janitza takes to long')


    