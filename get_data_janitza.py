 # -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:15:15 2016

@authors: Nils, Jule, Leo
"""

import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import json
import time
import tables
import datetime
import os

jsonpath = 'jsonfiles'
h5path = 'h5files'
os.makedirs(jsonpath, exist_ok=True)
os.makedirs(h5path, exist_ok=True)

def get_JanitzaUMG_data(IP='129.69.176.123'):
    
# Define measures and adresses:
    
    adresses = []
    measures = []    
    '''
    #"Häufig benötigte Messwerte" - common used measures (19000-19120):
    for adress in range(19000,19121,2):
        adresses.append(adress)       
    measures.extend(['U1','U2','U3',
                     'U12','U23','U31',
                     'I1','I2','I3','I123',
                     'P1','P2','P3','P123',
                     'S1','S2','S3','S123',
                     'Q1','Q2','Q3','Q123',
                     'CosPhi1','CosPhi2','CosPhi3',
                     'f','rot_field',
                     'E1_real','E2_real','E3_real','E123_real',
                     'E1_real_cons','E2_real_cons','E3_real_cons','E123_real_cons',
                     'E1_real_del','E2_real_del','E3_real_del','E123_real_del',
                     'E1_app','E2_app','E3_app','E123_app',
                     'E1_react','E2_react','E3_react','E123_react',                       
                     'E1_react_ind','E2_react_ind','E3_react_ind','E123_react_ind',
                     'E1_react_cap','E2_react_cap','E3_react_cap','E123_react_cap',
                     'THD_U1','THD_U2','THD_U3',
                     'THD_I1','THD_I2','THD_I3'])  
    '''
    # "Messwerte" - actual measures (800-858, 860-938):
    for adress in range(800,859,2):
        adresses.append(adress) 
    measures.extend(['f',
                     'U_zero','U_neg','U_pos',
                     'U1','U2','U3',
                     'U12','U23','U31',
                     'CosPhi1','CosPhi2','CosPhi3','CosPhi123',
                     'ULN_powerfactor1','ULN_powerfactor2','ULN_powerfactor3','ULN_powerfactor123',
                     'THD_U1','THD_U2','THD_U3',
                     'THD_U12','THD_U23','THD_U31',
                     'U1_real','U2_real','U3_real',
                     'U1_imag','U2_imag','U3_imag'])
    for adress in range(860,939,2):
        adresses.append(adress)                     
    measures.extend(['I1','I2','I3','I123',
                     'P1','P2','P3','P123',
                     'Q1','Q2','Q3','Q123',
                     'S1','S2','S3','S123',
                     'P01','P02','P03','P0123',
                     'D1','D2','D3','D123',
                     'THD_I1','THD_I2','THD_I3',
                     'TDD_I1','TDD_I2','TDD_I3',
                     'I_zero','I_neg','I_pos',
                     'I1_real','I2_real','I3_real',
                     'I1_imag','I2_imag','I3_imag',
                     'rot_field'])
    
    # "Mittelwerte" - average measures (1720-1738, 2220-2258, 2500-2576):  
    for adress in range(1720,1739,2):
        adresses.append(adress) 
    measures.extend(['f_av',
                     'U_zero_av','U_neg_av','U_pos_av',
                     'U1_av','U2_av','U3_av',
                     'U12_av','U23_av','U31_av'])
    for adress in range(2220,2259,2):
        adresses.append(adress) 
    measures.extend(['CosPhi1_av','CosPhi2_av','CosPhi3_av','CosPhi123_av',
                     'ULN_powerfactor1_av','ULN_powerfactor2_av','ULN_powerfactor3_av','ULN_powerfactor123_av',
                     'THD_U1_av','THD_U2_av','THD_U3_av',
                     'THD_U12_av','THD_U23_av','THD_U31_av',
                     'U1_real_av','U2_real_av','U3_real_av',
                     'U1_imag_av','U2_imag_av','U3_imag_av'])
    for adress in range(2500,2577,2):
        adresses.append(adress)                     
    measures.extend(['I1_av','I2_av','I3_av','I123_av',
                     'P1_av','P2_av','P3_av','P123_av',
                     'Q1_av','Q2_av','Q3_av','Q123_av',
                     'S1_av','S2_av','S3_av','S123_av',
                     'P01_av','P02_av','P03_av','P0123_av',
                     'D1_av','D2_av','D3_av','D123_av',
                     'THD_I1_av','THD_I2_av','THD_I3_av',
                     'TDD_I1_av','TDD_I2_av','TDD_I3_av',
                     'I_zero_av','I_neg_av','I_pos_av',
                     'I1_real_av','I2_real_av','I3_real_av',
                     'I1_imag_av','I2_imag_av','I3_imag_av'])
    
    # "Minimalwerte" - minimum measures (3436-3494):
    for adress in range(3436,3495,2):
        adresses.append(adress)                     
    measures.extend(['f_min',
                     'U_zero_min','U_neg_min','U_pos_min',
                     'U1_min','U2_min','U3_min',
                     'U12_min','U23_min','U31_min',
                     'CosPhi1_min','CosPhi2_min','CosPhi3_min','CosPhi123_min',
                     'ULN_powerfactor1_min','ULN_powerfactor2_min','ULN_powerfactor3_min','ULN_powerfactor123_min',
                     'THD_U1_min','THD_U2_min','THD_U3_min',
                     'THD_U12_min','THD_U23_min','THD_U31_min',
                     'U1_real_min','U2_real_min','U3_real_min',
                     'U1_imag_min','U2_imag_min','U3_imag_min'])
    
    # "Maximalwerte" - maximum measures (2578-2596, 3078-3116, 3358-3434)   
    for adress in range(2578,2597,2):
        adresses.append(adress)                    
    measures.extend(['f_max',
                     'U_zero_max','U_neg_max','U_pos_max',
                     'U1_max','U2_max','U3_max',
                     'U12_max','U23_max','U31_max'])
    for adress in range(3078,3117,2):
        adresses.append(adress)                    
    measures.extend(['CosPhi1_max','CosPhi2_max','CosPhi3_max','CosPhi123_max',
                     'ULN_powerfactor1_max','ULN_powerfactor2_max','ULN_powerfactor3_max','ULN_powerfactor123_max',
                     'THD_U1_max','THD_U2_max','THD_U3_max',
                     'THD_U12_max','THD_U23_max','THD_U31_max',
                     'U1_real_max','U2_real_max','U3_real_max',
                     'U1_imag_max','U2_imag_max','U3_imag_max'])
    for adress in range(3358,3435,2):
        adresses.append(adress)                    
    measures.extend(['I1_max','I2_max','I3_max','I123_max',
                     'P1_max','P2_max','P3_max','P123_max',
                     'Q1_max','Q2_max','Q3_max','Q123_max',
                     'S1_max','S2_max','S3_max','S123_max',
                     'P01_max','P02_max','P03_max','P0123_max',
                     'D1_max','D2_max','D3_max','D123_max',
                     'THD_I1_max','THD_I2_max','THD_I3_max',
                     'TDD_I1_max','TDD_I2_max','TDD_I3_max',
                     'I_zero_max','I_neg_max','I_pos_max',
                     'I1_real_max','I2_real_max','I3_real_max',
                     'I1_imag_max','I2_imag_max','I3_imag_max'])
                     
    # "Energie" - energy (from most common measures: 19054-19108)
    for adress in range(19054,19109,2):
        adresses.append(adress)                    
    measures.extend(['E1_real','E2_real','E3_real','E123_real',
                     'E1_real_cons','E2_real_cons','E3_real_cons','E123_real_cons',
                     'E1_real_del','E2_real_del','E3_real_del','E123_real_del',
                     'E1_app','E2_app','E3_app','E123_app',
                     'E1_react','E2_react','E3_react','E123_react',                       
                     'E1_react_ind','E2_react_ind','E3_react_ind','E123_react_ind',
                     'E1_react_cap','E2_react_cap','E3_react_cap','E123_react_cap'])
                     
    # harmonics are separated from the other categories because they are saved as arrays for each measures
    
    # "Harmonische" - harmonics (arrays with the first 40 harmonics of each measure: 1000-1718)  
    for adress in range(1000,1641,80):
        adresses.append(adress)                    
    measures.extend(['H_U1','H_U2','H_U3',
                     'H_U12','H_U23','H_U31',
                     'H_I1','H_I2','H_I3'])   
    # "Durchschnitt Harmonische" - average harmonics (arrays with the first 40 harmonics of each measure: 1740-2218, 2260-2498)
    for adress in range(1740,2141,80):
        adresses.append(adress)                    
    measures.extend(['H_U1_av','H_U2_av','H_U3_av',
                     'H_U12_av','H_U23_av','H_U31_av'])
    for adress in range(2260,2421,80):
        adresses.append(adress)                    
    measures.extend(['H_I1_av','H_I2_av','H_I3_av'])
    # "Maximalwerte Harmonische" - max. values of harmonics (arrays with the first 40 harmonics of each measure: 2598-3076, 3118-3356)
    for adress in range(2598,2999,80):
        adresses.append(adress)                    
    measures.extend(['H_U1_max','H_U2_max','H_U3_max',
                     'H_U12_max','H_U23_max','H_U31_max'])
    for adress in range(3118,3279,80):
        adresses.append(adress)                    
    measures.extend(['H_I1_max','H_I2_max','H_I3_max'])

    # define dictionary to assign each adress to the corresponding measure data:
    adress_measure_dict = dict(zip(adresses,measures)) 

# Define charts:     
    # chosen measures for charts with json (average value of 10 minutes):
    measures_charts =  ['localtime','f_av',
                        'U1_av','U2_av','U3_av',
                        'U12_av','U23_av','U31_av',
                        'CosPhi1_av','CosPhi2_av','CosPhi3_av','CosPhi123_av',
                        'THD_U1_av','THD_U2_av','THD_U3_av',
                        'THD_U12_av','THD_U23_av','THD_U31_av',
                        'I1_av','I2_av','I3_av','I123_av',
                        'P1_av','P2_av','P3_av','P123_av',
                        'Q1_av','Q2_av','Q3_av','Q123_av',
                        'S1_av','S2_av','S3_av','S123_av',
                        'THD_I1_av','THD_I2_av','THD_I3_av',
                        'E1_real','E2_real','E3_real','E123_real']

# Define hdf5-file:
    
    # chosen measures for hdf5-file (average value of 10 minutes):
    measures_h5 =      ['localtime','f_av',
                        'U1_av','U2_av','U3_av',
                        'I1_av','I2_av','I3_av',
                        'P1_av','P2_av','P3_av',
                        'H_U1_av','H_U2_av','H_U3_av',
                        'H_U12_av','H_U23_av','H_U31_av',
                        'H_I1_av','H_I2_av','H_I3_av']
     
#    class janitza_table_storage(tables.IsDescription):
#        # 1 data for common used measures:
#        f_av_h5=U1_av_h5=U2_av_h5=U3_av_h5=I1_av_h5=I2_av_h5=I3_av_h5=P1_av_h5=P2_av_h5=P3_av_h5 = tables.Float32Col()
#        # 40 datas for harmonics:        
#        H_U1_av_h5=H_U2_av_h5=H_U3_av_h5=H_U12_av_h5=H_U23_av_h5=H_U31_av_h5=H_I1_av_h5=H_I2_av_h5=H_I3_av_h5 = tables.Float32Col(40)
#        # localtime as string:        
#        localtime_h5=tables.StringCol(24)
#        
#    try:    
#        h5file = tables.open_file("data_janitza.h5", mode = "w", title = "measure data hdf5-file") 
#        group = h5file.create_group("/", 'janitza', 'Janitza measure group')
#        table = h5file.create_table(group, 'janitza_measure_data', janitza_table_storage, "Janitza table")           
#    finally:        
#        h5file.close()          

    
# Connect to the slave:
    master = modbus_tcp.TcpMaster(host = IP)
    master.set_timeout(5)    
    starttime=time.time()    
    
# get data:
    counter=0 
    #while counter<200: # "while counter" just for testing purposes, replace with "while True"
    while True:
        t1=time.time()
        measure_data_dict = {}
        adress_data_dict = {}
        data_converted = []
        harmonics_converted=[]
        
        '''
        #"Häufig benötigte Messwerte" - common used measures (19000-19120):
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,19000,122)
        for n in range(0,122,2):
            data_converted.append(convert_to_float(data[n:n+2]))
        '''
        # "Messwerte" - actual measures (800-858, 860-938):
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,800,60) # f, U, CosPhi, power_factor, THD_U, U_real/imag
        for n in range(0,60,2):
            data_converted.append(convert_to_float(data[n:n+2])) 
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,860,80) # I, P, Q, S, P0, D, THD_I, I_real/imag, rot_field
        for n in range(0,80,2):
            data_converted.append(convert_to_float(data[n:n+2])) 
        
        # "Mittelwerte" - average measures (1720-1738, 2220-2258, 2500-2576):
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1720,20) # f_av, U_av
        for n in range(0,20,2):
            data_converted.append(convert_to_float(data[n:n+2]))      
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2220,40) # CosPhi_av, power_factor_av, THD_U_av, U_real/imag_av
        for n in range(0,40,2):
            data_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2500,78) # I_av, P_av, Q_av, S_av, P0_av, D_av, THD_I_av, I_real/imag_av
        for n in range(0,78,2):
            data_converted.append(convert_to_float(data[n:n+2]))
        
        # "Minimalwerte" - minimum measures (3436-3494):
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,3436,60) # f_min, U_min, CosPhi_min, power_factor_min, THD_U_min, U_real/imag_min
        for n in range(0,60,2):
            data_converted.append(convert_to_float(data[n:n+2]))
        
        # "Maximalwerte" - maximum measures (2578-2596, 3078-3116, 3358-3434)  
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2578,20) # f_max, U_max
        for n in range(0,20,2):
            data_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,3078,40) # CosPhi_max, power_factor_max, THD_U_max, U_real/imag_max
        for n in range(0,40,2):
            data_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,3358,78) # I_max, P_max_ Q_max, S_max, P0_max, D_max, THD_I_max, I_real/imag_max
        for n in range(0,78,2):
            data_converted.append(convert_to_float(data[n:n+2])) 
        
        # "Energie" - energy (from most common measures: 19054-19108)
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,19054,56) # E_real (+ cons, del), E_app, E_react (+ ind, cap)
        for n in range(0,56,2):
            data_converted.append(convert_to_float(data[n:n+2]))        
        
        # "Harmonische" - harmonics (arrays with the first 40 harmonics of each measure: 1000-1718)        
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1000,80) # H_U1
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1080,80) # H_U2
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1160,80) # H_U3
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1240,80) # H_U12
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1320,80) # H_U23
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1400,80) # H_U31
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1480,80) # H_I1
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1560,80) # H_I2
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1640,80) # H_I3
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
            
        # "Durchschnitt Harmonische" - average harmonics (arrays with the first 40 harmonics of each measure: 1740-2218, 2260-2498)
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1740,80) # H_U1_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1820,80) # H_U2_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1900,80) # H_U3_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,1980,80) # H_U12_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2060,80) # H_U23_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2140,80) # H_U31_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2260,80) # H_I1_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2340,80) # H_I2_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2420,80) # H_I3_av
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
            
        # "Maximalwerte Harmonische" - max. values of harmonics (arrays with the first 40 harmonics of each measure: 2598-3356)
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2598,80) # H_U1_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2678,80) # H_U2_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2758,80) # H_U3_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2838,80) # H_U12_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2918,80) # H_U23_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,2998,80) # H_U31_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,3118,80) # H_I1_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))                
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,3198,80) # H_I2_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
        data = master.execute(1, cst.READ_HOLDING_REGISTERS,3278,80) # H_I3_max
        for n in range(0,80,2):
            harmonics_converted.append(convert_to_float(data[n:n+2]))
            
        for i in range(0,len(data_converted)):
            if data_converted[i]>10**10 or data_converted[i]<-10**10:
                data_converted[i]=666
        
        # create dictionaries:
        measure_data_dict = dict(zip(measures, data_converted))
        adress_data_dict = dict(zip(adresses, data_converted))
        
        # update dictionaries with the harmonics in arrays
        # update measure_data_dict 
        measure_data_dict.update({"H_U1": harmonics_converted[0:40]})
        measure_data_dict.update({"H_U2": harmonics_converted[40:80]})
        measure_data_dict.update({"H_U3": harmonics_converted[80:120]})
        measure_data_dict.update({"H_U12": harmonics_converted[120:160]})
        measure_data_dict.update({"H_U23": harmonics_converted[160:200]})
        measure_data_dict.update({"H_U31": harmonics_converted[200:240]})
        measure_data_dict.update({"H_I1": harmonics_converted[240:280]})
        measure_data_dict.update({"H_I2": harmonics_converted[280:320]})
        measure_data_dict.update({"H_I3": harmonics_converted[320:360]})
        
        measure_data_dict.update({"H_U1_av": harmonics_converted[360:400]})
        measure_data_dict.update({"H_U2_av": harmonics_converted[400:440]})
        measure_data_dict.update({"H_U3_av": harmonics_converted[440:480]})
        measure_data_dict.update({"H_U12_av": harmonics_converted[480:520]})
        measure_data_dict.update({"H_U23_av": harmonics_converted[520:560]})
        measure_data_dict.update({"H_U31_av": harmonics_converted[560:600]})
        measure_data_dict.update({"H_I1_av": harmonics_converted[600:640]})
        measure_data_dict.update({"H_I2_av": harmonics_converted[640:680]})
        measure_data_dict.update({"H_I3_av": harmonics_converted[680:720]})
        
        measure_data_dict.update({"H_U1_max": harmonics_converted[720:760]})
        measure_data_dict.update({"H_U2_max": harmonics_converted[760:800]})
        measure_data_dict.update({"H_U3_max": harmonics_converted[800:840]})
        measure_data_dict.update({"H_U12_max": harmonics_converted[840:880]})
        measure_data_dict.update({"H_U23_max": harmonics_converted[880:920]})
        measure_data_dict.update({"H_U31_max": harmonics_converted[920:960]})
        measure_data_dict.update({"H_I1_max": harmonics_converted[960:1000]})
        measure_data_dict.update({"H_I2_max": harmonics_converted[1000:1040]})
        measure_data_dict.update({"H_I3_max": harmonics_converted[1040:1080]})
        
        # update adress_data_dict
        adress_data_dict.update({1000: harmonics_converted[0:40]})
        adress_data_dict.update({1080: harmonics_converted[40:80]})
        adress_data_dict.update({1160: harmonics_converted[80:120]})
        adress_data_dict.update({1240: harmonics_converted[120:160]})
        adress_data_dict.update({1320: harmonics_converted[160:200]})
        adress_data_dict.update({1400: harmonics_converted[200:240]})
        adress_data_dict.update({1480: harmonics_converted[240:280]})
        adress_data_dict.update({1560: harmonics_converted[280:320]})
        adress_data_dict.update({1640: harmonics_converted[320:360]})
        
        adress_data_dict.update({1740: harmonics_converted[360:400]})
        adress_data_dict.update({1820: harmonics_converted[400:440]})
        adress_data_dict.update({1900: harmonics_converted[440:480]})
        adress_data_dict.update({1980: harmonics_converted[480:520]})
        adress_data_dict.update({2060: harmonics_converted[520:560]})
        adress_data_dict.update({2140: harmonics_converted[560:600]})
        adress_data_dict.update({2260: harmonics_converted[600:640]})
        adress_data_dict.update({2340: harmonics_converted[640:680]})
        adress_data_dict.update({2420: harmonics_converted[680:720]})
        
        adress_data_dict.update({2598: harmonics_converted[720:760]})
        adress_data_dict.update({2678: harmonics_converted[760:800]})
        adress_data_dict.update({2758: harmonics_converted[800:840]})
        adress_data_dict.update({2838: harmonics_converted[840:880]})
        adress_data_dict.update({2918: harmonics_converted[880:920]})
        adress_data_dict.update({2998: harmonics_converted[920:960]})
        adress_data_dict.update({3118: harmonics_converted[960:1000]})
        adress_data_dict.update({3198: harmonics_converted[1000:1040]})
        adress_data_dict.update({3278: harmonics_converted[1040:1080]})
        
        # localtime:
        measure_data_dict.update({'localtime': time.asctime( time.localtime(time.time()) )})
        
        # Harmonics-help-list for harmonic bar chart in JavaScript:
        if counter==0:
            H_help=[]
            for i in range(1,41):
                H_help.append(i)
        measure_data_dict.update({'H_help':H_help})
        
        # create json:
        
        with open(jsonpath+'UMGdata_measure_data_dict.json','w') as f:
            f.write(json.dumps(measure_data_dict))
#            with open('../Server/static/data/UMGdata_adress_data_dict.json','w') as f:
#                f.write(json.dumps(adress_data_dict))
        
        #print('Saved measure_data_dict in JSON : '+str(measure_data_dict['U1']))
        #print('Saved adress_data_dict in JSON: '+str(adress_data_dict[19000]))
    
        # create json for charts:

        if counter == 0:
            charts_duration = 48*60 # in minutes
            charts_act_time = 1 # update time in minutes - if changed, please also change the update algorithm below!!!
            charts_data_number = int(charts_duration/charts_act_time) # numbers of values in list for each measure
            charts_dict = {}
            
            # list of zeros for each measure in size of chosen max chart hours and update time:
            for key in measures_charts:
                charts_dict.update({key: [0]*charts_data_number})
                
            lastminute = -1 # for first update
        
        # update of charts_dict every minute:
        currentminute = datetime.datetime.now().minute
        if currentminute > lastminute or (lastminute == 59 and currentminute == 0):
            lastminute = currentminute
            for key in charts_dict.keys():
                for i in range (1, charts_data_number):
                    charts_dict[key][i-1] = charts_dict[key][i]
                charts_dict[key][charts_data_number-1] = measure_data_dict[key]
                
        print('Current minute: '+str(currentminute))
        with open(jsonpath+'UMGdata_charts_dict.json','w') as f:
            f.write(json.dumps(charts_dict))

        # save some data in HDF5 File:            
        # hdf5 append:
        
#        if(counter == 0):
#            h5file = tables.open_file(h5path+"data_janitza.h5", mode = "a", title = "measure data hdf5-file")
#            lastminute_h5 = -1
#        
#        # append every new minute:
#        currentminute_h5 = datetime.datetime.now().minute
#        if currentminute_h5 > lastminute_h5 or (lastminute_h5 == 59 and currentminute_h5 == 0):
#            lastminute_h5 = currentminute_h5
#            table = h5file.root.janitza.janitza_measure_data
#            particles = table.row
#            for i in range(0, len(measures_h5)):
#                particles[measures_h5[i]+'_h5'] = measure_data_dict[measures_h5[i]]
#            particles.append()
#            table.flush()

        print('Counter: '+str(counter))
        print('Duration loop: '+str(time.time()-t1))        # Loop duration
        
        print('Duration total: '+str(time.time()-starttime)) # total duration
        counter = counter + 1


    #h5file.close()    
   
    
    return measure_data_dict, adress_data_dict, adress_measure_dict, data, charts_dict, counter
    
        

def convert_to_float(data): 
    sign = 1 if data[0] < 32768 else -1
    exponent = ((data[0] % 2**15) >> 7) - 127
    high0 = data[0] % 128 * 2**16
    low0 = data[1]
    mantisse = (high0 + low0) % 2**23
    return round(sign * (1.0 + mantisse / 2**23) * 2**exponent, 4)

if __name__ == '__main__':

    measure_data_dict, adress_data_dict, adress_measure_dict, data, charts_dict, counter = get_JanitzaUMG_data()

