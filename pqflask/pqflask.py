from flask import Flask, request, make_response
import io
import numpy as np
from pg import DB
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

def get_data_from_db(startTime, endTime, dataName):
    # get data from DB
    tc = time.time()
    db = connect_to_db(db_config)
    ttc = time.time() - tc
    indices = np.linspace(startTime,endTime,num=1000,dtype=int)
    rule = 'timestamp between {} and {} and where timestamp in ({})'.format(startTime, endTime, ','.join(str(i) for i in indices))

    ts = time.time()
    try:
        df = np.array(db.query('select {} from {} where {}'.format('timestamp', db_config['tablename'], rule)).getresult())[:,-1]
    except IndexError:
        return 'No data in that time period', ''
    tts = time.time() - ts
    print('complete number of timestamp values per day: ' + str(df.size))

    # get voltag
    if dataName == 'voltage':
        selectors = ['port_808','port_810','port_812']
        header = 'timestamp,u1,u2,u3'
        df_short = np.empty((1000,len(selectors)+1))
        df_short[:,0] = df[indices]
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[indices,-1]
    # get current
    elif dataName == 'current':
        selectors = ['port_860','port_862','port_864']
        df_short = np.empty((1000,len(selectors)+1))
        df_short[:,0] = df[indices]
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[indices,-1]
    # get frequency
    elif dataName == 'frequency':
        selectors = ['port_800']
        header = 'timestamp,frequency'
        df_short = np.empty((1000,len(selectors)+1))
        df_short[:,0] = df[indices]
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[indices,-1]
    # get power
    elif dataName == 'power':
        selectors = ['port_868','port_870','port_872']
        header = 'timestamp,p1,p2,p3'
        df_short = np.empty((1000,len(selectors)+1))
        df_short[:,0] = df[indices]
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[indices,-1]
    else:
        return 'wrong data type input', ''
    ttsa = time.time() - ts
    print('Conncetion Time: ' + str(ttc) + ' s , Single Selection Time' + str(tts) + ' s , Total Selection Time' + str(ttsa) + ' s')
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

    csvdata, header = get_data_from_db(startTime, endTime, dataName)
    if header == '':
        return csvdata
    print(type(csvdata))
    output = io.BytesIO()
    #writer = csv.writer(output, delimiter=',', newline='\n', header='Voltage', comments='')
    writer = np.savetxt(output,csvdata, delimiter=',', newline='\n', header=header, comments='')
    print('csvdata size: '+str(csvdata.size))

    response = make_response(output.getvalue())
    response.headers["Content-type"] = "text"
    endtime = time.time()
    print('time needed for response: ' + str(endtime-starttime) + ' s')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
