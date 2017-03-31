# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:59:51 2016

@author: malte
"""

from pg import DB
import json
import numpy as np

# database config
with open('db_config.json', 'r') as f:
    db_config = json.loads(f.read())
tablename = db_config['tablename']

db_table_config = {'voltage':'float',
                   'current':'float'}

def get_data(db, tablename, selector, rule):
    try:
        if rule == None:
            # get all data
            data = np.array(db.query('select {} from {}'.format(selector, tablename)).getresult())[:,-1]
        else:
            # get data depending on rule
            data = np.array(db.query('select {} from {} where {}'.format(selector, tablename, rule)).getresult())[:,-1]
    except IndexError:
        print('No data in that time period')
        return np.array([])
    return data

def create_db_table(db, tablename, description):
    config_string = 'create table '+tablename+' (timestamp float primary key, '
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
    tablename = db_config['tablename']
    
    if not 'public.'+tablename in db.get_tables():
        create_db_table(db,tablename,db_table_config)
        
    # Get all data
    data = get_data(db, tablename, 'port_808', None)
    print(data)
    
    # Get data with rule
    data = get_data(db, tablename, 'port_808', 'timestamp between 1490981000 and 1490982000')
    print(data)
