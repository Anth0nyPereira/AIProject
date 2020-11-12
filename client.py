import asyncio
import getpass
import json
import os

import websockets
from mapa import Map

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # Next 3 lines are not needed for AI agent perguntar ao stor
        SCREEN = pygame.display.set_mode((299, 123))
        SPRITES = pygame.image.load("data/pad.png").convert_alpha()
        SCREEN.blit(SPRITES, (0, 0))

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
                #TODO : CHANGE THIS

                for key in actions:
                    if key == MoveRight() or key == PushRight():
                        key = "d"
                    if key == MoveLeft() or key == PushLeft():
                        key == "a"
                    if key == MoveUp() or key == PushUp():
                        key = "w"
                    if key == MoveDown() or key == PushDown():
                        key == "s"
                    await websocket.send(json.dumps({"cmd": "key", "key": key}))  # send key command to server - you must implement this send in the AI agent
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return
"""
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:

                        elif event.key == pygame.K_d:
                            import pprint

                            pprint.pprint(state)
                            print(Map(f"levels/{state['level']}.xsb"))
                        
                        break
"""
# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
