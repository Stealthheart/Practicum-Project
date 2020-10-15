import json

def readJsonLessons(lang):
    if(lang == 0):
        fileString = 'hiraLessons.txt'
    elif(lang == 1):
        fileString = 'kataLessons.txt'
    else:
        fileString = 'kanjiLessons.txt'

    with open(fileString, 'r') as json_file:
        lessonArray = json.load(json_file)

    return lessonArray


