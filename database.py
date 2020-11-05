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
    print("hello?????")
    conn = sql.connect('Database/test.db')
    query = 'UPDATE Profiles SET hiragana_lessons_completed = ?,' \
            '                    katakana_lessons_completed = ?,' \
            '                    kanji_lessons_completed = ?,' \
            '                    highest_hiragana_lesson_completed = ?,' \
            '                    highest_katakana_lesson_completed = ?,' \
            '                    highest_kanji_lesson_completed = ?,' \
            '                    last = ? ' \
            '               WHERE name = ?'
    conn.execute(query, (infoList[1], infoList[2], infoList[3], infoList[4], infoList[5], infoList[6], infoList[7], infoList[0]))
    conn.commit()
    conn.close()

def checkIfProfileExists(profName):
    conn = sql.connect('Database/test.db')
    query = 'SELECT COUNT(*) FROM Profiles WHERE NAME = ?'
    cursor = conn.execute(query, (profName,))
    for row in cursor:
        return row[0]

def createProfile(profName):
    conn = sql.connect('Database/test.db')
    query = 'INSERT INTO Profiles(name, hiragana_lessons_completed, katakana_lessons_completed, kanji_lessons_completed, ' \
            'highest_hiragana_lesson_completed, highest_katakana_lesson_completed, highest_kanji_lesson_completed, last)' \
            ' VALUES (?, 0, 0, 0, 0, 0, 0, 0)'
    conn.execute(query, (profName,))
    conn.commit()

def getLastUsedProfile():
    conn = sql.connect('Database/test.db')
    query = 'SELECT name FROM Profiles WHERE last = 1'
    cursor = conn.execute(query)
    for row in cursor:
        return row[0]

def profileSwapped(profName):
    conn = sql.connect('Database/test.db')
    query = 'UPDATE Profiles SET last = 0 WHERE name = ?'
    print(profName)
    conn.execute(query, (profName,))
    conn.commit()
    testDB()

def testDB():
    conn = sql.connect('Database/test.db')
    cursor = conn.execute("SELECT * FROM Profiles")
    for row in cursor:
        print("ID =", row[0])
        print("NAME =", row[1])
        print("HIRAGANA_LESSONS_COMPLETED =", row[2])
        print("KATAKANA_LESSONS_COMPLETED =", row[3])
        print("KANJI_LESSONS_COMPLETED =", row[4])
        print("Highest_Hira_LESSONS_COMPLETED =", row[5])
        print("Highest_Kata_LESSONS_COMPLETED =", row[6])
        print("Highest_Kanji_LESSONS_COMPLETED =", row[7])
        print("Last =", row[8])

def deleteProfileFromDB(profName):
    conn = sql.connect('Database/test.db')
    query = 'DELETE FROM Profiles WHERE NAME = ?'
    conn.execute(query, (profName,))
    conn.commit()
    return True
