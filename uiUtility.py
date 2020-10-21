from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

import lessonLogic as lLogic
import profileLogic as pLogic

def generateLessonList(screen, lang):
    lessonArr = lLogic.generateLessons(lang)

    layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))
    for i in range(len(lessonArr)):
        button = Button(text='Lesson ' + str(i + 1) + ": " + lessonArr[i],
                        id=str(i + 1),
                        size_hint=(None, None),
                        border = (20, 20, 20, 20),
                        size=(300, 60))
        button.bind(on_press=screen.setLesson)
        layout.add_widget(button)
    svLayout = ScrollView(size_hint=(1, None), size=(500, 550), do_scroll_x=False, do_scroll_y=True,
                          pos_hint={'center_x': .5, 'center_y': .5})
    svLayout.add_widget(layout)
    screen.add_widget(svLayout)

def generateProfileList(screen):
    layout = GridLayout(cols=1, spacing=15, size_hint=(None, None), padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))
    for i in range(pLogic.getProfileNameLength()):
        button = Button(text=pLogic.getProfileName(i),
                        id=pLogic.getProfileName(i),
                        size_hint=(None, None),
                        border=(20, 20, 20, 20),
                        size=(150, 40))
        button.bind(on_press=screen.selectProfile)
        layout.add_widget(button)
    svLayout = ScrollView(size_hint=(None, None), size=(270, 250), do_scroll_x=False, do_scroll_y=True,
                          pos_hint={'center_x': .15, 'center_y': .55})
    svLayout.add_widget(layout)
    screen.add_widget(svLayout)

def getCurrLessonScreen():
    currLang = getSelectedLanguageName()
    if currLang == "Hiragana":
        retStr = "hLessons"
    elif currLang == "Katakana":
        retStr = "kataLessons"
    else:
        retStr = "kanjiLessons"
    return retStr

def setAttr(screen):
    screen.ids.lessonText.text = getSelectedLanguageName()
    screen.ids.lessonNum.text = "Lesson " + str(getCurrentLessonNum())
    screen.ids.lessonTitle.text = getCurrentLessonTitle()
    lLogic.resetQuestionCounters()

def isAnswerCorrect():
    correct = lLogic.retrieveResultString()
    if correct == 0:
        return "Correct"
    else:
        return "Incorrect"

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

def setupNextLessonInfo():
    lLogic.loadNextLessonInfo()

def sendAnswer(answerImg):
    lLogic.checkAnswer(answerImg)

def setCurrLesson(lessonNum, lang):
    lLogic.setLesson(lessonNum, lang)
