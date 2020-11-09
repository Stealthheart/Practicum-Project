"""
    This class will hold the profile logic.
"""

profileNames = [] # holds every name in DB. Used to populate profile buttons.
currProfInfo = [] # holds the individual profile information for easy access.

'''
    Returns the given profile name. Used prior to selecting a profile only.
'''
def getProfileName(index):
    return str(profileNames[index][0])

'''
    Sets the profile names array to a list of all profile names.
'''
def setProfileNames(nameList):
    global profileNames
    profileNames = nameList

'''
    Stores the currently selected profile into a list to allow easier access.
'''
def setProfileInfo(profList):
    global currProfInfo
    currProfInfo = profList

'''
    Gets the current profile name
'''
def getCurrProfileName():
    return currProfInfo[0]

'''
    Increments the lesson counters if a highest lesson was completed.
'''
def incrementHighestLesson(lang):
    if lang == "Hiragana":
        currProfInfo[4] += 1
    elif lang == "Katakana":
        currProfInfo[5] += 1
    else:
        currProfInfo[6] += 1

'''
    Gets the profile info pertaining to the given index.
    0 -> Name
    1 -> Total Hiragana Lessons Completed
    2 -> Total Katakana Lessons Completed
    3 -> Total Kanji Lessons Completed
    4 -> Highest Hiragana Lesson Completed
    5 -> Highest Katakana Lesson Completed
    6 -> Highest Kanji Lesson Completed
    7 -> Previously selected profile.
'''
def getProfileInfo(index):
    return currProfInfo[index]

'''
    Increments the total lessons completed
'''
def incrementTotalLessons(lang):
    currProfInfo[lang + 1] += 1

'''
    Sets the current profile info to the empty list. Used primarily after profile deletion.
'''
def nullList():
    global currProfInfo
    currProfInfo = []

'''
    Returns the entire profile list. Only used for writing to DB.
'''
def getProfileList():
    return currProfInfo

'''
    Checks if a profile has been selected.
'''
def isProfileSet():
    if currProfInfo:
        return True
    return False

