#!/usr/bin/env python3
# coding: utf-8

import netifaces
import logging

def ifaces():
    maces = {}
    for ni in netifaces.interfaces():
        address = ni.ifaddresses(ni)
        try:
            if_mac = address[netifaces.AF_LINK][0]['addr']
            if_ip  = address[netifaces.AF_INET][0]['addr']
        except IndexError, KeyError:
            if_mac = if_ip = None
        if if_mac:
            maces[address] = (if_mac,if_ip)
    return maces
