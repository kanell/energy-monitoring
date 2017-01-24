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

def analyse_database(starttime, endtime):
    '''Analyses live Data: frequency, voltage'''
    
    db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}
    
    db = pqdb.connect_to_db(db_config)
    
    rule = 'port_800 < {}'.format(50)

    
    data = pqdb.get_data(db, tablename, 'port_800', rule )
    return data
    
data = analyse_database(starttime, endtime)