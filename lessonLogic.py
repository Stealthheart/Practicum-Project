import uiFileIOLibrary as io
from random import randrange

'''
    This class will hold the logic for the lessons and questions. Currently, everything is hardcoded into arrays,
    except the lesson titles, which are held in some .txt file. The majority of this implementation is coming next.
'''

langTypes = ["Hiragana", "Katakana", "Kanji"]
lessonArr = []
arrLang = -1
currLesson = -1
currLang = -1
currQuestionNum = 1
correctQuestions = 0
totalQuestionNum = 10
questionArray = ["Write down the character for: 'a'", "Write down the character for: 'i'",
                 "Write down the character for: 'u'",
                 "Write down the character for: 'e'", "Write down the character for: 'o'",
                 "Write down the character for: 'ka'",
                 "Write down the character for: 'ki'", "Write down the character for: 'ku'",
                 "Write down the character for: 'ke'",
                 "Write down the character for: 'ko'"]
correctAnswer = 0

#region Lesson Methods

# Returns the lesson array for the UI. Also sets up the lesson array internally for titles.
def generateLessons(lang):
    global lessonArr
    lessonArr = io.readJsonLessons(lang)
    return lessonArr

'''
    This method will set the variables to appropriate numbers for the lessons. Also, it will reset the lessen
    array if the language given is different from the one currently set. 
'''
def setLesson(lessonNum, lang):
    global currLesson, currLang, arrLang, lessonArr, questionArray, totalQuestionNum
    if lang != currLang:
        repopulateLessonArray(lang)
    currLesson = int(lessonNum) - 1
    currLang = int(lang)
    arrLang = currLang
    questionArray = io.readLessonQuestions(lessonNum)
    totalQuestionNum = len(questionArray)

# Resets the lesson array to the given language
def repopulateLessonArray(lang):
    global lessonArr
    lessonArr = io.readJsonLessons(lang)

# Returns the current lesson number
def getCurrentLessonNum():
    return currLesson

# increments the current lesson by one if needed
def loadNextLessonInfo():
    global currLesson, totalQuestionNum
    currLesson += 2
    setLesson(currLesson, currLang)

# Returns the title of the current lesson.
def getCurrLessonTitle():
    return lessonArr[currLesson]

# Determines if there are more lessons in the array.
def areMoreLessons():
    if currLesson == len(lessonArr) - 1:
        return False
    return True

#endregion Lesson Methods

#region Question Methods

# Resets question variables to starting values when a new lesson begins.
def resetQuestionCounters():
    global currQuestionNum, correctQuestions
    currQuestionNum = 1
    correctQuestions = 0

# Returns the next question string.
def getNextQuestion():
    return questionArray[currQuestionNum - 1][0]

# Returns the question we are currently on.
def getCurrQuestionCount():
    return currQuestionNum

# Increments the current question number
def incrementQuestionNum():
    global currQuestionNum
    currQuestionNum += 1

# Returns the total amount of questions answered correctly.
def getCorrectQuestionCount():
    return correctQuestions

# Returns the total question count in the lesson
def getTotalQuestionCount():
    return totalQuestionNum

def getCorrectAnswer():
    return questionArray[currQuestionNum - 2][2]

#endregion Question Methods

#region Answer Methods

'''
    Sets the correct answer variable. This method currently will randomly pick a number, either 0 or 1, with 0 being
    correct and 1 incorrect. Eventually, this method will pass the given image to the AI, and will check what is
    returned to determine the correct answer.
'''
def checkAnswer(img):
    global correctQuestions, correctAnswer
    num = randrange(2)
    if num == 0:
        correctAnswer = 0
        correctQuestions += 1
    else:
        correctAnswer = 1

# Returns 0 or 1, depending if the answer was correct.
def retrieveResultString():
    return correctAnswer

#endregion Answer Methods

# Returns the selected language string.
def getSelectedLanguage():
    return langTypes[currLang]

def getSelectedLanguageNum():
    return currLang
