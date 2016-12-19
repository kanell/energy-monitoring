# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:59:51 2016

@author: malte
"""

from pg import DB
import numpy as np

db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}

db_table_config = {'voltage':'float',
                   '1111':'float'}

def get_data(db, tablename, selector, rule):
    if rule == None:
        # get all data
        data = np.array(db.query('select {} from {}'.format(selector, tablename)).getresult())[:,-1]
    else:
        # get data depending on rule
        data = np.array(db.query('select {} from {} where {}'.format(selector, tablename, rule)).getresult())[:,-1]
    return data

def create_db_table(db, tablename, description):
    config_string = 'create table '+tablename+' ('
    for key in description.keys():
        config_string = config_string+key+' '+description[key]+','
    config_string = config_string[:-1]+')'
    db.query(config_string)
    return 1
    
def connect_to_db(description):
    dbname = description['dbname']
    host = description['host']
    port = description['port']
    opt = description['opt']
    user = description['user']
    passwd = description['passwd']
    db = DB(dbname, host, port, opt, user, passwd)
    return db
    
    
if __name__ == '__main__':
    
    # Connecting to Database an create Table if neccessary
    db = connect_to_db(db_config)
    tablename = 'testdata'
    
    if not 'public.'+tablename in db.get_tables():
        create_db_table(db,tablename,db_table_config)
    
    # Put data in Database
    for i in range(200):
        data = {'voltage':2.3314*i, 'current':0.1564*i}
        db.insert(tablename,data)
        
    # Get all data
    data = get_data(db, tablename, 'voltage', None)
    print(data)
    
    # Get data with rule
    data = get_data(db, tablename, 'voltage', '1111 > 15')
    print(data)