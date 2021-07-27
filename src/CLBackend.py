## This is a testing document to test general code functions to interface with the database
## Author: Alexander Christopher
## Date: 07/27/2021

import os
import sqlite3
import datetime
from sqlite3 import Error

class DatabaseControl:
    def __init__(self):
        """ """
        path = '/Users/alexchristopher/Desktop/Intern_Projects/Delaware_Electric'
        self.__DBName = 'DE_Main'
        self.__conn = sqlite3.connect(self.__DBName) # create new database
        self.__cur = self.__conn.cursor()   # Save the database in current working directory

    def commit_database(self):
        """ Save changes to database. """
        self.__conn.commit()

    def get_database(self):
        """ Return the object holding the database. """
        return self.__c

    def close_database(self):
        """ Close the database. """
        self.__conn.close()

    def basic_execute(self, sql, **kargs):
        """ Execute a basic sql statement. """
        return

    def complex_execute(self, sql, **kargs):
        """ Execute a sql statement with any addition values if necessary. """
        return

    def get_prefix(self, ID):
        """ Get the prefix of the primary key. """
        return

    def create_newID(self, table):
        """ Create a new unique ID for a table """
        return

    def insert(self, table, **preset_attributes):
        """ Insert new value into a specified table with preset attributes if provided. """
        return

    def insert_weak(self, table, ID, **preset_attributes):
        """ Insert new value into a specified weak table with preset attributes if provided. """
        return

    def find(self, table, **additional):
        """ Search a specified table with any"""
        return

    def find_weak(self):
        """ """
        return

    def delete(self):
        """ Delete an item from a table. """
        return

    def delete_weak(self, table, ID):
        """ Delete linked value(s) from a weak entity. """
        return

    def modify_value(self):
        """ Modify a specific value.  """
        return

    def modify_weak_value(self):
        """ Modify a value and all weak values if applicable. """
        return

    def value_exists(self):
        """ Return True if a value exists with specified attribute values or False if it does not. """
        return

    def count_results(self):
        """ Return the number of results that are returned from query. """
        return
