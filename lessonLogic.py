from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import uiFileIOLibrary as io
from random import randrange

langTypes = ["Hiragana", "Katakana", "Kanji"]
lessonArr = []
arrLang = -1
currLesson = -1
currLang = -1
currQuestionNum = 1
correctQuestions = 0
totalQuestionNum = 10
questionArray = ["Write down the character for: 'a'", "Write down the character for: 'i'",
                 "Write down the character for: 'u'",
                 "Write down the character for: 'e'", "Write down the character for: 'o'",
                 "Write down the character for: 'ka'",
                 "Write down the character for: 'ki'", "Write down the character for: 'ku'",
                 "Write down the character for: 'ke'",
                 "Write down the character for: 'ko'"]
correctAnswer = 0

#region Lesson Methods
def generateLessons(lang):
    global lessonArr
    lessonArr = io.readJsonLessons(lang)
    return lessonArr


def setLesson(lessonNum, lang):
    global currLesson, currLang, arrLang, lessonArr
    if lang != currLang:
        repopulateLessonArray(lang)
    currLesson = int(lessonNum) - 1
    currLang = int(lang)
    arrLang = currLang

def repopulateLessonArray(lang):
    global lessonArr
    lessonArr = io.readJsonLessons(lang)

def getCurrentLessonNum():
    return currLesson

def loadNextLessonInfo():
    global currLesson, currQuestionNum
    currLesson += 1

def getCurrLessonTitle():
    return lessonArr[currLesson]

def areMoreLessons():
    if currLesson == len(lessonArr) - 1:
        return False
    return True

#endregion Lesson Methods

#region Question Methods
def resetQuestionCounters():
    global currQuestionNum, correctQuestions
    currQuestionNum = 1
    correctQuestions = 0

def getNextQuestion():
    return questionArray[currQuestionNum - 1]

def getCurrQuestionCount():
    return currQuestionNum

def incrementQuestionNum():
    global currQuestionNum
    currQuestionNum += 1

def getCorrectQuestionCount():
    return correctQuestions

def getTotalQuestionCount():
    return totalQuestionNum

#endregion Question Methods

#region Answer Methods

def checkAnswer(img):
    global correctQuestions, correctAnswer
    num = randrange(2)
    if num == 0:
        correctAnswer = 0
        correctQuestions += 1
    else:
        correctAnswer = 1

def retrieveResultString():
    return correctAnswer

#endregion Answer Methods


def getSelectedLanguage():
    return langTypes[currLang]