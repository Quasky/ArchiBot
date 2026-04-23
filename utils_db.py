import sqlite3
import uuid
import os
import json

def db_spinup(db_name):
    """
    Spin up the sqlite database and populate it with the room table and its columns if it doesn't already exist.
    """
    
    _db_object = sqlite3.connect(db_name)
    _db_object.cursor().execute("CREATE TABLE IF NOT EXISTS room(hash, cid, oid, title, datetime, duration, data)")
    return _db_object

def db_addroom(db_object, room_hash, dis_channelID, dis_ownerID, r_title, r_datetime, r_duration):
    """
    Add a new room to the database. 
    (room_hash, dis_channelID, dis_ownerID, r_title, r_datetime, r_duration, r_data)
    """
    
    r_data = "{}"
    db_object.cursor().execute("INSERT INTO room VALUES (?,?,?,?,?,?,?)", (room_hash, dis_channelID, dis_ownerID, r_title, r_datetime, r_duration, r_data))
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

def db_setroomname(db_object, room_hash, new_name):
    """
    Update the name of a room in the database based on its hash.
    """
    db_object.cursor().execute("UPDATE room SET cid=? WHERE hash=?", (new_name, room_hash))
    db_object.commit()
    
def db_getupcominggames(db_object):
    """
    Retrieve the 10 upcoming games from the database, ordered by datetime.
    """
    return db_object.cursor().execute("SELECT * FROM room ORDER BY datetime ASC").fetchmany(size = 10)

# "(hash cid, oid, cn, st, dur, data)"
# "date time tz title duration role"
# "yyyy-mm-dd hh-mm tz title hrs role"