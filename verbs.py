from tkinter import *
from random import choice, randrange
from winsound import *
import codecs
import tkinter.font as font
import configparser

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.honorifics = ["Informal Low Respect", "Informal High Respect", "Formal Low Respect", "Formal High Respect"]
        self.tenses = ["Past", "Present", "Future"]              
        self.korean_words = []
        self.english_words = []
        with codecs.open('dictionary.txt', 'r+', 'UTF-8') as f:
            for line in f:
                words = line.split(":")
                self.korean_words.append(words[0])
                self.english_words.append(words[1].rstrip())
            if self.korean_words[0][0]=="\ufeff": #this line is to fix a weird bug
                self.korean_words[0] = self.korean_words[0][1:]
        assert len(self.korean_words) == len(self.english_words)
        self.used = [""]
        self.myfont = font.Font(family='Helvetica', size=24)
        
        self.korean_label = Label(self, font = self.myfont)
        self.honorific_label = Label(self, font = self.myfont)
        self.tense_label = Label(self, font = self.myfont)
        self.english_button = Button(self, text = "Meaning?", command = self.show_korean, font = self.myfont, underline = 0)
        self.next_button = Button(self, text = "Next word", command = self.next_word, font = self.myfont, underline = 0)
        self.klabel = Label(self, text = "Verb/Adjective:", font = self.myfont)
        self.hlabel = Label(self, text = "Honorific level:", font = self.myfont)
        self.tlabel = Label(self, text = "Tense:", font = self.myfont)
        self.english_label = Label(self, font = self.myfont)
        self.count = -1 #really dumb
        self.count_label = Label(self, text = "Words conjugated: " + str(self.count), font = self.myfont)
        self.next_word()
        
        self.klabel.grid(row = 0, column = 0, sticky = W)
        self.hlabel.grid(row = 1, column = 0, sticky = W)
        self.tlabel.grid(row = 2, column = 0, sticky = W)
        self.korean_label.grid(row = 0, column = 1, sticky = W)
        self.honorific_label.grid(row = 1, column = 1, sticky = W)
        self.tense_label.grid(row = 2, column = 1, sticky = W)
        self.english_button.grid(row = 3, column = 0, sticky = W)
        self.english_label.grid(row = 3, column = 1, sticky = W)
        self.next_button.grid(row = 4, column = 0, sticky = W)
        self.count_label.grid(row = 4, column = 1, sticky = W)

    def next_word(self):
        #option 1
        """self.honorific_label["text"] = choice(self.honorifics)
        self.tense_label["text"] = choice(self.tenses) + " Tense" """

        #option 2
        code = ""
        while code in self.used:
            ind = randrange(0, 12)
            i = randrange(len(self.korean_words))
            code = str(ind) + "-" + str(i)
        self.used.append(code)
        self.honorific_label["text"] = self.honorifics[randrange(12) % 4]
        self.tense_label["text"] = self.tenses[randrange(12) // 4]       

        self.count += 1
        self.count_label["text"] = "Words conjugated: " + str(self.count)
        self.korean_label["text"] = self.korean_words[i]
        self.english_label["text"] = ""
        self.english = self.english_words[i]
        
        
    def show_korean(self):
        if self.english_label["text"] == "":
            self.english_label["text"] = self.english
        else:
            MessageBeep(MB_OK)

    def next_word_event(self, event):
        self.next_word()

    def show_korean_event(self, event):
        self.show_korean()

def go():
    root = Tk()
    root.title("Conjugation Time!")
    root.geometry("600x280")
    app = Application(root)
    app.bind_all("n", app.next_word_event)
    app.bind_all("m", app.show_korean_event)
    root.mainloop()

go()
