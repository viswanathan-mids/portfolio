# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 23:32:30 2021
@author: Viswanathan
Program: Flower Shop Manager Application
This application helps manage a small flower shop with the inventory(create 
and update items), register(perform a sale and return) and view accounts. The
program is executed from the command prompt.
"""
import pickle
import random
from datetime import datetime
from os import system
import csv


class menu():
    """ menu class creates an instance of the menu for user option
    selection. No inputs required for creating the instance"""
    def __init__(self):
        '''Initializes the menu for the user and creates other 
        class instances based on the user selection'''
        print('\n' + '*' * 100 + '\n')
        print(" " * 40, "Welcome to the 'Flower Shop Manager'\n")
        self.userinput = input(
                               "Select what you want to do\n" \
                               "Enter '1' for Register Menu\n" \
                               "Enter '2' for Item Menu\n" \
                               "Enter '3' for Accounts Menu\n" \
                               "Enter '5' to Quit application\n"\
                               "Enter '9' for Bulk Features\n"\
                               "\nYour Choice: "
                              )
        # Check for errors in userinput and typecast input to integer
        if self.userinput not in "12359" or self.userinput == "":
            # Call clearscreen method in class quitclass to clear screen
            quitclass.clearscreen()
            print('\n\nPlease select a valid option from (1, 2, 3, 5, 9)\n')
            self.__init__()
        else:
            self.userinput = int(self.userinput)

        # Create register, items, accounts, quitclass instances based on
        # user selection
        if self.userinput == 1:
            quitclass.clearscreen()
            self.registers = register()

        if self.userinput == 2:
            quitclass.clearscreen()
            self.itemins = items()

        if self.userinput == 3:
            quitclass.clearscreen()
            self.account = accounts()

        if self.userinput == 5:
            self.quits = quitclass()
        
        if self.userinput == 9:
            quitclass.clearscreen()
            self.upd = bulk()


class items():
    """ items class creates an instance for capturing user input to 
    perform various items functions using its methods. No inputs required for 
    creating the instance"""
    def __init__(self):

        # Get the current items from the pickle file using the quitclass
        # readitems method
        items.itemdict = quitclass.readitems()

        # Present the user choices
        print('\n' + '*' * 100 + '\n')
        print(" " * 40, "Welcome to the 'Item Menu'\n")
        self.iteminput = input(
                               "Select what you want to do\n" \
                               "Enter '1' to View Items\n" \
                               "Enter '2' to Update Item Details\n" \
                               "Enter '3' to Add Item\n" \
                               "Enter '4' to Update Inventory\n" \
                               "Enter '5' to go to Main Menu\n"\
                               "\nYour Choice: "
                              )

        # Check for user input errors and typecast to integer
        if self.iteminput not in "12345" or self.iteminput == "":
            quitclass.clearscreen()
            print('\n\nPlease select a valid option from (1, 2, 3, 4, 5)\n')
            self.__init__()
        else:
            self.iteminput = int(self.iteminput)

        # Call items instace methods based on user input
        if self.iteminput == 1:
            quitclass.clearscreen()
            self.getitems()

        if self.iteminput == 2:
            quitclass.clearscreen()
            self.upditems()

        if self.iteminput == 3:
            quitclass.clearscreen()
            self.additems()

        if self.iteminput == 4:
            quitclass.clearscreen()
            self.setinv()

        if self.iteminput == 5:
            quitclass.clearscreen()
            menu.__init__(self)

    def getitems(self):
        ''' This method calls the item print method with the current items
        dictionary to display all items'''
        self.itemprint(items.itemdict)
        # Initialze items menu after display
        self.__init__()

    def setitems(self, name, color, cost, price, pack, inv, itemid):
        ''' This method takes name, color, cost, price, pack-quantity,
        inventory and item-id as input and creates or updates an entry 
        in the items dictionary'''

        # Assign received parameters to local variables
        self.name = name
        self.color = color
        self.cost = cost
        self.price = price
        self.pack = pack
        self.inv = inv
        self.itemid = itemid

        # Insert or update entry in the items dictionary
        items.itemdict[self.itemid] = {
                                        "Item": self.name,
                                        "Color": self.color,
                                        "Cost": self.cost,
                                        "Price": self.price,
                                        "Pack": self.pack,
                                        "Inventory": self.inv
                                       }

        print('\nItem Entry Complete\n')
        # Call quitclass saveitems method to save to the pickle file
        quitclass.saveitems(items.itemdict)
        self.__init__()

    def additems(self):
        '''This method interactively takes user input of different item
        attributes for new item creation'''
        self.name = input('Input Item Name: ')
        self.color = input('Input Color: ')
        self.cost = input('Input Cost: ')
        self.price = input('Input Price: ')
        self.pack = input('Input Sale-Pack Qty: ')
        self.inv = int(input('Input Item Inventory: '))

        # Get the maximum item id and increment by 1
        # If no item exists, start from an initial value set
        try:
            self.itemid = int(max(items.itemdict.keys())) + 1
        except:
            self.itemid = 10

        # Call setitems instance method to create the item
        self.setitems(self.name, self.color, self.cost, self.price, self.pack,
                      self.inv, self.itemid
                      )

    def upditems(self):
        '''This method interactively asks the user to input the item
        and the attribute that nees to be updated to make changes'''
        self.itemid = input('\nInput Item ID to be updated: ')

        # Error check user input
        if self.itemid.isdigit() == False:
            print('\nPlease enter a valid item\n')
            self.__init__()
        else:
            self.itemid = int(self.itemid)

        # Using dictionary comprehension create a dictionary of
        # the input item and its value
        self.upddict = {
            i: items.itemdict[i]
            for i in items.itemdict if i == self.itemid
        }
        # If the length of the created dictionary is 0, the entred item
        # does not exist in the original items dictionary
        if len(self.upddict) == 0:
            print('\nItem Not Found\n')
            self.__init__()
        print("\n\nCurrent Details:")
        # Format the screen print of the input item with its attributes
        # using itemprint instance method
        self.itemprint(self.upddict)

        print("\nSelect an option number"\
                  " to update")

        # Load the selected item attributes into local variables
        self.name = items.itemdict[self.itemid]['Item']
        self.color = items.itemdict[self.itemid]['Color']
        self.cost = items.itemdict[self.itemid]['Cost']
        self.price = items.itemdict[self.itemid]['Price']
        self.pack = items.itemdict[self.itemid]['Pack']
        self.inv = items.itemdict[self.itemid]['Inventory']

        # Get the user selection to update an attribute
        self.updoption = input('1 -Name\n2 -Color\n3 -Cost\n4 -Price\n'\
                              '5 -Pack\n\nSelected Option: '\
                              )
        # Check for valid option selection and alert no changes
        # will be made on invalid selection. Capture the changes value
        try:
            self.updoption = int(self.updoption)
            self.newvalue = input('Enter New value: ')
        except:
            self.newvalue = input('Enter New value: ')
            print('\nNo changes will be made')

        # Depending on user selection, update the changed value in the
        # corresponding local variable
        if self.updoption == 1:
            self.name = self.newvalue
        elif self.updoption == 2:
            self.color = self.newvalue
        elif self.updoption == 3:
            self.cost = self.newvalue
        elif self.updoption == 4:
            self.price = self.newvalue
        elif self.updoption == 5:
            self.pack = self.newvalue
        else:
            print('\nExisiting values used to update the item as invalid'\
                  ' option selected'\
                  )
        # Call the setitems instance method and save the change
        self.setitems(self.name, self.color, self.cost, self.price, self.pack,
                      self.inv, self.itemid)

    def getinv(self, itemid):
        '''This method takes an item id as input and returns the 
        current inventory of the item'''
        self.itemid = itemid
        self.currinv = items.itemdict[self.itemid]['Inventory']
        return self.currinv

    def setinv(self):
        '''This method is used to interactively update inventory of an 
        item based on user input'''
        self.itemid = input('\nInput Item ID to update inventory: ')
        # Error check user input
        if self.itemid.isdigit() == False:
            print('\nPlease enter a valid item\n')
            self.__init__()
        else:
            self.itemid = int(self.itemid)

        # Check if the item entered by user is in items dictionary and
        # print the item name and current inventory
        try:
            print("Item ID: {} \nItem: {} \nCurrent"\
                  " Inventory: {}".format(self.itemid,\
                   items.itemdict[self.itemid]['Item'],\
                   items.itemdict[self.itemid]['Inventory'])
                  )
        except KeyError:
            print('\nItem not found, please try again\n')
            self.__init__()

        # Get the new inventory to be updated
        self.updinv = input('New Inventory: ')

        # update inventory in items dictionary
        items.itemdict[self.itemid]['Inventory'] = int(self.updinv)
        print('\nInventory Update Complete\n')
        # Save items dsctionary to the pickle file using quitclass
        # saveitems method
        quitclass.saveitems(items.itemdict)
        self.__init__()

    def itemprint(self, itemdict):
        '''This method takes an item dictionary as input and prints the 
        screen output in a nice format'''

        # Store items dictionary parameter in a local variable
        self.itemdict = itemdict

        print('\n')
        print("Item-ID".ljust(8," "), "Description".ljust(15, " "),\
              "Color".ljust(13," "),"Cost".ljust(8," "),\
              "Price".ljust(8," "), "Pack".ljust(10," "),\
              "Inventory".ljust(8," ")\
              )
        print("-" * 85)
        # print each item in the items dictionary in the format
        for item in self.itemdict:
            print("{:<9d}{:<16}{:<14}{:<9}{:<9}{:<12}{:<10d}"\
                  .format(item,\
                          self.itemdict[item]["Item"],\
                          self.itemdict[item]["Color"],\
                          self.itemdict[item]["Cost"],\
                          self.itemdict[item]["Price"],\
                          self.itemdict[item]["Pack"],\
                          self.itemdict[item]["Inventory"]\
                          )\
                 )
        print("")
        return


class register(items):
    """ register class creates an instance for capturing user input to 
    perform various register functions using its methods. No inputs 
    required for creating the instance"""
    def __init__(self):
        '''This method initializes the register menu for getting user 
        selection and then calling the methods based on selection'''
        # Read items dictionary from pickle file using quitclass
        # readitems method
        items.dict = quitclass.readitems()

        print('\n' + '*' * 100 + '\n')
        print(" " * 40, "Welcome to the 'Register Menu'\n")
        # get user input for selection
        self.reginput = input(
                               "Select what you want to do\n" \
                               "Enter '1' to Perform a Sale\n" \
                               "Enter '2' to Perform a Return\n" \
                               "Enter '5' to go to Main Menu\n"\
                               "\nYour Choice: "\
                              )
        # Error check user input and call the corresponding method
        # based on selection
        if self.reginput not in "125" or self.reginput == "":
            quitclass.clearscreen()
            print('\n\nPlease select a valid option from (1, 2, 5)\n')
            self.__init__()
        else:
            self.reginput = int(self.reginput)

        if self.reginput == 1:
            quitclass.clearscreen()
            self.sale()

        if self.reginput == 2:
            quitclass.clearscreen()
            self.returns()

        if self.reginput == 5:
            quitclass.clearscreen()
            menu.__init__(self)

    def sale(self):
        '''This method interactively receives user input of the items and 
        the quantities to be sold and updates accounts class dictionary
        and inventory in items dictionary'''

        # flag to continuously take user input of items to be sold
        # Item id 0 will reset flag
        self.complete = True
        print('\nEnter "0" in Item ID field if you want to exit Sales\n')

        # a randon number is assigned to identify all items in a transaction
        self.seq = random.randint(100, 999)
        # Running count of the transaction total as items are being added
        self.total = 0

        # While flag is true contnue to take input and perform the sale
        while self.complete:
            self.itemid = input('\nInput Item ID to sell: ')
            # Error check item entry
            if self.itemid.isdigit() == False:
                print('\nPlease enter a valid item\n')
                continue
            else:
                self.itemid = int(self.itemid)

            # Check if user wants to exit
            if self.itemid == 0:
                self.complete = False
                break
            # Check if the item exists in items dictionary
            # and print name and price
            try:
                print("Item : ", items.itemdict[self.itemid]['Item'])
                print("Price: ", items.itemdict[self.itemid]['Price'])
            except KeyError:
                print('\nItem not found, please try again\n')
                continue

            self.qty = int(input('Input sell quantity: '))

            # Calculate the item subtotal using price and quantity
            self.itemtotal = float(items.itemdict[self.itemid]['Price'])\
                            * self.qty

            # Print item sub-total
            print("Item-Total: {:4.2f}".format(self.itemtotal))

            # Decrement inventory from items dictionary for the
            # quantity sold
            self.inventory = items.itemdict[self.itemid]['Inventory']
            items.itemdict[self.itemid]['Inventory'] = self.inventory\
                                                      - self.qty

            # Assign the attributes for updating accounts dictionary
            self.trantype = 'Sale'
            self.trantotal = float(items.itemdict[self.itemid]['Price'])\
                                    *self.qty

            # Call the quitclass gettime method to get current date and time
            self.date = quitclass.gettime()[0]
            self.time = quitclass.gettime()[1]

            # call accounts class settran method with the required parameters
            # to save the transaction
            accounts.settran(self, self.trantype, self.itemid, self.qty,
                             self.trantotal, self.date, self.time, self.seq
                             )
            # Add item sub-total to the transaction total
            self.total += self.itemtotal

        # On exiting the loop, pint the transaction total
        print('\n\nTransaction Total: {:4.2f}'.format(self.total), '\n\n')

        # save the items dictionary after the inventory updates based
        # on the sale
        quitclass.saveitems(items.itemdict)

        # Initialize the register menu
        self.__init__()

    def returns(self):
        '''This method interactively receives user input of the items and 
        the quantities to be returned and updates accounts class dictionary'''

        # flag to continuously take user input of items to be sold
        # Item id 0 will reset flag
        self.complete = True
        print('\nEnter "0" in Item ID field if you want to exit Returns\n')

        # a randon number is assigned to identify all items in a transaction
        self.seq = random.randint(100, 999)
        # Running count of the transaction total as items are being added
        self.total = 0

        # While flag is true contnue to take input and perform the return
        while self.complete:
            self.itemid = input('\nInput Item ID to return: ')
            # Error check item entry
            if self.itemid.isdigit() == False:
                print('\nPlease enter a valid item\n')
                continue
            else:
                self.itemid = int(self.itemid)

            # Check if user wants to exit
            if self.itemid == 0:
                self.complete = False
                break
            # Check if the item exists in items dictionary
            # and print name and price
            try:
                print("Item: ", items.itemdict[self.itemid]['Item'])
                print("Price: ", items.itemdict[self.itemid]['Price'])
            except KeyError:
                print('\nItem not found, please try again\n')
                continue

            self.qty = int(input('Input return quantity: '))
            # Calculate the item subtotal using price and quantity
            self.itemtotal = float(items.itemdict[self.itemid]['Price'])\
                            * self.qty
            # Print the item sub-total
            print("Item-Total: {:4.2f}".format(self.itemtotal))

            # Assign the attributes for updating accounts dictionary
            self.trantype = 'Return'
            self.trantotal = float(items.itemdict[self.itemid]['Price'])\
                                    *self.qty

            # Call the quitclass gettime method to get current date and time
            self.date = quitclass.gettime()[0]
            self.time = quitclass.gettime()[1]

            # call accounts class settran method with the required parameters
            # to save the transaction
            accounts.settran(self, self.trantype, self.itemid, self.qty,
                             self.trantotal, self.date, self.time, self.seq
                             )
            # Add item sub-total to the transaction total
            self.total += self.itemtotal
        # On exiting the loop, pint the transaction total
        print('\n\nTransaction Total: {:4.2f}'.format(self.total), '\n\n')

        # Initialize register menu. No auto inventory update required for
        # a return as the item will be checked for damages
        self.__init__()


class accounts(register):
    '''This class interactively gets user input and displays the full
    transaction history or the current day's transaction history'''
    def __init__(self):
        '''This method initializes the options for user selection to view
        all transactions or for the current day'''
        print('\n' + '*' * 100 + '\n')
        print(" " * 40, "Welcome to the 'Accounts Menu'\n")
        self.accinput = input(
                               "Select what you want to do\n" \
                               "Enter '1' to Display All Transactions\n" \
                               "Enter '2' to Display Today's Transactions\n" \
                               "Enter '5' to go to main menu\n"\
                               "\nYour Choice: "
                              )
        # Error check user input
        if self.accinput not in "125" or self.accinput == "":
            quitclass.clearscreen()
            print('\n\nPlease select a valid option from (1, 2, 5)\n')
            self.__init__()
        else:
            self.accinput = int(self.accinput)

        # Call the instance methods based on user input
        if self.accinput == 1:
            quitclass.clearscreen()
            # Call gettran method to get all transactions
            self.gettran()

        if self.accinput == 2:
            # Assign current date and call gettran method to get
            # only the current date transactions
            self.date = quitclass.gettime()[0]
            quitclass.clearscreen()
            self.gettran(self.date)

        if self.accinput == 5:
            quitclass.clearscreen()
            menu.__init__(self)

    def settran(self, trantype, itemid, qty, trantotal, date, time, seq):
        '''This method takes arguments of tran-type, item-id, quantity,
        transaction-total, date, time and a sequence number to save the
        transaction in the accounts dictionary'''

        # Read the accounts dictionary from the pickle file
        accounts.trans = quitclass.readaccounts()

        # Take the maximum of transaction id and increment by 1
        # If no rows, start with a number
        try:
            self.tranid = int(max(accounts.trans.keys())) + 1
        except:
            self.tranid = 5000

        # Udaate the transaction in the accounts dictionary
        accounts.trans[self.tranid] = {
                                        "Tran-Type": trantype,
                                        "Item ID": itemid,
                                        "Quamtity": qty,
                                        "Total": trantotal,
                                        "Date": date,
                                        "Time": time,
                                        "Tran-ID": seq
                                       }
        # Save the accounts dictionary in the pickle file using
        # quitclass saveaccounts method
        quitclass.saveaccounts(accounts.trans)

    def gettran(self, date=None):
        '''This method takes an option parameter date as input
        and prints the list of transactions'''

        # Read the accounts dictionary from the pickle file using
        # quitclass readaccounts method
        accounts.trans = quitclass.readaccounts()

        # initialize the sales and returns amounts before they are
        # summarized for all the transactions
        self.salestotal = 0
        self.returntotal = 0
        self.date = date
        # if no date is passed skip to use full accounts dictionary
        if self.date == None:
            pass
        # if a date is passed, create a dictionary with only the required
        # entries for the date
        else:
            accounts.trans = {
                each[0]: each[1]
                for each in accounts.trans.items()
                if each[1]['Date'] == self.date
            }

        print('\n')
        print("Seq.".ljust(7," "), "Tran-Type".ljust(9, " "),\
              "Item-ID".ljust(7," "),"Quantity".ljust(8," "),\
              "Item-Total".ljust(10," "), "Tran-Date".ljust(11," "),\
              "Tran-Time".ljust(8," "),"Tran-ID".ljust(7," ")\
              )
        print("-" * 75)
        # for each item in the dictionary add the transaction total to the
        # overall sales and returns total and the print the values
        # in a format
        for transaction in accounts.trans:
            if accounts.trans[transaction]["Tran-Type"] == 'Sale':
                self.salestotal += float(accounts.trans[transaction]["Total"])
            else:
                self.returntotal += float(accounts.trans[transaction]["Total"])

            print("{:<8d}{:<10}{:<8d}{:<9d}{:<11.2f}{:<12}{:<10}{:<10d}"\
                  .format(transaction,\
                          accounts.trans[transaction]["Tran-Type"],\
                          accounts.trans[transaction]["Item ID"],\
                          accounts.trans[transaction]["Quamtity"],\
                          accounts.trans[transaction]["Total"],\
                          accounts.trans[transaction]["Date"],\
                          accounts.trans[transaction]["Time"],\
                          accounts.trans[transaction]["Tran-ID"]\
                          )\
                 )

        # Print the sales and returns total amount
        print("\nSales Total  : {:10.2f}".format(self.salestotal))
        print("Returns Total: {:10.2f}".format(self.returntotal))
        self.__init__()


class quitclass():
    '''This class different utility methods to read/save data (items and
    accounts from/to a pickle file, clear screen contents, get current
    date and time and exit the application'''
    
    def __init__(self):
        '''This method calls the instance method leave to print a message 
        and exit the application'''
        self.leave()
        
    @staticmethod
    def saveitems(itemdict):
        '''This static method takes the items dictionary as an input and
        saves it to a pickle file and returns none'''
        storage = "Items.pkl"
        open_storage = open(storage, "wb")
        pickle.dump(itemdict, open_storage)
        open_storage.close()
        return

    @staticmethod
    def readitems():
        '''This static method takes no inputs, reads the items dictionary 
        from a pickle file. If no file exists or the file is empty, it 
        returns an empty items dictionary'''
        try:
            storage = "Items.pkl"
            open_storage = open(storage, "rb")
            items.itemdict = pickle.load(open_storage)
            open_storage.close()
            return items.itemdict
        except:
            items.itemdict = {}
            storage = "Items.pkl"
            open_storage = open(storage, "wb")
            pickle.dump(items.itemdict, open_storage)
            open_storage.close()
            return items.itemdict

    @staticmethod
    def saveaccounts(trans):
        '''This static method takes the accounts dictionary as an input and
        saves it to a pickle file and returns none'''
        storage = "Accounts.pkl"
        open_storage = open(storage, "wb")
        pickle.dump(trans, open_storage)
        open_storage.close()
        return

    @staticmethod
    def readaccounts():
        '''This static method takes no inputs, reads the accounts dictionary 
        from a pickle file. If no file exists or the file is empty, it 
        returns an empty accounts dictionary'''
        try:
            storage = "Accounts.pkl"
            open_storage = open(storage, "rb")
            accounts.trans = pickle.load(open_storage)
            open_storage.close()
            return accounts.trans
        except:
            accounts.trans = {}
            storage = "Accounts.pkl"
            open_storage = open(storage, "wb")
            pickle.dump(accounts.trans, open_storage)
            open_storage.close()
            return accounts.trans

    def leave(self):
        '''This instance method clears the screen and quits the application'''
        self.clearscreen()
        print('\n' + '*' * 100 + '\n')
        print(" " * 40 + '\n\nThank you for using "Flower Shop Manager"\n\n')
        print('\n' + '*' * 100 + '\n')
        exit()

    @staticmethod
    def gettime():
        '''This static method returns the current date and time to the 
        calling step'''
        now = datetime.now()
        date = now.strftime("%m/%d/%Y")
        time = now.strftime("%H:%M:%S")
        return date, time

    @staticmethod
    def clearscreen():
        '''This static method clear the screen contents'''
        _ = system('clear')

class bulk():
    '''This class interactively provides the user to upload a csv file with 
        the new items and attributes or extract all existing items into a csv.
        The csv file should have the following attributes in each line for 
        upload: Item Name(str), Color(str), Cost(upto 2 decimals), 
        Price(upto 2 decimals), sale pack quantity(integer),
        Item inventory quantiry(integer) and end witn newline char and the 
        download file will have an additional Item-Id at the beginning'''
    
    def __init__(self):
        '''This method initializes the options for user selection to 
        do bulk maintenance'''
        print('\n' + '*' * 100 + '\n')
        print(" " * 40, "Welcome to the 'Bulk Maintenance'\n")
        self.bulkinput = input(
                               "Select what you want to do\n" \
                               "Enter '1' to Bulk Upload New Items\n" \
                               "Enter '2' to Extract all existing items\n" \
                               "Enter '5' to go to main menu\n"\
                               "\nYour Choice: "
                              )
        # Error check user input
        if self.bulkinput not in "125" or self.bulkinput == "":
            quitclass.clearscreen()
            print('\n\nPlease select a valid option from (1, 2, 5)\n')
            self.__init__()
        else:
            self.bulkinput = int(self.bulkinput)

        # Call the instance methods based on user input
        if self.bulkinput == 1:
            quitclass.clearscreen()
            # Call upload method to bulk upload new items
            self.upload()

        if self.bulkinput == 2:
            quitclass.clearscreen()
            #Call extract method to extract all existing items into a csv
            self.extract()

        if self.bulkinput == 5:
            quitclass.clearscreen()
            menu.__init__(self)
          
        
    def upload(self):
        '''This method asks the user for a csv file with 
        the new items and attributes in the current directory.
        The csv file should have the following attributes in each line for 
        upload: Item Name(str), Color(str), Cost(upto 2 decimals), 
        Price(upto 2 decimals), sale pack quantity(integer),
        Item inventory quantity(integer) and end witn newline char'''
        
        items.itemdict = quitclass.readitems()
        
        # get csv file name as input
        self.bulkitemfile = input('\n\nInput bulk item csv file name'\
                                  ' (like bulk.csv): ')
        
        # get the maximum item id
        try:
            self.itemid = int(max(items.itemdict.keys())) + 1
        except:
            self.itemid = 10
        
        # iterate through csv file and save items
        try:
            csvfile =  open(self.bulkitemfile, mode = 'r') 
            self.newitems = csv.reader(csvfile, delimiter=',')
                               
            for row in self.newitems:                                   
                    
                items.itemdict[self.itemid] = {
                                                "Item": row[0],
                                                "Color": row[1],
                                                "Cost": row[2],
                                                "Price": row[3],
                                                "Pack": row[4],
                                                "Inventory": int(row[5])
                                                }
                    
                # Call quitclass saveitems method to save to the pickle file
                quitclass.saveitems(items.itemdict)
                self.itemid += 1
            csvfile.close()
        
            print('\nBulk upload Complete. View your items from Items'\
                      ' Menu\n')
            self.__init__()
        
        # Error when no input file or file is empty for upload
        except (FileNotFoundError,IndexError):
            print('\nNo {} file found or file is empty\n'\
                    .format(self.bulkitemfile))
            self.__init__()
    
    def extract(self):
        '''This method extracts all existing items into a csv.
        The csv file will have the following attributes in each line: 
        Item-Id, Item Name, Color, Cost, Price, sale pack quantity,
        Item inventory and end witn newline char'''
        
        items.itemdict = quitclass.readitems()
        
        # Write to csvfile with all the items        
        csvfile = open("Itemextract.csv", mode = 'w', newline='')
        self.writer = csv.writer(csvfile, delimiter=',')
        for each in items.itemdict:
            self.row = [each, 
                        items.itemdict[each]["Item"],
                        items.itemdict[each]["Color"],
                        items.itemdict[each]["Cost"],
                        items.itemdict[each]["Price"],
                        items.itemdict[each]["Pack"],
                        items.itemdict[each]["Inventory"]
                        ]
            self.writer.writerow(self.row)
        csvfile.close()
            
        print('\nItemextract.csv file created with items\n')
        self.__init__()


# Initiate an instance of the flower shop program menu class
Menu = menu()