from kivy.config import Config
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
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

# helper file to modularize the code
import uiUtility as uiLogic

# loads kv file to control the design of the us
with open("uiDesignMain.kv", encoding='utf-8') as f:
    Builder.load_string(f.read())

# Main menu screen
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
    pass

# Lists the courses (Hira, Kata, Kanji)
class CourseScreen(Screen):
    def __init__(self, **kwargs):
        super(CourseScreen, self).__init__(**kwargs)
    pass

'''
    This screen holds the profile creation, selection, and deletion. Not yet fully implemented.
'''
class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.flag = 0

    # Generates the profile list prior to entering
    def on_pre_enter(self, *args):
        if self.flag == 0:
            uiLogic.generateProfileList(self)
            self.flag = 1

    # Change the selected profile.
    def selectProfile(self, args):
        print(args.id)
    pass

class ProfilePopup(RelativeLayout):
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

    # Generates the lesson list prior to entering the screen. Only will run once.
    def on_pre_enter(self):
        if self.flag == 0:
            uiLogic.generateLessonList(self, 0)
            self.flag = 1

    # Loads the selected lesson
    def setLesson(self, args):
        uiLogic.setCurrLesson(args.id, 0)
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

    #Generates the lesson list prior to entering the screen. Only will run once.
    def on_pre_enter(self):
        if self.flag == 0:
            uiLogic.generateLessonList(self, 1)
            self.flag = 1

    # Loads the selected lesson
    def setLesson(self, args):
        uiLogic.setCurrLesson(args.id, 1)
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

    # Generates the lesson list prior to entering the screen. Only will run once.
    def on_pre_enter(self):
        if self.flag == 0:
            uiLogic.generateLessonList(self, 2)
            self.flag = 1

    # Loads the selected lesson
    def setLesson(self, args):
        uiLogic.setCurrLesson(args.id, 2)
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

    # Sets the information of the screen to the appropriate lesson info prior to entering
    def on_pre_enter(self, *args):
        uiLogic.setAttr(self)

    # Displays the help popup. Will be changed with lesson implementation.
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

    # Loads the lesson list we came from if button is pressed
    def loadOriginalLessonList(self):
        self.manager.current = uiLogic.getCurrLessonScreen()

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

    # Loads the question information prior to entering. Also disables the next question button.
    def on_pre_enter(self):
        uiLogic.getNextQuestion(self)
        self.ids.nextQBtn.disabled = True

    # Will send the answer to the logic to determine if it is correct.
    def getAnswerResult(self):
        return uiLogic.isAnswerCorrect()

    # This will retrieve the answer the AI determines
    def getUserAnswer(self):
        return "あ"

    # This will retrieve the correct answer stored in the question
    def getCorrectAnswer(self):
        return "あ"

    # Retrieves the next question. Will display the results screen if no more remain.
    def getNextQuestion(self):
        lessContinues = uiLogic.getNextQuestion(self)
        if not lessContinues:
            self.manager.current = 'results'

    pass


'''
    This class will display the result screen after completing a lesson. The screen will display the lesson number,
    title, language type, accuracy, correct question count, total question count, and a message detailing if you
    unlocked the next lesson. Also contains buttons to go back to lesson list, immediately move to the next lesson,
    or to go back to the main menu.
'''
class ResultsScreen(Screen):

    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

    # Loads all relevant information prior to entering the screen.
    def on_pre_enter(self, *args):
        # Stores percentage value for repeated use.
        percentage = 100 * (float(uiLogic.getCorrectQuestionCount()) / float(uiLogic.getTotalQuestionCount()))

        # Stores correct information to display in the relevant fields.
        self.ids.resCurrLessonLang.text = uiLogic.getSelectedLanguageName()
        self.ids.resCurrLessonNum.text = "Lesson " + str(uiLogic.getCurrentLessonNum())
        self.ids.resCurrLessonTitle.text = uiLogic.getCurrentLessonTitle()
        self.ids.resTotalCorrect.text = str(uiLogic.getCorrectQuestionCount()) + "/" + str(uiLogic.getTotalQuestionCount()) + " correct"
        self.ids.resAccuracy.text = "Accuracy: " + str(percentage) + "%"

        # Displays a different message depending on if you passed the lesson or not.
        if percentage >= 80:
            self.ids.resLessonUnlockLbl.text = "You have unlocked the next lesson!"
        else:
            self.ids.resLessonUnlockLbl.text = "Try again for 80% to unlock the next lesson."

        # disables next lesson button if there are no more lessons after the one completed.
        if not uiLogic.checkIfMoreLessons():
            self.ids.resNextLessonBtn.disabled = True

    # Loads the next lesson immediately
    def loadNextLesson(self):
        uiLogic.setupNextLessonInfo()
        self.manager.current = 'priorToQuestions'

    # Loads the lesson list of the language selected.
    def loadLessonList(self):
        self.manager.current = uiLogic.getCurrLessonScreen()

    pass


color = [1, 1, 1, 1]  # color array for paint widget
xCoord = 0  # holds the current x coordinate, used for moving the mouse
yCoord = 0  # holds the current y coordinate, used for moving the mouse
wide = 2  # holds the width of the line to be drawn
'''
    This widget is the drawing UI found on the question screen. It handles touch input and can clear the screen after
    submission and when a button is pressed.
'''
class MyPaintWidget(Widget):
    # creates a new property for the widget
    col = ListProperty(color)

    # Stores the drawn answer into a jpg, then passes it to the logic to check against the AI.
    def submitAnswer(self):
        self.export_to_png("image.jpg")
        image = open('image.jpg')
        uiLogic.sendAnswer(image)

    # Captures the x and y coordinates when the user clicks or presses down on the drawing canvas
    def on_touch_down(self, touch):
        global xCoord, yCoord, wide

        # Determines if thr coordinates are within the canvas.
        if checkWithinCanvas(touch.x, touch.y):

            # If so, the line is allowed to be drawn
            with self.canvas:
                Color(*self.col)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=wide)
                xCoord = touch.x
                yCoord = touch.y

    # Captures the movement of the user, and draws the line if we are within the canvas.
    def on_touch_move(self, touch):
        global xCoord, yCoord, wide
        if checkWithinCanvas(touch.x, touch.y) and checkWithinCanvas(xCoord, yCoord):
            touch.ud["line"].points += [touch.x, touch.y]

'''
    Helper method for the drawing UI. Checks if the current coordinates being drawn are within the bounds for the
    drawing UI. The canvas begins at x = 25, and extends to x = 475. The y-coordinates begin at 225, and extends to
    600.
'''
def checkWithinCanvas(x, y):
    if 25 < x < 475 and 225 < y < 600:
        return True

# Driver method
class ScreenManagerTestApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    ScreenManagerTestApp().run()
