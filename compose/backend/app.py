from flask import Flask, make_response, jsonify
app = Flask(__name__)
import json
import redis

import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

import gitlab
import base64
import re

def gitlab_file( p, fpath ):
    rp = p.repository_tree(recursive=True,all=True)
    for ff in rp:
        if ff['name'] == fpath:
            f = p.files.get( ff['path'], 'main').decode().decode()
            return { 'content': f }
    return None

def gitlab_query(project=None,fpath=None):
    if gitlab_query.g is None:
        gitlab_query.g = gitlab.Gitlab(private_token='glpat-qNf7AsMoxoASEcU5RUk7')
    if gitlab_query.projects is None:
        gitlab_query.projects = gitlab_query.g.projects.list( owned=True, search='test' )
    if project is None:
        gitlab_query.projects = gitlab_query.g.projects.list( owned=True, search='test' )
        return [ p.name for p in gitlab_query.projects ]
    p_found = None
    for p in gitlab_query.projects:
        if project == p.name:
            p_found = True
            break
    if p_found:
        if fpath:
            return gitlab_file( p, fpath )
        rp = p.repository_tree(recursive=True,all=True)
        files = []
        for x in [ f['name'] for f in rp]:
            if re.match( 'm.*\.py', x ):
                files.append(x)
        return files
    return None

gitlab_query.g = None
gitlab_query.projects = None

def send2Db():
    if send2Db.r is None:
        send2Db.r = redis.Redis( host="redis-stack", port=6379 )
    jarr = []
    for d in send2Db.r.ft('info').search( Query('*').return_fields( "node", "platform", "docker", "python3" ) ).docs:
        node = d.__dict__
        node.pop('id', None)
        node.pop('payload', None)
        jarr.append(node)
    return jarr

send2Db.r = None

@app.route('/api/nodes')
def hello_world():
    resp = make_response( jsonify( send2Db() ) )
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status = 200
    return resp

@app.route('/api/test/<project>/file/<fname>', methods=['GET'] )
def test_file( project, fname ):
    try:
        val = gitlab_query( project, fname )
    except gitlab.GitlabAuthenticationError as ge:
        print ( f"Receive gitlab error {ge}" )
        error = { 'origin': 'gitlab',
                 'value': str(ge) }
        resp = make_response( jsonify( error ) )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status = 400
        return resp
    if val is None:
        error = { 'origin': 'parser',
                 'value': f"No project {project}" }
        resp = make_response( jsonify( error ) )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status = 418
        return resp
    resp = make_response( jsonify( val ) )
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status = 200
    return resp
    

@app.route('/api/tests', methods=['GET'] )
@app.route('/api/tests/', methods=['GET'] )
@app.route('/api/tests/<project>', methods=['GET'] )
def tests_from_gitlab(project=None):
    try:
        val = gitlab_query( project )
    except gitlab.GitlabAuthenticationError as ge:
        print ( f"Receive gitlab error {ge}" )
        error = { 'origin': 'gitlab',
                 'value': str(ge) }
        resp = make_response( jsonify( error ) )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status = 400
        return resp
    if val is None:
        error = { 'origin': 'parser',
                 'value': f"No project {project}" }
        resp = make_response( jsonify( error ) )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status = 418
        return resp
    resp = make_response( jsonify( val ) )
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

