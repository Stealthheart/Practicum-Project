from kivy import app
from kivy.config import Config

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

import uiFileIOLibrary as io

from random import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class StartScreen(Screen):
    pass


class CourseScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


class HiraganaLessonScreen(Screen):
    def __init__(self, **kwargs):
        super(HiraganaLessonScreen, self).__init__(**kwargs)
        self.add_buttons()

    def add_buttons(self):
        io.generateLessons(self, 0)

    def testFunction(self, args):
        print("Hello from Hiragana")
        self.manager.current = "results"

    pass


class KatakanaLessonScreen(Screen):
    def __init__(self, **kwargs):
        super(KatakanaLessonScreen, self).__init__(**kwargs)
        self.add_buttons()

    def add_buttons(self):
        io.generateLessons(self, 1)

    def testFunction(self, args):
        print("Hello from Katakana")
        self.manager.current = "results"

    pass


class KanjiLessonScreen(Screen):

    def __init__(self, **kwargs):
        super(KanjiLessonScreen, self).__init__(**kwargs)
        self.add_buttons()

    def add_buttons(self):
        io.generateLessons(self, 2)

    def testFunction(self, args):
        print("Hello from Kanji")
        self.manager.current = "results"
    pass


class PriorToQuestionsScreen(Screen):
    pass


class QuestionScreen(Screen):
    pass


class ResultsScreen(Screen):
    pass


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
