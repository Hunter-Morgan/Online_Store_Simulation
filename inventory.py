import sqlite3
import sys

class Inventory:

    # Constructor
    def __init__(self, databaseName = "", tableName = ""):
        self.databaseName = databaseName
        self.tableName = tableName

    
    # Function for viewing inventory
    def viewInventory(self):
        # attempts to connect to the database
        try:
            connection = sqlite3.connect("store.db")

        except:
            print("Failed connection.")

            # exits the program if unsuccessful
            sys.exit()

        print() # for spacing

        # Cursor to send queries through
        cursor = connection.cursor()

        # Select All query
        cursor.execute("SELECT * FROM inventory")

        # Retrieve data from table
        result = cursor.fetchall()
        # Display inventory
        print("Inventory:\n")
        for x in result:

            print("ISBN:", x[0], "\tTitle:", x[1])
            print("Author:", x[2])
            print("Genre:", x[3], "\tPages:", x[4])
            print("Release Date:", x[5])
            print("In Stock:", x[6])
            print()
    
        # Close cursor and connection
        cursor.close()
        connection.close()

    
    # Function for searching inventory
    def searchInventory(self):
        # attempts to connect to the database
        try:
            connection = sqlite3.connect("store.db")

        except:
            print("Failed connection.")

            # exits the program if unsuccessful
            sys.exit()
        
        print() # for spacing

        # Cursor to send queries through
        cursor = connection.cursor()

        # Create a query with user input
        query = "SELECT * FROM inventory WHERE Title=?"

        # Request book title
        data = (input("What is the title of the book you would like to search? "),)

        # Execute search
        cursor.execute(query, data)
        result = cursor.fetchall()

        # Commits change
        connection.commit()

        # Display search results
        if result:
            print("\nMatches found:\n")

            for x in result:
                print("ISBN:", x[0], "\tTitle:", x[1])
                print("Author:", x[2])
                print("Genre:", x[3], "\tPages:", x[4])
                print("Release Date:", x[5])
                print("In Stock:", x[6])
                print()    
        else:
            print("\nNo matches found.\n")

        # Close cursor and connection
        cursor.close()
        connection.close()

    def decreaseStock(self, ISBN):
        # attempts to connect to the database
        try:
            connection = sqlite3.connect("store.db")

        except:
            print("Failed connection.")

            # exits the program if unsuccessful
            sys.exit()
        
        print() # for spacing

        # Cursor to send queries through
        cursor = connection.cursor()

        # Create a query to select Stock
        query = "SELECT Stock FROM inventory WHERE ISBN=?"

        # Input ISBN
        data = (ISBN,)

        # Execute search
        cursor.execute(query, data)
        result = cursor.fetchall()
        
        # Decrease stock
        for x in result:
            result = x[0] -1
        
        # Commits change
        connection.commit()

        # Create a query to update Stock
        query = "UPDATE inventory SET Stock=? WHERE ISBN=?"

        # Input data
        data = (result, ISBN,)

        # Execute search
        cursor.execute(query, data)

        # Commits change
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

    # Getters
    def getDatabaseName(self):
        return self.databaseName

    def getTableName(self):
        return self.tableName

    # Setters
    def setDatabaseName(self, databaseName):
        self.databaseName = databaseName

    def setTableName(self, tableName):
        self.tableName = tableName