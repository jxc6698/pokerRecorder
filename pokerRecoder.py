#!/usr/bin/python

import os
import sys
from datetime import datetime
import time


from Tkinter import *
from PIL import ImageTk, Image
# file format: win lose deposit withdraw time


class myPoker(object):

    def __init__(self):
        self.money = 0
        self.totalWin = 0
        self.totalDeposit = 0
        self.totalWithdraw = 0
        self.timeMap = {}

################################
# Help function
################################
    def getCurrentTime(self):
        # getcurrenttime datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        return datetime.strftime(datetime.now(), '%Y-%m-%d')

    def getCurrentTimeBydatInInt(self):
        t = datetime.strptime(self.getCurrentTime(),'%Y-%m-%d')
        day = int(time.mktime(t.timetuple()))
        return day

################################
# Help function over
################################

################################
# cmd function
################################

    def deposit(self, data, date):
        with open("data/pokerrecord.txt", "a") as pfile:
            pfile.write("0 0 "+data[1]+" 0 " + self.getCurrentTime())
            pfile.write("\n")

        print self.getCurrentTimeBydatInInt()
        self.inputHandler(0, 0, float(data[1]), 0, self.getCurrentTimeBydatInInt())
        return

    def win(self, data, date):
        with open("data/pokerrecord.txt", "a") as pfile:
            pfile.write(data[1]+" 0 0 0 " + self.getCurrentTime())
            pfile.write("\n")

        self.inputHandler(float(data[1]), 0, 0, 0, self.getCurrentTimeBydatInInt())
        return

    def lose(self, data, date):
        with open("data/pokerrecord.txt", "a") as pfile:
            pfile.write("0 "+data[1]+" 0 0 " + self.getCurrentTime())
            pfile.write("\n")

        self.inputHandler(0, float(data[1]), 0, 0, self.getCurrentTimeBydatInInt())
        return

    def withdraw(self, data, date):
        with open("data/pokerrecord.txt", "a") as pfile:
            pfile.write("0 0 0 "+data[1]+" " + self.getCurrentTime())
            pfile.write("\n")

        self.inputHandler(0, 0, 0, float(data[1]), self.getCurrentTimeBydatInInt())
        return

    def exit(self, data, date):
        sys.exit();

    def check(self, data, other):
        if len(data) == 1:
            self.printCurrentState()
        return

################################
# cmd function over
################################

    def run(self):

        self.loadFile()

        operators = {"deposit": self.deposit,
                     "win": self.win,
                     "lose": self.lose,
                     "withdraw": self.withdraw,
                     "check": self.check,
                     "exit": self.exit}
        while 1:
            try:
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                break


            if not line:
                break
# remove \n character
            line = line[0:-1]
#            print line
            words = line.split(" ")
            cmd = words[0]

            try:
                operators[cmd](words, None)
            except KeyError:
                print "not support"
                break


    def loadFile(self):
        win = 0;
        with open("data/pokerrecord.txt", "r") as pfile:
            for line in pfile:
                if line[-1] == "\n":
                    line = line[0:-1]
                # sys.stdout.write(line)
                # sys.stdout.flush()
                d = line.split(" ")
                print d[4]
# get date in int
                ttime = datetime.strptime(d[4],'%Y-%m-%d')
                day = int(time.mktime(ttime.timetuple()))
                if not day in self.timeMap:
                   self.timeMap[day] = {"win": 0, "lose": 0, "deposit": 0, "withdraw": 0}

                self.inputHandler(float(d[0]), float(d[1]), float(d[2]), float(d[3]), day)

        self.printCurrentState()


    def inputHandler(self, win, lose, deposit, withdraw, day):
        self.money = self.money + win + deposit - lose - withdraw
        self.totalWin = self.totalWin + win - lose
        self.totalDeposit = self.totalDeposit + deposit
        self.totalWithdraw = self.totalWithdraw + withdraw

        thatday = self.timeMap[day]
        thatday["win"] += win
        thatday["lose"] += lose
        thatday["deposit"] += deposit
        thatday["withdraw"] += withdraw

    def printCurrentState(self):

        sys.stdout.write("total money: "+str(self.money))
        sys.stdout.write("\n")
        sys.stdout.write("total win: "+str(self.totalWin))
        sys.stdout.write("\n")
        sys.stdout.write("total deposit: "+str(self.totalDeposit))
        sys.stdout.write("\n")
        sys.stdout.write("total withdraw: "+str(self.totalWithdraw))
        sys.stdout.write("\n")

        return




class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # self.helloLabel = Label(self, text='PokerRecoder')
        # self.helloLabel.pack()

        bm = ImageTk.PhotoImage(Image.open('./images/pokerrecorder_logo.png'))
        self.label2 = Label(self, image = bm)
        self.label2.bm = bm # keep a reference
        self.label2.pack()

        self.contentText = Text(self, height=5)
        self.contentText.pack(padx=2);
        self.contentText.config(highlightbackground="black")

        self.nameInput = Entry(self)
        self.nameInput.pack(side="left")
        self.nameInput.config(highlightbackground="blue")

        OPTIONS = ["win", "lose", "deposit", "withdraw"]
        self.typeOptionMenuV = StringVar(self)
        self.typeOptionMenuV.set(OPTIONS[0])
        self.typeOptionMenu = apply(OptionMenu, (self, self.typeOptionMenuV)+ tuple(OPTIONS))
        self.typeOptionMenu.pack(side="left")

        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack(side="right")
        self.quitButton = Button(self, text='save', command=self.test)
        self.quitButton.pack(side="right")


    def hello(self):
        name = self.nameInput.get() or 'world'
        tkMessageBox.showinfo('Message', 'Hello, %s' % name)

    def test(self):
        self.contentText.insert(INSERT, "insert...")
        self.contentText.insert(END, "end...")
        print self.typeOptionMenuV.get()


################################
# global function
#
# logo generate by http://patorjk.com/software/taag/#p=display&c=bash&f=Big&t=pokerRecorder%0A
# or command line tool like figlet, toliet
#
def Logo():
    str = '''
#                _             _____                        _
#               | |           |  __ \                      | |
#    _ __   ___ | | _____ _ __| |__) |___  ___ ___  _ __ __| | ___ _ __
#   | '_ \ / _ \| |/ / _ \ '__|  _  // _ \/ __/ _ \| '__/ _` |/ _ \ '__|
#   | |_) | (_) |   <  __/ |  | | \ \  __/ (_| (_) | | | (_| |  __/ |
#   | .__/ \___/|_|\_\___|_|  |_|  \_\___|\___\___/|_|  \__._|\___|_|
#   | |
#   |_|
    '''
    print str


if __name__ == "__main__":
    Logo()
    myPoker().run()
    app = Application()
    app.master.title('pokerRecoder')
# main message loop
#    app.mainloop()

