import lessonLogic as lLogic
import profileLogic as pLogic
import sqlite3

# Returns a string resembling the screen to swap
def getCurrLessonScreen():
    currLang = getSelectedLanguageName()
    if currLang == "Hiragana":
        retStr = "hLessons"
    elif currLang == "Katakana":
        retStr = "kataLessons"
    else:
        retStr = "kanjiLessons"
    return retStr

# Sets the attributes of the given screen to the appropriate items set in the lesson logic.
def setAttr(screen):
    screen.ids.lessonText.text = getSelectedLanguageName()
    screen.ids.lessonNum.text = "Lesson " + str(getCurrentLessonNum())
    screen.ids.lessonTitle.text = getCurrentLessonTitle()
    screen.ids.questionCount.text = str(getTotalQuestionCount()) + " Questions"
    lLogic.resetQuestionCounters()

# Returns a string depending on if the answer was correct.
def isAnswerCorrect():
    correct = lLogic.retrieveResultString()
    if correct == 0:
        return "Correct"
    else:
        return "Incorrect"

# Returns false if there are no more questions. True otherwise.
def getNextQuestion(screen):
    currQuestion = lLogic.getCurrQuestionCount()
    totalQuestions = lLogic.getTotalQuestionCount()
    if currQuestion == totalQuestions + 1:
        return False
    else:
        screen.ids.questionLabel.text = lLogic.getNextQuestion()
        screen.ids.questionNum.text = "Q: " + str(currQuestion) + "/" + str(totalQuestions)
        lLogic.incrementQuestionNum()
        return True

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

def setupNextLessonInfo():
    lLogic.loadNextLessonInfo()

def sendAnswer(answerImg):
    lLogic.checkAnswer(answerImg)

def setCurrLesson(lessonNum, lang):
    lLogic.setLesson(lessonNum, lang)
#endregion Helper Methods

def getProfileNameLength():
    return pLogic.getProfileNameLength()

def getProfileName(index):
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


def createDB():
    conn = sqlite3.connect('Database/test.db')
    print("Opened database successfully!")
    conn.execute('CREATE TABLE Profiles\n'
                 '        (id INTEGER PRIMARY KEY,\n'
                 '        name TEXT NOT NULL,\n'
                 '        hiragana_lessons_completed INT NOT NULL,\n'
                 '        katakana_lessons_completed INT NOT NULL,\n'
                 '        kanji_lessons_completed INT NOT NULL,\n'
                 '        highest_hiragana_lesson_completed INT NOT NULL,\n'
                 '        highest_katakana_lesson_completed INT NOT NULL,\n'
                 '        highest_kanji_lesson_completed INT NOT NULL,\n'
                 '        last INT NOT NULL);')
    print("Table created successfully!")
    conn.close()

def testDB():
    conn = sqlite3.connect('Database/test.db')
    '''conn.execute('INSERT INTO Profiles(name, hiragana_lessons_completed, katakana_lessons_completed, kanji_lessons_completed,'
                 'highest_hiragana_lesson_completed, highest_katakana_lesson_completed, highest_kanji_lesson_completed) VALUES ("Auto", 12, 21, 30, 9, 1, 1)')
    conn.execute(
        'INSERT INTO Profiles(name, hiragana_lessons_completed, katakana_lessons_completed, kanji_lessons_completed,'
                 'highest_hiragana_lesson_completed, highest_katakana_lesson_completed, highest_kanji_lesson_completed) VALUES ("Bots", 51, 25, 12, 5, 1, 1)')
    conn.commit()'''

    conn.close()

def getTotalHiraLessons(profName):
    return pLogic.getTotalHiraLessons(profName)

def getTotalKataLessons(profName):
    return pLogic.getTotalKataLessons(profName)

def getTotalKanjiLessons(profName):
    return pLogic.getTotalKanjiLessons(profName)

def getHighestKanjiLessons(profName):
    return pLogic.getHighestKanjiLessons(profName)

def getHighestKataLessons(profName):
    return pLogic.getHighestKataLessons(profName)

def getHighestHiraLessons(profName):
    return pLogic.getHighestHiraLessons(profName)

def setProfileInfo(profName):
    pLogic.setProfileInfo(profName)

def checkPerformance():
    if lLogic.unlockedNextLesson() and lLogic.getCurrentLessonNum() == pLogic.getProfileInfo(lLogic.getLangNumber() + 4):
        pLogic.incrementHighestLesson(lLogic.getSelectedLanguage())
    pLogic.incrementTotalLessons(lLogic.getLangNumber())

def getLangNum():
    return lLogic.getLangNumber()

def getProfileInfo(index):
    return pLogic.getProfileInfo(index)

def saveInformation():
    pLogic.writeToDB()

def createNewProfile(name):
    if pLogic.canCreateProfile(name):
        pLogic.createNewProfile(name)
        return True
    return False

def setProfileInfoOnStartup():
    pLogic.startUpProfileSet()

def deleteProfile():
    return pLogic.deleteCurrentProfile()

def clearProfileList():
    pLogic.nullList()

def isProfileSet():
    return pLogic.checkIfSelectedProfile()

def wasProfileSelectedPreviously():
    return pLogic.checkForProfileSelectedPreviously()
