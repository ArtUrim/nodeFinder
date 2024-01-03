#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets

import logging

import msg_proto_pb2

async def hello(websocket):
    msg = await websocket.recv()
    node = msg_proto_pb2.NodeInfo()
    node.ParseFromString( msg )
    logging.info(f"name: {node.name}, version: {node.ver}" )

    ack = msg_proto_pb2.Ack()
    ack.ack = True
    await websocket.send(ack.SerializeToString())
    logging.info(f">>> {ack.ack}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhost_pem)

async def main():
    async with websockets.serve(hello, "localhost", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    logging.basicConfig( level = logging.INFO )
    logging.info( "Ready to serve" )
    asyncio.run(main())
