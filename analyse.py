# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 16:08:28 2017

@author: Paul-G
"""

import pandas as pd

def analyse(pq_data, frequency_average_10s, i):
    '''Analyses live Data from pq_data: frequency, voltage, THD, harmonics. i = [0...9] for frequency_average_10s'''
    data_dict = pq_data[0]
               
    '''Analyses frequency and checks if measured data is confom with EN 50160
    Both frequency_average_10s AND frequency are returned'''
#   frequency_average_10s = [] '''in pqmain.py'''
            
    if len(frequency_average_10s) < 10:
        frequency_average_10s.append(data_dict.get("port_800"))
    else:
        frequency_average_10s[i] = data_dict.get("port_800")
     
    frequency = sum(frequency_average_10s)/len(frequency_average_10s)
               
    if frequency_average_10s < 47.5 or frequency_average_10s > 52:
        frequency = "bad"
    elif frequency_average_10s < 49.5 or frequency_average_10s > 50.5:
        frequency = "critical"
    else:    
        frequency = "okay"
            
    '''Analyses voltage and checks if measured data is confom with EN 50160'''
    voltage_L1_average =  data_dict.get("port_1728")
    voltage_L2_average =  data_dict.get("port_1730")
    voltage_L3_average =  data_dict.get("port_1732")
            
    if voltage_L1_average < 208 or voltage_L1_average > 254:
        voltage_L1 = "critical"
    else:
        voltage_L1 = "okay"
        
    if voltage_L2_average < 208 or voltage_L1_average > 254:
        voltage_L2 = "critical"
    else:
        voltage_L2 = "okay"
        
    if voltage_L3_average < 208 or voltage_L1_average > 254:
        voltage_L3 = "critical"
    else:
        voltage_L3 = "okay"
                                
    '''Analyses Total Harmonics Distortion (THD) and checks if measured data is confom with EN 50160'''
    THD_L1 = data_dict.get("port_836")
    THD_L2 = data_dict.get("port_868")
    THD_L3 = data_dict.get("port_840")
            
    if THD_L1  >= 8:
        THD_L1 = "bad"
    else:
        THD_L1 = "okay"
        
    if THD_L2 >= 8:
        THD_L2 = "critical"
    else:
        THD_L2 = "okay"
               
    if THD_L3 >= 8:
        THD_L3 = "critical"
    else:
        THD_L3 = "okay"
            
    '''Analyses most important harmonics (5th & 7th) and checks if data is conform with EN 50160'''
#    data_dict = pq_data[1]

    '''Harmonics U L1,L2,L3: Maximum of mean value'''
    harmonic_5th_U1 = data_dict.get("port_1008")
    harmonic_7th_U1 = data_dict.get("port_1012")
    voltage_U1 = data_dict.get("port_808") 
            
    harmonic_5th_U2 = data_dict.get("port_1088")
    harmonic_7th_U2 = data_dict.get("port_1092")
    voltage_U2 = data_dict.get("port_810") 
    
    '''inacceptable values from janitza for L3'''
    harmonic_5th_U3 = data_dict.get("port_1168")
    harmonic_7th_U3 = data_dict.get("port_1172")
    voltage_U3 = data_dict.get("port_812") 
    
    
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
                
                
    return frequency_average_10s, frequency, voltage_L1, voltage_L2, voltage_L3, THD_L1, THD_L2, THD_L3, harmonic_5th_U1, harmonic_7th_U1, harmonic_5th_U2, harmonic_7th_U2, harmonic_5th_U3, harmonic_7th_U3