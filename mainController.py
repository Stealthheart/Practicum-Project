import lessonLogic as lLogic
import profileLogic as pLogic
import databaseController as dataLogic

#region Language Methods
'''
    Returns Hiragana, Katakana, or Kanji depending on the selected language
'''
def getSelectedLanguageName():
    return lLogic.getSelectedLanguage()

'''
    Returns the internal language number used by the lesson logic. Used by the results UI.
'''
def getLangNum():
    return lLogic.getLangNumber()
#endregion
#region Lesson Methods

'''
    Returns the lesson number. 1 is added since lists are 0-indexed
'''
def getCurrentLessonNum():
    return lLogic.getCurrentLessonNum() + 1

'''
    Returns the title of the lessons held in the *lessons.txt file
'''
def getCurrentLessonTitle():
    return lLogic.getCurrLessonTitle()

'''
    Sets the information for the next lesson
'''
def setupNextLessonInfo():
    lLogic.loadNextLessonInfo()

'''
    Sets the current lesson number and the language type
'''
def setCurrLesson(lessonNum, lang):
    lLogic.setLesson(lessonNum, lang)

'''
     Returns a list of lesson titles for the UI to use.
'''
def generateLessons(lang):
    return lLogic.generateLessons(lang)

'''
    Checks if the performance in the lesson was enough to unlock the next lesson. We need to check if the current lesson
    we are finishing is the same as the highest completed. Otherwise, we don't care about the highest and just increment
    total lessons.
'''
def checkPerformance():
    if lLogic.unlockedNextLesson() and lLogic.getCurrentLessonNum() == pLogic.getProfileInfo(lLogic.getLangNumber() + 4):
        pLogic.incrementHighestLesson(lLogic.getSelectedLanguage())
    pLogic.incrementTotalLessons(lLogic.getLangNumber())

'''
    Check if there are more lessons beyond the current one we are doing
'''
def checkIfMoreLessons():
    return lLogic.areMoreLessons()

#endregion
#region Question Methods

'''
    Returns the number of questions answered correctly
'''
def getCorrectQuestionCount():
    return lLogic.getCorrectQuestionCount()

'''
    Returns the total amount of questions within the lesson
'''
def getTotalQuestionCount():
    return lLogic.getTotalQuestionCount()

'''
    Get the number of the current question we are on.
'''
def getCurrQuestionCount():
    return lLogic.getCurrQuestionCount()

'''
    Sets question counters back to the default values. (1, 0)
'''
def resetQuestionCounters():
    lLogic.resetQuestionCounters()

'''
    Returns false is there are no more questions to be asked. True otherwise.
'''

def getNextQuestion():
    return lLogic.getNextQuestion()

'''
    Increments the question counter by 1.
'''

def incrementQuestionNum():
    lLogic.incrementQuestionNum()

#endregion
#region Answer Methods
'''
    Sends the answer image to the logic to be checked against the AI
'''
def sendAnswer(answerImg):
    lLogic.checkAnswer(answerImg)

'''
    Returns a string resembling correctness after an answer is submitted
'''
def isAnswerCorrect():
    correct = lLogic.retrieveResultString()
    if correct == 0:
        return "Correct"
    else:
        return "Incorrect"

'''
    Get the correct answer string from the lesson file
'''
def getCorrectAnswer():
    return lLogic.getCorrectAnswer()

#endregion
#region Image Methods

'''
    Removes the image list from the lesson array
'''
def removeImgList():
    lLogic.deleteImgList()

'''
    Gets the image list from the lesson array to load in the image
'''
def getImgList():
    return lLogic.getImagePaths()

'''
    Returns the size of the image for the popup menu. It will default to 128, 128 unless it is Kanji, in which case the
    size is doubled. sizeList[0] is the padding for the GridLayout. sizeList[1] is the size of the image.
'''
def getLanguageSize():
    sizeList = [120, 128]
    if getSelectedLanguageName() == "Kanji":
        sizeList[0] = 60
        sizeList[1] = 256
    return sizeList

#endregion
#region Profile Methods

'''
    Handles setting the profile info. If the profile was already set, we will change it's flag in the DB back to 0. We
    also will store the profile info into pLogic, then write to DB to store the most recent profile used.
'''
def setProfileInfo(profName):
    if pLogic.isProfileSet():
        dataLogic.profileSwapped(pLogic.getProfileInfo(0))
    profInfo = dataLogic.getProfileList(profName)
    pLogic.setProfileInfo(profInfo)
    dataLogic.writeInfoToDB(pLogic.getProfileList())

'''
    Returns the chosen profile info from the profile list.
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
    return pLogic.getProfileInfo(index)

'''
    Writes the current profile information to the database. Only used by ResultsScreen
'''
def saveInformation():
    profInfo = pLogic.getProfileList()
    dataLogic.writeInfoToDB(profInfo)

'''
    Creates a new profile with the given name, assuming the name doesn't already exist in the DB.
'''
def createNewProfile(name):
    if dataLogic.canCreateProfile(name):
        dataLogic.createNewProfile(name)
        return True
    return False

'''
    Immediately loads the previously used profile (flag == 1) upon starting the app.
'''
def setProfileInfoOnStartup():
    prevProf = dataLogic.getPreviouslySetProfile()
    if prevProf is None:
        return
    setProfileInfo(prevProf)

'''
    Deletes a profile from the database. Profile to be deleted is always the selected profile.
'''
def deleteProfile():
    return dataLogic.deleteCurrentProfile(pLogic.getProfileInfo(0))

'''
    Resets the internal profile list
'''
def clearProfileList():
    pLogic.nullList()

'''
    Checks if there is a selected profile
'''
def isProfileSet():
    return pLogic.isProfileSet()

'''
    Check if a profile was selected at some point in the past.
'''
def wasProfileSelectedPreviously():
    return dataLogic.checkForProfileSelectedPreviously()

'''
    Gets the selected profile name, and sets the profile information in the profile logic
'''
def getProfileName(index):
    pLogic.setProfileNames(dataLogic.getProfileNameList())
    return pLogic.getProfileName(index)

#endregion
#region Database Methods
'''
    Creates a new database file if it doesn't exist
'''
def createDB():
    if not dataLogic.doesDatabaseExist():
        dataLogic.createDB()

'''
    Gets the total number of hiragana lessons from the database
'''
def getTotalHiraLessons(profName):
    return dataLogic.getTotalHiraLessons(profName)

'''
    Gets the total number of katakana lessons from the database
'''
def getTotalKataLessons(profName):
    return dataLogic.getTotalKataLessons(profName)

'''
    Gets the total number of kanji lessons from the database
'''
def getTotalKanjiLessons(profName):
    return dataLogic.getTotalKanjiLessons(profName)

'''
    Gets the number of the highest hiragana lesson completed from the database
'''
def getHighestKanjiLessons(profName):
    return dataLogic.getHighestKanjiLessons(profName)

'''
    Gets the number of the highest katakana lesson completed from the database
'''
def getHighestKataLessons(profName):
    return dataLogic.getHighestKataLessons(profName)

'''
    Gets the number of the highest kanji lesson completed from the database
'''
def getHighestHiraLessons(profName):
    return dataLogic.getHighestHiraLessons(profName)

'''
    Gets the number of profiles within the database file
'''
def getProfileNameLength():
    return dataLogic.getNumProfiles()

#endregion

def initializeAI():
    lLogic.initializeAI()

def getUserAnswer():
    return lLogic.getUserAnswer()
