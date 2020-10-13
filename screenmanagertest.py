from kivy import app
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

from random import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line

hiraLessonTitles = ["Vowels + K Lines", "S + T Lines", "N + H Lines", "M + Y Lines", "R + W + n Lines",
                    "V + K + K + T Lines", "N + H + M Lines", "Y + R + W + n Lines", "V, K, S, T, N, H Lines",
                    "M, Y, R, W, n Lines", "All Standard Hiragana", "Voiced Hiragana", "All Hiragana"]

kataLessonTitles = ["Vowels + K Lines", "S + T Lines", "N + H Lines", "M + Y Lines", "R + W + n Lines",
                    "V + K + K + T Lines", "N + H + M Lines", "Y + R + W + n Lines", "V, K, S, T, N, H Lines",
                    "M, Y, R, W, n Lines", "All Katakana"]

kanjiLessonTitles = ["Words 1", "Words 2", "Words 3"]


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
        layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(hiraLessonTitles)):
            button = Button(text='Lesson ' + str(i+1) + ": " + hiraLessonTitles[i],
                            id=str(i+1),
                            size_hint=(None, None),
                            size=(300, 60))
            button.bind(on_press=self.testFunction)
            layout.add_widget(button)
        svLayout = ScrollView(size_hint=(1, None), size=(500, 550), do_scroll_x=False, do_scroll_y=True,
                              pos_hint={'center_x': .5, 'center_y': .5})
        svLayout.add_widget(layout)
        self.add_widget(svLayout)

    def testFunction(self, args):
        print(args.id)
        self.manager.current = "results"

    pass


class KatakanaLessonScreen(Screen):
    def __init__(self, **kwargs):
        super(KatakanaLessonScreen, self).__init__(**kwargs)
        self.add_buttons()

    def add_buttons(self):
        layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(kataLessonTitles)):
            button = Button(text='Lesson ' + str(i+1) + ": " + kataLessonTitles[i],
                            id=str(i+1),
                            size_hint=(None, None),
                            size=(300, 60))
            button.bind(on_press=self.testFunction)
            layout.add_widget(button)
        svLayout = ScrollView(size_hint=(1, None), size=(500, 550), do_scroll_x=False, do_scroll_y=True,
                              pos_hint={'center_x': .5, 'center_y': .5})
        svLayout.add_widget(layout)
        self.add_widget(svLayout)

    def testFunction(self, args):
        print(args.id)
        self.manager.current = "results"

    pass


class KanjiLessonScreen(Screen):

    def __init__(self, **kwargs):
        super(KanjiLessonScreen, self).__init__(**kwargs)
        self.add_buttons()

    def add_buttons(self):
        layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(kanjiLessonTitles)):
            button = Button(text='Lesson ' + str(i+1) + ": " + kanjiLessonTitles[i],
                            id=str(i+1),
                            size_hint=(None, None),
                            size=(300, 60))
            button.bind(on_press=self.testFunction)
            layout.add_widget(button)
        svLayout = ScrollView(size_hint=(1, None), size=(500, 550), do_scroll_x=False, do_scroll_y=True,
                              pos_hint={'center_x': .5, 'center_y': .5})
        svLayout.add_widget(layout)
        self.add_widget(svLayout)

    def testFunction(self, args):
        print(args.id)
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
