from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import uiFileIOLibrary as io

langTypes = ["Hiragana", "Katakana", "Kanji"]
lessonArr = []
arrLang = -1
currLesson = -1
currLang = -1

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
    global currLesson, currLang, arrLang
    currLesson = int(lessonNum) - 1
    currLang = int(lang)
    arrLang = currLang

def setAttr(screen):
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