import random

# Seedlist of 500 words, should be enough for 500*500*500 = 125,000,000 unique room names... enough for now :)
seedlist = [
  "game","play","fun","win","lose","score","level","point","player","team",
  "match","round","turn","start","finish","pause","menu","map","mode","goal",
  "time","timer","clock","health","power","speed","jump","run","walk","move",
  "shoot","hit","block","dodge","attack","defense","skill","item","gear","armor",
  "weapon","tool","key","coin","gold","bonus","reward","prize","life","damage",
  "energy","magic","fire","ice","water","earth","air","boss","enemy","friend",
  "ally","party","quest","task","mission","story","world","stage","zone","room",
  "gate","door","chest","shop","trade","build","craft","upgrade","unlock","save",
  "load","retry","checkpoint","victory","defeat","rank","badge","title","skin",
  "emote","avatar","control","screen","sound","music","voice","text","chat",
  "signal","button","icon","cursor","click","tap","press","hold","drag","drop",
  "slide","zoom","view","camera","angle","light","shadow","color","pixel","sprite",
  "model","shape","size","scale","path","road","bridge","tower","wall","floor",
  "roof","stairs","ladder","portal","spawn","respawn","base","camp","home","safe",
  "danger","trap","puzzle","riddle","logic","pattern","matchup","random","chance",
  "luck","roll","dice","card","deck","hand","draw","shuffle","board","tile",
  "grid","slot","line","row","column","matchthree","combo","chain","streak","boost",
  "powerup","shield","heal","cure","buff","nerf","status","effect","cooldown",
  "charge","ammo","reload","aim","target","range","melee","ranged","cover","hide",
  "seek","chase","escape","capture","defend","attackers","defenders","teamwork",
  "solo","duo","group","crowd","lobby","queue","ready","waiting","connect",
  "disconnect","server","online","offline","local","remote","invite","join",
  "leave","kick","ban","host","guest","admin","settings","options","toggle",
  "slider","audio","video","graphics","quality","performance","smooth","lag",
  "delay","ping","frame","rate","update","patch","version","release","beta",
  "demo","trial","full","premium","free","locked","open","closed","hidden",
  "visible","secret","easter","rewarded","earned","lost","found","collect",
  "gather","harvest","farm","mine","dig","cut","chop","buildings","tools","parts",
  "pieces","materials","wood","stone","metal","iron","steel","crystal","gem",
  "diamond","ruby","sapphire","emerald","bag","pack","slotbag","inventory",
  "storage","bank","vault","cache","supply","dropoff","pickup","delivery","tradeoff",
  "market","price","cost","value","cheap","expensive","rare","common","epic",
  "legend","mythic","basic","advanced","expert","master","novice","easy","normal",
  "hard","extreme","casual","ranked","practice","training","tutorial","lesson",
  "hint","tip","guide","help","support","assist","revive","rescue","protect",
  "escort","follow","lead","command","order","signal","pinged","marked","tracked",
  "watch","guard","patrol","sneak","stealth","noise","alert","warning","dangerous",
  "safezone","boundary","limit","edge","corner","center","middle","side","left",
  "right","up","down","forward","backward","north","south","east","west","compass",
  "radar","scanner","sensor","vision","focus","zoomed","lockedon","unlocked",
  "progress","percent","bar","meter","counter","stack","queueing","cycle","loop",
  "repeat","reset","restart","continue","advance","retreat","fail","success",
  "complete","incomplete","ongoing","active","inactive","idle","busy","readyup",
  "spectate","viewer","replay","record","clip","highlight","share","stream",
  "broadcast","watcher","audience","scoreboard","leaderboard","stats","recorded",
  "history","profile","account","user","guestmode","signin","signout","password",
  "username","nickname","avataricon","custom","default","preset","randomized",
  "shuffleplay","sandbox","openworld","linear","pathway","checkpointed","branch",
  "choice","option","decision","ending","multiple","single","storyline","dialog",
  "textline","cutscene","scene","moment","event","trigger","script","logicgate",
  "condition","rule","limitless","finite","countdown","timerend","overtime",
  "sudden","deathmatch","arena","battle","skirmish","fight","brawl","duel","clash"
]

# Create lookup dictionary for O(1) word-to-index mapping
_word_to_index = {word: idx for idx, word in enumerate(seedlist)}

def rm_generatecode():
    """
    Generate a random room code in the format 'word1-word2-word3' using the seedlist.
    """
    _name = f"{random.choice(seedlist)}-{random.choice(seedlist)}-{random.choice(seedlist)}"
    return _name

def rm_codetohash(room_code):
    """
    Convert a room code (e.g., 'word1-word2-word3') to a reversible hash number.
    The hash is calculated as: index1 * (seedlist_len^2) + index2 * seedlist_len + index3
    """
    try:
        words = room_code.split('-')
        if len(words) != 3:
            raise ValueError("Room code must have exactly 3 words separated by hyphens")
        
        seedlist_len = len(seedlist)
        indices = []
        
        for word in words:
            if word not in _word_to_index:
                raise ValueError(f"Word '{word}' not found in seed list")
            indices.append(_word_to_index[word])
        
        # Convert to unique number: index1 * (len^2) + index2 * len + index3
        hash_value = indices[0] * (seedlist_len ** 2) + indices[1] * seedlist_len + indices[2]
        return hash_value
    
    except Exception as e:
        raise ValueError(f"Invalid room code format: {e}")

def rm_hashtocode(hash_value):
    """
    Convert a hash number back to the original room code.
    Reverses the calculation: hash = index1 * (len^2) + index2 * len + index3
    """
    try:
        seedlist_len = len(seedlist)
        
        # Extract indices from the hash
        index1 = hash_value // (seedlist_len ** 2)
        remainder = hash_value % (seedlist_len ** 2)
        index2 = remainder // seedlist_len
        index3 = remainder % seedlist_len
        
        # Validate indices are within range
        if index1 >= seedlist_len or index2 >= seedlist_len or index3 >= seedlist_len:
            raise ValueError("Hash value is out of valid range")
        
        # Reconstruct the room code
        room_code = f"{seedlist[index1]}-{seedlist[index2]}-{seedlist[index3]}"
        return room_code
    
    except Exception as e:
        raise ValueError(f"Invalid hash value: {e}")

def rm_generatecodewithhash():
    """
    Generate a room code and return both the code and its hash value.
    """
    code = rm_generatecode()
    hash_value = rm_codetohash(code)
    return {"code": code, "hash": hash_value}