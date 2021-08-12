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
            print("""Welcome to Delaware Electric Motor Supply Company""")
            menu = """Main Menu \n\t1: Jobs \n\t2: Sales \n\t3: Employees \n\t4: Clients \n\t5: Suppliers \n\t6: Inventory \n\t7: More \n\t0: Exit"""
            while True:
                print(menu)
                user_choice = input('Select Option: ')
                print()
                if user_choice == '1':
                    self.job()
                elif user_choice == '2':
                    self.sales()
                elif user_choice == '3':
                    self.employee()
                elif user_choice == '4':
                    self.client()
                elif user_choice == '5':
                    self.suppliers()
                elif user_choice == '6':
                    self.inventory()
                elif user_choice == '7':
                    self.more()
                elif user_choice == '0':
                    break
                else:
                    print('Sorry that option was not found.')
                self.commit_database()
                print()
        finally:
            self.close_database()
            print('\nGoodbye')

    def job(self):
        job_menu = "Job Menu\n\t1: Create New Job \n\t2: Find Job \n\t3: Update Job \n\t4: Delete Job \n\t5: Job Tasks \n\t0: Exit"
        while True:
            print(job_menu)
            user_choice = input('Select Option: ')
            print()
            if user_choice == '1':
                ## New Job
                preset = {'Job_ID':self.create_newID('Job'), 'Start_Date':self.get_current_datetime()}
                user = {}
                table = self.get_attributes('Job')
                for a in table:
                    print(a[1], a[2])
                    ui = input('Enter value or leave blank for empty: ')
                    if ui != '':
                        user[a[1]] = ui
                self.insert('Job', user, preset)
                print('Success')
            elif user_choice == '2':
                ## Find Job
                table_attributes = self.get_attributes('Job')
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
                    results = self.find('Job')
                elif selected_attributes == [] and order != '' and asec_or_desc == '':
                    results = self.find('Job', Order = [table_attributes[int(order)][1]])
                elif selected_attributes == [] and order != '' and asec_or_desc != '':
                    results = self.find('Job', Order = [table_attributes[int(order)][1], True])
                elif selected_attributes != [] and order == '':
                    results = self.find('Job', Where = selected_attributes)
                elif selected_attributes != [] and order != '' and asec_or_desc == '':
                    results = self.find('Job', Where = selected_attributes, Order = [table_attributes[int(order)][1]])
                else:
                    results = self.find('Job', Where = selected_attributes, Order = [table_attributes[int(order)][1], True])
                self.print_sql(results)
            elif user_choice == '3':
                ## Update Job
                self
            elif user_choice == '4':
                ## Delete Job
                self
            elif user_choice == '5':
                ## Job Task
                self.task()
            elif user_choice == '0':
                break
            else:
                print('Sorry that option was not found.')
            self.commit_database()
            print()


    def task(self):
        task_menu = "Task Menu\n\t1: \n\t2: \n\t3: \n\t4: \n\t5: \n\t0: Exit"
        return

    def sales(self):
        job_menu = " Menu\n\t1: \n\t2: \n\t3: \n\t4: \n\t5: \n\t0: Exit"
        return

    def employee(self):
        job_menu = " Menu\n\t1: \n\t2: \n\t3: \n\t4: \n\t5: \n\t0: Exit"
        return

    def client(self):
        job_menu = " Menu\n\t1: \n\t2: \n\t3: \n\t4: \n\t5: \n\t0: Exit"
        return

    def suppliers(self):
        job_menu = " Menu\n\t1: \n\t2: \n\t3: \n\t4: \n\t5: \n\t0: Exit"
        return

    def inventory(self):
        job_menu = " Menu\n\t1: \n\t2: \n\t3: \n\t4: \n\t5: \n\t0: Exit"
        return

    def more(self):
        """ List options for campus, equipment, and more. """
        job_menu = " Menu\n\t1: \n\t2: \n\t3: \n\t4: \n\t5: \n\t0: Exit"
        return


CLMain()
