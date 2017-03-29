from flask import Flask
app = Flask(__name__)

@app.route('/flask')
def test():
    return 'hello world'

@app.route('/get_data', methods=['POST'])
def get_data():
    return 'hello world'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
