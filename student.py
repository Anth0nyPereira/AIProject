import asyncio
import getpass
import json
import os

import websockets
from mapa import Map
from tree_search import *

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                update = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                if "map" in update:
                    # we got a new level
                    game_properties = update
                    mapa = Map(update["map"])
                else:
                    # we got a current map state update
                    state = update

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                my_dom = MyDomain(mapa._map)
                my_prob = MyProblem(my_dom)
                my_tree = MyTree(my_prob)
                
                my_tree.search()

                win_the_game = my_tree.getplan(my_tree.solution)

                for key in win_the_game:
                    await websocket.send(json.dumps({"cmd": "key", "key": key}))  # send key command to server - you must implement this send in the AI agent
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
