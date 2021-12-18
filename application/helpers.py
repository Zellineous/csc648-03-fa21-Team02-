import re
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

def checkPasswordOfUser(entered_username, entered_password): #checks password of entered user from login
    cursor.execute(f"SELECT password FROM user WHERE name='{entered_username}'")
    password = cursor.fetchone()['password']
    #print("from checkPass" + password)
    if(decryptPass(password) == entered_password):
        return True
    
    return False


def getUserData(entered_user):
    cursor.execute(f"SELECT * FROM user WHERE name='{entered_user}'")
    return cursor.fetchone()

def getUserId(entered_user):
    cursor.execute(f"SELECT sfsu_id FROM user WHERE name='{entered_user}'")
    return cursor.fetchone()

def getUserProfile(id):
    cursor.execute(f"SELECT * FROM user_profile WHERE sfsu_id={id}")
    return cursor.fetchone()

