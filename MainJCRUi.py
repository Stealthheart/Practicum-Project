from kivy import app
from kivy.config import Config
from kivy.lang import Builder

# Sets the config first
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

# helper files to modularize the code
import lessonLogic as lLogic

from random import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# loads kv file to control the design of the us
with open("uiDesignMain.kv", encoding='utf-8') as f:
    Builder.load_string(f.read())


# Main menu screen
class StartScreen(Screen):
    pass


# Lists the courses (Hira, Kata, Kanji)
class CourseScreen(Screen):
    pass


# View and select profiles for the different users
class ProfileScreen(Screen):
    pass


# Main screen manager to handle control of the different screens
class MyScreenManager(ScreenManager):
    pass


'''
    Hiragana Lesson Screen. This screen will display the hiragana lesson list when loaded in. It will also
    set the lesson info for the pre-lesson screen when a lesson is selected.
'''
class HiraganaLessonScreen(Screen):
    def __init__(self, **kwargs):
        super(HiraganaLessonScreen, self).__init__(**kwargs)
        self.flag = 0
        # self.add_buttons()

    def on_pre_enter(self):
        if self.flag == 0:
            lLogic.generateLessons(self, 0)
            self.flag = 1

    def testFunction(self, args):
        lLogic.setLesson(args.id, 0)
        print(args.id)
        self.manager.current = "priorToQuestions"

    pass


'''
    Katakana Lesson Screen. This screen will display the Katakana lesson list when loaded in. It will also
    set the lesson info for the pre-lesson screen when a lesson is selected.
'''
class KatakanaLessonScreen(Screen):
    def __init__(self, **kwargs):
        super(KatakanaLessonScreen, self).__init__(**kwargs)
        self.flag = 0
        # self.add_buttons()

    def on_pre_enter(self):
        if (self.flag == 0):
            lLogic.generateLessons(self, 1)
            self.flag = 1

    def testFunction(self, args):
        lLogic.setLesson(args.id, 1)
        print(args.id)
        self.manager.current = "priorToQuestions"

    pass


'''
    Kanji Lesson Screen. This screen will display the kanji lesson list when loaded in. It will also
    set the lesson info for the pre-lesson screen when a lesson is selected.
'''
class KanjiLessonScreen(Screen):

    def __init__(self, **kwargs):
        super(KanjiLessonScreen, self).__init__(**kwargs)
        self.flag = 0
        # self.add_buttons()

    def on_pre_enter(self):
        if (self.flag == 0):
            lLogic.generateLessons(self, 2)
            self.flag = 1

    def testFunction(self, args):
        lLogic.setLesson(args.id, 2)
        print(args.id)
        self.manager.current = "priorToQuestions"

    pass


'''
    This is the screen that is loaded prior to beginning a lesson. It will list the language used, the lesson number,
    the number of questions, the accuracy needed to unlock the next lesson, and will allow you to either start the
    lesson or return to the lesson list. It will also display a popup detailing the different characters that will
    be present within that lesson.
'''
class PriorToQuestionsScreen(Screen):
    def __init__(self, **kwargs):
        super(PriorToQuestionsScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        lLogic.setAttr(self)

    def displayPopup(self):
        popup = Popup(title='Characters To Know',
                      content=Label(font_name="fonts/meiryo.ttf",
                                    text="a: あ      ka: か\n"
                                         "i: い      ki: き\n"
                                         "u: う      ku: く\n"
                                         "e: え      ke: け\n"
                                         "o: お      ko: こ\n"),
                      size_hint=(None, None),
                      size=(400, 400))
        popup.open()

    def loadOriginalLessonList(self):
        self.manager.current = lLogic.getCurrLessonScreen()

    pass


# Main question screen and drawing ui
class QuestionScreen(Screen):
    pass


# shows overall results after a completed lesson
class ResultsScreen(Screen):
    pass


'''
    This widget is the drawing UI found on the question screen. It handles touch input and can clear the screen after
    submission and when a button is pressed.
'''
class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class ScreenManagerTestApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    ScreenManagerTestApp().run()
