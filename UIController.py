import lessonLogic as lLogic
import profileLogic as pLogic

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