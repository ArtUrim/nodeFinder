#!/usr/bin/env python3
# coding: utf-8

import platform
import subprocess
import json
import requests

import toml

with open( 'config.toml','rt') as fh:
    config = toml.load(fh)

try:
    ADDRESS = config['server']['ip']
    PORT    = config['server']['port']
    NODE_HEADERS = config['http']['header']
except KeyError as ke:
    print( "Unknown field {} in config.toml".format(e) )
    exit(1)

def installedApp( jDict, app, detailQueries = {}, versQuery = '--version' ):
    subp = subprocess.run( ["/usr/bin/env", app, versQuery],
                          capture_output=True )
    if subp.returncode == 0:
        jDict[app] = subp.stdout.decode().strip()
    else:
        jDict[app] = None
    if detailQueries:
        jDict[app + '_details'] = {}
        for dq in detailQueries:
            queries = ["/usr/bin/env", app]
            doFunc = None
            if type(detailQueries[dq]) is str:
                queries.append(detailQueries[dq])
            elif type(detailQueries[dq]) is list:
                queries.extend(detailQueries[dq])
            elif type(detailQueries[dq]) is dict:
                if 'func' in detailQueries[dq] and 'query' in detailQueries[dq]:
                    if type(detailQueries[dq]) is str:
                        queries.append(detailQueries[dq]['query'])
                    elif type(detailQueries[dq]) is list:
                        queries.extend(detailQueries[dq]['query'])
                    doFunc = detailQueries[dq]['func']
                else:
                    continue
            else:
                continue
            subp = subprocess.run( queries, capture_output =  True )
            if subp.returncode == 0:
                if doFunc:
                    jDict[app + '_details'][dq] = doFunc(subp.stdout.decode())
                else:
                    jDict[app + '_details'][dq] = subp.stdout.decode().strip()
    
if __name__ == "__main__":
    nodeInfo = {}
    nodeInfo["platform"] = platform.machine()
    nodeInfo["node"] = platform.node()
    nodeInfo["release"] = platform.release()
    nodeInfo["system"] = platform.system()

    nodeInfo["lsb"] = {}
    for k,v in platform.freedesktop_os_release().items():
        nodeInfo["lsb"][k] = v

    installedApp( nodeInfo, "python3" )
    installedApp( nodeInfo, "docker" )
    installedApp( nodeInfo, "ls", detailQueries = { "all": "-a", "some": ["-t", "-l"] } )

    requests.post( "http://" + ADDRESS + ":" + PORT,
                  data = json.dumps( nodeInfo ),
                  headers = NODE_HEADERS )
