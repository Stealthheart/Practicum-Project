import database as db
from os import path

def createDB():
    db.createDatabase()

def doesDatabaseExist():
    return path.exists('Database/test.db')

def writeInfoToDB(profInfo):
    db.updateProfile(profInfo)

def canCreateProfile(profName):
    if db.checkIfProfileExists(profName) == 0:
        return True
    return False

def createNewProfile(profName):
    db.createProfile(profName)

def getProfileList(profName):
    returnList = [profName, getTotalHiraLessons(profName),
                  getTotalKataLessons(profName),
                  getTotalKanjiLessons(profName),
                  getHighestHiraLessons(profName),
                  getHighestKataLessons(profName),
                  getHighestKanjiLessons(profName),
                  1]

    return returnList

def getTotalHiraLessons(profName):
    return db.getTotalHiraLessons(profName)[0]

def getTotalKataLessons(profName):
    return db.getTotalKataLessons(profName)[0]

def getTotalKanjiLessons(profName):
    return db.getTotalKanjiLessons(profName)[0]

def getHighestHiraLessons(profName):
    return db.getHighestHiraLessons(profName)[0]

def getHighestKataLessons(profName):
    return db.getHighestKataLessons(profName)[0]

def getHighestKanjiLessons(profName):
    return db.getHighestKanjiLessons(profName)[0]

def profileSwapped(profName):
    db.profileSwapped(profName)

def wasProfileSetPreviously():
    return db.getLastUsedProfile()

def deleteCurrentProfile(profName):
    return db.deleteProfileFromDB(profName)

def checkForProfileSelectedPreviously():
    if db.getLastUsedProfile() is None:
        return False
    return True

def getProfileNameList():
    return db.getProfileNames()

def getNumProfiles():
    return db.getNumberOfProfiles()
