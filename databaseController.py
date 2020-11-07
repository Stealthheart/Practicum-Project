import sqlite3
import database as db
from os import path

def createDB():
    conn = sqlite3.connect('Database/test.db')
    conn.execute('CREATE TABLE Profiles\n'
                 '        (id INTEGER PRIMARY KEY,\n'
                 '        name TEXT NOT NULL,\n'
                 '        hiragana_lessons_completed INT NOT NULL,\n'
                 '        katakana_lessons_completed INT NOT NULL,\n'
                 '        kanji_lessons_completed INT NOT NULL,\n'
                 '        highest_hiragana_lesson_completed INT NOT NULL,\n'
                 '        highest_katakana_lesson_completed INT NOT NULL,\n'
                 '        highest_kanji_lesson_completed INT NOT NULL,\n'
                 '        last INT NOT NULL);')
    conn.close()

def doesDatabaseExist():
    return path.exists('Database/test.db')

def writeInfoToDB(profInfo):
    db.updateProfile(profInfo)

def canCreateProfile(profName):
    if db.checkIfProfileExists(profName) == 0:
        return True
    return False

def createNewProfile(profName):
    db.createProfile(profName)