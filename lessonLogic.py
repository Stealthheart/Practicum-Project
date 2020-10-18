from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import uiFileIOLibrary as io

langTypes = ["Hiragana", "Katakana", "Kanji"]
lessonArr = []
arrLang = -1
currLesson = -1
currLang = -1
currQuestionNum = 1
correctQuestions = 0
totalQuestionNum = 10
questionArray = ["Write down the character for: 'a'", "Write down the character for: 'i'", "Write down the character for: 'u'",
                 "Write down the character for: 'e'", "Write down the character for: 'o'", "Write down the character for: 'ka'",
                 "Write down the character for: 'ki'", "Write down the character for: 'ku'", "Write down the character for: 'ke'",
                 "Write down the character for: 'ko'"]

def generateLessons(screen, lang):
    global lessonArr
    lessonArr = io.readJsonLessons(lang)

    layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))
    for i in range(len(lessonArr)):
        button = Button(text='Lesson ' + str(i + 1) + ": " + lessonArr[i],
                        id=str(i + 1),
                        size_hint=(None, None),
                        border = (20, 20, 20, 20),
                        size=(300, 60))
        button.bind(on_press=screen.testFunction)
        layout.add_widget(button)
    svLayout = ScrollView(size_hint=(1, None), size=(500, 550), do_scroll_x=False, do_scroll_y=True,
                          pos_hint={'center_x': .5, 'center_y': .5})
    svLayout.add_widget(layout)
    screen.add_widget(svLayout)

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

def setAttr(screen):
    global currQuestionNum
    currQuestionNum = 1
    screen.ids.lessonText.text = langTypes[currLang]
    screen.ids.lessonNum.text = "Lesson " + str(currLesson + 1)
    screen.ids.lessonTitle.text = lessonArr[currLesson]

def getCurrLessonScreen():
    if(currLang == 0):
        retStr = "hLessons"
    elif(currLang == 1):
        retStr = "kataLessons"
    else:
        retStr = "kanjiLessons"
    return retStr

def getNextQuestion(screen):
    global currQuestionNum
    if currQuestionNum == totalQuestionNum + 1:
        return False
    else:
        screen.ids.questionLabel.text = questionArray[currQuestionNum - 1]
        screen.ids.questionNum.text = "Q: " + str(currQuestionNum) + "/" + str(totalQuestionNum)
        currQuestionNum += 1
        return True

def getSelectedLanguage():
    return langTypes[currLang]

def getCurrentLessonNum():
    return currLesson

def loadNextLessonInfo():
    global currLesson, currQuestionNum
    currLesson += 1

def resetCurrLessonProg():
    global currQuestionNum
    currQuestionNum = 1

def getCurrLessonTitle():
    return lessonArr[currLesson]

def getCorrectQuestionCount():
    return correctQuestions

def getTotalQuestionCount():
    return totalQuestionNum
