## This document is to test general code functions to interface with the database
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
        self.__conn = sqlite3.connect(self.__DBName) # open database if exists else create new data
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

    def table_relations(self, table):
        """ Return the table and any relationships the specified table has. """
        tables = {'Job':['Task','Task_Photo'], 'Employee':['Sales', 'Task', 'Manager', 'Employee_Photo', 'Employee_Time_Clock'],
        'Sales':[], 'Client':['Job', 'Sales'], 'Supplier':['Inventory'], 'Inventory':['Inventory_Photo'],
        'Campus':['Job', 'Task', 'Sales', 'Inventory', 'Equipment', 'Employee'],
        'Equipment':['Equipment_Photo']}
        return tables[table] if table in tables else False

    def dependent_tables(self, table):
        """ Return the tables are dependent upon another for a meaning. """
        tables = {'Job':['Task','Task_Photo'], 'Employee':['Manager', 'Employee_Photo', 'Employee_Time_Clock'], 'Sales':[], 'Client':[],
        'Supplier':[], 'Inventory':['Inventory_Photo'], 'Campus':[], 'Equipment':['Equipment_Photo']}
        return tables[table] if table in tables else False

    def create_newID(self, table):
        """ Create a new unique ID for a table """
        element = self.basic_execute("SELECT {}_ID FROM {} WHERE {}_ID == (SELECT MAX({}_ID) FROM {}) AND {}_ID LIKE '{}%' ".format(table, table, table, table, table, table, self.get_prefix(table)))
        element = element.fetchone()
        table_prefix = self.get_prefix(table)
        if element == None:
            return table_prefix + '1'.zfill(6) if table_prefix != None else None
        else:
            return table_prefix + str(int(element[0][len(table_prefix):]) + 1).zfill(6) if table_prefix != None else None

    def get_current_datetime(self):
        """ Return the current datetime in the format  %Y-%m-%d %H:%M:%S """
        return (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    def insert(self, table, user_value = None, preset_attribute_value = None):
        """ Insert new value into a specified table with preset attributes if provided. Use Dictionary for optional args"""
        table_attributes = self.get_attributes(table)
        sql = f'INSERT INTO {table} ('
        attributes = ''
        placeholder_values = ') VALUES ('
        values = []
        if preset_attribute_value != None:
            preset_keys = preset_attribute_value.keys()
        else:
            preset_keys = []
        if user_value != None:
            user_keys  = user_value.keys()
        else:
            user_keys = []
        for x in range(len(table_attributes)):
            if table_attributes[x][1] in user_keys:
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
            elif table_attributes[x][1] in preset_keys:
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

        ## Need to add more variables to where statement
        ## Need to add operator chioces to where clause
    def find(self, table, **additional):
        """ Search a specified table with any. Attributes key: Exact Name of desired attribute.
        Where key: Index of attribute in get_attributes function.
        Order key: list, index 0 is the values, index 1 is the descending option if requested."""
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
                    query.append(f"{table_attributes[index[0]][1]} == {index[1]}")
            sql += 'WHERE ' + ' AND '.join(query)
        if 'Order' in additional:
            ## The most genreal search of a table, but the query results are ordered
            if len(additional['Order']) == 1:
                sql += f" ORDER BY {additional['Order'][0]}"
            else:
                sql += f" ORDER BY {additional['Order'][0]} DESC"
        return self.__cur.execute(sql)

    def delete(self, table, attribute, ID, weak_table=None, weak_attribute=None):
        """ Delete an item from a table. Weak table given as list."""
        find_ID = self.value_exists(table, attribute, ID, text=True)
        if not find_ID:
            ## Value does not exists within the specified table.
            return False
        else:
            ## Insert Pop Up to confirm action
            if weak_table == None:
                ## Delete the value given from the table
                self.__cur.execute(f"DELETE FROM {table} WHERE {table}_ID == '{ID}'")
            else:
                ## Delete the value given from the table and all of its attributes linked to this value
                for wt in weak_table:
                    try:
                        if self.value_exists(wt, f'{table}_ID', ID, text=True):
                            self.__cur.execute(f"DELETE FROM {wt} WHERE {table}_ID == '{ID}'")
                    except:
                        if self.value_exists(wt, f'{wt}_ID', ID, text=True):
                            self.__cur.execute(f"DELETE FROM {wt} WHERE {table}_ID == '{ID}'")
                self.__cur.execute(f"DELETE FROM {table} WHERE {table}_ID == '{ID}'")
        self.commit_database()
        return True

    def update(self, table, ID, update_attribute_value=None, weak_table=None, update_weak=None, foreign_key=None):
        """ Modify a specific value. update_attribute_value: enter arg as list with attribute name, type, and value in the list. weak_table: enter arg as list. """
        find_ID = self.value_exists(table, f'{table}_ID', ID, text=True)
        if weak_table != None and foreign_key == None:
            ## Need to have new foreign key list in arg if weak_table is given in arg
            return False
        elif not find_ID:
            ## Value does not exists within the specified table.
            return False
        else:
            ## Update specified value
            sql = f'UPDATE {table} SET '
            for value in update_attribute_value:
                if value[1] == 'TEXT':
                    ## UPDATE TEXT attribute
                    sql += f"{value[0]} = '{value[2]}', "
                else:
                    sql += f"{value[0]} = {value[2]}, "
            sql = sql[:-2] + f"WHERE {table}_ID == '{ID}' "
            self.__cur.execute(sql)
            self.commit_database()
            if weak_table != None:
                ## Change foreign key in each listed table where applicable
                if update_weak == None:
                    update_weak = [[f'{table}_ID', 'TEXT', foreign_key]]
                for t in weak_table:
                    sql = f'UPDATE {t} SET '
                    for value in update_weak:
                        if value[1] == 'TEXT':
                            ## UPDATE TEXT attribute
                            sql += f"{value[0]} = '{value[2]}', "
                        else:
                            sql += f"{value[0]} = {value[2]}, "
                    sql = sql[:-2] + f"WHERE {table}_ID == '{ID}' "
                    self.__cur.execute(sql)
                    self.commit_database()
            return True

    def value_exists(self, table, attribute, value, like=False, text=False):
        """ Return True if a value exists with specified attribute values or False if it does not. table arg: list the table to search. attribute arg: list the attribute search by. value arg: list the value to find in the table. like arg: specify if like clause will be used in statement. text arg: will use quotes in clause."""
        if not like:
            if text:
                find = self.__cur.execute(f"SELECT * FROM {table} WHERE {attribute} == '{value}'")
            else:
                find = self.__cur.execute(f"SELECT * FROM {table} WHERE {attribute} == {value}")
        else:
            find = self.__cur.execute(f"SELECT * FROM {table} WHERE {attribute} LIKE '{value}'")
        if find.fetchone() != None:
            return True
        else:
            return False

    def count_results(self):
        """ Return the number of results that are returned from query. """
        return

    def employee_time(self):
        """ A function for managing the employee_time_clock table. """
        return
