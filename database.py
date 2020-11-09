import sqlite3 as sql
conn = None

'''
    Makes the connection to the database
'''
def connectToDB():
    global conn
    conn = sql.connect('Database/profiles.db')

'''
    Closes the connection to the database
'''
def disconnectFromDB():
    conn.close()

'''
    Queries the database and returns the number of profiles inside the Profiles table.
'''
def getNumberOfProfiles():
    connectToDB()
    cursor = conn.execute("SELECT COUNT(*) FROM Profiles")
    profNum = cursor.fetchone()
    disconnectFromDB()
    return profNum[0]

'''
    Returns a list of all the names inside the Profiles table.
'''
def getProfileNames():
    connectToDB()
    cursor = conn.execute("SELECT NAME FROM Profiles")
    retList = cursor.fetchall()
    disconnectFromDB()
    return retList

'''
    Returns a tuple of the hiragana lessons completed for the given profile name
'''
def getTotalHiraLessons(profName):
    connectToDB()
    cursor = conn.execute("SELECT hiragana_lessons_completed FROM Profiles WHERE NAME = ?", (profName,))
    retTup = cursor.fetchone()
    disconnectFromDB()
    return retTup

'''
    Returns a tuple of the katakana lessons completed for the given profile name
'''
def getTotalKataLessons(profName):
    connectToDB()
    cursor = conn.execute("SELECT katakana_lessons_completed FROM Profiles WHERE NAME = ?", (profName,))
    retTup = cursor.fetchone()
    disconnectFromDB()
    return retTup

'''
    Returns a tuple of the kanji lessons completed for the given profile name
'''
def getTotalKanjiLessons(profName):
    connectToDB()
    cursor = conn.execute("SELECT kanji_lessons_completed FROM Profiles WHERE NAME = ?", (profName,))
    retTup = cursor.fetchone()
    disconnectFromDB()
    return retTup

'''
    Returns a tuple of the highest hiragana lesson completed for the given profile name
'''
def getHighestHiraLessons(profName):
    connectToDB()
    cursor = conn.execute("SELECT highest_hiragana_lesson_completed FROM Profiles WHERE NAME = ?", (profName,))
    retTup = cursor.fetchone()
    disconnectFromDB()
    return retTup

'''
    Returns a tuple of the highest katakana lesson completed for the given profile name
'''
def getHighestKataLessons(profName):
    connectToDB()
    cursor = conn.execute("SELECT highest_katakana_lesson_completed FROM Profiles WHERE NAME = ?", (profName,))
    retTup = cursor.fetchone()
    disconnectFromDB()
    return retTup

'''
    Returns a tuple of the highest kanji lesson completed for the given profile name
'''
def getHighestKanjiLessons(profName):
    connectToDB()
    cursor = conn.execute("SELECT highest_kanji_lesson_completed FROM Profiles WHERE NAME = ?", (profName,))
    retTup = cursor.fetchone()
    disconnectFromDB()
    return retTup

'''
    Saves updated profile information into the table.
'''
def updateProfile(infoList):
    connectToDB()
    query = "UPDATE Profiles SET hiragana_lessons_completed = ?," \
            "katakana_lessons_completed = ?, " \
            "kanji_lessons_completed = ?,  " \
            "highest_hiragana_lesson_completed = ?, " \
            "highest_katakana_lesson_completed = ?, " \
            "highest_kanji_lesson_completed = ?, " \
            "last = ? " \
            "WHERE name = ?"
    conn.execute(query, (infoList[1], infoList[2], infoList[3], infoList[4],
                         infoList[5], infoList[6], infoList[7], infoList[0]))
    conn.commit()
    disconnectFromDB()

'''
    Check if the given profile exists within the table.
'''
def checkIfProfileExists(profName):
    returnVal = -1
    connectToDB()
    query = 'SELECT COUNT(*) FROM Profiles WHERE NAME = ?'
    cursor = conn.execute(query, (profName,))
    for row in cursor:
        returnVal = row[0]
    disconnectFromDB()
    return returnVal

'''
    Creates a new profile and stores it into the database with default values.
'''
def createProfile(profName):
    connectToDB()
    query = 'INSERT INTO Profiles(name, hiragana_lessons_completed, katakana_lessons_completed, ' \
            'kanji_lessons_completed, highest_hiragana_lesson_completed, highest_katakana_lesson_completed, ' \
            'highest_kanji_lesson_completed, last)' \
            ' VALUES (?, 0, 0, 0, 0, 0, 0, 0)'
    conn.execute(query, (profName,))
    conn.commit()
    disconnectFromDB()

'''
    Returns the profile name of the last selected profile.
'''
def getLastUsedProfile():
    profName = ()
    connectToDB()
    query = 'SELECT name FROM Profiles WHERE last = 1'
    cursor = conn.execute(query)
    for row in cursor:
        profName = row[0]
    disconnectFromDB()
    return profName

'''
    Changes the last column for the given profile name, to indicate another profile was selected.
'''
def profileSwapped(profName):
    connectToDB()
    query = 'UPDATE Profiles SET last = 0 WHERE name = ?'
    conn.execute(query, (profName,))
    conn.commit()
    disconnectFromDB()

'''
    Deletes the given profile name from the database
'''
def deleteProfileFromDB(profName):
    connectToDB()
    query = 'DELETE FROM Profiles WHERE NAME = ?'
    conn.execute(query, (profName,))
    conn.commit()
    disconnectFromDB()
    return True

'''
    Creates the Profiles table within the database file if it doesn't exist.
'''
def createDatabase():
    connectToDB()
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
    disconnectFromDB()
