import sqlite3
import uuid
import os
import json

def db_spinup(db_name):
    _db_object = sqlite3.connect(db_name)
    _db_object.cursor().execute("CREATE TABLE IF NOT EXISTS rooms(uuid)")
    _db_object.cursor().execute("CREATE TABLE IF NOT EXISTS roomdeets(uuid, name, owner)")
    return _db_object

def db_addroom(db_object, dis_channelID, dis_ownerID):
    room_uuid = str(uuid.uuid4())
    db_object.cursor().execute("INSERT INTO rooms VALUES (?)", (room_uuid,))
    db_object.cursor().execute("INSERT INTO roomdeets VALUES (?,?,?)", (room_uuid, dis_channelID, dis_ownerID))
    db_object.commit()
    return room_uuid

def db_removeroom(db_object, room_uuid):
    db_object.cursor().execute("DELETE FROM rooms WHERE uuid=?", (room_uuid,))
    db_object.cursor().execute("DELETE FROM roomdeets WHERE uuid=?", (room_uuid,))
    db_object.commit()

def db_getroom(db_object, room_uuid):
    return db_object.cursor().execute("SELECT * FROM roomdeets WHERE uuid=?", (room_uuid,)).fetchall()

