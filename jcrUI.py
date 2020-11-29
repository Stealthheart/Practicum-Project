from kivy.config import Config
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, Clock
from PIL import Image as pilImg
from PIL import ImageOps as opsImg


# Sets the config first
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

# helper file to modularize the code
import mainController as cont

# loads kv file to control the design of the us
with open("uiDesignMain.kv", encoding='utf-8') as f:
    Builder.load_string(f.read())

'''
    This screen is where the app will first load. It will dynamically load the profile name and generate the
    course lessons whenever the screen is left. 
'''
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        # Creates the database file if it is missing
        cont.createDB()

        # Immediately loads a profile if one was ever selected previously
        cont.setProfileInfoOnStartup()

        # Controls the generation of lessons
        self.flag = 0

    # Calls a helper method when the screen is entered to show the currently selected profile.
    def on_enter(self, *args):
        if len(self.ids) == 0:
            Clock.schedule_once(self.setName)
        else:
            self.setName()

    # Generates the lessons whenever the screen is changed. Only runs 1 time.
    def on_leave(self):
        if self.flag == 0:
            self.manager.get_screen('hLessons').generateLessons()
            self.manager.get_screen('kataLessons').generateLessons()
            self.manager.get_screen('kanjiLessons').generateLessons()
            self.flag = 1

    # Loads the course selection screen
    def loadCourseScreen(self):
        changeScreen(self, 'course')

    # Loads the profile selection screen
    def loadProfileScreen(self):
        changeScreen(self, 'profiles')

    # Sets the profile name on the start screen
    def setName(self, *args):
        if cont.isProfileSet():
            self.ids.currSelectedProf.text = "Hi, " + cont.getProfileInfo(0)

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
    This screen holds most of the profile information. It displays the lessons completed for each course, as well as
    the highest course completed for each of the lessons. It also allows profile creation, selection, and deletion.
    All of the profile info is held in a database, which is queried using SQLite. It is purely a local database, so
    a network connection isn't required.
