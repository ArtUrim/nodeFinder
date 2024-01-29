from flask import Flask, request
node_con = Flask(__name__)
import json
import redis

def send2Db(name,js):
    if send2Db.r is None:
        send2Db.r = redis.Redis( host="redis-stack", port=6379 )
    send2Db.r.json().set( name, '$', js )

send2Db.r = None

@node_con.route('/node/info', methods=['POST'])
def hello_world():

    js = request.get_json()
    if "node" in js:
        send2Db( "node:" + js["node"],js)
        print( str(type(js)) )
        for s in js:
            print( "{}: {}".format(s, js[s]) )
        return '', 204
    else:
        return "", 404

if __name__ == "__main__":
    node_con.run(host='0.0.0.0')

