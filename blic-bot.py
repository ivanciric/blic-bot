import requests
import json
import urllib
import urllib2
import random
import time
import Tkinter


class blicbot_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
    self.parent = parent
    self.initialize()

    def initialize(self):
        self.grid()

    #entry
    self.discVariable = Tkinter.StringVar()
        self.entryDisc = Tkinter.Entry(self,
                    textvariable=self.discVariable)
        self.entryDisc.grid(column=0, row=0, columnspan=2, sticky='EW')
    #self.entryDisc.bind("<Return>", self.OnPressEnter)
    self.discVariable.set("disc_id")
    #entry

    #entry
    self.entryIdVariable = Tkinter.StringVar()
        self.entryEntryId = Tkinter.Entry(self,
                    textvariable=self.entryIdVariable)
        self.entryEntryId.grid(column=0, row=1, columnspan=2, sticky='EW')
    self.entryIdVariable.set("entry_id")
    #entry

    #entry
    self.typeVariable = Tkinter.StringVar()
        self.entryType = Tkinter.Entry(self,
                    textvariable=self.typeVariable)
        self.entryType.grid(column=0,row=2, columnspan=2, sticky='EW')
    self.typeVariable.set("1")
    #entry

    #entry
    self.votesVariable = Tkinter.StringVar()
        self.entryVotes = Tkinter.Entry(self,
                    textvariable=self.votesVariable)
        self.entryVotes.grid(column=0,row=3, columnspan=2, sticky='EW')
    self.votesVariable.set("15")
    #entry

    #label
        self.labelVariable = Tkinter.StringVar()
    label = Tkinter.Label(self,
                textvariable=self.labelVariable,
                wraplength=160,
                anchor="nw",fg="white",bg="black",
                )
        label.grid(column=0, row=4, rowspan=2, columnspan=2, sticky='EWNS')
    self.labelVariable.set("Status...")
    #label

    #button
    button = Tkinter.Button(self,
                text="Glasaj",
                command=self.OnButtonClick)
        button.grid(column=0,row=6)
    #button

    """
    #button
    stopButton = Tkinter.Button(self,
                text="Prekini",
                command=self.OnStopButtonClick)
        stopButton.grid(column=1,row=6)
    #button
    """

    #label
        self.copyrightVariable = Tkinter.StringVar()
    copyrightLabel = Tkinter.Label(self,
                textvariable=self.copyrightVariable,
                font=("Helvetica", 8, "italic"),
                anchor="center",fg="black")
        copyrightLabel.grid(column=0, row=7, columnspan=2, sticky='EWNS')
    self.copyrightVariable.set(u"\N{COPYRIGHT SIGN}2016, Hamato Yoshi")
    #label


    self.grid_columnconfigure(0,weight=1)
    self.grid_rowconfigure(4,weight=2)
    self.resizable(True,True)
    self.update()
        #self.geometry(self.geometry())
    self.geometry('300x160')

    self.entryDisc.focus_set()
        self.entryDisc.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
    self.running = True
    self.ExecuteVoting()

    def OnStopButtonClick(self):
    self.stop()

    def stop(self):
        self.running = False

    """
    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryIdVariable.get()")
    """


    def ExecuteVoting(self):

    if(self.running == True):
        url = 'http://events.ocdn.eu/v2/etag?_ac=events'
        payload = {
            "Host": "events.ocdn.eu",
            "Connection": "keep-alive",
            "Content-Length": 129,
            "Origin": "https://www.blic.rs",
            "Referer": "http://www.blic.rs/forum/tvrava-evropa-demonstracije-u-istonoj-evropi-poljs,2,2598909,0,czytaj-najnowsze.html",
            "Cookie": ""
        }


        num_votes = self.votesVariable.get()

        for i in range(1, int(num_votes) + 1):

            self.labelVariable.set("Glas br. " + str(i) + ": pokusavam...")
            self.update()

            try:
                r = requests.get(url, data=json.dumps(payload), headers=payload)
            except requests.exceptions.RequestException as e:
                self.labelVariable.set("Greska... Zabelezeno " + str(i) + " glasova do sad. Pokrenite proces ponovo.")


            j_data = json.loads(r.content)
            tckt = j_data['eaUUID']
            comm_payload = {
                'disc_id': self.discVariable.get(),
                'entry_id': self.entryIdVariable.get(),
                'ticket': tckt,
                'vote': self.typeVariable.get()
            }

            url_vote = 'http://www.blic.rs/forum/addvoteup.json'
            if(self.typeVariable.get() == '-1'):
                url_vote = 'http://www.blic.rs/forum/addvotedown.json'

            data = urllib.urlencode(comm_payload)

            try:
                req = urllib2.Request(url_vote, data)
                response = urllib2.urlopen(req)
            except urllib2.HTTPError, e:
                self.labelVariable.set('Greska - %s.' % e.code)

            self.labelVariable.set("Glas br. " + str(i) + ": OK")
            self.update()

            time.sleep(random.randint(1,4))

        self.labelVariable.set("Glasanje zavrseno.")
        self.update()

    else:
        self.labelVariable.set("Glasanje prekinuto.")
        self.update()



if __name__ == "__main__":
    app = blicbot_tk(None)
    app.title('BlicBot')
    app.mainloop()