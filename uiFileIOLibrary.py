from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import json

hiraLessonTitles = []
kataLessonTitles = ["Vowels + K Lines", "S + T Lines", "N + H Lines", "M + Y Lines", "R + W + n Lines",
                    "V + K + K + T Lines", "N + H + M Lines", "Y + R + W + n Lines", "V, K, S, T, N, H Lines",
                    "M, Y, R, W, n Lines", "All Katakana"]

kanjiLessonTitles = ["Words 1", "Words 2", "Words 3"]


def generateLessons(screen, lang):
    lessonArr = readJsonLessons(lang)

    layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))
    for i in range(len(lessonArr)):
        button = Button(text='Lesson ' + str(i + 1) + ": " + lessonArr[i],
                        id=str(i + 1),
                        size_hint=(None, None),
                        size=(300, 60))
        button.bind(on_press=screen.testFunction)
        layout.add_widget(button)
    svLayout = ScrollView(size_hint=(1, None), size=(500, 550), do_scroll_x=False, do_scroll_y=True,
                          pos_hint={'center_x': .5, 'center_y': .5})
    svLayout.add_widget(layout)
    screen.add_widget(svLayout)

def readJsonLessons(lang):
    if(lang == 0):
        fileString = 'hiraLessons.txt'
    elif(lang == 1):
        fileString = 'kataLessons.txt'
    else:
        fileString = 'kanjiLessons.txt'

    with open(fileString, 'r') as json_file:
        lessonArray = json.load(json_file)

    return lessonArray


