## This is a testing document to test general code functions to interface with the database
## Author: Alexander Christopher
## Date: 07/27/2021

import os
import sqlite3
import datetime
from sqlite3 import Error
from Search import BinarySearch

    ### Notes to self:
        ### Make sure to call non-kargs by argument name when calling function and give name to kargs
            ## EX: test(t1 = 4, name = "Alex")

class DatabaseController:
    def __init__(self):
        """ """
        path = os.getcwd()
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

    def print_sql(self, sql):
        """ Print sql objects to command line. """
        for line in sql: print(line)

    def get_attributes(self, table):
        """ Return the attributes of a table. """
        attributes = []
        for x in self.__cur.execute('PRAGMA TABLE_INFO({})'.format(table)): attributes.append(x)
        return attributes

    def basic_execute(self, sql):
        """ Execute a basic sql statement. """
        return self.__cur.execute(sql)

    def value_dependent_execute(self, sql, *values):
        """ Execute a sql statement with any addition values if necessary. """
        return self.__cur.execute(sql, values)

    def get_prefix(self, table):
        """ Get the prefix of the primary key. """
        dic = {'Employee':'EMP', 'Sales':'SAL', 'Job':'JOB', 'Task':'RJT', 'Client':'CLI', 'Campus':'CAM', 'Manager':'MAN',
        'Employee_Photo':'PEM', 'Supplier':'SUP', 'Inventory':'INV', 'Inventory_Photo':'PIN', 'Equipment':'EQU', 'Equipment_Photo':'PEQ',
        'Task_Photo':'PJT', 'Employee_Time_Clock':'TCE'}
        return dic[table] if table in dic else None

    def create_newID(self, table):
        """ Create a new unique ID for a table """
        element = (self.basic_execute(f'SELECT MAX({table}_ID) FROM {table}')).fetchone()
        if element == None:
            return self.get_prefix(table) + '1'.zfill(6) if self.get_prefix(table) != None else None
        else:
            ##
            ##
            return self.get_prefix(table) + element[:] if self.get_prefix(table) != None else None

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
