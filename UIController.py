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


# noinspection SqlNoDataSourceInspection
def createDB():
    conn = sqlite3.connect('Database/test.db')
    print("Opened database successfully!")
    conn.execute('CREATE TABLE Profiles\n'
                 '        (ID INT PRIMARY KEY NOT NULL,\n'
                 '        NAME TEXT NOT NULL,\n'
                 '        HIRAGANA_LESSONS_COMPLETED INT NOT NULL,\n'
                 '        KATAKANA_LESSONS_COMPLETED INT NOT NULL,\n'
                 '        KANJI_LESSONS_COMPLETED INT NOT NULL);')
    print("Table created successfully!")
    conn.close()

# noinspection SqlNoDataSourceInspection
def testDB():
    conn = sqlite3.connect('Database/test.db')

    cursor = conn.execute("SELECT * FROM Profiles")
    for row in cursor:
        print("ID = ", row[0])
        print("NAME = ", row[1])
        print("HIRAGANA_LESSONS_COMPLETED = ", row[2])
        print("KATAKANA_LESSONS_COMPLETED = ", row[3])
        print("KANJI_LESSONS_COMPLETED = ", row[4])
    print("Selected * Successfully!")
    conn.close()

def getTotalHiraLessons(profName):
    return pLogic.getTotalHiraLessons(profName)

def getTotalKataLessons(profName):
    return pLogic.getTotalKataLessons(profName)

def getTotalKanjiLessons(profName):
    return pLogic.getTotalKanjiLessons(profName)


