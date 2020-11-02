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
    cursor = conn.execute("SELECT HIRAGANA_LESSONS_COMPLETED FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()


def getTotalKataLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT KATAKANA_LESSONS_COMPLETED FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()


def getTotalKanjiLessons(profName):
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT KANJI_LESSONS_COMPLETED FROM Profiles WHERE NAME = ?", (profName,))
    return cursor.fetchone()