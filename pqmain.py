# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:53:13 2016

@author: malte
"""

import pqdb
import get_data as gd
import numpy as np
import time

# read ports from csv
addresses, ports = gd.Read_Port_CSV()

old_timestamp = time.time()

while True:
    timestamp = time.time()
    if timestamp-old_timestamp < 0.2:
        time.sleep(0.2-timestamp+old_timestamp)
    else:
        print('getting data from janitza takes to long')
    pq_data = gd.Call(ports, addresses)
    