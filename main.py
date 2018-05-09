# store my diary stuffs into a database
# date , time ...automatically takes
# title and diary content from user
import sqlite3
import getpass
import hashlib
import datetime
import os

#verbose
verbose = True

#First Time
firstTime = False

#Databasename
dbName = "log.db"

#to read password and check
def passlock(storedPswd):
    pswd = ""
    i = 3
    while (pswd != storedPswd):
        if i < 3:
            print("Wrong Password , try again")
    
        if i==0:
            print("Wrong attempt 3 times.. quiting")
            exit()

        pswd = (hashlib.md5(getpass.getpass('Enter yout Password ').encode())).hexdigest()
        
        #print(pswd)
        i = i -1
    return 1

#to add new user
def newUser():
    username = input("Enter your username: ")
    while True:
        pswd = (hashlib.md5(getpass.getpass('Enter your Password: ').encode())).hexdigest()
        if pswd == (hashlib.md5(getpass.getpass('ReEnter your Password: ').encode())).hexdigest() :
            break    
        print("Passwords dont match, Try again ")

    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    t = (username,pswd,)
    try:
        c.execute('INSERT INTO users(name,pass) VALUES(?,?)',t) #Entry to users table
        #TO:DO think of everything required to be used to save a log entry
        
        c.execute("CREATE TABLE %s (date text, time text, title text, diary text)"% username)#New table for new user
        conn.commit()
    except Exception as e:
        if verbose:
            print(e)
        print('User already present')
        conn.commit()
        conn.close()
        exit()
    
    conn.close()

#Username and password verification
def userStuffs():
    user = input("username ( enter \"new\" for new user ) :")
    if(user == 'new'):
        newUser()
        print('Log in using this credentials')
        return None

    conn = sqlite3.connect(dbName)
    c = conn.cursor()    
    t = (user,)
    c.execute('SELECT pass FROM users WHERE name = ?',t)
    storedPswd = c.fetchone() #output is a tuple
    conn.commit()
    conn.close()
    if storedPswd is None:
        print("user not found ")
        return None
    print(storedPswd[0])    
    if passlock(storedPswd[0]):
        return user
    else:
        exit()


#incomplete
def diaryLog(user):
    title = input("So..what's it about today ")
    diary = input("Ok tell me about it ")
    conn = sqlite3.connect(dbName)
    #date and time
    now = datetime.datetime.now()
    currTime = str(now.strftime("%Y-%m-%d"))
    currDate = str(now.strftime("%H:%M"))
    t = (currDate,currTime,title,diary,)
    c = conn.cursor()
    c.execute('INSERT INTO %s (date,time,title,diary) VALUES (?,?,?,?) ' % user,t)
    conn.commit()
    conn.close()


#Authentication function
def auth():
    username = userStuffs()
    if username is not None :
        return username
    else:
        print(" Try Again !")
        exit()

#check existance of DB
def checkDB():
    try:
        os.open(dbName,os.O_RDONLY)       
    except:    
        global firstTime
        firstTime = True 

#creating db
def createDB():
    conn = sqlite3.connect(dbName)
    c = conn.cursor()    
    c.execute ('''CREATE TABLE users (`name` TEXT NOT NULL,`user_id` INTEGER NOT NULL DEFAULT 100 PRIMARY KEY AUTOINCREMENT, `pass`	TEXT NOT NULL)''')
    print("Created User Database ")
    conn.commit()
    conn.close()

def main():
    checkDB() # to see if db exist
    global firstTime
    if firstTime: 
        createDB() # to create db if it doesnt exist
        firstTime = False

    user = auth() #authenticates the user and returns user's name if the user is valid 
    diaryLog(user) #to write the diary

#main function
main()