'''
class ProfileScreen(Screen):
    # Creates a flag, profName, create and delete Popup variables into the class
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.flag = 0
        self.createProfName = ''
        self.createPop = Popup()
        self.deletePop = Popup()

    # Generates the profile list prior to entering
    def on_pre_enter(self, *args):
        # Will update profile information if one is already set
        if cont.isProfileSet():
            self.loadProfileInformation()

        # Disables delete button if no profile is selected
        if not cont.isProfileSet():
            self.children[0].children[1].disabled = True

        # Will populate the profile list only on the first load
        if self.flag == 0:
            generateProfileList(self)
            self.flag = 1

    # Resets the creation and deletion text upon leaving.
    def on_exit(self, *args):
        self.hideBoolLabels()

    # Changes the selected profile and updates lessons accordingly.
    def selectProfile(self, args):
        # Sets profile info internally to allow quick access
        cont.setProfileInfo(args.profName)

        # Loads profile information
        self.loadProfileInformation(self)

        # Locks every lessons upon switching profiles
        lockLessons(self)

        # Re-enables delete button when a profile is selected
        self.children[1].children[1].disabled = False

        # Resets the creation and deletion labels upon selecting a profile
        self.hideBoolLabels(self)

    # Displays a popup, which the user can enter a new profile name to create a new profile.
    def createNewProfile(self):
        # Creates the layout where everything will be positioned
        layout = RelativeLayout()

        # The button for the creation of the new profile
        submitBtn = Button(text='Create',
                            size_hint = (None, None),
                            border = (20, 20, 20, 20),
                            size = (250, 60),
                            pos_hint = {'center_x':.5, 'center_y': .25})

        # A label prompting for a unique profile name
        nameLabel = Label(text='Enter Name (Must be unique)',
                          font_size=15,
                          pos_hint = {'center_x':.4, 'center_y': .85})

        # Text box for taking in input from the user for the new profile name
        textField = TextInput(multiline=False,
                              size_hint = (None, None),
                              size=(250, 30),
                              pos_hint = {'center_x':.5, 'center_y': .65})

        # Binds the text box to store the new name, and the button is binded to a function to create a profile
        textField.bind(text=self.saveName)
        submitBtn.bind(on_release=self.createProfile)

        # Each of these items are added to the relative layout
        layout.add_widget(submitBtn)
        layout.add_widget(nameLabel)
        layout.add_widget(textField)

        # Popup object is created and stored within the screen, which is then opened.
        self.createPop = Popup(title='Create a new Profile',
                               content=layout,
                               size=(300,200),
                               size_hint=(None, None))
        self.createPop.open()

    # A method to store the entered name as each key is pressed
    def saveName(self, *args):
        self.createProfName = args[1]

    # A method to create the profile upon a button press
    def createProfile(self, *args):
        # Closes the popup
        self.createPop.dismiss()

        # Tries to create the new profile
        success = cont.createNewProfile(self.createProfName)

        # Checks if the profile was created successfully
        if success:
            # Displays an appropriate message upon creation
            self.ids.profileCreationBool.text = "Profile Created Successfully!"

            # A new button is created for the profile, which is then added to the profile list grid layout(profList)
            button = Button(text=self.createProfName,
                            size_hint=(None, None),
                            border=(20, 20, 20, 20),
                            size=(150, 40))
            button.bind(on_press=self.selectProfile)
            button.profName = self.createProfName
            self.profList.add_widget(button)

        # Otherwise, the profile already exists within the database.
        else:
            self.ids.profileCreationBool.text = "Profile already exists!"

    # Displays a delete popup box when a profile is going to be deleted
    def showDeletePopup(self):
        # Creates the layout where everything will be positioned
        layout = RelativeLayout()

        # Button to delete a profile when clicked
        deleteBtn = Button(text='Delete',
                           size_hint=(None, None),
                           border=(20, 20, 20, 20),
                           size=(250, 60),
                           pos_hint={'center_x': .5, 'center_y': .25})

        # Label to clarify a profile is going to be deleted.
        deletePrompt = Label(text='Are you sure you want to delete the profile?',
                             font_size=15,
                             pos_hint={'center_x': .5, 'center_y': .85})

        # The currently selected profile to be deleted
        deleteName = Label(text=cont.getProfileInfo(0),
                           font_size=18,
                           pos_hint={'center_x': .5, 'center_y': .68})

        # Binds the delete button to call a helper method to delete a profile
        deleteBtn.bind(on_release=self.deleteProfile)

        # Adds each of the widgets to the relative layout
        layout.add_widget(deleteBtn)
        layout.add_widget(deletePrompt)
        layout.add_widget(deleteName)

        # Creates a new popup, stores it inside of the screen, then opens the popup
        self.deletePop = Popup(title='Delete Profile',
                               content=layout,
                               size=(400, 200),
                               size_hint=(None, None))
        self.deletePop.open()

    # A method to handle the deletion of a profile upon button press
    def deleteProfile(self, *args):
        # Closes the popup
        self.deletePop.dismiss()

        # Checks if the profile is deleted successfully (Should always succeed)
        success = cont.deleteProfile()

        # Checks if the deletion was successful
        if success:
            self.ids.profileDeletionBool.text = "Profile Deleted Successfully!"

        # Loops through the buttons in the list to remove the current selected profile.
        for x in range(len(self.profList.children)):
            if self.profList.children[x].profName == cont.getProfileInfo(0):
                self.profList.remove_widget(self.profList.children[x])
                break

        # Calls a helper function to lock lessons in each of the courses
        lockLessons(self)

        # Clears out all of the deleted profile information from the app
        self.manager.get_screen('start').ids.currSelectedProf.text = ''
        cont.clearProfileList()
        self.ids.currProfile.text = ''

        # Disables delete button until a new profile is selected
        self.children[1].children[1].disabled = True

    # A helper method to help display the information relavent to the profile.
    def loadProfileInformation(self, *args):
        # Sets the various lesson information for the profile
        self.ids.highestHiraLessons.text = str(cont.getProfileInfo(4))
        self.ids.highestKataLessons.text = str(cont.getProfileInfo(5))
        self.ids.highestKanjiLessons.text = str(cont.getProfileInfo(6))
        self.ids.totalHiraLessons.text = str(cont.getProfileInfo(1))
        self.ids.totalKataLessons.text = str(cont.getProfileInfo(2))
        self.ids.totalKanjiLessons.text = str(cont.getProfileInfo(3))

        # Sets the profile name in the start menu and the profile menu
        self.ids.currProfile.text = "Welcome, " + cont.getProfileInfo(0)
        self.manager.get_screen('start').ids.currSelectedProf.text = "Hi, " + cont.getProfileInfo(0)

    # A helper method to reset the labels whenever a profile is selected or when the screen is left.
    def hideBoolLabels(self, *args):
        self.ids.profileCreationBool.text = ''
        self.ids.profileDeletionBool.text = ''

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

    # Unlocks lessons appropriately for the selected user profile
    def on_pre_enter(self):
        if cont.isProfileSet():
            unlockLessons(self, 4)

    # Generates the lesson list, with 0 being the value for Hiragana
    def generateLessons(self):
        generateLessonList(self, 0)

    # Loads the selected lesson
    def setLesson(self, args):
        cont.setCurrLesson(args.lessonNum, 0)
        self.manager.current = "priorToQuestions"

    # locks the lessons of this language
    def lockLessons(self):
        for x in range(len(self.children[0].children[0].children)):
            self.children[0].children[0].children[x].disabled = True

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
        if cont.isProfileSet():
            unlockLessons(self, 5)

    # Generates the lesson list, with 1 being the value for Katakana
    def generateLessons(self):
        generateLessonList(self, 1)

    # Loads the selected lesson
    def setLesson(self, args):
        cont.setCurrLesson(args.lessonNum, 1)
        self.manager.current = "priorToQuestions"

    # locks the lessons of this language
    def lockLessons(self):
        for x in range(len(self.children[0].children[0].children)):
            self.children[0].children[0].children[x].disabled = True

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
        if cont.isProfileSet():
            unlockLessons(self, 6)

    # Generates the lesson list, with 2 being the value for Kanji
    def generateLessons(self):
        generateLessonList(self, 2)

    # Loads the selected lesson
    def setLesson(self, args):
        cont.setCurrLesson(args.lessonNum, 2)
        self.manager.current = "priorToQuestions"

    # locks the lessons of this language
    def lockLessons(self):
        for x in range(len(self.children[0].children[0].children)):
            self.children[0].children[0].children[x].disabled = True

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
        setAttr(self)


    '''
        Method to build and display the help popup when the button is clicked. It will dynamically load the
        appropriate images depending on the language selected. It will also change the size and padding depending
        on the language, since Kanji are more detailed than Hiragana and Katakana.
    '''
    def displayPopup(self):
        # Loads the imgs from the lesson array
        charList = cont.getImgList()

        # Checks what size the padding and images should be.
        imgSize = cont.getLanguageSize()

        #Creates a grid layout to display the images
        layout_popup = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[imgSize[0],0,0,0])
        layout_popup.bind(minimum_height=layout_popup.setter('height'))

        # Creates the path for the appropriate images.
        path = "Images/" + getCurrLessonScreen() + "Imgs/"

        # Loops through each character in charList and loads the image with the matching name, then adds to the layout
        for char in charList:
            img1 = Image(source=path + "so" + char + ".png", size_hint=(None, None), size=(imgSize[1], imgSize[1]))
            layout_popup.add_widget(img1)

        # Creates a scroll view to allow scrolling of the images.
        root = ScrollView(size_hint=(None, None), size=(375,425))
        root.add_widget(layout_popup)

        # Creates the popup with the title and context, then displays the popup.
        popup = Popup(title='Characters To Know', content=root, size=(400,500), size_hint=(None, None))
        popup.open()

    # Loads the lesson list we came from if button is pressed
    def loadOriginalLessonList(self):
        self.manager.current = getCurrLessonScreen()

    # Loads the question UI screen
    def startLesson(self):
        cont.removeImgList()
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
        getNextQuestion(self)
        self.ids.nextQBtn.disabled = True
        cont.initializeAI()

    # Submits the drawing for checking against the AI.
    def submitDrawing(self):
        print("fucking what")
        self.ids.submitBtn.disabled = True
        print("fucking what1")
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
        return cont.isAnswerCorrect()

    # This will retrieve the answer the AI determines
    def getUserAnswer(self):
        return cont.getUserAnswer()

    # This will retrieve the correct answer stored in the question
    def getCorrectAnswer(self):
        return cont.getCorrectAnswer()

    # Retrieves the next question. Will display the results screen if no more remain.
    def getNextQuestion(self):
        lessContinues = getNextQuestion(self)
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
        # Will display the relevant information, then call the logic to save information of the profile.
        self.showQuestionInfo()
        self.displayPerformance()
        cont.checkPerformance()
        cont.saveInformation()

        # disables next lesson button if there are no more lessons after the one completed.
        if not cont.checkIfMoreLessons():
            self.ids.resNextLessonBtn.disabled = True
        else:
            self.ids.resNextLessonBtn.disabled = False
        if cont.getCurrentLessonNum() > cont.getProfileInfo(cont.getLangNum() + 4):
            self.ids.resNextLessonBtn.disabled = True

    # Displays information regarding to the lesson and question counts.
    def showQuestionInfo(self):
        # Stores correct information to display in the relevant fields.
        self.ids.resCurrLessonLang.text = cont.getSelectedLanguageName()
        self.ids.resCurrLessonNum.text = "Lesson " + str(cont.getCurrentLessonNum())
        self.ids.resCurrLessonTitle.text = cont.getCurrentLessonTitle()
        self.ids.resTotalCorrect.text = str(cont.getCorrectQuestionCount()) + "/" + \
                                        str(cont.getTotalQuestionCount()) + " correct"

    # Displays accuracy and info text detailing if the next lesson has been unlocked.
    def displayPerformance(self):
        # Stores percentage value for repeated use.
        percentage = 100 * (float(cont.getCorrectQuestionCount()) / float(cont.getTotalQuestionCount()))
        self.ids.resAccuracy.text = "Accuracy: {:0.2f}%".format(percentage)

        # Displays a different message depending on if you passed the lesson or not.
        if percentage >= 60:
            self.ids.resLessonUnlockLbl.text = "You have unlocked the next lesson!"
        else:
            self.ids.resLessonUnlockLbl.text = "Try again for 60% to unlock the next lesson."
            self.ids.resNextLessonBtn.disabled = True

    # Loads the next lesson immediately
    def loadNextLesson(self):
        cont.setupNextLessonInfo()
        changeScreen(self, 'priorToQuestions')

    # Loads the lesson list of the language selected.
    def loadLessonList(self):
        changeScreen(self, getCurrLessonScreen())

    # Loads the start screen of the app
    def backToMain(self):
        changeScreen(self, 'start')

    pass


color = [1, 1, 1, 1]  # color array for paint widget
xCoord = 0  # holds the current x coordinate, used for moving the mouse
yCoord = 0  # holds the current y coordinate, used for moving the mouse
wide = 4  # holds the width of the line to be drawn
'''
    This widget is the drawing UI found on the question screen. It handles touch input and can clear the screen after
    submission and when a button is pressed.
