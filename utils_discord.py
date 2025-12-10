import json

def dis_tagmatch(tag):
    tags = json.load(open('tags.json','r'))
    return tags[tag]