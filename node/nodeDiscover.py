#!/usr/bin/env python3
# coding: utf-8

import platform
import subprocess
import json
import requests

import toml
import logging
import re
 
noNetifaces = None
try:
    import macInfo
except ModuleNotFoundError:
    noNetifaces = True

with open( 'config.toml','rt') as fh:
    config = toml.load(fh)

try:
    ADDRESS = config['server']['ip']
    PORT    = config['server']['port']
    NODE_URL = config['server']['url']
    NODE_HEADERS = config['http']['header']
except KeyError as ke:
    print( "Unknown field {} in config.toml".format(e) )
    exit(1)

def jsonify( strj: str ):
    try:
        js = json.loads(strj)
    except json.JSONDecodeError as jde:
        logging.error( "Cannot convert to JSON: {}".format(jde.msg) )
        js = jde.doc
    return js

def jsonifyTable( strj: str ):
    s2 = '[' + strj.strip() + ']'
    return jsonify( s2.replace('\n',',') )

def installedApp( jDict, app, detailQueries = {}, versQuery = '--version', name=None ):
    if not name:
        name = app
    subp = subprocess.run( ["/usr/bin/env", app, versQuery],
                          capture_output=True )
    if subp.returncode == 0:
        verr = subp.stdout.decode().strip()
        m = re.search( '\d+\.\d+\.\d+', verr )
        if m:
            verr = m.group()
        else:
            m = re.search( '\d+\.\d+', verr )
            if m:
                verr = m.group()
        jDict[name] = verr
    else:
        jDict[name] = None
    if detailQueries:
        jDict[name + '_details'] = {}
        for dq in detailQueries:
            queries = ["/usr/bin/env", app]
            doFunc = None
            if type(detailQueries[dq]) is str:
                queries.append(detailQueries[dq])
            elif type(detailQueries[dq]) is list:
                queries.extend(detailQueries[dq])
            elif type(detailQueries[dq]) is dict:
                if 'func' in detailQueries[dq] and 'query' in detailQueries[dq]:
                    if type(detailQueries[dq]['query']) is str:
                        queries.append(detailQueries[dq]['query'])
                    elif type(detailQueries[dq]['query']) is list:
                        queries.extend(detailQueries[dq]['query'])
                    doFunc = detailQueries[dq]['func']
                else:
                    continue
            else:
                continue
            subp = subprocess.run( queries, capture_output =  True )
            if subp.returncode == 0:
                if doFunc:
                    jDict[name + '_details'][dq] = doFunc(subp.stdout.decode())
                else:
                    jDict[name + '_details'][dq] = subp.stdout.decode().strip()

def findPyVenv( jDict: dict ):
    name = "venv"
    jDict[name] = None
    res = subprocess.run( [ "/usr/bin/env", "pip3", "show", name ],
                         capture_output = True )
    if res.returncode == 0:
        verr = subp.stdout.decode().strip()
        m = re.search( '\d+\.\d+\.\d+', verr )
        if m:
            verr = m.group()
        else:
            m = re.search( '\d+\.\d+', verr )
            if m:
                verr = m.group()
        jDict[name] = verr
    else:
        res = subprocess.run( [ "/usr/bin/env", "apt", "list", "python3-" + name ],
                             capture_output = True )
        if res.returncode == 0:
            sl = res.stdout.decode().split('\n')
            for s in sl:
                if s.endswith('[installed]'):
                    m = re.search( '\d+(\.\d+){2,3}', s )
                    if m:
                        jDict[name] = m.group()


if __name__ == "__main__":
    nodeInfo = {}
    nodeInfo["platform"] = platform.machine()
    nodeInfo["node"] = platform.node()
    nodeInfo["release"] = platform.release()
    nodeInfo["system"] = platform.system()

    if 'freedesktop_os_release' in dir(platform):
        nodeInfo["lsb"] = {}
        for k,v in platform.freedesktop_os_release().items():
            nodeInfo["lsb"][k] = v
    else:
        logging.warn( "TODO: (#3) Module platform does not contain freedesktop_os_release" )

    installedApp( nodeInfo, "python3" )
    nodeInfo["python3_details"] = {}
    installedApp( nodeInfo["python3_details"], "pip3" )
    installedApp( nodeInfo["python3_details"], "pipenv" )
    installedApp( nodeInfo["python3_details"], "poetry" )
    installedApp( nodeInfo["python3_details"], "pytest" )
    findPyVenv( nodeInfo['python3_details'] )

    installedApp( nodeInfo, "docker", 
                 detailQueries = {
                     "images": { "query": ["images","--format","json","--digests"],
                                "func": jsonifyTable },
                     "containers": { "query": ["ps","-a","--format","json","--size"],
                                    "func": jsonifyTable }
                     }
                 )
    installedApp( nodeInfo, "ldd", name="glibc" )
    installedApp( nodeInfo, "openssl", versQuery="version" )

    if not noNetifaces:
        nodeInfo["netifaces"] = macInfo.ifaces()
        nodeInfo["gateways"] = macInfo.gates()
    else:
        logging.error( "TODO: (#4) backup for netifaces (route -n and ip a)" )

    requests.post( "http://" + ADDRESS + ":" + PORT + NODE_URL,
                  data = json.dumps( nodeInfo ),
                  headers = NODE_HEADERS )
