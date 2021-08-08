## Set up SQL database for delaware electric
## Author: Alexander Christopher
## Date: 07/27/2021

import os
import sqlite3
from sqlite3 import Error

path = '../src/DE_Main'

conn = sqlite3.connect(path) # create new database

c = conn.cursor()   # Save the database in current working directory

# Create Tables
## Clients
c.execute(''' CREATE TABLE IF NOT EXISTS Client (
Client_ID TEXT PRIMARY KEY NOT NULL, Name TEXT, Street_Address TEXT, City TEXT,
State TEXT, Zip INT, Country TEXT, Hours TEXT, Relationship TEXT,
Payment_Type TEXT)
''')

## Campus
c.execute(''' CREATE TABLE IF NOT EXISTS Campus (
Campus_ID TEXT PRIMARY KEY NOT NULL, Name TEXT, Street_Address TEXT, City TEXT,
State TEXT, Zip INT, Country TEXT, Hours TEXT, Type TEXT, Description TEXT)
''')

## Employee
c.execute(''' CREATE TABLE IF NOT EXISTS Employee (
Employee_ID TEXT PRIMARY KEY NOT NULL, Manager_ID TEXT, Campus_ID TEXT, First_Name TEXT,
Last_Name TEXT, Phone_Number TEXT, Street_Address TEXT, City TEXT,
State TEXT, Zip INT, Country TEXT, Access_Level TEXT, Position TEXT, Start_Date DATE,
Emergency_Contact_First_Name TEXT, Emergency_Contact_Last_Name TEXT,
Emergency_Number TEXT, Hourly_Rate REAL, Commission_Rate REAL,
FOREIGN KEY (Campus_ID) REFERENCES Campus (Campus_ID),
FOREIGN KEY (Manager_ID) REFERENCES Manager (Manager_ID))
''')
    ## Removed: FOREIGN KEY (Manager_ID) REFERENCE Manager(Manager_ID),

## Manager
c.execute(''' CREATE TABLE IF NOT EXISTS Manager(
Manager_ID TEXT PRIMARY KEY,
FOREIGN KEY (Manager_ID) REFERENCES Employee(Employee_ID))
''')

## Employee Photo
c.execute(''' CREATE TABLE IF NOT EXISTS Employee_Photo(
Employee_Photo_ID TEXT PRIMARY KEY NOT NULL, Server TEXT, Company_Name TEXT, Campus_ID TEXT,
Employee_ID,
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID),
FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID))
''')

## Supplier
c.execute(''' CREATE TABLE IF NOT EXISTS Supplier(
Supplier_ID TEXT PRIMARY KEY NOT NULL, Name TEXT, Phone_Number TEXT, Street_Address TEXT,
City TEXT, State TEXT, Zip INT, Country TEXT, Website TEXT, Relationship TEXT,
Hours TEXT)
''')

## Inventory
c.execute(''' CREATE TABLE IF NOT EXISTS Inventory(
Inventory_ID TEXT PRIMARY KEY NOT NULL, Name TEXT, Supplier_ID TEXT, Campus_ID TEXT, Cost REAL,
Shipping_And_Handling REAL, Quantity REAL, Item_Type TEXT, Date_Purchased DATE,
FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID),
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID))
''')

## Inventory Photo
c.execute(''' CREATE TABLE IF NOT EXISTS Inventory_Photo(
Inventory_Photo_ID TEXT PRIMARY KEY NOT NULL, Server TEXT, Company_Name TEXT, Campus_ID TEXT,
Inventory_ID TEXT,
FOREIGN KEY(Campus_ID) REFERENCES Campus(Campus_ID),
FOREIGN KEY(Inventory_ID) REFERENCES Inventory(Inventory_ID))
''')

## Equipement
c.execute(''' CREATE TABLE IF NOT EXISTS Equipment(
Equipment_ID TEXT PRIMARY KEY NOT NULL, Campus_ID TEXT, Name TEXT, Make TEXT, Model TEXT,
Year INT, Purchase_Price REAL, Date_Purchased DATE, Type Name, Description Name,
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID))
''')

