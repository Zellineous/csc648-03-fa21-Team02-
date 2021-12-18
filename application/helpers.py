import re
import datetime
from flask import Flask
import database as db
from cryptography.fernet import Fernet
import base64

conn = db.connect()
cursor = conn.cursor()
key = base64.b64encode('12345678912345678912345678912345'.encode("utf-8"))

fernet = Fernet(key)

def isValidSfsuEmail(s):
    return( (re.search('sfsu.edu$',s)) and re.match(r'[^@]+@[^@]+\.[^@]+',s)) #returns None if failure

def encryptPass(s): #enter a string to encrypt it and return the string
    encryptedPass = fernet.encrypt(s.encode()).decode() 
    #print(f"password: {encryptedPass}")
    return encryptedPass

def decryptPass(s): #input an encrypted string
    #print(s)
    decryptedPass = fernet.decrypt(s.encode()).decode()
    #print("from decrypt:" + decryptedPass + "  " + s)
    return decryptedPass

def createMessage(msg, sender, receiver):
    user1 = getUserData(sender)
    user2 = getUserData(receiver)
    print(f"sending {msg} from {user1['name']} to {user2['name']}")

    cursor.execute(f"INSERT INTO message (msg, sending_user, datetime, conversation) VALUES ({msg},{user1['sfsu_id']},{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{getConversation(user1,user2)})")

    
    

def checkPasswordOfUser(entered_username, entered_password): #checks password of entered user from login
    cursor.execute(f"SELECT password FROM user WHERE name='{entered_username}'")
    password = cursor.fetchone()['password']
    #print("from checkPass" + password)
    if(decryptPass(password) == entered_password):
        return True
    
    return False
def getConversationMessages(user1,user2): #(sfsu_id,sfsu_id)
    convo = getConversation(user1,user2)
    messages = []
    if convo:
        print(convo)
        cursor.execute(f"SELECT message,conversation FROM message WHERE conversation = {convo['id']}")
        messages = cursor.fetchall()

    print(messages)
    return messages

def getConversation(user1,user2):
    cursor.execute(f"SELECT * FROM conversation WHERE user1={user1} AND user2={user2}")
    convo = cursor.fetchone()
    if convo:
        return convo
    else:
        cursor.execute(f"SELECT * FROM conversation WHERE user1={user2} AND user2={user1}")
        convo = cursor.fetchone()
        if convo:
            return convo
    return None
    

def getUserData(entered_user):
    cursor.execute(f"SELECT * FROM user WHERE name='{entered_user}'")
    return cursor.fetchone()

def getUserDataWithId(id):
    cursor.execute(f"SELECT * FROM user WHERE sfsu_id={id}")
    return cursor.fetchone()

def getUserId(entered_user):
    cursor.execute(f"SELECT sfsu_id FROM user WHERE name='{entered_user}'")
    return cursor.fetchone()

def getUserProfile(id):
    cursor.execute(f"SELECT * FROM user_profile WHERE sfsu_id={id}")
    return cursor.fetchone()


def makeUserProfile(sfsu_id):
    user = getUserData(sfsu_id)
    cursor.execute(f"INSERT INTO user_profile (name,sfsu_id) VALUE ('{user['name']}',{user['sfsu_id']})")
    cursor.commit()
    print(getUserProfile(sfsu_id))


# returns all courses
def getAllCourses():
    cursor.execute(f"SELECT * FROM course")
    return cursor.fetchall()

# returns courses that are similar to search term
def getSearch(search):
    cursor.execute(f"SELECT * FROM course WHERE name LIKE '%" + search + "%'")
    return cursor.fetchall()


# returns corresponding major id
def getMajor(search_category):
    cursor.execute(f"SELECT * FROM major WHERE name LIKE '%" + search_category + "%'")
    return cursor.fetchone()


# returns courses that belong to correct major
def getMajorSearch(id):
    cursor.execute(f"SELECT * FROM course WHERE major_id={id}")
    return cursor.fetchall()


# returns courses that match both major and search term
def getMCSearch(search, id):
    cursor.execute(f"SELECT * FROM course WHERE major_id={id} AND name LIKE '%" + search + "%'")
    return cursor.fetchall()



def getTutorId(course_id):
    cursor.execute(f"SELECT * FROM teaches WHERE course={course_id}")
    return cursor.fetchone()

def getTutorInfo(tutor_id):
    cursor.execute(f"SELECT * FROM user_profile WHERE sfsu_id={tutor_id}")
    return cursor.fetchone()