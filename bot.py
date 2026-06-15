# Dependencies
## Core
import time
import json
from datetime import datetime
from threading import Thread

## Custom Utilities
from utils_db import *
from utils_discord import *
from utils_roomcode import*

#from utils_db import db_spinup, db_addroom, db_removeroom, db_getroomfromroomhash, db_getroomfromchannelid, db_getupcominggames, db_setroomdescription
#from utils_discord import dis_commandCreateNewRoom, dis_tagmatch, dis_parsefortags
#from utils_roomcode import rm_generatecodewithhash, rm_hashtocode, rm_codetohash

## Discord
import discord
from discord import app_commands
from discord.ext import tasks

# Initilization and Global Variables 
## Discord Bot Initialization
intents = discord.Intents.default()
intents.message_content = True
DiscordClient = discord.Client(intents=intents)
DiscordCommands = app_commands.CommandTree(DiscordClient)

## Global Variables
config = json.load(open('config.json','r'))
db_object = None
DiscordThread = None
_GlobalServerStop = False
CommandProcessorThread = None

## Discord held variables
OpenRooms = []

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
    # Load config and database connection into global variables for use in events and tasks.
    global config
    
    # Spin up the database connection and store it in a global variable for use in events and tasks.
    global db_object
    db_object = db_spinup(config["config_db"]['db_name'])
    
    # Sync the command tree to the server to register slash commands.
    await DiscordCommands.sync(guild=discord.Object(id=config["config_discord"]['server_id']))
    
    # Finally, print that we're logged in, and start background tasks.
    print(f'[Discord] We have logged in as {DiscordClient.user}')
    CheckCommandQueue.start()
    CloseInactiveRooms.start()
    RefreshUpcomingEvents.start()

@DiscordClient.event
async def on_message(message):
    global config
    global db_object
    
    if message.author == DiscordClient.user:
        return
    
    # Tag Handling
    for tag in dis_parsefortags(message.content):
        tag_response = dis_tagmatch(tag)
        await message.channel.send(tag_response)
    
    if message.content.startswith('&newroom'):
        if message.channel.id != int(config["config_discord"]['new_room_schdule_channel_id']):
            await message.channel.send(f"You can only use &newroom in {(message.guild).get_channel(int(config['config_discord']['new_room_schdule_channel_id'])).mention}")
            return
        
        _roomname = [s.strip() for s in (message.content.replace('&newroom','').strip()).split('|')]
        
        if not (_roomname[0] and _roomname[1] and _roomname[2]):
            await message.channel.send("**Invalid &newroom Format!**\n\nCorrect Format: `&newroom title|yyyy-mm-dd-hh-mm|hrs`")
            return
        
        _rtitle = _roomname[0]
        _rdatetime = _roomname[1]
        _rduration = _roomname[2]
        
        if not _rdatetime.count('-') == 4:
            await message.channel.send("**Invalid DATETIME Format!**\n\nCorrect Format: `&newroom title|yyyy-mm-dd-hh-mm|hrs`")
            return
        
        if not _rduration.isdigit():
            await message.channel.send("**Invalid DURATION Format!**\n\nCorrect Format: `&newroom title|yyyy-mm-dd-hh-mm|hrs`")
            return
        
        while True:
            _iroom = rm_generatecodewithhash()
            existing_room = db_getroomfromroomhash(db_object, _iroom['hash'])
            if len(existing_room) == 0:
                break
        
        _epochtime = int(datetime.strptime(_rdatetime, "%Y-%m-%d-%H-%M").timestamp())
        
        new_channel = await (message.guild).create_voice_channel(name = _rtitle,reason = "&newroom was used",category = (message.guild).get_channel(int(config["config_discord"]['new_room_catagory_id'])))
        await new_channel.send(f"**Welcome to your new room!**\n\nRoom Title: {_rtitle}\nRoom Start Time: <t:{str(_epochtime)}:F>\nRoom Starts in: <t:{str(_epochtime)}:R>\nExpected Duration: {_rduration} hours\n\nRoom link: {new_channel.mention}\nRoom Code: {_iroom['code']}")
        
        db_addroom(db_object, _iroom['hash'], str(new_channel.id), str(message.author.id), _rtitle, _epochtime, _rduration)

        await message.channel.send(f"New room created: \"{_rtitle}\" ({_iroom['code']})")
        
    if message.content.startswith('&removeroom'):
        room_record = db_getroomfromchannelid(db_object, str(message.channel.id))
        if len(room_record) == 0:
            await message.channel.send("This command can only be used in a room created with &newroom.")
            return
        print(room_record)
        if str(message.author.id) != room_record[0][2]:
            await message.channel.send("Only the room owner can remove this room.")
            return
        await message.channel.delete(reason="Room removed by owner using &removeroom")
        db_removeroom(db_object, room_record[0][1])
        
        print(f"[Discord] Removed room {room_record[0][2]} (UUID: {room_record[0][1]}) as requested by owner.")
        
    if message.content.startswith('&joinroom '):
        _roomcode = (message.content).replace('&joinroom ','').strip()
        
        if not _roomcode:
            await message.channel.send("Please provide a room code to join. Format: `&joinroom room-code`")
            return
        
        try:
            _roomhash = rm_codetohash(_roomcode)
        except ValueError as e:
            await message.channel.send(f"Invalid room code! Please check the code and try again.")
            return
        
        _room_record = db_getroomfromroomhash(db_object, _roomhash)
        if len(_room_record) == 0:
            await message.channel.send("Unknown room code! Please check the code and try again.")
            return
        
        _targetchannel = message.guild.get_channel(int(_room_record[0][1]))
        await _targetchannel.set_permissions(message.author, connect=True,
                                                       view_channel=True,
                                                       send_messages=True)
        await message.channel.send(f"You have been granted access to the room: {_targetchannel.mention}")

    if message.content.startswith('&editroom '):
        _messageinfo = [s.strip() for s in (message.content.replace('&editroom','').strip()).split('|')]
        _roomcode = _messageinfo[0]
        _roomdescription = _messageinfo[1]
        db_setroomdescription(db_object, rm_codetohash(_roomcode), _roomdescription)
        await message.channel.send(f"Room description modified for room code: {_roomcode}")
      
