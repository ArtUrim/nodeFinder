from flask import Flask, make_response, jsonify
app = Flask(__name__)
import json
import redis

import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

def send2Db():
    if send2Db.r is None:
        send2Db.r = redis.Redis( host="redis-stack", port=6379 )
    jarr = []
    for d in send2Db.r.ft('info').search( Query('*').return_fields( "node", "platform" "docker" "python3" ) ).docs:
        jarr.append(d.__dict__)
    return jarr

send2Db.r = None

@app.route('/api/nodes')
def hello_world():
    resp = make_response( jsonify( send2Db() ) )
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status = 200
    return resp

@app.route( '/api/species' )
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
    app.run(host='0.0.0.0')

