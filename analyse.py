# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 16:08:28 2017

@author: Paul-G
"""

import pandas as pd
<<<<<<< HEAD
import time 
import os
import json 

keylist = ['frequency_status', 'voltage_L1, voltage_L2', 'voltage_L3', 'THD_U_L1', 'THD_U_L2', 'THD_U_L3', 'THD_I_L1', 'THD_I_L2', 'THD_I_L3',
=======
import time

keylist = ['frequency_status', 'voltage_L1, voltage_L2', 'voltage_L3', 'THD_L1', 'THD_L2', 'THD_L3',
>>>>>>> origin/master
    'harmonic_5th_U1', 'harmonic_7th_U1', 'harmonic_5th_U2', 'harmonic_7th_U2', 'harmonic_5th_U3', 'harmonic_7th_U3']

status_dict = {}
frequency_average_10s = []
index = 0
long_interruption_df = pd.DataFrame(columns = ['Time', 'Time_float','Voltage_L1','Voltage_L2','Voltage_L3'])
basefolder = 'Website/temp/json'

def analyse(pq_data):
    global index
    global long_interruption_df
    global frequency_average_10s

<<<<<<< HEAD
    
#   Analyses live Data from pq_data and checks if measured data is confom with EN 50160: frequency, voltage, THD, harmonics. i = [0...9] for frequency_average_10s       

#   Analyses frequency and checks if measured data is confom with EN 50160
    
=======
    #   Analyses live Data from pq_data and checks if measured data is confom with EN 50160: frequency, voltage, THD, harmonics. i = [0...9] for frequency_average_10s
    '''Analyses frequency and checks if measured data is confom with EN 50160
    Both frequency_average_10s AND frequency are returned'''

>>>>>>> origin/master
    if len(frequency_average_10s) < 10:
        frequency_average_10s.append(pq_data[800])
    else:
        if index == 10:
            index = 0
        frequency_average_10s[index] = pq_data[800]
    index += 1

    frequency_10s = sum(frequency_average_10s)/len(frequency_average_10s)

    if frequency_10s < 47.5 or frequency_10s > 52:
        frequency_status = "bad"
    elif frequency_10s < 49.5 or frequency_10s > 50.5:
        frequency_status = "critical"
    else:
        frequency_status = "okay"
    status_dict['frequency'] = frequency_status

#   Voltage magnitude variations
    voltage_L1_average =  pq_data[1728]
    voltage_L2_average =  pq_data[1730]
    voltage_L3_average =  pq_data[1732]

    if voltage_L1_average < 207 or voltage_L1_average > 253:
        voltage_L1 = "critical"
    else:
        voltage_L1 = "okay"

    if voltage_L2_average < 207 or voltage_L1_average > 253:
        voltage_L2 = "critical"
    else:
        voltage_L2 = "okay"

    if voltage_L3_average < 207 or voltage_L1_average > 253:
        voltage_L3 = "critical"
    else:
        voltage_L3 = "okay"

    status_dict['voltage_L1'] = voltage_L1
    status_dict['voltage_L2'] = voltage_L2
    status_dict['voltage_L3'] = voltage_L3

#   Long interruption of supply voltage
    m = long_interruption_df.index.size
    if voltage_L1_average < 1 or voltage_L2_average < 1 or voltage_L3_average < 1:
        long_interruption_df.at[m,'Time'] = time.asctime()
        long_interruption_df.at[m,'Time_float'] = time.time()
        long_interruption_df.at[m,'Voltage_L1'] = voltage_L1_average
        long_interruption_df.at[m,'Voltage_L2'] = voltage_L2_average
<<<<<<< HEAD
        long_interruption_df.at[m,'Voltage_L3'] = voltage_L3_average    
        
    elif voltage_L1_average > 1 and voltage_L2_average > 1 and voltage_L3_average > 1 and m < ((3*60)-1):
        long_interruption_df = pd.DataFrame(columns = ['Time', 'Time_float','Voltage_L1','Voltage_L2','Voltage_L3'])
        
=======
        long_interruption_df.at[m,'Voltage_L3'] = voltage_L3_average

    elif voltage_L1_average > 1 and voltage_L2_average > 1 and voltage_L3_average > 1 and m < (3*60) and m > 0:
        long_interruption_df = pd.DataFrame(columns = ['Time','Voltage_L1','Voltage_L2','Voltage_L3'])

>>>>>>> origin/master
    else:
        starttime = long_interruption_df.at[0,'Time']
        endtime = long_interruption_df.at[(m),'Time']
# duration of interruption in seconds
        timedelta = long_interruption_df.at[(m),'Time_float'] - long_interruption_df.at[0,'Time_float']
        
        time_dict = {'Beginn': starttime, 'Ende': endtime, 'Dauer': timedelta}   

# add start and endtime to existing json or create new json
        my_file = 'Website/temp/json/longterm_interruptions.json'

        if os.path.isfile(my_file): 
            with open(os.path.join(basefolder, 'longterm_interruptions.json')) as out_file:
                data = json.load(out_file)
                data.append(time_dict)
            with open(os.path.join(basefolder, 'longterm_interruptions.json'),"w") as out_file:
                out_file.write(json.dumps(data))   
        else: 
            data = []
            data.append(time_dict)
            with open(os.path.join(basefolder, 'longterm_interruptions.json'),"w") as out_file:
                out_file.write(json.dumps(data))           
            
# save full dataframe with date and time of the beginning of the interruption as seperate json file            
        json_name = 'longterm_interruption ({}).json'.format(time.strftime('%Y-%m-%d %H.%M', time.localtime(long_interruption_df.at[0,'Time_float']))) 
        with open(os.path.join(basefolder, json_name),"w") as out_file:
            out_file.write(long_interruption_df.to_json())
<<<<<<< HEAD
        long_interruption_df = pd.DataFrame(columns = ['Time', 'Time_float','Voltage_L1','Voltage_L2','Voltage_L3'])
               
#   Analyses Total Harmonics Distortion (THD) of voltage U and checks if measured data is confom with EN 50160
    THD_U_L1 = pq_data[2236]
    THD_U_L2 = pq_data[2238]
    THD_U_L3 = pq_data[2240]

    if THD_U_L1 >= 8:
        THD_U_L1 = "bad"
    else:
        THD_U_L1 = "okay"

    if THD_U_L2 >= 8:
        THD_U_L2 = "critical"
    else:
        THD_U_L2 = "okay"

    if THD_U_L3 >= 8:
        THD_U_L3 = "critical"
    else:
        THD_U_L3 = "okay"
        
    status_dict['THD_U_L1'] = THD_U_L1
    status_dict['THD_U_L2'] = THD_U_L2
    status_dict['THD_U_L3'] = THD_U_L3

#    Analyses Total Harmonics Distortion (THD) of current I and checks if measured data is confom with EN 50160
    THD_I_L1 = pq_data[2548]
    THD_I_L2 = pq_data[2550]
    THD_I_L3 = pq_data[2552]
=======
        long_interruption_df = pd.DataFrame(columns = ['Time','Voltage_L1','Voltage_L2','Voltage_L3'])

#    Analyses Total Harmonics Distortion (THD) and checks if measured data is confom with EN 50160
    THD_L1 = pq_data[2236]
    THD_L2 = pq_data[2238]
    THD_L3 = pq_data[2240]
>>>>>>> origin/master

    if THD_I_L1 >= 8:
        THD_I_L1 = "bad"
    else:
        THD_I_L1 = "okay"

    if THD_I_L2 >= 8:
        THD_I_L2 = "critical"
    else:
        THD_I_L2 = "okay"

    if THD_I_L3 >= 8:
        THD_I_L3 = "critical"
    else:
<<<<<<< HEAD
        THD_I_L3 = "okay"
        
    status_dict['THD_I_L1'] = THD_I_L1
    status_dict['THD_I_L2'] = THD_I_L2
    status_dict['THD_I_L3'] = THD_I_L3
            
=======
        THD_L3 = "okay"

    status_dict['THD_L1'] = THD_L1
    status_dict['THD_L2'] = THD_L2
    status_dict['THD_L3'] = THD_L3

>>>>>>> origin/master
#    Analyses most important harmonics (5th & 7th) and checks if data is conform with EN 50160
    '''Harmonics U L1,L2,L3: Maximum of mean value'''
    harmonic_5th_U1 = pq_data[1008]
    harmonic_7th_U1 = pq_data[1012]
    voltage_U1 = pq_data[808]

    harmonic_5th_U2 = pq_data[1088]
    harmonic_7th_U2 = pq_data[1092]
    voltage_U2 = pq_data[810]

    '''inacceptable values from janitza for L3'''
    harmonic_5th_U3 = pq_data[1168]
    harmonic_7th_U3 = pq_data[1172]
    voltage_U3 = pq_data[812]


    if harmonic_5th_U1/voltage_U1 > 0.06:
        harmonic_5th_U1 = "bad"
    else:
        harmonic_5th_U1 = "okay"

    if harmonic_7th_U1/voltage_U1 > 0.05:
        harmonic_7th_U1 = "bad"
    else:
        harmonic_7th_U1 = "okay"

    if harmonic_5th_U2/voltage_U2 > 0.06:
        harmonic_5th_U2 = "bad"
    else:
        harmonic_5th_U2 = "okay"

    if harmonic_7th_U2/voltage_U2 > 0.05:
        harmonic_7th_U2 = "bad"
    else:
        harmonic_7th_U2 = "okay"

    if harmonic_5th_U3/voltage_U3 > 0.06:
        harmonic_5th_U3 = "bad"
    else:
        harmonic_5th_U3 = "okay"

    if harmonic_7th_U3/voltage_U3 > 0.05:
        harmonic_7th_U3 = "bad"
    else:
        harmonic_7th_U3 = "okay"

    return frequency_10s, status_dict
