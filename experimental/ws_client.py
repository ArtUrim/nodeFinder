#!/usr/bin/env python3

import asyncio
import logging
import json

from time import sleep

import pathlib
import ssl
import websockets

import msg_proto_pb2

certbase = "localhost"
pem = certbase + '.pem'

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name(pem)
ssl_context.load_verify_locations(localhost_pem)

async def hello():
    async with websockets.connect("wss://localhost:8765", ssl=ssl_context) as websocket:
        msg = msg_proto_pb2.NodeInfo()
        msg.name = "wyse"
        msg.ver  = "linux"
        await websocket.send( msg.SerializeToString())
        mstr = await websocket.recv()
        recv = msg_proto_pb2.Ack()
        recv.ParseFromString( mstr )

        print(f"Received: {recv.ack}")

logging.basicConfig( level = logging.INFO )
logging.info( "Ready to serve" )
asyncio.run(hello())
