#Created by robytoby154, amino.py provided by Slimakoi

#Modules

from tkinter import *
from tkinter import messagebox
import time
import re
from tkinter import ttk

#Variables

chatids = {}
count = 1
selectedchatids = ""
x = 0

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
        checkmsg(data)
        self.listbx.insert(END, msgstr)
        self.listbx.select_set(END)
        self.listbx.yview(END)

#Functions

def checkmsg(data): #Message is put through algorithm
    userid = data.message.author.userId
    nickname = data.message.author.nickname
    content = data.message.content

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
        global chatbx
        chatbx.AddNew(data)

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

gui.mainloop()
