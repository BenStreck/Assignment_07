#------------------------------------------#
# Title: CDInventory.py
# Desc: This is a script to store CD Inventory Data
#       This script demonstrates my understanding of how to use structured
#       error handling. It also demonstrates my ability to work with
#       binary data
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# BStreck, 2022-Nov-16, Started adding functionality in the 'TO-DO' sections (Assignment06)
# BStreck, 2022-Nov-19, Finished adding functionality in the 'TO-DO' sections (Assignment06)
# BStreck, 2022-Nov-26, Added structured error handling and changed data strage to binary data (Assignment07)
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """
    Processing the data during runtime
    """
    
    @staticmethod
    def add_CD(table, ID, strTitle, strArtist):
        """
        Function to add a new CD to the current inventory and show the updated inventory afterwards.
    
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            ID (integer): the ID number of the new CD being added to the inventory
            strTitle (string): the title of the new CD being added to the inventory
            strArtist (string): the artist of the new CD being added to the inventory

        Returns:
            None
        """
        dicRow = {'ID': ID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)
        print()
        IO.show_inventory(table)
    
    @staticmethod
    def delete_CD(table, intIDDel):
        """
        Function to delete a CD from the current inventory and show the updated inventory afterwards.
        It also relabels the ID numbers to prevent discontinuities in the inventory.
    
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            intIDDel (integer): the ID number of the CD being deleted from the inventory

        Returns:
            table (list of dict): updated 2D data structure (list of dicts) that holds the data during runtime
        """
        if intIDDel < 1:
            print('\nID Number Invalid... Choose a positive, nonzero value\n')
            print('No Entries Deleted\n')
        elif intIDDel > len(table):
            print('\nID Number Invalid... There are not that many CDs in the inventory\n')
            print('No Entries Deleted\n')
        else:
            table = list(filter(lambda i: i['ID'] != intIDDel, table))
            print('\nEntry Deleted')
            print('Relabeling ID Numbers...')
            i = 1
            for row in table:
                row['ID'] = i
                i += 1
            print('ID numbers have been updated\n')
        IO.show_inventory(table)
        return table
    
    @staticmethod
    def load_inventory(file_name, table):
        """
        Function managing the FileProcessor.read_file() function.
        This helps prevent unintentional overwriting of data in the current inventory.
        It also shows the current inventory after it has been loaded.
    
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        print('WARNING: If you continue, all unsaved data will be lost when the Inventory is re-loaded.\n')
        print('Type \'yes\' to continue and reload data from the file. Otherwise reload will be canceled.')
        strYesNo = input('Would you like to continue? ')
        if strYesNo.strip().lower() == 'yes':
            print('\nReloading...')
            FileProcessor.read_file(file_name, table)
            IO.show_inventory(table)
        else:
            input('Canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu. ')
            IO.show_inventory(table)
    
    @staticmethod
    def save_inventory(file_name, table):
        """
        Function managing the FileProcessor.write_file() function.
        It shows the current inventory prior to saving which allows users to verify they are saving the correct data.
    
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        IO.show_inventory(table)
        print('\nSave this inventory to file? Type \'yes\' to continue and save data to the file.')
        strYesNo = input('Would you like to continue? ')
        if strYesNo.strip().lower() == 'yes':
            print('\nSaving updated inventory...')
            FileProcessor.write_file(file_name, table)
            print('Done')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu. ')


