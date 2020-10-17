from kivy.config import Config
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ListProperty

# Sets the config first
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

# helper files to modularize the code
import lessonLogic as lLogic

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
        if self.flag == 0:
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

    def on_pre_enter(self):
        if self.flag == 0:
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


'''
    Question Screen. This screen controls the display of questions. It holds the drawing UI within itself. It will
    pass information along to the logic to retrieve and display the current and future questions. It also displays
    feedback to the user when they answer a question, detailing if the question was correct, what the AI perceived
    what was written, and what was expected.
'''
class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)
        showDrawingUiBorder(self)

    def on_pre_enter(self):
        lLogic.getNextQuestion(self)

    def getAnswerResult(self):
        return "Correct"

    def getUserAnswer(self):
        return "あ"

    def getCorrectAnswer(self):
        return "あ"

    def getNextQuestion(self):
        lessContinues = lLogic.getNextQuestion(self)
        if not lessContinues:
            self.manager.current = 'results'
        else:
            self.ids.nextQBtn.disabled = True

    pass


# shows overall results after a completed lesson
class ResultsScreen(Screen):
    pass


clr = [1, 1, 1, 1]  # color array for paint widget
xs = 0  # holds the current x coordinate, used for moving the mouse
ys = 0  # holds the current y coordinate, used for moving the mouse
wide = 2  # holds the width of the line to be drawn
'''
    This widget is the drawing UI found on the question screen. It handles touch input and can clear the screen after
    submission and when a button is pressed.
'''
class MyPaintWidget(Widget):
    col = ListProperty(clr)

    def submitAnswer(self):
        self.export_to_png("image.jpg")

    def on_touch_down(self, touch):
        global xs, ys, wide
        if checkWithinCanvas(touch.x, touch.y):
            self.col = getClr()

            with self.canvas:
                Color(*self.col)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=wide)
                xs = touch.x
                ys = touch.y

    def on_touch_move(self, touch):
        global xs, ys, wide
        if checkWithinCanvas(touch.x, touch.y) and checkWithinCanvas(xs, ys):
            self.col = getClr()
            if checkWithinCanvas(xs, ys):
                touch.ud["line"].points += [touch.x, touch.y]


'''
    Helper method for the drawing UI. Returns the global color list. 
    Exists to help testing and quick modification.
'''
def getClr():
    return clr


'''
    Helper method for Question Screen and Drawing UI. Displays a white border to visualize how large the drawing
    UI is. (Might not be necessary)
'''
def showDrawingUiBorder(self):
    with self.canvas.after:
        col = [1, 1, 1, 1]
        Color(*col)
        Line(rectangle=(25, 225, 450, 375), width=5)


'''
    Helper method for the drawing UI. Checks if the current coordinates being drawn are within the bounds for the
    drawing UI.
'''
def checkWithinCanvas(x, y):
    if 25 < x < 475 and 225 < y < 600:
        return True


class ScreenManagerTestApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    ScreenManagerTestApp().run()
