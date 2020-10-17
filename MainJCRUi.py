from kivy import app
from kivy.config import Config
from kivy.lang import Builder

# Sets the config first
from kivy.properties import ListProperty

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

# helper files to modularize the code
import lessonLogic as lLogic

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
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)
        self.flag = 0
        default(self)
    pass


# shows overall results after a completed lesson
class ResultsScreen(Screen):
    pass


clr=[1,1,1,1]
pre_clr=clr
xs=0
ys=0
wide=2
'''
    This widget is the drawing UI found on the question screen. It handles touch input and can clear the screen after
    submission and when a button is pressed.
'''
class MyPaintWidget(Widget):
    col = ListProperty(clr)
    def save(self):
        self.export_to_png("image.jpg")

    def on_touch_down(self, touch):
        # print "down"
        global xs, ys, wide
        press = 1
        if incanvasxy(touch.x, touch.y):
            self.col = retclr()
            if Widget.on_touch_down(self, touch):
                xs = touch.x
                ys = touch.y
                return True

            with self.canvas:
                Color(*self.col)
                # d = 30
                # Ellipse(pos=(touch.x - d / 2,touch.y - d / 2), size=(d,d))
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=wide)
                # if sline:
                xs = touch.x
                ys = touch.y

    def on_touch_move(self, touch):
        global xs, ys, wide
        if incanvasxy(touch.x, touch.y) and incanvasxy(xs, ys):
            self.col = retclr()
            if incanvasxy(xs, ys):
                touch.ud["line"].points += [touch.x, touch.y]

def retclr():
    return clr

def default (self):
    with self.canvas.after:
        col =[1,1,1,1]
        Color(*col)
        Line(rectangle=(25, 225, 450, 375),width=5)

def incanvasxy(x,y):
    if x > 25 and y > 225 and x < 475 and y < 600:
        return True

class ScreenManagerTestApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    ScreenManagerTestApp().run()
