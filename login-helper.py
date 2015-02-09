#!/usr/bin/env python3

import subprocess
import sys
import os

class Login:
    def __init__(self, username, password, notes=''):
        self.username = username
        self.password = password.rstrip()
        self.notes = notes.rstrip()


def input_text(text):
    adbCommand = 'adb shell input text'
    return adbCommand + ' ' + text


def input_key(keyValue):
    adbCommand = 'adb shell input keyevent'
    return adbCommand + ' ' + keyValue


def loginToApp(login):
    tab = '61'
    enter = '66'
    command = ' && '.join([input_text(login.username), 
                        input_key(tab), 
                        input_text(login.password),
                        input_key(tab), input_key(tab), input_key(tab),
                        input_key(enter)])
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


def getLogins():
    try:
        loginList = []
        loginFile = open('test-accounts.txt', 'r')
        for line in loginFile.readlines():
            if line[:1] != '#':
                words = line.split(' ')
                username = words[0]
                password = words[1]
                notes = ' '.join(words[2:])
                loginList.append(Login(username, password, notes))
        return loginList
    except FileNotFoundError:
        print('Error: cannot find test-accounts.txt file.\nCheck that the test-accounts.txt file is located in this directory.')
        sys.exit(1)


def printIndexedLogins():
    loginList = getLogins()
    
    indexFieldLength = 7 
    userFieldLength = getMaxLength(o.username for o in loginList) + 5
    passFieldLength = getMaxLength(o.password for o in loginList) + 5 

    indexFieldSpec = '{:<{indexFieldLength}}'
    userFieldSpec = '{:<{userFieldLength}}'
    passFieldSpec = '{:<{passFieldLength}}'

    rowFormat = indexFieldSpec + userFieldSpec + passFieldSpec + '{}'
    print(rowFormat.format('Index', 'Username', 'Password', 'Notes',
                                 indexFieldLength=indexFieldLength, 
                                 userFieldLength=userFieldLength, 
                                 passFieldLength=passFieldLength))
    for i in range(0, len(loginList)):
        login = loginList[i]
        print((rowFormat).format(i, 
                                 login.username, 
                                 login.password, 
                                 login.notes,
                                 indexFieldLength=indexFieldLength, 
                                 userFieldLength=userFieldLength, 
                                 passFieldLength=passFieldLength))


def getMaxLength(strings):
    maxLength = 0
    for s in strings:
        if len(s) > maxLength:
            maxLength = len(s)
    return maxLength


indexArgMessage = 'To initiate adb login, use index of desired login as an argument.'
errorMessage = 'Invalid argument: Pass no arguments to see a list of available logins. ' + indexArgMessage
if len(sys.argv) == 1:
    print() # blank line
    printIndexedLogins()
    print('\n' + indexArgMessage)   
elif len(sys.argv) == 2:
    arg = sys.argv[1]
    try:
        index = int(arg)
        allLogins = getLogins()
        if index >=0 and index < len(allLogins):
            login = allLogins[index]
            print('Attempting to log in user: {}\t{}'.format(login.username, login.notes))
            loginToApp(login)
        else:
            print('Invalid index: Enter the index of one of the logins displayed when you run this script without any arguments.')
    except ValueError:
        print(errorMessage)
else:
    print(errorMessage)
