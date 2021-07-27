## This is a testing document to test output for specific inputs
## Author: Alexander Christopher
## Date: 07/27/2021

from CLBackend import DatabaseController
import os
import sqlite3
import datetime
from sqlite3 import Error


class CLMain(DatabaseController):
    def __init__(self):
        """ Initialize class objects. """
        DatabaseController.__init__(self)
        try:
            user_choice = ''
            print('')
            menu = 'Main Menu:\n \n\t0: Exit'
            while user_choice != '0':
                print(menu)
                user_choice = input('Select Option: ')
                print()
        finally:
            self.close_database()
            print('\nGoodbye')


CLMain()
