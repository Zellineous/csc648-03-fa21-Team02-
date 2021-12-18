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

def encryptPass(s):
    encryptedPass = fernet.encrypt(s.encode()).decode()
    print(f"password: {encryptedPass}")
    return encryptedPass

def decryptPass(s):
    decryptedPass = fernet.decrypt(s.encode()).decode()
    print(decryptedPass)
    return decryptedPass

def checkPasswordOfUser(entered_username, entered_password): #checks password of entered user from login
    cursor.execute(f"SELECT password FROM user WHERE name='{entered_username}'")
    password = cursor.fetchone()['password']
    print(password)
    if(decryptPass(password) == entered_password):
        return True
    
    return False



    
    

def getUserData(entered_user):
    cursor.execute(f"SELECT * FROM user WHERE name='{entered_user}'")
    return cursor.fetchone()

