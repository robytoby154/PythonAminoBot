#Created by robytoby154, amino.py provided by Slimakoi

#Modules

from tkinter import *
from tkinter import messagebox
import time
import re
from tkinter import ttk

#Variables
basecommands = [["help", "?", "h", "cmd", "commands", "cmds", "list"], ["uptime", "ontime", "runtime", "ut", "ot", "rt"]]
chatids = {}
count = 1
selectedchatids = ""
x = 0
cmdprefix = "!"
livecmdupdate = False
commandslist = []
startingtime = time.time()

#Loading

gui = Tk()
gui.geometry("350x150")
gui.title("Please wait...")
gui.update()

try:
    import amino
    client = amino.Client()
except:
    messagebox.showerror("Uh oh...", "Something went wrong with the Amino api")
    gui.destroy()
    raise ValueError("Could not refer to amino module / api")

#Commands Class

class COMMANDS():
    def __init__(self, cmd, temprsp = "", *k):
        self.temprsp = temprsp
        basecmds = {"custom" : self.customfnc, "help" : self.helpfnc, "uptime" : self.uptimefnc}
        basecmds[cmd](*k)

    def customfnc(self, *k):
        send_msg(self.temprsp)
        
    def helpfnc(*k):
        counter = 1
        tempstr = "Commands prefix: " + cmdprefix + "\n[bu]Base Commands:\n"
        for x in range(len(basecommands)):
            tempstr += str(counter) + ". " + basecommands[x][0] + " : "
            for z in range(len(basecommands[x])):
                tempstr += basecommands[x][z] + ", "
            tempstr += "\n"
            counter += 1
        tempstr += "[bu]Custom Commands:\n"
        counter = 1
        for x in range(len(commandslist)):
            tempstr += str(counter) + ". " + commandslist[x][0] + "\n"
            counter += 1
        counter = 1
        send_msg(tempstr)

    def uptimefnc(*k):
        send_msg("Bot has been active for " + str(round(((time.time() - startingtime)/60), 3)) + " minutes")

#ChatId Button Class

class chatnamebtn:
    def __init__(self, parent, txt, **k):
        self.parent = parent
        self.txt = txt
        self.newbtn()
    def newbtn(self):
        btn = Button(self.parent, text = self.txt)
        btn.config(command = self.txtshow)
        btn.pack()
    def txtshow(self):
        global selectedchatids
        selectedchatids = str(chatids[self.txt])

#Chat Scroll Class

class chatbox:
    def __init__(self, parent):
        global x
        frame = Frame(parent, width=750, height=450, bd=1)
        frame.pack()
        self.listbx = Listbox(frame, height=12, width = 50)
        self.listbx.pack(side=LEFT,fill=Y)
        self.scrollbr = Scrollbar(frame) 
        self.scrollbr.pack(side=RIGHT, fill=Y)
        self.listbx.config(yscrollcommand = self.scrollbr.set)
        self.scrollbr.config(command = self.listbx.yview)
        x = 2
    def AddNew(self, data):
        msgstr = str(f"{data.message.author.nickname}: {data.message.content}")
        try:
            self.listbx.insert(END, msgstr)
            self.listbx.select_set(END)
            self.listbx.yview(END)
        except:
            x = 2

#Functions

def send_msg(msg):
    subclient = amino.SubClient(comId = selectedchatids[:selectedchatids.find(":::")], profile = client.profile)
    subclient.send_message(message = msg, chatId = selectedchatids[selectedchatids.find(":::") + 3:])

def readcommands(*k):
    try:
        commandslist = []
        with open("Commands.csv", "r") as cmdsfile:
            content = cmdsfile.readlines()
            counter = 1
            for x in range(len(content)):
                try:
                    CmdID = int(content[x][0:int(content[x].find(","))])
                    index1 = content[x].find(",")
                    index2 = content[x].find(",", index1 + 1)
                    index3 = content[x].find(",", index2 + 1)
                    if CmdID == counter:
                        counter += 1
                        newcmd = [str(content[x][index1+1:index2]),str(content[x][index2+1:index3]),str(content[x][index3+1:len(content[x])-1])]
                        commandslist.append(newcmd)
                except:
                    continue
    except:
        commandslist = []
    return commandslist

def checkmsg(data): #Message is put through algorithm
    global chatbx, commandslist, livecmdupdate
    userid = data.message.author.userId
    nickname = data.message.author.nickname
    msgchatid = data.message.chatId
    if str(msgchatid) == selectedchatids[selectedchatids.find(":::") + 3:]:
        chatbx.AddNew(data)
        tempflag = False
        cmd = ""
        temprsp = ""
        msg = data.message.content
        if livecmdupdate == True:
            commandslist = readcommands()
        if msg[0] != cmdprefix:
            return
        try:
            for x in range(len(basecommands)):
                if tempflag == False:
                    for z in range(len(basecommands[x])):
                        if str(msg[1:].lower()) == str(basecommands[x][z].lower()) and tempflag == False:
                            cmd = basecommands[x][0]
                            tempflag = True
                            break
            try:
                if tempflag == False:
                    for x in range(len(commandslist)):
                        if commandslist[x][2][0] == "0":
                            if commandslist[x][0].lower() == msg[1:].lower():
                                tempflag = True
                        else:
                            if commandslist[x][0] == msg[1:]:
                                tempflag = True
                        if tempflag == True:
                            temprsp = commandslist[x][1]
                            cmd = "custom"
                            break
            except:
                raise ValueError("Commands Error")
            if tempflag == True:
                COMMANDS(cmd, temprsp)
        except:
            print("Message was unreadable")

