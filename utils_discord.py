from datetime import datetime
from email import message
import json
from utils_db import *
from utils_roomcode import *

def dis_tagmatch(tag):
    """
    Check if a tag exists, then return it.
    """
    
    tags = json.load(open('tags.json','r'))
    return tags[tag]

def dis_parsefortags(message_content):
    """
    Parse a message for any tags (e.g., &tag) and return a list of found tags.
    """
    
    tags = json.load(open('tags.json','r'))
    found_tags = []
    for tag in tags.keys():
        if f"&{tag}" in message_content.lower():
            found_tags.append(tag)
    return found_tags

async def dis_commandCreateNewRoom(DiscordClient, db_object, channel_id, owner, title, start_time, _duration, description=None):
    """
    Create a new room in the database and return its room code.
    """
    
    if not start_time.count('-') == 4:
        return "Invalid START_TIME Format! Correct Format: `yyyy-mm-dd-hh-mm`"
        
    if not _duration.isdigit():
        return "Invalid DURATION Format! Correct Format: `#` of hours (e.g., 2)"
    
    _epochtime = int(datetime.strptime(start_time, "%Y-%m-%d-%H-%M").timestamp())
    
    while True:
        _iroom = rm_generatecodewithhash()
        existing_room = db_getroomfromroomhash(db_object, _iroom['hash'])
        if len(existing_room) == 0:
            break
    
    room_code, room_hash = _iroom['code'], _iroom['hash']
    
    postedmessage = await DiscordClient.get_channel(channel_id).send(f"<Big Join thig goes here> Room Code: `{room_code}`")
    subthread = await postedmessage.create_thread(name=f"{title}", auto_archive_duration=10080,reason=f"Thread for room {room_code}")
    await subthread.send(f"**Welcome to your new room!**\n\nRoom Title: {title}\nRoom Description: {description}\n\nRoom Start Time: <t:{str(_epochtime)}:F>\nRoom Starts in: <t:{str(_epochtime)}:R>\nExpected Duration: {_duration} hours\n\nRoom link: {subthread.mention}\nRoom Code: {room_code}")
    
    db_addroom(db_object, room_hash, dis_ownerID=owner, dis_channelID=subthread.id, r_title=title, r_datetime=_epochtime, r_duration=_duration, r_desc=description)
    
    return "Created new room with code: " + room_code

async def dis_commandStartVC(DiscordClient, vc_catagoryID, db_object, interaction):
    """
    Create a voice channel for the room.
    """
    _room_record = db_getroomfromchannelid(db_object, interaction.channel_id)
    
    if len(_room_record) == 0:
        return "This command can only be used in a room's thread channel!"
    
    _hash = _room_record[0][0]
    _oid = _room_record[0][1]
    _cid = _room_record[0][2]
    _vid = _room_record[0][3]
    _rtitle = _room_record[0][4]
    
    if _cid != interaction.channel_id:
        return "I don't know how you got this! - This command can only be used in the room's thread channel!"
    
    if _vid != None:
        return "A voice channel has already been created for this room! Voice Channel: " + (interaction.guild).get_channel(int(_vid)).mention
    
    if interaction.user.id != _oid:
        return "You are not the owner of this room! Only the owner can start the voice channel."
    
    new_vcchannel = await (interaction.guild).create_voice_channel(name=_rtitle, reason="/start-vc was used", category=DiscordClient.get_channel(int(vc_catagoryID)))
    await new_vcchannel.send(f"Linked to room: {DiscordClient.get_channel(int(_cid)).mention}")
    
    db_setVCchannelID(db_object, _hash, new_vcchannel.id)
    
    return "Voice channel created: " + new_vcchannel.mention