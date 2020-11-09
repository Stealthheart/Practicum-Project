import database as db
from os import path

#region General Database Methods

'''
    Creates a database file
'''
def createDB():
    db.createDatabase()

'''
    Checks if the database exists
'''
def doesDatabaseExist():
    return path.exists('Database/profiles.db')

'''
    Saves the given profile info to the database
'''
def writeInfoToDB(profInfo):
    db.updateProfile(profInfo)

#endregion
#region Database Profile Methods
'''
    Returns true if the profile name doesn't exist in the database. False otherwise.
'''
def canCreateProfile(profName):
    if db.checkIfProfileExists(profName) == 0:
        return True
    return False

'''
    Creates a new profile with the given name
'''
def createNewProfile(profName):
    db.createProfile(profName)

'''
    Gets the appropriate profile info, and stores it into a list to return
'''
def getProfileList(profName):
    returnList = [profName,
                  getTotalHiraLessons(profName),
                  getTotalKataLessons(profName),
                  getTotalKanjiLessons(profName),
                  getHighestHiraLessons(profName),
                  getHighestKataLessons(profName),
                  getHighestKanjiLessons(profName),
                  1]

    return returnList

'''
    Gets the total hiragana lessons completed
'''
def getTotalHiraLessons(profName):
    return db.getTotalHiraLessons(profName)[0]

'''
    Gets the total katakana lessons completed
'''
def getTotalKataLessons(profName):
    return db.getTotalKataLessons(profName)[0]

'''
    Gets the total kanji lessons completed
'''
def getTotalKanjiLessons(profName):
    return db.getTotalKanjiLessons(profName)[0]

'''
    Gets the highest hiragana lesson completed
'''
def getHighestHiraLessons(profName):
    return db.getHighestHiraLessons(profName)[0]

'''
    Gets the highest katakana lesson completed
'''
def getHighestKataLessons(profName):
    return db.getHighestKataLessons(profName)[0]

'''
    Gets the highest kanji lesson completed
'''
def getHighestKanjiLessons(profName):
    return db.getHighestKanjiLessons(profName)[0]

'''
    Changes the given profile flag
'''
def profileSwapped(profName):
    db.profileSwapped(profName)

'''
    Returns the last selected profile.
'''
def getPreviouslySetProfile():
    return db.getLastUsedProfile()

'''
    Deletes the given profile
'''
def deleteCurrentProfile(profName):
    return db.deleteProfileFromDB(profName)

'''
    Checks if a profile was selected previously
'''
def checkForProfileSelectedPreviously():
    if db.getLastUsedProfile() is None:
        return False
    return True

'''
    Returns a list of all profile names
'''
def getProfileNameList():
    return db.getProfileNames()

'''
    Returns the number of profiles
'''
def getNumProfiles():
    return db.getNumberOfProfiles()
#endregion
