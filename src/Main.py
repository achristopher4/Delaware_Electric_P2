## Author: Alexander Christopher
## Date: 08/22/20218

from Backend import DatabaseController
from GUI import *
import os
import sqlite3
import datetime
from tkinter import *
from tkmacosx import *
from sqlite3 import Error


class GUIMain(DatabaseController):
    def __init__(self):
        """ Initialize class objects. """
        DatabaseController.__init__(self)
        root = Tk()
        root.title("Welcome to Delaware Electric")

    def create_entry(self):
        """ """
        return

    def create_label(self):
        """ """
        return

    def create_grid(self):
        """ """
        return

    def create_button(self):
        """ """
        return
