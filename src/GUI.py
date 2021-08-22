## This is a testing document to display output for specific inputs
## Author: Alexander Christopher
## Date: 07/27/2021

from Backend import DatabaseController
import os
import sqlite3
import datetime
from sqlite3 import Error


class Main(GUIMain):
    def __init__(self):
        """ Initialize class objects. """
        DatabaseController.__init__(self)
        try:
            self.commit_database()
        finally:
            self.close_database()
            print('\nGoodbye')


Main()
