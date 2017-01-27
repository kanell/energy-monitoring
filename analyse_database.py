# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:55:29 2017

@author: Paul-G
"""

import pqdb

def analyse_database():
    '''Analyses live Data: frequency, voltage'''
    
    db_config = {'dbname': 'postgres',
             'host': 'localhost',
             'port': 5432,
             'opt': None,
             'user': 'postgres',
             'passwd': 'pqdata'}
    
    db = pqdb.connect_to_db(db_config)
    
    pqdb.get_data(db, tablename, selector, rule)