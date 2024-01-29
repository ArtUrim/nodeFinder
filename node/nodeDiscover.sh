#!/usr/bin/env bash

/usr/bin/env python nodeDiscover.py
if [ "${?}" == "0" ]
then
	if [ -e "result.json" ]
	then
		curl -X POST -H "Content-Type: application/json" -d @result.json http://192.168.0.241:5000/node/info
	fi
fi
