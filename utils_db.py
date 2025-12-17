import sqlite3
import uuid
import os
import json

def db_spinup(db_name):
    _db_object = sqlite3.connect(db_name)
    _db_object.cursor().execute("CREATE TABLE IF NOT EXISTS room(hash, cid, oid, title, datetime, duration)")
    return _db_object

def db_addroom(db_object, room_hash, dis_channelID, dis_ownerID, r_title, r_datetime, r_duration):
    db_object.cursor().execute("INSERT INTO room VALUES (?,?,?,?,?,?)", (room_hash, dis_channelID, dis_ownerID, r_title, r_datetime, r_duration))
    db_object.commit()

def db_removeroom(db_object, room_hash):
    db_object.cursor().execute("DELETE FROM room WHERE hash=?", (room_hash,))
    db_object.commit()

def db_getroomfromroomhash(db_object, room_hash):
    return db_object.cursor().execute("SELECT * FROM room WHERE hash=?", (room_hash,)).fetchall()

def db_getroomfromchannelid(db_object, dis_channelID):
    return db_object.cursor().execute("SELECT * FROM room WHERE cid=?", (dis_channelID,)).fetchall()

def db_setroomname(db_object, room_hash, new_name):
    db_object.cursor().execute("UPDATE room SET cid=? WHERE hash=?", (new_name, room_hash))
    db_object.commit()
    
def db_getupcominggames(db_object):
    return db_object.cursor().execute("SELECT * FROM room ORDER BY datetime ASC").fetchmany(size = 10)

# "(hash cid, oid, cn, st, dur)"
# "date time tz title duration role"
# "yyyy-mm-dd hh-mm tz title hrs role"