import asyncio
import websockets
import json

translator = {
    "Syringe": "syringes",
    "Med Kit (Level 2)": "medkits",
    "Phoenix Kit (Level 3)": "phoenixKits",
    "Shield Cell": "shieldCells",
    "Shield Battery (Level 2)": "shieldBatteries",
    "Ultimate Accelerant (Level 3)": "ultimateAccelerants"
}

class WSServer:
    def __init__(self, host='localhost', port=7777, msg_handler=None, respawn_callback=None):
        self.host = host
        self.port = port
        self.server = None
        self.swap = True
        self.names = set()
        self.msg_handler = msg_handler
        self.respawn_callback = respawn_callback
        self.active_player = None
        self.all_meds = {}

    async def handle_message(self, message):
        incoming = json.loads(message)
        if "category" in incoming:
            # print(f"Category: {incoming['category']}")
            if incoming["category"] == "init":
                print(f"Connected!")
            if incoming["category"] == "playerConnected":
                self.all_meds[incoming["player"]["nucleusHash"]] = {
                    "syringes": 4,
                    "medkits": 0,
                    "phoenixKits": 0,
                    "shieldCells": 4,
                    "shieldBatteries": 0,
                    "ultimateAccelerants": 0
                }
            elif incoming["category"] == "matchSetup":
                print(f"-------- {incoming["startingLoadout"]} --------")
            elif incoming["category"] == "matchStateEnd":
                self.all_meds = {}
            elif incoming["category"] == "observerSwitched":
                self.active_player = incoming["target"]["nucleusHash"]
            elif incoming["category"] == "playerRespawnTeam":
                print(f"-------- {message} --------")
                self.respawn_callback(team=incoming["player"]["teamName"], players=[player["name"] for player in incoming["respawnedTeammates"]])
                # will need a callback function for displaying the respawned player's info on the overlay (Team respawned X [and Y])
            elif incoming["category"] == "inventoryPickUp":
                if incoming["item"] in translator:
                    med_type = translator[incoming["item"]]
                    if incoming["player"]["nucleusHash"] in self.all_meds:
                        self.all_meds[incoming["player"]["nucleusHash"]][med_type] += incoming["quantity"]
            elif incoming["category"] == "inventoryDrop":
                if incoming["item"] in translator:
                    med_type = translator[incoming["item"]]
                    if incoming["player"]["nucleusHash"] in self.all_meds:
                        self.all_meds[incoming["player"]["nucleusHash"]][med_type] -= incoming["quantity"]
            elif incoming["category"] == "inventoryUse":
                if incoming["item"] in translator:
                    med_type = translator[incoming["item"]]
                    if incoming["player"]["nucleusHash"] in self.all_meds:
                        self.all_meds[incoming["player"]["nucleusHash"]][med_type] -= incoming["quantity"]
                        
    
    async def main(self, websocket):
        print(f"Connecting to {websocket.remote_address[0]}!")
        print(self.server.connections)

        async for message in websocket:
            try:
                if self.msg_handler:
                    await self.msg_handler(message)
                else:
                    await self.handle_message(message)
            except Exception as e:
                print(e)
                continue
    
    def get_active_player_meds(self):
        if self.active_player and self.active_player in self.all_meds:
            return self.all_meds[self.active_player]
        return {
            "syringes": 0,
            "medkits": 0,
            "phoenixKits": 0,
            "shieldCells": 0,
            "shieldBatteries": 0,
            "ultimateAccelerants": 0
        }
            
    async def start(self):
        async with websockets.serve(self.main, self.host, self.port, open_timeout=None, ping_timeout=None) as serv:
            self.server = serv
            print(f"Serving on port {self.port}...")
            await asyncio.Future()