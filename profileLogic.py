profileNames = []
import database as db
'''
    This class will hold the profile logic.
    Uses hardcoded array currently. Implementation of profiles will come after lessons.
'''

def getProfileNameLength():
    return db.getNumberOfProfiles()

def getProfileName(index):
    global profileNames
    profileNames = db.getProfileNames()
    return str(profileNames[index][0])

def getTotalHiraLessons(profName):
    return str(db.getTotalHiraLessons(profName)[0])

def getTotalKataLessons(profName):
    return str(db.getTotalKataLessons(profName)[0])

def getTotalKanjiLessons(profName):
    return str(db.getTotalKanjiLessons(profName)[0])