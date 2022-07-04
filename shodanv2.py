import shodan
import os
from tkinter import *
from tkinter.ttk import *
import json
import tkinter.scrolledtext as tkscrolled
from tkinter import messagebox
from tkinter import simpledialog
import datetime
import requests
import math

api = ''
window = Tk()
window.geometry('812x628')
window.title('Shodan tool V3')
window.resizable(width = 0, height = 0)
ip = IntVar()
data = IntVar()

if not os.path.exists('./conf/'):
    os.makedirs('./conf/')

if not os.path.exists('./export/'):
    os.makedirs('./export/')

if not os.path.isfile('./conf/history.txt'):
    with open('./conf/history.txt', 'w') as historyFile:
        historyFile.write('')
        historyFile.close()

def saveKey():
    apiKey = simpledialog.askstring('Set API key' ,'Please insert an API key, it will be saved.', parent = window)
    with open('./conf/key.txt', 'w') as keyFile:
        keyFile.write(apiKey)
        keyFile.close()
    setKey()

def setKey():
    global api
    global key
    with open('./conf/key.txt', 'r') as keyFile:
        key = keyFile.read()
        api = shodan.Shodan(key)
        keyFile.close()

def keyFileCheck():
    if not os.path.isfile('./conf/key.txt'):
        saveKey()
    else:
        setKey()

def printIp(text):
    ipText.config(state = NORMAL)
    ipText.delete('1.0', END)
    ipText.insert(END, text)

def printData(text):
    dataText.config(state = NORMAL)
    dataText.delete('1.0', END)
    dataText.insert(END, text)

def clearHistoryBox():
    result = messagebox.askquestion('Clear history', 'Are you sure?', icon = 'warning')
    if result == 'yes':
        with open('./conf/history.txt', 'w') as historyFile:
            historyFile.write('')
            historyFile.close()
        history.clear()

def search(event = None):
    try:
        outputIp = ''
        outputData = ''
        searchStr = ipStr.get()
        if searchStr != '':
            with open('./conf/history.txt', 'r') as historyFile:
                if not searchStr in historyFile.read():
                    with open('./conf/history.txt', 'a') as historyFile:
                        historyFile.write(searchStr + '\n')
                        historyFile.close()
        maxPage.set('/' + str(int(math.ceil(api.count(searchStr)['total']/100))))
        results = api.search('{0}'.format(searchStr), page=int(pageStr.get()))
        for i, result in enumerate(results['matches']):
            outputIp += 'IP:' + str(i + 1) + '\n' + str(result['ip_str']) + ':' + str(result['port']) + '\n\n'
            outputData += 'IP:' + str(i + 1) + '\n------------------\n' + str(result['data']) + '\n\n'
        printIp(outputIp)
        printData(outputData)
    except Exception as err:  
        printIp(err)
        printData(' ')
        pass

def lookup(event = None):
    try:
        outputData = ''
        searchStr = ipStr.get()
        with open('./conf/history.txt', 'r') as historyFile:
            if not searchStr in historyFile.read():
                with open('./conf/history.txt', 'a') as historyFile:
                    historyFile.write(searchStr + '\n')
                    historyFile.close()
        maxPage.set('/?')
        results = api.host(searchStr)
        for result in results:
            if 'data' != result:
                parsedFinal = "%s: %s\n" % (result.title(), results[result])
                outputData += parsedFinal.translate({ord(i): None for i in "[]'"})
        printData(outputData)
        printIp(ipStr.get())
    except Exception as err:
        if searchStr == '':
            printIp('Empty search query')
            printData(' ')
        else:
            printIp(err)
            printData(' ')
        pass

def saveResults():
    result = messagebox.askquestion('Export', 'Do you want to save the results to the export folder?', icon = 'info')
    if result == 'yes':
        if ipChk.get() == '1':
            print('jou')
            with open('./export/IPExport-' + str(datetime.datetime.now().strftime('%d.%m.%y_%H-%M-%S')) + '.txt', 'w') as IPExportfile:
                IPExportfile.write('--Dump from shodan tool V3--\n\n' + ipText.get('1.0', END))
                IPExportfile.close()
        else:
            None
        if dataChk.get() == '1':
            with open('./export/DATAExport-' + str(datetime.datetime.now().strftime('%d.%m.%y_%H-%M-%S')) + '.txt', 'w') as DATAExportfile:
                DATAExportfile.write('--Dump from shodan tool V3--\n\n' + dataText.get('1.0', END))
                DATAExportfile.close()
        else:
            None

def historyUpdate():
    with open('./conf/history.txt', 'r') as historyFile:
        history = historyFile.read().split('\n')
        del history[len(history)-1]
        history = list(reversed(history))
        ipEntry.config(values=history)
        historyFile.close()

with open('./conf/history.txt', 'r') as historyFile:
    history = historyFile.read().split()
    historyFile.close()
    

keyFileCheck()

ipLabel = Label(window, text = 'Query or IP', width = 11)
ipLabel.grid(row = 0, column = 0)

ipStr = StringVar(window)
ipEntry = Combobox(window, textvariable = ipStr, values = history, postcommand = historyUpdate)
ipEntry.grid(row = 0, column = 1)

ipEntry.focus()

pageLabel = Label(window, text = 'Page :')
pageLabel.grid(row = 0, column = 2)

pageStr = StringVar(window)
pageCount = Entry(window, textvariable = pageStr, width = 6)
pageCount.grid(row = 0, column = 3)

pageStr.set('1')

maxPage = StringVar(window)
maxLabel = Label(window, textvariable = maxPage, width = 12)
maxLabel.grid(row = 0, column = 4)

maxPage.set('/?') 

searchButton = Button(window, text = 'Search', command = search, width = 9)
searchButton.grid(row = 0, column = 5, padx = 5)

lookupButton = Button(window, text = 'Lookup', command = lookup, width = 9)
lookupButton.grid(row = 0, column = 6)

ipChk = StringVar(window)
ipSave = Checkbutton(window, text = 'IP', variable = ipChk)
ipSave.grid(row = 0, column = 7)

dataChk = StringVar(window)
dataSave = Checkbutton(window, text = 'Data', variable = dataChk)
dataSave.grid(row = 0, column = 8)

saveButton = Button(window, text = 'Save results', command = saveResults, width = 11)
saveButton.grid(row = 0, column = 9)

clearHistory = Button(window, text = 'Clear history', command = clearHistoryBox, width = 11)
clearHistory.grid(row = 0, column = 10)

setapiButton = Button(window, text = 'Set API key', command = saveKey, width = 11)
setapiButton.grid(row = 0, column = 11)

ipText = tkscrolled.ScrolledText(window, state = DISABLED, width = 48, height = 37)
ipText.grid(row = 1, column = 0, columnspan = 8, sticky = W)

dataText = tkscrolled.ScrolledText(window, state = DISABLED, width = 48, height = 37)
dataText.grid(row = 1, column = 1, columnspan = 11, sticky = E)

printIp('Welcome to shdoan tool V3!\nMade by: Lohiv\nCredits to: Omso\n\nTo get started check the link below for help.\nhttps://danielmiessler.com/study/shodan/')
printData('Press "Search" to search the shodan database.\nPress "lookup" to check ports.\nPress "Save results" to export.\n(Use the checkboxes to select exported data).\nPress "Clear history" to delete the history.\nPress "Set API key" to set a new key for shodan.\n\nUse Enter to search normally\nUse Shift+Enter to do a lookup')

window.bind('<Return>', search)
window.bind('<Shift-Return>', lookup)

window.mainloop()