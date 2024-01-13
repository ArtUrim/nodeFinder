from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/node/info", methods=['POST'])
def hello_world():
    js = request.get_json()
    print( type(js))
    for s in js:
        print( "{}: {}".format(s, js[s]) )
    return '', 204

if __name__ == "__main__":
    app.run( host = '0.0.0.0' )
