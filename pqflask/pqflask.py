from flask import Flask, request, make_response
import io
import numpy as np
from pg import DB
import os
import analyse_database as ana_db
import json
import time
import datetime as dt
app = Flask(__name__)

with open('../db_config.json', 'r') as f:
    db_config = json.loads(f.read())

def connect_to_db(description):
    dbname = description['dbname']
    host = description['host']
    port = description['port']
    opt = description['opt']
    user = description['user']
    passwd = description['passwd']
    db = DB(dbname, host, port, opt, user, passwd)
    return db

def get_data_from_db(startTime, endTime, dataName, dataSize):
    # get data from DB
    tc = time.time()
    db = connect_to_db(db_config)
    ttc = time.time() - tc
    if dataSize == 0:
        dataSize = endTime - startTime
    indices = np.linspace(startTime,endTime,num=dataSize,dtype=int)
    rule = 'timestamp between {} and {} and timestamp in ({})'.format(startTime, endTime, ','.join(str(i) for i in indices))

    ts = time.time()
    try:
        df = np.array(db.query('select {} from {} where {}'.format('timestamp', db_config['tablename'], rule)).getresult())[:,-1]
    except IndexError:
        return 'No data in that time period', ''
    tts = time.time() - ts

    # get voltag
    if dataName == 'voltage':
        selectors = ['port_808','port_810','port_812']
        header = 'timestamp,u1,u2,u3'
        df_short = np.empty((df.size,len(selectors)+1))
        df_short[:,0] = df
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[:,-1]
        print('number of timestamps: ' + str(df.size) + ',number of values: ' + str(df_short.size))
    # get current
    elif dataName == 'current':
        selectors = ['port_860','port_862','port_864']
        header = 'timestamp,i1,i2,i3'
        df_short = np.empty((df.size,len(selectors)+1))
        df_short[:,0] = df
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[:,-1]
        print('number of timestamps: ' + str(df.size) + ',number of values: ' + str(df_short.size))
    # get frequency
    elif dataName == 'frequency':
        selectors = ['port_800']
        header = 'timestamp,frequency'
        df_short = np.empty((df.size,len(selectors)+1))
        df_short[:,0] = df
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[:,-1]
        print('number of timestamps: ' + str(df.size) + ',number of values: ' + str(df_short.size))
    # get power
    elif dataName == 'power':
        selectors = ['port_868','port_870','port_872']
        header = 'timestamp,p1,p2,p3'
        df_short = np.empty((df.size,len(selectors)+1))
        df_short[:,0] = df
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[:,-1]
        print('number of timestamps: ' + str(df.size) + ',number of values: ' + str(df_short.size))
    else:
        return 'wrong data type input', ''
    ttsa = time.time() - ts
    print('Conncetion Time: ' + str(ttc) + ' s , Single Selection Time: ' + str(tts) + ' s , Total Selection Time: ' + str(ttsa) + ' s')
    return df_short, header

@app.route('/get_data/', methods=['POST'])
def get_data():
    starttime = time.time()
    # get JSONrequest
    requestJSON = request.get_json()
    print(requestJSON)
    if requestJSON['startTime'] == '':
        startTime = dt.datetime(dt.date.today().year,dt.date.today().month,dt.date.today().day).timestamp()
        endTime = startTime + 24*60*60
    else:
        startTime = requestJSON['startTime']
        endTime = requestJSON['endTime']
    dataName = requestJSON['dataName']
    dataSize = requestJSON['dataSize']
    dataType = requestJSON['dataType']

    csvdata, header = get_data_from_db(startTime, endTime, dataName, dataSize)
    if header == '':
        return csvdata
    output = io.BytesIO()
    #writer = csv.writer(output, delimiter=',', newline='\n', header='Voltage', comments='')
    writer = np.savetxt(output,csvdata, delimiter=',', newline='\n', header=header, comments='')

    response = make_response(output.getvalue())
    response.headers["Content-type"] = dataType
    endtime = time.time()
    print('time needed for response: ' + str(endtime-starttime) + ' s')
    return response

@app.route('/get_data/analyse', methods=['POST'])
def analyse_database():
    requestJSON = request.get_json()
    print(requestJSON)
    dataName = requestJSON['dataName']
    dataPhase = requestJSON['dataPhase']
    # check db for events and write jsons
    if dataName == 'voltage':
        #ana_db.analyse_database_voltage()
        if os.path.isfile('../Website/temp/json/voltage_L{}.json'.format(dataPhase)):
            with open('../Website/temp/json/voltage_L{}.json'.format(dataPhase), 'r') as f:
                responseJSON = f.read()
        else:
            responseJSON = json.dumps(['no data'])

    elif dataName == 'frequency':
        #ana_db.analyse_database_frequency()
        if os.path.isfile('../Website/temp/json/frequency_critical_{}.json'.format(dataPhase)):
            with open('../Website/temp/json/frequency_critical_{}.json'.format(dataPhase), 'r') as f:
                responseJSON = f.read()
        else:
            responseJSON = json.dumps(['no data'])
    elif dataName == 'thdu':
        #ana_db.analyse_database_THD_U()
        if os.path.isfile('../Website/temp/json/THD_U_L{}.json'.format(dataPhase)):
            with open('../Website/temp/json/THD_U_L{}.json'.format(dataPhase), 'r') as f:
                responseJSON = f.read()
        else:
            responseJSON = json.dumps(['no data'])
    elif dataName == 'thdi':
        #ana_db.analyse_database_THD_I()
        if os.path.isfile('../Website/temp/json/THD_I_L{}.json'.format(dataPhase)):
            with open('../Website/temp/json/THD_I_L{}.json'.format(dataPhase), 'r') as f:
                responseJSON = f.read()
        else:
            responseJSON = json.dumps(['no data'])
    elif dataName == 'supplyinterrupt':
        #analyse voltage interruptions
        if os.path.isfile('../Website/temp/json/longterm_interruptions.json'):
            with open('../Website/temp/json/longterm_interruptions.json', 'r') as f:
                responseJSON = f.read()
        else:
            responseJSON = json.dumps(['no data'])       
    else:
        return 'wrong request input'
    response = make_response(responseJSON)
    response.headers['Content-type'] = 'json'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
