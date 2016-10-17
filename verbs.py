from tkinter import *
from random import choice, randrange
from pygame import mixer
import codecs
import configparser
import sys
import time
import tkinter.font as font

class Application(Frame):

    def __init__(self, master):
        """Creates the structure and functionality of the application.

        Args:
        master -- the window for the Application
        """
        Frame.__init__(self, master)
        self.honorifics = ["Informal Low Respect", "Informal High Respect", "Formal Low Respect", "Formal High Respect"]
        self.tenses = ["Past", "Present", "Future"]
        self.used = [""]
        self.myfont = font.Font(family='Helvetica', size=24)

        # Reads the dictionary file into lists of words.
        self.korean_words = []
        self.english_words = []
        with codecs.open('dictionary.txt', 'r+', 'UTF-8') as f:
            for line in f:
                words = line.split(":")
                self.korean_words.append(words[0])
                self.english_words.append(words[1].rstrip())
            # Fixes an encoding problem that occurs with UTF-8.
            if self.korean_words[0][0]=="\ufeff":
                self.korean_words[0] = self.korean_words[0][1:]
        assert len(self.korean_words) == len(self.english_words), \
               "There are a different number of korean and english words."

        # Initialize the sound.
        mixer.init()
        self.alert = mixer.Sound('Funk.wav')

        # Place the app on the grid and create its widgets.
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Creates all of the necessary widgets for the application."""


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

    def beep(self):
        """Plays a beep noise."""
        self.alert.play()

    def next_word(self):
        """Changes the displayed word and updates the window accordingly."""

        """Finds a word and conjugation pair that hasn't been used yet, then add
        it to the list of used pairs."""
        verb_conjugation_pair = ""
        while verb_conjugation_pair in self.used:
            ind = randrange(0, 12)
            i = randrange(len(self.korean_words))
            verb_conjugation_pair = str(ind) + "-" + str(i)
        self.used.append(verb_conjugation_pair)

        """Adds the new word, conjugation, and count, while deleting the old
        english meaning."""
        self.honorific_label["text"] = self.honorifics[randrange(12) % 4]
        self.tense_label["text"] = self.tenses[randrange(12) // 4]
        self.count += 1
        self.count_label["text"] = "Words conjugated: " + str(self.count)
        self.korean_label["text"] = self.korean_words[i]
        self.english_label["text"] = ""
        self.english = self.english_words[i]


    def show_korean(self):
        """Shows the english translation or beeps if it's already displayed."""
        if self.english_label["text"] == "":
            self.english_label["text"] = self.english
        else:
            self.beep()

    def next_word_event(self, event):
        """Calls the next_word method.
        The EVENT paramater is automatically passed in by the bind_all method.
        """
        self.next_word()

    def show_korean_event(self, event):
        """Calls the show_korean method.
        The EVENT paramater is automatically passed in by the bind_all method.
        """
        self.show_korean()


def run():
    """Starts the program."""
    root = Tk()
    root.title("Conjugation Time!")
    root.geometry("600x280")
    app = Application(root)
    app.bind_all("n", app.next_word_event)
    app.bind_all("m", app.show_korean_event)
    root.lift()
    root.mainloop()

run()
