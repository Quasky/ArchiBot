# Dependencies
## Core
import time
import json
from threading import Thread

## Custom Utilities
from utils_db import db_spinup
from utils_discord import dis_tagmatch

## Discord
import discord
from discord.ext import tasks

# Initilization and Global Variables 
## Discord Bot Initialization
intents = discord.Intents.default()
intents.message_content = True
DiscordClient = discord.Client(intents=intents)

## Global Variables
config = json.load(open('config.json','r'))
db_object = None
DiscordThread = None
_GlobalServerStop = False
CommandProcessorThread = None

# Command Processor Class
## Used to handle in-console command to help control the bot
class CommandProcessor(Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True
        self.start()
        
    def run(self):
        global _GlobalServerStop
        
        print("[CMD Processor] Starting Command Processor")
        while not _GlobalServerStop:
            user_input = input()
            self.callback(user_input)
        print("[CMD Processor] Stopping Command Processor...")
        
def handle_input(user_input):
    user_input = user_input.lower()
    print(f"[CMD Processor] Received command: {user_input}")
    if user_input == "stop":
        global _GlobalServerStop
        _GlobalServerStop = True
    elif user_input == "":
        pass
    else:
        print("[CMD Processor] Unknown command. Available commands: stop")
# END Command Processor Class

# Discord Bot Class, Events, and Tasks
## Handles Running the Discord Bot and its events
class DiscordNodeClass(Thread):
    def __init__(self) -> None:
        super().__init__()

    # Allows us to use threading to start and manage the Discord client
    def run(self):
        DiscordClient.run(config["config_discord"]['token'])

@DiscordClient.event
async def on_ready():
    print(f'[Discord] We have logged in as {DiscordClient.user}')
    CheckCommandQueue.start()

@DiscordClient.event
async def on_message(message):
    if message.author == DiscordClient.user:
        return
    
    if "&template" in message.content.lower():
            await message.channel.send(dis_tagmatch("template"))
    if "&test" in message.content.lower():
            await message.channel.send(dis_tagmatch("test"))

@tasks.loop(seconds=1)
async def CheckCommandQueue():
    global _GlobalServerStop
    if _GlobalServerStop:
        print("[Discord] Global Stop Triggered, shutting down Discord client...")
        await DiscordClient.close()
# END Discord Bot Class, Events, and Tasks

# Main Holder Process
## Keeps application running and manages threads and global variables
def MainProcess():
    # Variable Loading
    global _GlobalServerStop
    global db_object
    global CommandProcessorThread
    global DiscordThread
    
    # Database Loading
    db_object = db_spinup(config["config_db"]['db_name'])
    
    # Command Processor Loading
    CommandProcessorThread = CommandProcessor(handle_input)
    
    # Discord Loading
    DiscordThread = DiscordNodeClass()
    DiscordThread.start()

    while not _GlobalServerStop:
        time.sleep(5)
    print("[Main] Exiting Main Process")
# END Main Holder Process

if __name__ == '__main__':
    MainProcess()
    print("[Main] Shutdown Triggered, joining threads to exit cleanly...")
    print("[Main] Joining CommandProcessorThread")
    CommandProcessorThread.join()
    print("[Main] Joining DiscordThread")
    DiscordThread.join()
    print("[Main] All threads joined and exited, Goodnight :)")
