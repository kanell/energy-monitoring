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
    db = connect_to_db(db_config)
    rule = 'timestamp between ' + str(startTime) + ' and ' + str(endTime)
    try:
        df = np.array(db.query('select {} from {} where {}'.format('timestamp', db_config['tablename'], rule)).getresult())[:,-1]
    except IndexError:
        return 'No data in that time period', ''
    indices = np.linspace(0,df.size-1,num=1000,dtype=int)
    print('complete number of timestamp values per day: ' + str(df.size))

    if dataName == 'voltage':
        selectors = ['port_808','port_810','port_812']
        header = 'timestamp,u1,u2,u3'
        df_short = np.empty((1000,len(selectors)+1))
        df_short[:,0] = df[indices]
        for index, selector in enumerate(selectors):
            df_short[:,index+1] = np.array(db.query('select {} from {} where {}'.format(selector, db_config['tablename'], rule)).getresult())[indices,-1]

    elif dataName == 'current':
        pass
    elif dataName == 'frequency':
        pass
    elif dataName == 'power':
        pass
    else:
        return 'wrong data type input', ''
    return df_short, header

@app.route('/get_data/', methods=['POST'])
def get_data():
    starttime = time.time()
    # get JSONrequest
    requestJSON = request.get_json()
    print(requestJSON)
    if requestJSON['date'] == '':
        startTime = int(dt.datetime.now().timestamp())
    else:
        startTime = dt.datetime.strptime(requestJSON['date'],'%m/%d/%Y').timestamp()
    endTime = startTime + 24*60*60
    dataName = requestJSON['dataName']

    csvdata, header = get_data_from_db(startTime, endTime, dataName)
    if type(csvdata) == 'str':
        return csvdata
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
