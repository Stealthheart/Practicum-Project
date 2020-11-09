import json

'''
    This class will hold all functions for reading and writing to files.
'''

# Reads the given lesson list from the json txt file. Will return an array holding the lesson titles.
def readJsonLessons(lang):
    if lang == 0:
        fileString = 'hiraganaLessons/hiraLessons.txt'
    elif lang == 1:
        fileString = 'katakanaLessons/kataLessons.txt'
    else:
        fileString = 'kanjiLessons/kanjiLessons.txt'

    with open(fileString, 'r') as json_file:
        lessonArray = json.load(json_file)

    return lessonArray

# Reads the given lesson number and will return a list holding the questions for that lesson.
def readLessonQuestions(lessonNum, lang):
    if lang == 0:
        fileString = 'hiraganaLessons/hLesson' + str(lessonNum) + '.txt'
    elif lang == 1:
        fileString = 'katakanaLessons/kataLesson' + str(lessonNum) + '.txt'
    else:
        fileString = 'kanjiLessons/kanjiLesson' + str(lessonNum) + '.txt'
    with open(fileString, 'r', encoding='utf-8') as json_file:
        questionArray = json.load(json_file)

    return questionArray
