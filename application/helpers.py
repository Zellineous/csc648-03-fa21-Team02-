import re

def isValidSfsuEmail(s):
    if(re.search('sfsu.edu$',s)):
        print('has sfsu.edu at the end')
    if(re.match(r'[^@]+@[^@]+\.[^@]+',s)):
        print('is an email')
    return( (re.search('sfsu.edu$',s)) and re.match(r'[^@]+@[^@]+\.[^@]+',s)) #returns None if failure
