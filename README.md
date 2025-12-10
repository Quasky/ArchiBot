# ArchiBot
An Archipelago; Lobby Managment, FAQ, and Operations bot

## Install & Run
```
1) Clone repo
2) Create venv
3) pip install -r requirements.txt
4) run 'python bot.py'
```

## Command Processor
I've imbedded a command processor into the bot to allow control from the script console. This is handy due to the threads that run to keep this going.  
Type `stop` into the console to gracefully stop the threads and allow the script to close.  
This will eventually be used to do some more 'administrative' actions around the DB, and bot.

-----
-----

## TO DO
* Lobby managment  
    1) Create rooms  
    1) remove rooms  
    1) reschedule rooms  
    1) post to schedule

* Run managment  
    1) ready-up  
    1) unready-up  
    1) START  
  
* Tags  
    1) Transcribe tags to tags.json  
    1) add tags via discord  
    1) remove tags via discord  
    1) list all tags  

## Tags in AginahBot now:
|Tag|Status|
|-----|-----|
|addplayers||
|afterdark||
|aginahbotspam||
|apworld||
|async||
|balancing||
|bk||
|cache||
|channels||
|customsupport||
|docs||
|down||
|eyepatch||
|legalrom||
|locationcount||
|manual||
|multiworldnews||
|newgames||
|number||
|oldgames||
|pins||
|queue||
|qusb||
|roles||
|room||
|template|DONE -Q|
|topic||
|uicolors||
|update||
|weights||
|whatsapquest||
|worlds||



## Slash commands in AginahBot now:
Most of these can be ditched for a 'mod' bot, but keeping/improving on the lobby managment bits.

|Slash|Status|
|-----|-----|
|Mod-contact-open||
|mod-contact-resolve||
|pin||
|pin-grant||
|pin-list||
|pin-revoke||
|room-system-create||
|room-system-destroy||
|save-log||
|schedule-adjust||
|schedule-board-delete||
|schedule-board-post||
|schedule-cancel||
|schedule-new||
|schedule-new-relative||
|schedule-new-ts||
|shhedule-view||
|tag-add||
|tag-delete||
|unpin||

