# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 16:08:28 2017

@author: Paul-G
"""

def analyse(dict_list):
    dict = dict_list[0]
               
    '''Analyses frequency and checks if measured data is confom with EN 50160'''
#            frequency_average_10s = [10]
#            while True:
#                for i in frequency_average:
#                frequency = dict.get("port_19050")  
#                frequency_average.append(frequency)

    freqeuency_average_10s = dict.get("port_800")
                    
    if freqeuency_average_10s < 49.999 or freqeuency_average_10s > 50.001:
        frequency = "bad"
    elif freqeuency_average_10s < 49.5 or freqeuency_average_10s > 50.5:
        frequency = "critical"
    else:    
        frequency = "okay"
            
    '''Analyses voltage and checks if measured data is confom with EN 50160'''
    voltage_L1_average =  dict.get("port_1728")
    voltage_L2_average =  dict.get("port_1730")
    voltage_L3_average =  dict.get("port_1732")
            
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
    THD_L1 = dict.get("port_836")
    THD_L2 = dict.get("port_868")
    THD_L3 = dict.get("port_840")
            
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
    dict = dict_list[1]

    '''Harmonics U L1,L2,L3: Maximum of mean value'''
    harmonic_5th_U1 = dict.get("port_2606")
    harmonic_7th_U1 = dict.get("port_2610")
            
    harmonic_5th_U2 = dict.get("port_2686")
    harmonic_7th_U2 = dict.get("port_2690")
    
    harmonic_5th_U3 = dict.get("port_2766")
    harmonic_7th_U3 = dict.get("port_2770")
    
    
    if harmonic_5th_U1/231 > 0.06:
        harmonic_5th_U1 = "bad"
    else:
        harmonic_5th_U1 = "okay"
    
    if harmonic_7th_U1/231 > 0.05:
        harmonic_7th_U1 = "bad"
    else:
        harmonic_7th_U1 = "okay"
        
    if harmonic_5th_U2/231 > 0.06:
        harmonic_5th_U2 = "bad"
    else:
        harmonic_5th_U2 = "okay"
   
    if harmonic_7th_U2/231 > 0.05:
        harmonic_7th_U2 = "bad"
    else:
        harmonic_7th_U2 = "okay"
        
    if harmonic_5th_U3/231 > 0.06:
        harmonic_5th_U3 = "bad"
    else:
        harmonic_5th_U3 = "okay"
    
    if harmonic_7th_U3/231 > 0.05:
        harmonic_7th_U3 = "bad"
    else:
        harmonic_7th_U3 = "okay"
                
                
    return frequency, voltage_L1, voltage_L2, voltage_L3, THD_L1, THD_L2, THD_L3, harmonic_5th_U1, harmonic_7th_U1, harmonic_5th_U2, harmonic_7th_U2, harmonic_5th_U3, harmonic_7th_U3