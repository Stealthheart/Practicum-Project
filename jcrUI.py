import os

from kivy.config import Config
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, DictProperty

# Sets the config first
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

# helper file to modularize the code
import UIController as uiLogic

# loads kv file to control the design of the us
with open("uiDesignMain.kv", encoding='utf-8') as f:
    Builder.load_string(f.read())

# Main menu screen
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

    def loadCourseScreen(self):
        changeScreen(self, 'course')

    def loadProfileScreen(self):
        changeScreen(self, 'profiles')

    pass

# Lists the courses (Hira, Kata, Kanji)
class CourseScreen(Screen):
    def __init__(self, **kwargs):
        super(CourseScreen, self).__init__(**kwargs)

    # Loads the lesson UI depending on lang.
    def loadLessonList(self, lang):
        if lang == 0:
            changeScreen(self, 'hLessons')
        elif lang == 1:
            changeScreen(self, 'kataLessons')
        else:
            changeScreen(self, 'kanjiLessons')

    # Loads the main menu screen UI
    def backToStart(self):
        changeScreen(self, 'start')

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
            generateProfileList(self)
            self.flag = 1

    # Change the selected profile.
    def selectProfile(self, args):
        print(args.profName)

    # Loads the main menu screen UI
    def backToStart(self):
        changeScreen(self, 'start')

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
            generateLessonList(self, 0)
            self.flag = 1

    # Loads the selected lesson
    def setLesson(self, args):
        uiLogic.setCurrLesson(args.lessonNum, 0)
        print("Hi " + args.lessonNum)
        self.manager.current = "priorToQuestions"

    # Loads the course screen UI
    def backToCourse(self):
        changeScreen(self, 'course')

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
            generateLessonList(self, 1)
            self.flag = 1

    # Loads the selected lesson
    def setLesson(self, args):
        uiLogic.setCurrLesson(args.lessonNum, 1)
        print(args.lessonNum)
        self.manager.current = "priorToQuestions"

    # Loads the course screen UI
    def backToCourse(self):
        changeScreen(self, 'course')

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
            generateLessonList(self, 2)
            self.flag = 1

    # Loads the selected lesson
    def setLesson(self, args):
        uiLogic.setCurrLesson(args.lessonNum, 2)
        print(args.lessonNum)
        self.manager.current = "priorToQuestions"

    # Loads the course screen UI
    def backToCourse(self):
        changeScreen(self, 'course')

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
        lessonNum = str(uiLogic.getCurrentLessonNum())
        charList = uiLogic.getImgList()
        layout_popup = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[120,0,0,0])
        layout_popup.bind(minimum_height=layout_popup.setter('height'))
        path = "Images/hiraganaLessonImgs/Lesson" + lessonNum
        for char in charList:
            img1 = Image(source=path + "/so" + char + ".png", size_hint=(None, None), size=(128, 128))
            layout_popup.add_widget(img1)

        root = ScrollView(size_hint=(None, None), size=(375,425))
        root.add_widget(layout_popup)
        popup = Popup(title='Characters To Know', content=root, size=(400,500), size_hint=(None, None))
        popup.open()

    # Loads the lesson list we came from if button is pressed
    def loadOriginalLessonList(self):
        self.manager.current = uiLogic.getCurrLessonScreen()

    # Loads the question UI screen
    def startLesson(self):
        uiLogic.removeImgList()
        changeScreen(self, 'question')

    # Loads the main menu UI screen
    def backToMain(self):
        changeScreen(self, 'start')

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

    # Submits the drawing for checking against the AI.
    def submitDrawing(self):
        self.ids.submitBtn.disabled = True
        self.ids.drawingCanvas.submitAnswer()
        self.ids.correctAns.text = self.getAnswerResult()
        self.ids.userAns.text = "You wrote: " + self.getUserAnswer()
        self.ids.trueAns.text = "Correct Answer: " + self.getCorrectAnswer()
        self.ids.nextQBtn.disabled = False

    # Clears the screen and reads in the next question
    def nextQuestionBtn(self):
        self.resetQuestionScreen()
        self.getNextQuestion()

    # Will send the answer to the logic to determine if it is correct.
    def getAnswerResult(self):
        return uiLogic.isAnswerCorrect()

    # This will retrieve the answer the AI determines
    def getUserAnswer(self):
        return "あ"

    # This will retrieve the correct answer stored in the question
    def getCorrectAnswer(self):
        return uiLogic.getCorrectAnswer()

    # Retrieves the next question. Will display the results screen if no more remain.
    def getNextQuestion(self):
        lessContinues = uiLogic.getNextQuestion(self)
        if not lessContinues:
            self.manager.current = 'results'

    # Resets the question screen to initial state if lesson is left or user is ready for the next question
    def resetQuestionScreen(self):
        self.ids.drawingCanvas.clearCanvas()
        self.ids.correctAns.text = ""
        self.ids.userAns.text = ""
        self.ids.trueAns.text = ""
        self.ids.submitBtn.disabled = False
        self.ids.nextQBtn.disabled = True

    # Loads the course screen after resetting the information for the question.
    def backToCourses(self):
        self.resetQuestionScreen()
        changeScreen(self, 'course')

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
        self.showQuestionInfo()
        self.displayPerformance()

        # disables next lesson button if there are no more lessons after the one completed.
        if not uiLogic.checkIfMoreLessons():
            self.ids.resNextLessonBtn.disabled = True

        # Displays information regarding to the lesson and question counts.

    def showQuestionInfo(self):
        # Stores correct information to display in the relevant fields.
        self.ids.resCurrLessonLang.text = uiLogic.getSelectedLanguageName()
        self.ids.resCurrLessonNum.text = "Lesson " + str(uiLogic.getCurrentLessonNum())
        self.ids.resCurrLessonTitle.text = uiLogic.getCurrentLessonTitle()
        self.ids.resTotalCorrect.text = str(uiLogic.getCorrectQuestionCount()) + "/" + \
                                        str(uiLogic.getTotalQuestionCount()) + " correct"

        # Displays accuracy and info text detailing if the next lesson has been unlocked.

    def displayPerformance(self):
        # Stores percentage value for repeated use.
        percentage = 100 * (float(uiLogic.getCorrectQuestionCount()) / float(uiLogic.getTotalQuestionCount()))
        self.ids.resAccuracy.text = "Accuracy: " + str(percentage) + "%"

        # Displays a different message depending on if you passed the lesson or not.
        if percentage >= 80:
            self.ids.resLessonUnlockLbl.text = "You have unlocked the next lesson!"
        else:
            self.ids.resLessonUnlockLbl.text = "Try again for 80% to unlock the next lesson."

        # Loads the next lesson immediately

    def loadNextLesson(self):
        uiLogic.setupNextLessonInfo()
        changeScreen(self, 'priorToQuestions')

        # Loads the lesson list of the language selected.

    def loadLessonList(self):
        changeScreen(self, uiLogic.getCurrLessonScreen())

        # Loads the start screen of the app

    def backToMain(self):
        changeScreen(self, 'start')

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

    def clearCanvas(self):
        self.canvas.clear()

