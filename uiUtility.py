from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

import lessonLogic as lLogic
import profileLogic as pLogic

'''
    This class holds methods to assist the UI in displaying details grabbed from other files.
'''

#region Generation Methods
'''
    This method will generate the lesson lists given the screen and the language type.
    Lang: 0 = Hiragana, 1 = Katakana, 2 = Kanji.
    It will call a helper method in lesson logic since that is where lessons will be controlled.
'''
def generateLessonList(screen, lang):
    # Gets the lesson array
    lessonArr = lLogic.generateLessons(lang)

    #Creates a new layout for the lessons.
    layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))

    # Loops until we have covered every lesson in the array.
    for i in range(len(lessonArr)):
        # Create a new button with appropriate names and ids.
        button = Button(text='Lesson ' + str(i + 1) + ": " + lessonArr[i],
                        id=str(i + 1),
                        size_hint=(None, None),
                        border = (20, 20, 20, 20),
                        size=(300, 60))
        button.bind(on_press=screen.setLesson)
        layout.add_widget(button)

    # Creates a scrollable layout to hold the lessons.
    svLayout = ScrollView(size_hint=(1, None), size=(500, 550), do_scroll_x=False, do_scroll_y=True,
                          pos_hint={'center_x': .5, 'center_y': .5})

    # Adds grid layout to the scrollable layout, then the scrollable layout to the screen.
    svLayout.add_widget(layout)
    screen.add_widget(svLayout)

'''
    This method will generate the profile list. Retrieves each profile name from the profile logic.
'''
def generateProfileList(screen):
    # Creates a new layout for the profiles.
    layout = GridLayout(cols=1, spacing=15, size_hint=(None, None), padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))

    # Loops through the entire profile list
    for i in range(pLogic.getProfileNameLength()):
        #Creates new button for each element, naming and id'ing them appropriately.
        button = Button(text=pLogic.getProfileName(i),
                        id=pLogic.getProfileName(i),
                        size_hint=(None, None),
                        border=(20, 20, 20, 20),
                        size=(150, 40))
        button.bind(on_press=screen.selectProfile)
        layout.add_widget(button)

    # Creates a scrollable layout to hold the lessons.
    svLayout = ScrollView(size_hint=(None, None), size=(270, 250), do_scroll_x=False, do_scroll_y=True,
                          pos_hint={'center_x': .15, 'center_y': .55})

    # Adds grid layout to the scrollable layout, then the scrollable layout to the screen.
    svLayout.add_widget(layout)
    screen.add_widget(svLayout)

#endregion Generation Methods

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
