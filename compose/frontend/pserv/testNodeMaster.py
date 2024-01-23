from flask import Flask, make_response, request, jsonify
import json

app = Flask(__name__)

@app.route("/node/info", methods=['POST'])
def hello_world():
    js = request.get_json()
    print( type(js))
    for s in js:
        print( "{}: {}".format(s, js[s]) )
    return '', 204

@app.route( '/species' )
def species():
    vals = [ {
        "name": 'African Elephant',
        "species": 'Loxodonta africana',
        "diet": 'Herbivore',
        "habitat": 'Savanna, Forests',
        },
        {
            "name": 'Mysz',
            "species": 'myszarka',
            "diet": 'co znajdzie',
            "habitat": 'domek'
        }
    ]
    resp = make_response( jsonify(vals) )
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status = 200
    return resp


if __name__ == "__main__":
    app.run( host = '0.0.0.0' )
