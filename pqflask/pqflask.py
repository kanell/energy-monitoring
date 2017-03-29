from flask import Flask, request
import io
app = Flask(__name__)

@app.route('/flask')
def test():
    return 'hello world'

@app.route('/get_data', methods=['POST'])
def get_data():
    requestJSON = request.get_json()
    print(requestJSON)
    startTime = requestJSON['startTime']
    endTime = requestJSON['endTime']
    dataName = requestJSON['dataName']

    csvdata = np.array([1,2,3,4,5], dtype=np.float64)
    output = io.BytesIO()
    #writer = csv.writer(output, delimiter=',', newline='\n', header='Voltage', comments='')
    writer = np.savetxt(output,csvdata, delimiter=',', newline='\n', header='Voltage', comments='')
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0')
