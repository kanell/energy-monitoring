from flask import Flask, request, make_response
import io
import numpy as np
from pg import DB
import json
import datetime as dt

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
    df = np.array([])

    if dataName == 'voltage':
        selectors = ['port_808','port_810','port_812']
        for selector in selectors:
            try:
                if rule == None:
                    # get all data
                    df = np.array(db.query('select {} from {}'.format(selector, tablename)).getresult())[:,-1]
                else:
                    # get data depending on rule
                    df = np.array(db.query('select {} from {} where {}'.format(selector, tablename, rule)).getresult())[:,-1]
            except IndexError:
                print('No data in that time period')
                df = np.array([])

    elif dataName == 'current':
        pass
    elif dataName == 'frequency':
        pass
    elif dataName == 'power':
        pass
    else:
        return 'wrong data type input'
    return df

@app.route('/get_data/', methods=['POST'])
def get_data():
    # get JSONrequest
    requestJSON = request.get_json()
    print(requestJSON)
    if requestJSON['date'] == '':
        return 'no date is selected'
    startTime = dt.datetime.strptime(requestJSON['date'],'%m/%d/%Y').timestamp()
    endTime = startTime + 24*60*60
    dataName = requestJSON['dataName']

    csvdata = get_data_from_db(startTime, endTime, dataName)
    if type(csvdata) == 'str':
        return csvdata
    output = io.BytesIO()
    #writer = csv.writer(output, delimiter=',', newline='\n', header='Voltage', comments='')
    writer = np.savetxt(output,csvdata, delimiter=',', newline='\n', header='Voltage', comments='')

    response = make_response(output.getvalue())
    response.headers["Content-type"] = "text"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
