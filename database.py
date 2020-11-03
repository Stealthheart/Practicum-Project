import sqlite3 as sql

def getNumberOfProfiles():
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT COUNT(*) FROM Profiles")
    for row in cursor:
        profNum = row[0]
    conn.close()
    return profNum

def getProfileNames():
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT NAME FROM Profiles")
    retList = cursor.fetchall()
    conn.close()
    return retList


def getTotalHiraLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT hiragana_lessons_completed FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()


def getTotalKataLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT katakana_lessons_completed FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()


def getTotalKanjiLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT kanji_lessons_completed FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()

def getHighestHiraLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT highest_hiragana_lesson_completed FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()

def getHighestKataLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT highest_katakana_lesson_completed FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()

def getHighestKanjiLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT highest_kanji_lesson_completed FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()

def updateProfile(infoList):
    conn = sql.connect('Database/test.db')
    query = 'UPDATE Profiles SET hiragana_lessons_completed = ?,' \
            '                    katakana_lessons_completed = ?,' \
            '                    kanji_lessons_completed = ?,' \
            '                    highest_hiragana_lesson_completed = ?,' \
            '                    highest_katakana_lesson_completed = ?,' \
            '                    highest_kanji_lesson_completed = ? ' \
            '               WHERE name = ?'
    conn.execute(query, (infoList[1], infoList[2], infoList[3], infoList[4], infoList[5], infoList[6], infoList[0],))
    conn.commit()
    conn.close()