'''
class MyPaintWidget(Widget):
    # creates a new property for the widget
    col = ListProperty(color)

    # Stores the drawn answer into a jpg, then passes it to the logic to check against the AI.
    def submitAnswer(self):
        self.export_to_png("image.png")
        image = pilImg.open("image.png")
        imTest = image.crop((25, 200, 475, 575))
        imTest = imTest.resize((48, 48))
        imTest.save('image.png')
        invImg = opsImg.invert(imTest.convert('RGB'))
        invImg = opsImg.invert(invImg)
        invImg.save('image.png')

        cont.sendAnswer(image)

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

    # Clears the canvas
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
    lessonArr = cont.generateLessons(lang)

    # Creates a new layout for the lessons.
    layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[100, 0, 0, 0])
    layout.bind(minimum_height=layout.setter('height'))

    # Loops until we have covered every lesson in the array.
    for i in range(len(lessonArr)):
        # Create a new button with appropriate names and ids.
        button = Button(text='Lesson ' + str(i + 1) + ": " + lessonArr[i],
                        size_hint=(None, None),
                        border=(20, 20, 20, 20),
                        size=(300, 60),
                        disabled=True,
                        disabled_color=(1,1,1,1))
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
    screen.profList = layout

    # Loops through the entire profile list
    for i in range(cont.getProfileNameLength()):
        # Creates new button for each element, naming and id'ing them appropriately.
        button = Button(text=cont.getProfileName(i),
                        size_hint=(None, None),
                        border=(20, 20, 20, 20),
                        size=(150, 40))
        button.bind(on_press=screen.selectProfile)
        button.profName = cont.getProfileName(i)
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

'''
    Helper method to lock the lessons for each of the language types.
