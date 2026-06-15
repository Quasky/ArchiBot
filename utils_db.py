import sqlite3
import uuid
import os
import json

def db_spinup(db_name):
    """
    Spin up the sqlite database and populate it with the room table and its columns if it doesn't already exist.
    """
    
    _db_object = sqlite3.connect(db_name)
    _db_object.cursor().execute("CREATE TABLE IF NOT EXISTS room(hash, oid, cid, vid, title, datetime, duration, data, desc, ex1, ex2, ex3, ex4, ex5)")
    return _db_object

def db_addroom(db_object, room_hash, dis_channelID=None, dis_voicelID=None, dis_ownerID=None, r_title=None, r_datetime=None, r_duration=None, r_data=None, r_desc=None, r_ex1=None, r_ex2=None, r_ex3=None, r_ex4=None, r_ex5=None):
    """
    Add a new room to the database. 
    (room_hash, dis_ownerID, dis_channelID, r_title, r_datetime, r_duration, r_data, r_desc, r_ex1, r_ex2, r_ex3, r_ex4, r_ex5)
    """

    db_object.cursor().execute("INSERT INTO room VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (room_hash, dis_ownerID, dis_channelID, dis_voicelID, r_title, r_datetime, r_duration, r_data, r_desc, r_ex1, r_ex2, r_ex3, r_ex4, r_ex5))
    db_object.commit()

def db_removeroom(db_object, room_hash):
    """
    Remove a room from the database based on its hash.
    """
    db_object.cursor().execute("DELETE FROM room WHERE hash=?", (room_hash,))
    db_object.commit()

def db_getroomfromroomhash(db_object, room_hash):
    """
    Retrieve a room from the database based on its hash.
    """
    return db_object.cursor().execute("SELECT * FROM room WHERE hash=?", (room_hash,)).fetchall()

def db_getroomfromchannelid(db_object, dis_channelID):
    """
    Retrieve a room from the database based on its Discord channel ID.
    """
    return db_object.cursor().execute("SELECT * FROM room WHERE cid=?", (dis_channelID,)).fetchall()

def db_getroomfromvoicechannelid(db_object, dis_voicechannelID):
    """
    Retrieve a room from the database based on its Discord voice channel ID.
    """
    return db_object.cursor().execute("SELECT * FROM room WHERE vid=?", (dis_voicechannelID,)).fetchall()

def db_setroomname(db_object, room_hash, new_name):
    """
    Update the name of a room in the database based on its hash.
    """
    db_object.cursor().execute("UPDATE room SET cid=? WHERE hash=?", (new_name, room_hash))
    db_object.commit()
    
def db_setroomdescription(db_object, room_hash, new_description):
    """
    Update the description of a room in the database based on its hash.
    """
    db_object.cursor().execute("UPDATE room SET desc=? WHERE hash=?", (new_description, room_hash))
    db_object.commit()
    
def db_setVCchannelID(db_object, room_hash, new_VCchannelID):
    """
    Update the voice channel ID of a room in the database based on its hash.
    """
    db_object.cursor().execute("UPDATE room SET vid=? WHERE hash=?", (new_VCchannelID, room_hash))
    db_object.commit()
    
def db_getupcominggames(db_object):
    """
    Retrieve the 10 upcoming games from the database, ordered by datetime.
    """
    return db_object.cursor().execute("SELECT * FROM room ORDER BY datetime ASC").fetchmany(size = 10)

# "(hash cid, oid, cn, st, dur, data)"
# "date time tz title duration role"
# "yyyy-mm-dd hh-mm tz title hrs role"