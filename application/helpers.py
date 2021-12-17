import re
from passlib.hash import sha256_crypt

def isValidSfsuEmail(s):
    return( (re.search('sfsu.edu$',s)) and re.match(r'[^@]+@[^@]+\.[^@]+',s)) #returns None if failure

def encryptPass(s):
    return sha256_crypt.encrypt(s)

def checkPasswordOfUser(username, password):
    
    return True