'''
def lockLessons(screen):
    screen.manager.get_screen('hLessons').lockLessons()
    screen.manager.get_screen('kataLessons').lockLessons()
    screen.manager.get_screen('kanjiLessons').lockLessons()

'''
    Unlocks the lessons less than or equal to the highest completed lesson of the profile.
'''
def unlockLessons(screen, lang):
    totalLessons = len(screen.children[0].children[0].children)
    for x in range(cont.getProfileInfo(lang) + 1, 0, -1):
        screen.children[0].children[0].children[totalLessons - x].disabled = False

'''
    Returns a string resembling the screen to swap
'''
def getCurrLessonScreen():
    currLang = cont.getSelectedLanguageName()
    if currLang == "Hiragana":
        retStr = "hLessons"
    elif currLang == "Katakana":
        retStr = "kataLessons"
    else:
        retStr = "kanjiLessons"
    return retStr

'''
    Sets the attributes of the given screen to the appropriate items set in the lesson logic.
'''
def setAttr(screen):
    screen.ids.lessonText.text = cont.getSelectedLanguageName()
    screen.ids.lessonNum.text = "Lesson " + str(cont.getCurrentLessonNum())
    screen.ids.lessonTitle.text = cont.getCurrentLessonTitle()
    screen.ids.questionCount.text = str(cont.getTotalQuestionCount()) + " Questions"
    cont.resetQuestionCounters()

'''
    Returns false if there are no more questions. True otherwise. Also sets the question number label
'''
def getNextQuestion(screen):
    currQuestion = cont.getCurrQuestionCount()
    totalQuestions = cont.getTotalQuestionCount()
    if currQuestion == totalQuestions + 1:
        return False
    else:
        screen.ids.questionLabel.text = cont.getNextQuestion()
        screen.ids.questionNum.text = "Q: " + str(currQuestion) + "/" + str(totalQuestions)
        cont.incrementQuestionNum()
        return True

# Driver method
class JCRApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    JCRApp().run()
