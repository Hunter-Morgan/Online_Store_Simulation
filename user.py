import sqlite3
import sys

class User:
    def __init__(self, databaseName, tableName):
        self.databaseName = databaseName
        self.tableName = tableName
        self.loggedIn = False
        self.connection = None
        self.cursor = None

    #checks if the table exists and if not, creates the table
    def __enter__(self):
        self.connection = self.databaseConnect(self.databaseName)
        self.cursor = self.connection.cursor()
        if not self.tableExists():
            self.createTable()
        return self

    #destructor
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
    
    def tableExists(self):
        self.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.tableName}'"
        )
        return self.cursor.fetchone() is not None
    
    def createTable(self):
        self.cursor.execute( f'''
            CREATE TABLE IF not exists {self.tableName} (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Email TEXT,
                Password TEXT,
                Firstname TEXT,
                Lastname TEXT,
                Address TEXT,
                City TEXT,
                State TEXT,
                Zip INTEGER,
                Payment TEXT
            )
        '''
        )
    
    #user functions
    def login(self, Email, Password):
        self.cursor.execute(
            f"SELECT * FROM {self.tableName} WHERE Email = ?", (Email,)
        )
        data = self.cursor.fetchone()
        if data and data[2] == Password:
            self.UserID = data[0]
            self.Email = data[1]
            self.Password = data[2]
            self.Firstname = data[3]
            self.Lastname = data[4]
            self.Address = data[5]
            self.City = data[6]
            self.State = data[7]
            self.loggedIn = True
            return True
        else:
            return None
    
    def logout(self):
        self.UserID = None
        self.loggedIn = False
    
    def viewAccountInformation(self):
        self.cursor.execute(
            f"SELECT * FROM {self.tableName} WHERE UserID = ?", (self.UserID,)
        )
        data = self.cursor.fetchone()
        if data:
            print(f"UserID: {data[0]}")
            print(f"Email: {data[1]}")
            print(f"Password: {data[2]}")
            print(f"Firstname: {data[3]}")
            print(f"Lastname: {data[4]}")
            print(f"Address: {data[5]}")
            print(f"City: {data[6]}")
            print(f"State: {data[7]}")
            print(f"Zip: {data[8]}")
            print(f"Payment: {data[9]}\n")
        else:
            print("account doesn't exist")
    
    def getUserID(self):
        self.cursor.execute(
            f"SELECT UserID FROM {self.tableName} WHERE UserID = ?", (self.UserID,)
        )
        id = self.cursor.fetchone()
        if id:
            return id[0]
        else:
            print("id not found")

    def createAccount(self, Email, Password, Firstname, Lastname, Address, City, State, Zip, Payment):
        self.cursor.execute('''
            INSERT INTO {table} (Email, Password, Firstname, Lastname, Address, City, State, Zip, Payment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''.format(table=self.tableName), (Email, Password, Firstname, Lastname, Address, City, State, Zip, Payment))
        self.UserID = self.cursor.lastrowid
        self.connection.commit()

    @staticmethod
    def databaseConnect(databaseName):
        try:
            connection = sqlite3.connect(databaseName)
            print("Connection Successful")
            return connection
        except:
            print("Connection unsuccessful, ending program")    
            sys.exit()