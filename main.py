import sqlite3
import sys
from user import User
from inventory import Inventory
from CartCode import Cart

def is_valid_zip(zip_code):
    return zip_code.isdigit() and len(zip_code) == 5

def main_menu(user):
    while True:
        print("Main Menu:")
        print("0. Exit")
        print("1. Login")
        print("2. Create Account")
        option = input("Enter an option: ")

        if option == "0":
            sys.exit()
        elif option == "1":
            login_menu(user)
        elif option == "2":
            create_account(user)
        else:
            print("Invalid input. Please try again.")

def login_menu(user):
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if user.login(email, password):
        print("Login successful!\n")
        logged_in_menu(user)
    else:
        print("Login failed. Please check your credentials.\n")

def logged_in_menu(user):
    x = Inventory()
    x.setTableName("inventory")
    x.setDatabaseName("store.db") 
    dbname=x.getDatabaseName() 
    UserID = user.getUserID()
    while True:
        print("Logged In Menu:")
        print("0. Logout")
        print("1. View Account Information")
        print("2. Inventory Information")
        print("3. Cart Information")
        option = input("Enter an option: ")

        if option == "0":
            user.logout()
            print("Logged out.\n")
            break
        elif option == "1":
            user.viewAccountInformation()
        elif option == "2":
            print("\nInventory Menu:")
            print("1. View Inventory")
            print("2. Search Inventory")
            print("Press Any Other Key To Go Back")
            option = input("Enter an option: ")
            if option == "1":
                view = Inventory()
                view.viewInventory()
            elif option == "2":
                search = Inventory()
                search.searchInventory()
            else:
                print()
                continue
        elif option=="3":
            choice ="-1"
            while choice != "0":
                print("\n Cart Menu:")
                print("0. Go Back")
                print("1. View Cart")
                print("2. Add Items to Cart")
                print("3. Remove an Item Cart")
                print("4. Check Out")
                choice= input("Enter an option: ")
                C=Cart()
                if choice=="1":
                    C.viewCart(UserID,dbname)
                elif choice=="2":
                    i = Inventory()
                    i.viewInventory()
                    ISBN=input("Enter The ISBN of the book you want to add:  ")
                    C.addToCart(UserID,ISBN)
                elif choice=="3":
                    connection = sqlite3.connect("store.db")
                    cursor=connection.cursor()
                    query=("Select * From inventory JOIN cart ON inventory.ISBN = cart.ISBN AND USerID= ?")
                    data=(UserID,)
                    cursor.execute(query,data,)
                    results=cursor.fetchall()
                    if len(results) !=0:
                        connection.close()
                        C.viewCart(UserID,dbname)
                        ISBN=input("Enter The ISBN of the book you want to remove:  ")
                        C.removeFromCart(UserID,ISBN)
                    else:
                        connection.close()
                        print("\tCart is currently empty.\n\tCan not delete at this time. ")
                    
                elif choice=="4":
                    C.checkOut(UserID)
        else:
            print("Invalid input. Please try again.")

def create_account(user):
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    firstname = input("Enter your firstname: ")
    lastname = input("Enter your lastname: ")
    address = input("Enter your address: ")
    city = input("Enter your city: ")
    state = input("Enter your state: ")

    while True:
        zipcode = input("Enter your zipcode (5 digits): ")
        if is_valid_zip(zipcode):
            break
        else:
            print("Invalid input. Zipcode must be an integer exactly 5 digits.")

    payment = input("Enter your payment method: ")

    user.createAccount(email, password, firstname, lastname, address, city, state, zipcode, payment)
    print("Account created successfully!\n")

if __name__ == "__main__":
    with User('store.db', 'User') as user:
        main_menu(user)

