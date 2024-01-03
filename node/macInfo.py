#!/usr/bin/env python3
# coding: utf-8

import netifaces
import logging

def ifaces():
    maces = {}
    for ni in netifaces.interfaces():
        address = netifaces.ifaddresses(ni)
        try:
            if_mac = address[netifaces.AF_LINK][0]['addr']
        except IndexError:
            if_mac = None
        except KeyError:
            if_mac = None
        if_ip = None
        if netifaces.AF_INET in address:
            if_ip  = address[netifaces.AF_INET][0]['addr']
        if if_mac:
            maces[ni] = (if_mac,if_ip)
    return maces

def gates():
    gg = {}
    for g in netifaces.gateways()[netifaces.AF_INET]:
        gg[g[0]] = g[1:]
    return gg

if __name__ == "__main__":
    ms = ifaces()
    for m in ms:
        print( "{}: {} - {}".format( m, ms[m][1], ms[m][0] ) )