@tasks.loop(seconds=1)
async def CheckCommandQueue():
    global _GlobalServerStop
    if _GlobalServerStop:
        print("[Discord] Global Stop Triggered, shutting down Discord client...")
        await DiscordClient.close()
        
@tasks.loop(seconds=10)
async def CloseInactiveRooms():
    global db_object
    _openrooms = DiscordClient.get_channel(int(config["config_discord"]['upcoming_events_channel_id'])).category.voice_channels
        
    for room in _openrooms:
        if room.members == [] and room.id in OpenRooms:
            print("Room has been empty for more than two cycles. Closing room: " + room.name + " (" + str(room.id) + ")")
            await room.delete(reason="Room has been inactive for more than two cycles.")
            _queriedrooms = db_getroomfromvoicechannelid(db_object, room.id)
            if len(_queriedrooms) == 0:
                print("No database record found for room: " + room.name + " (" + str(room.id) + ") - Likely ad-hoc VC.")
                continue
            db_setVCchannelID(db_object, _queriedrooms[0][0], None)
        else:
            if room.members == []:
                print("No one in room: " + room.name + " (" + str(room.id) + ")")
                if room.id not in OpenRooms:
                    OpenRooms.append(room.id)
            else:
                if room.id in OpenRooms:
                    OpenRooms.remove(room.id)

@tasks.loop(seconds=60)
async def RefreshUpcomingEvents():
    _eventlist = db_getupcominggames(db_object)
    
    # If there are no upcoming events, clear the channel and post a message about no events being found.
    if(len(_eventlist) == 0):
        await DiscordClient.get_channel(int(config["config_discord"]['upcoming_events_channel_id'])).purge()
        await DiscordClient.get_channel(int(config["config_discord"]['upcoming_events_channel_id'])).send(f"No upcoming events found! Create one with `&newroom` in <#{config['config_discord']['new_room_schdule_channel_id']}>!")
        return
    
    await DiscordClient.get_channel(int(config["config_discord"]['upcoming_events_channel_id'])).purge()
    
    for event in _eventlist:
        message = ""
        message = message + f"**{event[4]}** - <t:{str(event[5])}:F> ({event[6]} hrs) - Code: **{rm_hashtocode(event[0])}**\n"
        if event[8] != None:
            message = message + f"- *{event[8]}*\n\n"
        await DiscordClient.get_channel(int(config["config_discord"]['upcoming_events_channel_id'])).send(message)

@DiscordCommands.command(name="new-event",
    description="Creates a new room event with the given title, datetime, and duration.",
    guild=discord.Object(id=config["config_discord"]['server_id'])
)
async def first_command(interaction,title:str,start_time:str,duration:str,description:str=None):
    global db_object
    Status = await dis_commandCreateNewRoom(DiscordClient, db_object, int(config["config_discord"]['new_room_schdule_channel_id']), interaction.user.id, title, start_time, duration, description)
    await interaction.response.send_message(content=Status,ephemeral=True,delete_after=60)

@DiscordCommands.command(name="start-vc",
    description="Creates a voice channel for this room. Only the room owner can use this command.",
    guild=discord.Object(id=config["config_discord"]['server_id'])
)
async def first_command(interaction):
    global db_object
    Status = await dis_commandStartVC(DiscordClient, config["config_discord"]['new_room_catagory_id'], db_object, interaction)
    await interaction.response.send_message(content=Status)

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
    #db_object = db_spinup(config["config_db"]['db_name'])
    
    # Command Processor Loading
    CommandProcessorThread = CommandProcessor(handle_input)
    
    # Discord Loading
    DiscordThread = DiscordNodeClass()
    DiscordThread.start()

    while not _GlobalServerStop:
        time.sleep(1)
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
