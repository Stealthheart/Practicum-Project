"""
    This class will hold the profile logic.
    Uses hardcoded array currently. Implementation of profiles will come after lessons.
"""

profileNames = []
currProfInfo = []

def getProfileName(index):
    return str(profileNames[index][0])

def setProfileNames(nameList):
    global profileNames
    profileNames = nameList

def setProfileInfo(profList):
    global currProfInfo
    currProfInfo = profList

def getCurrProfileName():
    return currProfInfo[0]

def incrementHighestLesson(lang):
    if lang == "Hiragana":
        currProfInfo[4] += 1
    elif lang == "Katakana":
        currProfInfo[5] += 1
    else:
        currProfInfo[6] += 1

def getProfileInfo(index):
    return currProfInfo[index]

def incrementTotalLessons(lang):
    currProfInfo[lang + 1] += 1

def nullList():
    global currProfInfo
    currProfInfo = []

def checkIfSelectedProfile():
    if currProfInfo == []:
        return False
    return True

def getProfileList():
    return currProfInfo

def isProfileSet():
    if currProfInfo:
        return True
    return False

