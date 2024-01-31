#!/usr/bin/env python3
# coding: utf-8

import logging
import subprocess
import json

def readLines( fname: str ):
    with open( fname, 'rt' ) as fh:
        ll=fh.readlines()
    
    ll=[x.strip('\n') for x in ll]
    processor = []
    core = {}

    for l in ll:
        if l == '':
            continue
        vl=l.split(':')
        if len(vl) == 2:
            vl = [ x.strip( '\t\n ' ) for x in vl ]
            if vl[0] == 'processor':
                if core:
                    processor.append(core)
                core = {}
                core['processor'] = vl[1]
            elif vl[0] in core:
                logging.warning( f"{vl[0]} defined twice" )
            else:
                core[vl[0]] = vl[1]
        else:
            logging.warning( f"Incorrect line: {l}" )
    if core:
        processor.append( core )
        
    return processor
        
def memory():

    ret = subprocess.run( ['free', '-h'], capture_output=True)
    if ret.returncode == 0:
        retDict = {}
        olines = ret.stdout.decode().split('\n')
        fields = olines[0].split()
        for ol in olines[1:]:
            if ol == '':
                continue
            mem = ol.split()
            if mem[0] in retDict:
                logging.warning( f"Memory {mem[0]} defined twice" )
            else:
                retDict[mem[0]] = dict(map( lambda x,y: (x,y), fields, mem[1:]))
        return retDict
    else:
        logging.warning( "No free command" )
        return None

if __name__ == "__main__":
    p = readLines('/proc/cpuinfo')
    m = memory()
    with open( 'result.json', 'wt' ) as fh:
              json.dump( { 'cpu': p, 'memory': m }, fh )
