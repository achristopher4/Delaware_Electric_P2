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
            menu = 'Main Menu:\n\t1: Insert Test Value\n\t2: Find Test Value\n\t3: Modify value\n\t4: Delete Value \n\t0: Exit'
            while user_choice != '0':
                print(menu)
                user_choice = input('Select Option: ')
                if user_choice == '1':
                    ## Insert Test Value
                    table = input('Enter Table: ')
                    a = self.get_attributes(table)
                    print(a)
                elif user_choice == '2':
                    ## Find test value
                    table = input('Enter Table: ')
                    Attributes = None
                    Where = None
                    Order = None
                    if Attributes == None and Where == None and Order == None:
                        self.print_sql(self.find(table))
                    else:
                        self.find(table, Attributes, Where, Order)
                elif user_choice == '3':
                    ## Modify Value
                    break
                elif user_choice == '4':
                    ## Delete Value
                    a = self.delete('Employee', 'Employee_ID', 'EMP000002')
                    print(a)
                self.commit_database()
                print()
        finally:
            self.close_database()
            print('\nGoodbye')


CLMain()
