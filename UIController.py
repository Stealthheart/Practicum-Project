import lessonLogic as lLogic
import profileLogic as pLogic
import databaseController as dataLogic

# Returns a string depending on if the answer was correct.
def isAnswerCorrect():
    correct = lLogic.retrieveResultString()
    if correct == 0:
        return "Correct"
    else:
        return "Incorrect"

# Returns false if there are no more questions. True otherwise.
def getNextQuestion():
    return lLogic.getNextQuestion()

def incrementQuestionNum():
    lLogic.incrementQuestionNum()

#region Helper Methods
def getCorrectAnswer():
    return lLogic.getCorrectAnswer()

def checkIfMoreLessons():
    return lLogic.areMoreLessons()

def getSelectedLanguageName():
    return lLogic.getSelectedLanguage()

def getCurrentLessonNum():
    return lLogic.getCurrentLessonNum() + 1

def getCurrentLessonTitle():
    return lLogic.getCurrLessonTitle()

def getCorrectQuestionCount():
    return lLogic.getCorrectQuestionCount()

def getTotalQuestionCount():
    return lLogic.getTotalQuestionCount()

def getCurrQuestionCount():
    return lLogic.getCurrQuestionCount()

def resetQuestionCounters():
    lLogic.resetQuestionCounters()

def setupNextLessonInfo():
    lLogic.loadNextLessonInfo()

def sendAnswer(answerImg):
    lLogic.checkAnswer(answerImg)

def setCurrLesson(lessonNum, lang):
    lLogic.setLesson(lessonNum, lang)
#endregion Helper Methods

def getProfileNameLength():
    return dataLogic.getNumProfiles()

def getProfileName(index):
    pLogic.setProfileNames(dataLogic.getProfileNameList())
    return pLogic.getProfileName(index)

def generateLessons(lang):
    return lLogic.generateLessons(lang)

def removeImgList():
    lLogic.deleteImgList()

def getImgList():
    return lLogic.getImagePaths()

def getLanguageSize():
    sizeList = [120, 128]
    if getSelectedLanguageName() == "Kanji":
        sizeList[0] = 60
        sizeList[1] = 256
    return sizeList

def getTotalHiraLessons(profName):
    return dataLogic.getTotalHiraLessons(profName)

def getTotalKataLessons(profName):
    return dataLogic.getTotalKataLessons(profName)

def getTotalKanjiLessons(profName):
    return dataLogic.getTotalKanjiLessons(profName)

def getHighestKanjiLessons(profName):
    return dataLogic.getHighestKanjiLessons(profName)

def getHighestKataLessons(profName):
    return dataLogic.getHighestKataLessons(profName)

def getHighestHiraLessons(profName):
    return dataLogic.getHighestHiraLessons(profName)

def setProfileInfo(profName):
    if pLogic.isProfileSet():
        dataLogic.profileSwapped(pLogic.getProfileInfo(0))
    profInfo = dataLogic.getProfileList(profName)
    pLogic.setProfileInfo(profInfo)
    dataLogic.writeInfoToDB(pLogic.getProfileList())

def checkPerformance():
    if lLogic.unlockedNextLesson() and lLogic.getCurrentLessonNum() == pLogic.getProfileInfo(lLogic.getLangNumber() + 4):
        pLogic.incrementHighestLesson(lLogic.getSelectedLanguage())
    pLogic.incrementTotalLessons(lLogic.getLangNumber())

def getLangNum():
    return lLogic.getLangNumber()

def getProfileInfo(index):
    return pLogic.getProfileInfo(index)

def saveInformation():
    profInfo = pLogic.getProfileList()
    dataLogic.writeInfoToDB(profInfo)

def createNewProfile(name):
    if dataLogic.canCreateProfile(name):
        dataLogic.createNewProfile(name)
        return True
    return False

def setProfileInfoOnStartup():
    prevProf = dataLogic.wasProfileSetPreviously()
    if prevProf is None:
        return
    setProfileInfo(prevProf)

def deleteProfile():
    return dataLogic.deleteCurrentProfile(pLogic.getProfileInfo(0))

def clearProfileList():
    pLogic.nullList()

def isProfileSet():
    return pLogic.checkIfSelectedProfile()

def wasProfileSelectedPreviously():
    return dataLogic.checkForProfileSelectedPreviously()

#region Database Methods

def createDB():
    dataLogic.createDB()

def doesDatabaseExist():
    return dataLogic.doesDatabaseExist()

#endregion