## Equipment Photo
c.execute(''' CREATE TABLE IF NOT EXISTS Equipment_Photo(
Equipment_Photo_ID TEXT PRIMARY KEY NOT NULL, Equipment_ID TEXT, Server TEXT, Company_Name TEXT, Campus_ID TEXT,
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID),
FOREIGN KEY (Equipment_ID) REFERENCES Equipment(Equipment_ID))
''')

## Sales
c.execute(''' CREATE TABLE IF NOT EXISTS Sales(
Sales_ID TEXT PRIMARY KEY NOT NULL, Client_ID TEXT, Inventory_ID TEXT, Employee_ID TEXT,
Campus_ID TEXT, Type TEXT, Description TEXT, Purchase_Date DATE,
Shipping_And_Handling REAL, Cost REAL, Profit_Margin REAL, Commission REAL,
Payment_Type TEXT,
FOREIGN KEY (Client_ID) REFERENCES Clients(Client_ID),
FOREIGN KEY (Inventory_ID) REFERENCES Inventory(Inventory_ID),
FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID),
FOREIGN KEY (Cost) REFERENCES Inventory(Cost),
FOREIGN KEY (Shipping_And_Handling) REFERENCES Inventory(Shipping_And_Handling),
FOREIGN KEY (Payment_Type) REFERENCES Clients(Payment_Type),
FOREIGN KEY (Commission) REFERENCES Employee(Commission_Rate))
''')

## Repair Job
c.execute(''' CREATE TABLE IF NOT EXISTS Job(
Job_ID TEXT PRIMARY KEY NOT NULL, Campus_ID TEXT, Client_ID TEXT, Type TEXT,
Description TEXT, Start_Date DATE, Cost REAL, Shipping_And_Handling REAL,
Profit_Margin REAL, Payment_Type TEXT, Completed TEXT, End_Date DATE,
Paid TEXT,
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID),
FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID),
FOREIGN KEY (Payment_Type) REFERENCES Client(Payment_Type))
''')

## Repair Task
c.execute(''' CREATE TABLE IF NOT EXISTS Task(
Task_ID TEXT PRIMARY KEY NOT NULL, Job_ID TEXT, Inventory_ID TEXT, Employee_ID TEXT, Campus_ID TEXT,
Type TEXT, Description TEXT, Start_Date_Time DATE, End_Date_Time DATE, Labor_Time REAL, Hourly_Rate REAL,
Part_Cost REAL, Part_Quantity REAL, Shipping_And_Handling REAL, Completed TEXT,
End_Date DATE,
FOREIGN KEY (Job_ID) REFERENCES Job(Job_ID),
FOREIGN KEY (Inventory_ID) REFERENCES Inventory(Inventory_ID),
FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID),
FOREIGN KEY (Part_Cost) REFERENCES Inventory(Cost),
FOREIGN KEY (Shipping_And_Handling) REFERENCES Inventory(Shipping_And_Handling))
''')

## Repair Task Photo
c.execute(''' CREATE TABLE IF NOT EXISTS Task_Photo (
Task_Photo_ID TEXT PRIMARY KEY NOT NULL, Server TEXT, Company_Name TEXT, Campus_ID TEXT,
Job_ID TEXT, Task_ID Text,
FOREIGN KEY (Campus_ID) REFERENCES Campus(Campus_ID),
FOREIGN KEY (Job_ID) REFERENCES Job(Job_ID),
FOREIGN KEY (Task_ID) REFERENCES Task(Task_ID))
''')

## Employee Time Clock
c.execute(''' CREATE TABLE IF NOT EXISTS Employee_Time_Clock (
Employee_Time_Clock_ID TEXT PRIMARY KEY NOT NULL, Employee_ID TEXT, Year INT, Week INT, Day INT, Start_Time DATE,
End_Time DATE, Jobs_Worked_On TEXT,
FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID))
''')

conn.commit()
conn.close()
