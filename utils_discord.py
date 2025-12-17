import json

def dis_tagmatch(tag):
    tags = json.load(open('tags.json','r'))
    return tags[tag]

def dis_parsefortags(message_content):
    tags = json.load(open('tags.json','r'))
    found_tags = []
    for tag in tags.keys():
        if f"&{tag}" in message_content.lower():
            found_tags.append(tag)
    return found_tags