def exp_con():
    global canvas, expconbtn, x
    if x == 2:
        if expconbtn.cget("text") == ">>":
            for x in range(15):
                canvas.config(width = 180 - (5 * x) + 5)
                cnv.place(x = 245 + (5 * x), y = 100)
                chatcnv.place(x = -70 + (5 * x), y = 115)
                gui.update()
            expconbtn.config(text = "<<")
        else:
            for x in range(15):
                canvas.config(width = 105 + (5 * x) + 5)
                cnv.place(x = 320 - (5 * x), y = 100)
                chatcnv.place(x = 5 - (5 * x), y = 115)
                gui.update()
            expconbtn.config(text = ">>")
        x = 2

def listchats():
    global cnv, canvas, gui, expconbtn, chatbx, x, chatcnv
    expconbtn = Button(gui, text = ">>", command = exp_con)
    expconbtn.place(x = 420, y = 45)
    gui.update()
    canvas = Canvas(cnv, width = 180, height = 225)
    scrollbar = ttk.Scrollbar(cnv, orient = "vertical", command = canvas.yview)
    cnv.scrollable_frame = ttk.Frame(canvas)

    cnv.scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion = canvas.bbox("all")
            )
        )
    canvas.create_window((0, 0), window = cnv.scrollable_frame)

    canvas.configure(yscrollcommand = scrollbar.set)

    canvas.pack(side = "left", expand = True)
    scrollbar.pack(side = "right", fill = "y")

    subclients = client.sub_clients()
    try:
        for name, id in zip(subclients.name, subclients.comId):
            try:
                comcheck = cleanse_word(name)
                curcomid = id
                ttk.Label(cnv.scrollable_frame, text=comcheck).pack()
                subclient = amino.SubClient(comId = str(id), profile = client.profile)
                chats = subclient.get_chat_threads()
                gui.update()
            except:
                x = 1
            for name, id in zip(chats.title, chats.chatId):
                try:
                    wrdcheck = cleanse_word(name)
                    c = chatnamebtn(parent = cnv.scrollable_frame, txt = wrdcheck)
                    tempid = str(curcomid) + ":::" + str(id)
                    chatids[wrdcheck] = tempid
                    gui.update()
                except:
                    x = 1
    except:
        x = 1
    chatcnv = Canvas(gui)
    chatcnv.place(x = -70, y = 115)
    chatbx = chatbox(parent = chatcnv)
    gui.update()

def cleanse_word(text):
    global count
    try:
        regex = r"(\w|\s)*"
        matches = re.finditer(regex, text, re.DOTALL)
        newstr = ''
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            newstr = newstr + match.group()
    except:
        newstr = "Unidentified: " + str(count)
        count += 1
    return newstr

def login():
    global client, gui, accountnamelbl
    try:
        client.login(email = emailent.get(), password = passwordent.get())
        accountnamelbl = Label(gui, text = "Logged into: " + client.profile.nickname).place(x = 225, y = 5)
        disable(loginbtn)
        disable(emailent)
        passwordent.config(show = "*")
        disable(passwordent)
        shbtn.config(text = "Show")
        disable(shbtn)
        gui.update()
        listchats()
    except:
        loginbtn.config(text = "Invalid")
        gui.update()
        time.sleep(1.25)
        loginbtn.config(text = "Login")

def disable(obj):
    obj.config(state = "disabled")

def enable(obj):
    obj.config(state = "normal")

def sh():
    if shbtn.cget("text") == "Show":
        passwordent.config(show = "")
        shbtn.config(text = "Hide")
    else:
        passwordent.config(show = "*")
        shbtn.config(text = "Show")

#When Message is recieved

@client.callbacks.event("on_text_message")
def on_text_message(data):
    global x
    if x == 2:
        checkmsg(data)

#GUI Construction

gui.geometry("450x350")
gui.update()
gui.resizable(height = False, width = False)
gui.title("Amino Bot Account Information")
try:
    gui.iconbitmap("AminoIcon.ico")
except:
    x = 0
loginbtn = Button(gui, text = "Login", command = login)
loginbtn.place(x = 135, y = 55)
emaillbl = Label(gui, text = "Email :")
emaillbl.place(x = 26, y = 5)
passwordlbl = Label(gui, text = "Password :")
passwordlbl.place(x = 5, y = 25)
emailent = Entry(gui, width = 23)
emailent.place(x = 75, y = 7)
passwordent = Entry(gui, width = 23, show = "*")
passwordent.place(x = 75, y = 27)
shbtn = Button(gui, text = "Show", bg = "white", borderwidth = 1, command = sh)
shbtn.place(x = 225, y = 25)
cnv = Canvas(gui)
cnv.place(x = 250, y = 100)
commandslist = readcommands()

gui.mainloop()
