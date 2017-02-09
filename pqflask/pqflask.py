from flask import Flask
app = Flask(__name__)

@app.route('/flask')
def test():
    return 'hello world'

@app.route('/html/Historische-Werte.html', methods=['POST'])
def get_data():
    # parse POST request
    requested_values = request.get_json()

    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
