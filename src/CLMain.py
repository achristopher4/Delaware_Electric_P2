## This is a testing document to display output for specific inputs
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
            print("""Welcome to Delaware Electric Motor Supply Company""")
            menu = """Main Menu \n\t1: Jobs \n\t2: Sales \n\t3: Employees \n\t4: Clients \n\t5: Suppliers \n\t6: Inventory \n\t7: Campus \n\t8: Equipment \n\t0: Exit"""
            while True:
                print(menu)
                user_choice = input('Select Option: ')
                print()
                if user_choice == '1':
                    ## Weak
                    self.dependent('Job')
                elif user_choice == '2':
                    ## Strong
                    self.independent('Sales')
                elif user_choice == '3':
                    ## Weak
                    self.dependent('Employee')
                elif user_choice == '4':
                    ## Strong
                    self.independent('Client')
                elif user_choice == '5':
                    ## Strong
                    self.independent('Supplier')
                elif user_choice == '6':
                    ## Weak
                    self.dependent('Inventory')
                elif user_choice == '7':
                    ## Strong
                    self.independent('Campus')
                elif user_choice == '8':
                    ## Weak
                    self.dependent('Equipment')
                elif user_choice == '0':
                    break
                else:
                    print('Sorry that option was not found.')
                self.commit_database()
                print()
        finally:
            self.close_database()
            print('\nGoodbye')

    def independent(self, table_choice):
        """ A single option menu for table actions. Insert new data point, find a data point, update data point(s), delete data point in a specified table. """
        while True:
            ## Use table_choice as the table name to proceed
            menu = f"{table_choice} Menu\n\t1: Create New {table_choice} \n\t2: Find {table_choice} \n\t3: Update {table_choice} \n\t4: Delete {table_choice} \n\t0: Exit"
            print(menu)
            user_choice = input('Select Option: ')
            print()
            if user_choice == '1':
                ## Insert new data point
                preset = {f'{table_choice}_ID':self.create_newID(table_choice)}
                user = {}
                table = self.get_attributes(table_choice)
                for a in table:
                    print(a[1], a[2])
                    if 'Start' in a[1] or 'Purchase_Date' == a[1]:
                        preset[a[1]] = self.get_current_datetime()
                    ui = input('Enter value or leave blank for empty: ')
                    if ui != '':
                        user[a[1]] = ui
                self.insert(table_choice, user, preset)
                print('Success')
            elif user_choice == '2':
                ## Find data point in specified table
                table_attributes = self.get_attributes(table_choice)
                selected_attributes = []
                for attribute in table_attributes:
                    print(attribute[0], attribute[1], attribute[2])
                    value = input('Search by value or leave blank to not search by: ')
                    if value != '':
                        selected_attributes.append([attribute[0], value])
                order = input('Enter index of attribute or leave blank to not order: ')
                if order != '':
                    asec_or_desc = input('Enter Desc to order descending value or leave blank to order in ascending: ')
                if selected_attributes == [] and order == '':
                    results = self.find(table_choice)
                elif selected_attributes == [] and order != '' and asec_or_desc == '':
                    results = self.find(table_choice, Order = [table_attributes[int(order)][1]])
                elif selected_attributes == [] and order != '' and asec_or_desc != '':
                    results = self.find(table_choice, Order = [table_attributes[int(order)][1], True])
                elif selected_attributes != [] and order == '':
                    results = self.find(table_choice, Where = selected_attributes)
                elif selected_attributes != [] and order != '' and asec_or_desc == '':
                    results = self.find(table_choice, Where = selected_attributes, Order = [table_attributes[int(order)][1]])
                else:
                    results = self.find(table_choice, Where = selected_attributes, Order = [table_attributes[int(order)][1], True])
                self.print_sql(results)
                print()
            elif user_choice == '3':
                ## Update data point in specifed table
                table_attributes = self.get_attributes(table_choice)
                while True:
                    find_value = input(f'Enter {table_choice}_ID or type "0" to exit: ')
                    if find_value == '0':
                        break
                    elif find_value != '':
                        ## Continue to update
                            ## Selected attributes: [attribute name, type, value]
                        if not self.value_exists(table_choice, f'{table_choice}_ID', find_value, text=True):
                            print(f'{find_value} in {table_choice} does not exists.\n')
                        else:
                            selected_attributes = []
                            for a in table_attributes:
                                print(a[1], a[2])
                                user_input = input('Enter value or leave blank keep current value: ')
                                if user_input != '':
                                    selected_attributes.append([a[1], a[2], user_input])
                            if selected_attributes[0][0] == f'{table_choice}_ID':
                                ## Regular update
                                self.update(table_choice, ID=find_value, update_attribute_value=selected_attributes)
                                print('Success/n')
                            elif not self.value_exists(table_choice, f'{table_choice}_ID', selected_attributes[0][0], text=True):
                                ## Update all tables with new ID along with a regular update
                                related_tables = self.table_relations(table_choice)
                                if related_tables != []:
                                    new_ID = selected_attributes[0][2]
                                    update_key = [[f'{table_choice}_ID', 'TEXT', new_ID]]
                                    self.update(table_choice, ID=find_value, update_attribute_value=selected_attributes,
                                    weak_table=related_tables, foreign_key=new_ID)
                                print('Success\n')
                            else:
                                print(f'Cannot change {table_choice}_ID as {selected_attributes[0][0]} already exists.')
                    else:
                        print('Cannot leave empty.\n')
            elif user_choice == '4':
                ## Delete data point in specifed table with specifed primary key
                print('This is a permanent action. Are you sure you want to continue?')
                cont = input ('Enter Y to continue or N to go back: ')
                if cont == 'Y':
                    ## Continue to deletion action
                    prim_key_value = input(f'Enter {table_choice}_ID: ')
                    related_tables = self.table_relations(table_choice)
                    if self.delete(table_choice, f'{table_choice}_ID', prim_key_value):
                        print('Success\n')
                    else:
                        print(f'Sorry could not delete {prim_key_value}\n')
                else:
                    continue
            elif user_choice == '0':
                ## return to main menu
                break
            else:
                print('Sorry option not found.\n')

    def dependent(self, table_choice):
        """ A single option menu for table actions. Insert new data point, find a data point, update data point(s), delete data point in a specified table. """
        while True:
            ## Use table_choice as the table name to proceed
            menu = f"{table_choice} Menu\n\t1: Create New {table_choice} \n\t2: Find {table_choice} \n\t3: Update {table_choice} \n\t4: Delete {table_choice} \n\t5: More \n\t0: Exit"
            print(menu)
            user_choice = input('Select Option: ')
            print()
            if user_choice == '1':
                ## Insert new data point
                preset = {f'{table_choice}_ID':self.create_newID(table_choice)}
                user = {}
                table = self.get_attributes(table_choice)
                for a in table:
                    print(a[1], a[2])
                    if 'Start' in a[1] or 'Purchase_Date' == a[1]:
                        preset[a[1]] = self.get_current_datetime()
                    ui = input('Enter value or leave blank for empty: ')
                    if ui != '':
                        user[a[1]] = ui
                self.insert(table_choice, user, preset)
                print('Success')
            elif user_choice == '2':
                ## Find data point in specified table
                table_attributes = self.get_attributes(table_choice)
                selected_attributes = []
                for attribute in table_attributes:
                    print(attribute[0], attribute[1], attribute[2])
                    value = input('Search by value or leave blank to not search by: ')
                    if value != '':
                        selected_attributes.append([attribute[0], value])
                order = input('Enter index of attribute or leave blank to not order: ')
                if order != '':
                    asec_or_desc = input('Enter Desc to order descending value or leave blank to order in ascending: ')
                if selected_attributes == [] and order == '':
                    results = self.find(table_choice)
                elif selected_attributes == [] and order != '' and asec_or_desc == '':
                    results = self.find(table_choice, Order = [table_attributes[int(order)][1]])
                elif selected_attributes == [] and order != '' and asec_or_desc != '':
                    results = self.find(table_choice, Order = [table_attributes[int(order)][1], True])
                elif selected_attributes != [] and order == '':
                    results = self.find(table_choice, Where = selected_attributes)
                elif selected_attributes != [] and order != '' and asec_or_desc == '':
                    results = self.find(table_choice, Where = selected_attributes, Order = [table_attributes[int(order)][1]])
                else:
                    results = self.find(table_choice, Where = selected_attributes, Order = [table_attributes[int(order)][1], True])
                self.print_sql(results)
                print()
            elif user_choice == '3':
                ## Update data point in specifed table
                table_attributes = self.get_attributes(table_choice)
                while True:
                    find_value = input(f'Enter {table_choice}_ID or type "0" to exit: ')
                    if find_value == '0':
                        break
                    elif find_value != '':
                        ## Continue to update
                            ## Selected attributes: [attribute name, type, value]
                        if not self.value_exists(table_choice, f'{table_choice}_ID', find_value, text=True):
                            print(f'{find_value} in {table_choice} does not exists.\n')
                        else:
                            selected_attributes = []
                            for a in table_attributes:
                                print(a[1], a[2])
                                user_input = input('Enter value or leave blank keep current value: ')
                                if user_input != '':
                                    selected_attributes.append([a[1], a[2], user_input])
                            if selected_attributes[0][0] == f'{table_choice}_ID':
                                ## Regular update
                                self.update(table_choice, ID=find_value, update_attribute_value=selected_attributes)
                                print('Success/n')
                            elif not self.value_exists(table_choice, f'{table_choice}_ID', selected_attributes[0][0], text=True):
                                ## Update all tables with new ID along with a regular update
                                related_tables = self.table_relations(table_choice)
                                if related_tables != []:
                                    new_ID = selected_attributes[0][2]
                                    update_key = [[f'{table_choice}_ID', 'TEXT', new_ID]]
                                    self.update(table_choice, ID=find_value, update_attribute_value=selected_attributes,
                                    weak_table=related_tables, foreign_key=new_ID)
                                print('Success\n')
                            else:
                                print(f'Cannot change {table_choice}_ID as {selected_attributes[0][0]} already exists.')
                    else:
                        print('Cannot leave empty.\n')
            elif user_choice == '4':
                ## Delete data point in specifed table with specifed primary key
                print('This is a permanent action. Are you sure you want to continue?')
                cont = input ('Enter Y to continue or N to go back: ')
                if cont == 'Y':
                    ## Continue to deletion action
                    prim_key_value = input(f'Enter {table_choice}_ID: ')
                    related_tables = self.dependent_tables(table_choice)
                    if self.delete(table_choice, f'{table_choice}_ID', prim_key_value, weak_table = related_tables,
                    weak_attribute = f'{table_choice}_ID'):
                        print('Success\n')
                    else:
                        print(f'Sorry could not delete {prim_key_value}\n')
                else:
                    continue
            elif user_choice == '5':
                ## Allow to transgress into weak tables associated with a defined primary key
                tables = self.dependent_tables(table_choice)
                while True:
                    for x in range(len(tables)): print(f'{x+1}: {tables[x]}')
                    print('0: Exit\n')
                    dependent_choice = input('Select Table: ')
                    if dependent_choice == '0':
                        break
                    elif dependent_choice.isdigit() and int(dependent_choice)-1 <= len(tables)-1:
                        ## Go to new menu
                        self.independent(tables[int(dependent_choice)-1])
                    else:
                        print('Sorry option not found.\n')
            elif user_choice == '0':
                ## return to main menu
                break
            else:
                print('Sorry option not found.\n')

CLMain()
