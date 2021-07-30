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
        table_prefix = self.get_prefix(table)
        if element == None:
            return table_prefix + '1'.zfill(6) if table_prefix != None else None
        else:
            return table_prefix + str(int(element[len(table_prefix):]) + 1).zfill(6) if table_prefix != None else None

                            ## Need to fix argument default values
    def insert(self, table, user_value = None, preset_attribute_value = None):
        """ Insert new value into a specified table with preset attributes if provided. """
        table_attributes = self.get_attributes(table)
        sql = f'INSERT INTO {table} ('
        attributes = ''
        placeholder_values = ') VALUES (?, '
        values = []
        preset_keys = preset_attribute_value.keys()
        user_keys  = user_value.keys()
        for x in range(len(table_attributes)):
            if table_attributes[x][1] in preset_keys:
                ## Take value from preset_attributes
                if preset_attribute_value[table_attributes[x][1]] == None:
                    ## Add None to values
                    values.append(None)
                elif table_attributes[x][2] == 'TEXT':
                    ## Add TEXT to values
                    try:
                        values.append(preset_attribute_value[table_attributes[x][1]])
                    except:
                        values.append(None)
                elif table_attributes[x][2] == 'INT':
                    ## Add INT to values
                    try:
                        values.append(int(preset_attribute_value[table_attributes[x][1]]))
                    except:
                        values.append(None)
                elif table_attributes[x][2] == 'REAL':
                    ## Add REAL to values
                    try:
                        values.append(float(preset_attribute_value[table_attributes[x][1]]))
                    except:
                        values.append(None)
                elif table_attributes[x][2] == 'DATE':
                    ## Add DATE to values if requirements are met
                    if preset_attribute_value[table_attributes[x][1]] != None:
                        ## Add given value to values
                        values.append(preset_attribute_value[table_attributes[x][1]])
                    elif table_attributes[x][1] in ('Start_Date', 'Purchase_Date', 'Date_Purchased'):
                        ## Add current DATETIME to values
                        values.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
                    elif 'Year' in preset_keys:
                        ## Add current year
                        values.append((datetime.datetime.now()).strftime("%Y"))
                    elif 'Week' in preset_keys:
                        # Add current week
                        values.append(str((datetime.date.today())[1]))
                    elif 'Day' in preset_keys:
                        # Add Current day
                        values.append((datetime.datetime.now()).strftime("%d"))
                    elif 'Start_Time' in preset_keys:
                        # add current time
                        values.append((datetime.datetime.now()).strftime("%H:%M:%S"))
                    else:
                        ## Add NONE to values
                        values.append(None)
                elif table_attributes[x][2] == 'BLOB':
                    ## Add BLOB to values
                    try:
                        values.append(preset_attribute_value[table_attributes[x][1]])
                    except:
                        values.append(None)
                else:
                    ## Default to None
                    values.append(None)
            elif table_attributes[x][1] in user_keys:
                ## Take value from user input
                if user_value[table_attributes[x][1]] == None:
                    ## Add None to values
                    values.append(None)
                elif table_attributes[x][2] == 'TEXT':
                    ## Add TEXT to values
                    try:
                        values.append(user_value[table_attributes[x][1]])
                    except:
                        values.append(None)
                elif table_attributes[x][2] == 'INT':
                    ## Add INT to values
                    try:
                        values.append(int(user_value[table_attributes[x][1]]))
                    except:
                        values.append(None)
                elif table_attributes[x][2] == 'REAL':
                    ## Add REAL to values
                    try:
                        values.append(float(user_value[table_attributes[x][1]]))
                    except:
                        values.append(None)
                elif table_attributes[x][2] == 'DATE':
                    ## Add DATE to values if requirements are met
                    if user_value[table_attributes[x][1]] != None:
                        ## Add given value to values
                        values.append(user_value[table_attributes[x][1]])
                    else:
                        ## Add NONE to values
                        values.append(None)
                elif table_attributes[x][2] == 'BLOB':
                    ## Add BLOB to values
                    try:
                        values.append(user_value[table_attributes[x][1]])
                    except:
                        values.append(None)
                else:
                    ## Default to None
                    values.append(None)
            else:
                ## Add None as there is no give input directive
                values.append(None)
            attributes += f'{table_attributes[x][1]}, '
            placeholder_values += '?, '
        attributes = attributes[:-2]
        placeholder_values = placeholder_values[:-2] + ')'
        sql += attributes + placeholder_values
        try:
            self.__cur.execute(sql, tuple(values))
            self.__conn.commit()
            return True
        except:
            return False

    def insert_weak(self, table, ID, user_value=None, preset_attributes=None):
        """ Insert new value into a specified weak table with preset attributes if provided. """
        return

    def find(self, table, **additional):
        """ Search a specified table with any. Attributes key: Exact Name of desired attribute. Where key: Index of attribute in get_attributes function. Order key: list, index 0 is the values, index 1 is the descending option if requested."""
        table_attributes = self.get_attributes(table)
        sql = 'SELECT '
        if len(additional) == 0:
            ## The most general search of a table
            return self.__cur.execute(sql + f'* FROM {table}')
        if 'Attributes' in additional:
            ## Add desired attributes to query
            sql += ', '.join(additional['Attributes']) + f' FROM {table} '
        else:
            ## Default to all attributes if attributes not in additional
            sql += f'* FROM {table} '
        if 'Where' in additional:
            ## Add where and all specified search clause(s) to query
            query = []
            for index in additional['Where']:
                if table_attributes[index[0]][2] == 'TEXT':
                    ## Text search query
                    query.append(f"{table_attributes[index[0]][1]} == '{index[1]}'")
                elif table_attributes[index[0]][2] == 'INT':
                    ## Int search query
                    query.append(f"{table_attributes[index[0]][1]} == {int(index[1])}")
                elif table_attributes[index[0]][2] == 'REAL':
                    ## Real search query
                    query.append(f"{table_attributes[index[0]][1]} == {float(index[1])}")
                elif table_attributes[index[0]][2] == 'BLOB':
                    ## Blob search query
                    query.append(f"{table_attributes[index[0]][1]} == {index[1]}")
                elif table_attributes[index[0]][2] == 'NULL':
                    ## Null search query
                    query.append(f"{table_attributes[index[0]][1]} == {index[1]}")
                else:
                    ## No type given
                    e = 0
            sql += 'WHERE ' + ' AND '.join(query)
        if 'Order' in additional:
            ## The most genreal search of a table, but the query results are ordered
            if len(additional['ORDER']) == 1:
                sql += f' ORDER {additional['ORDER'][0]}'
            else:
                sql += f' ORDER {additional['ORDER'][0]} DESC'
        return self.__cur.execute(sql)

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
