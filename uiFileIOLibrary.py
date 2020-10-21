import json

'''
    This class will hold all functions for reading and writing to files.
'''

# Reads the given lesson list from the json txt file. Will return an array holding the lessons.
def readJsonLessons(lang):
    if lang == 0:
        fileString = 'hiraLessons.txt'
    elif lang == 1:
        fileString = 'kataLessons.txt'
    else:
        fileString = 'kanjiLessons.txt'

    with open(fileString, 'r') as json_file:
        lessonArray = json.load(json_file)

    return lessonArray


