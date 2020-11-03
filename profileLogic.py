profileNames = []
currProfInfo = []
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
    return db.getTotalHiraLessons(profName)[0]

def getTotalKataLessons(profName):
    return str(db.getTotalKataLessons(profName)[0])

def getTotalKanjiLessons(profName):
    return str(db.getTotalKanjiLessons(profName)[0])

def getHighestHiraLessons(profName):
    return db.getHighestHiraLessons(profName)[0]

def getHighestKataLessons(profName):
    return str(db.getHighestKataLessons(profName)[0])

def getHighestKanjiLessons(profName):
    return str(db.getHighestKanjiLessons(profName)[0])

def setProfileInfo(profName):
    global currProfInfo
    currProfInfo = []
    currProfInfo.append(profName)
    currProfInfo.append(getTotalHiraLessons(profName))
    currProfInfo.append(getTotalKataLessons(profName))
    currProfInfo.append(getTotalKanjiLessons(profName))
    currProfInfo.append(getHighestHiraLessons(profName))
    currProfInfo.append(getHighestKataLessons(profName))
    currProfInfo.append(getHighestKanjiLessons(profName))

def getCurrProfileName():
    return currProfInfo[0]

def incrementHighestLesson(lang):
    if lang == "Hiragana":
        currProfInfo[4] += 1
    elif lang == "Katakana":
        currProfInfo[5] += 1
    else:
        currProfInfo[6] += 1

    print("This is highest lesson completed now = ", currProfInfo[4])

def getProfileInfo(index):
    return currProfInfo[index]

def writeToDB():
    db.updateProfile(currProfInfo)

def incrementTotalLessons(lang):
    currProfInfo[lang + 1] += 1