'''
    Helper method for the drawing UI. Checks if the current coordinates being drawn are within the bounds for the
    drawing UI. The canvas begins at x = 25, and extends to x = 475. The y-coordinates begin at 225, and extends to
    600.
'''
def checkWithinCanvas(x, y):
    if 25 < x < 475 and 225 < y < 600:
        return True

'''
    This method will generate the lesson lists given the screen and the language type.
    Lang: 0 = Hiragana, 1 = Katakana, 2 = Kanji.
    It will call a helper method in lesson logic since that is where lessons will be controlled.
'''
def generateLessonList(screen, lang):
    # Gets the lesson array
    lessonArr = uiLogic.generateLessons(lang)

    # Creates a new layout for the lessons.
    layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))

    # Loops until we have covered every lesson in the array.
    for i in range(len(lessonArr)):
        # Create a new button with appropriate names and ids.
        button = Button(text='Lesson ' + str(i + 1) + ": " + lessonArr[i],
                        size_hint=(None, None),
                        border=(20, 20, 20, 20),
                        size=(300, 60))
        button.bind(on_press=screen.setLesson)
        button.lessonNum = str(i + 1)
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
    for i in range(uiLogic.getProfileNameLength()):
        # Creates new button for each element, naming and id'ing them appropriately.
        button = Button(text=uiLogic.getProfileName(i),
                        size_hint=(None, None),
                        border=(20, 20, 20, 20),
                        size=(150, 40))
        button.bind(on_press=screen.selectProfile)
        button.profName = uiLogic.getProfileName(i)
        layout.add_widget(button)

    # Creates a scrollable layout to hold the lessons.
    svLayout = ScrollView(size_hint=(None, None), size=(270, 250), do_scroll_x=False, do_scroll_y=True,
                          pos_hint={'center_x': .15, 'center_y': .55})

    # Adds grid layout to the scrollable layout, then the scrollable layout to the screen.
    svLayout.add_widget(layout)
    screen.add_widget(svLayout)

'''
    Helper method to change screens. Screen is the current screen we are in, and dest is the screen we load in next.
'''
def changeScreen(screen, dest):
    screen.manager.current = dest


# Driver method
class ScreenManagerTestApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    ScreenManagerTestApp().run()