class FileProcessor:
    """
    Processing the data to and from .DAT binary file
    """
    
    @staticmethod
    def read_file(file_name, table):
        """
        Function to manage data intake from the .DAT binary file to a list of dictionaries.
        The function reads data from the file identified by 'file_name' into a 2D table
        (list of dicts). It also includes structured error handling in case the file
        does not exist yet.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            with open(file_name, 'rb') as objFile:
                dum1 = pickle.load(objFile)
            objFile.close()
            for i in range(len(dum1)):
                table.append(dum1[i])
        except FileNotFoundError as e:
            print('\n{} does not exist...'.format(file_name))
            print('Type: ', type(e), '\nError: ', e, '\nMessage: ', e.__doc__)
            print('\nCreating the File...')
            file = open(file_name, 'wb')
            file.close()
            print('The file, {}, has now been created!'.format(file_name))
        except Exception as e:
            print('\nThere was a general error...')
            print('Type: ', type(e), '\nError: ', e, '\nMessage: ', e.__doc__)
    
    @staticmethod
    def write_file(file_name, table):
        """
        Function to manage data writing from the list of dictionaries to a .DAT binary file.
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)


# -- PRESENTATION (Input/Output) -- #
class IO:
    """
    Handling Input / Output
    """
    
    @staticmethod
    def print_menu():
        """
        Displays a menu of choices to the user

        Args:
            None

        Returns:
            None
        """
        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')
    
    @staticmethod
    def menu_choice():
        """
        Gets user input for menu selection

        Args:
            None

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice
    
    @staticmethod
    def show_inventory(table):
        """
        Displays the current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')
    
    @staticmethod
    def new_CD_choice(table):
        """
        Function to accept user inputs for a new CD.
        The data will be added to the current inventory using the DataProcessor.add_CD() function.

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            ID (integer): the ID number of the new CD being added to the inventory
            strTitle (string): the title of the new CD being added to the inventory
            strArtist (string): the artist of the new CD being added to the inventory
        """
        ID = len(table) + 1
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return ID, strTitle, strArtist
    
    @staticmethod
    def del_CD_choice(table):
        """
        Function to accept user inputs for deleting a CD.
        The chosen CD will be removed from the current inventory using the DataProcessor.delete_CD() function.
        It also includes structured error handling in case the input cannot be converted to an integer.
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            intIDDel (integer): the ID number of the CD being deleted from the inventory
        """
        print('Deleting an entry from the CD Inventory...')
        print('What is the ID number of the entry you want to delete?\n')
        IO.show_inventory(table)
        try:
            intIDDel = int(input('Enter ID Number Here: ').strip())
            return intIDDel
        except ValueError as e:
            print('\nThat is not a valid ID number...')
            print('Type: ', type(e), '\nError: ', e, '\nMessage: ', e.__doc__)
            print('\nNo Entries Deleted')
        except Exception as e:
            print('\nThere was a general error...')
            print('Type: ', type(e), '\nError: ', e, '\nMessage: ', e.__doc__)
            print('\nNo Entries Deleted')


# 1. When program starts, read in the Current Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. Start main loop
while True:
    
    # 3. Display menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    
    # 4. Process menu selections
    
        # 4.1 Exit
    if strChoice == 'x':
        print('Goodbye...')
        break
    
        # 4.2 Load Inventory
    if strChoice == 'l':
        DataProcessor.load_inventory(strFileName, lstTbl)
        continue
    
        # 4.3 Add a CD
    elif strChoice == 'a':
        ID, strTitle, strArtist = IO.new_CD_choice(lstTbl)
        DataProcessor.add_CD(lstTbl, ID, strTitle, strArtist)
        continue  # start loop back at top.
    
        # 4.4 Display Current Inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
        # 4.5 Delete a CD
    elif strChoice == 'd':
        try:
            intIDDel = IO.del_CD_choice(lstTbl)
            lstTbl = DataProcessor.delete_CD(lstTbl, intIDDel)
            continue # start loop back at top
        except:
            continue  # start loop back at top.
    
        # 4.6 Save Inventory to File
    elif strChoice == 's':
        DataProcessor.save_inventory(strFileName, lstTbl)
        continue  # start loop back at top.
    
        # 4.7 Catch-All Error... Should not be possible because the user's choice gets vetted in IO
    else:
        print('Invalid Input...\n')
        print('Please choose one of the options listed\n')
