import sqlite3
import sys
#from user import User
from inventory import Inventory

class Cart: 

    def __init__(self):
        #zero argument needed.
        freecode=0

    def Cart(self,databaseName,tableName):
        
        self.databaseName = databaseName
        self.tableName = tableName


    def viewCart(self ,UserID, inventoryDatabase):
        try:
            connection = sqlite3.connect(inventoryDatabase)
        except:
            print("Failed connection.")
            sys.exit()
        cursor=connection.cursor()
        query=("Select * From inventory JOIN cart ON inventory.ISBN = cart.ISBN AND USerID= ?")
        data=(UserID,)
        cursor.execute(query,data,)
        results=cursor.fetchall()
        if len(results) !=0:
            print("\nYour Cart : \n")
            for x in results:
                print("ISBN:", x[0], 
                    "\nTitle:", x[1],
                    "\nAuthor: ", x[2],
                    "\nTotal In Stock: ", x[6],
                    "     Quantity in Cart: ", x[9]
                     )
                print()
        else: 
            print("\n\tYour Cart is Currently empty.")
            print("\tAdd books to your Cart to view Cart.")

    def addToCart(self,UserID,ISBN):
        try:
            connection = sqlite3.connect("store.db")
        except:
            print("Failed connection.")
            sys.exit()
        cursor = connection.cursor()
        cursor.execute("Select ISBN From inventory")
        a=1
        b=1
        c=1
        resultsA=cursor.fetchall()
        Aresults=len(resultsA)
        for x in range(Aresults,0,-1):
            for x in resultsA:
                if x[0]==ISBN:
                    a=0
                    break
                elif x[0]!=ISBN:
                    a=1
            if a==1:
                print("\tInvalid ISBN.\n\tNothing added to cart")
                break
        query1=("Select stock From inventory where inventory.isbn= ?")
        data1=(ISBN,)
        cursor.execute(query1,data1,)
        resultsB=cursor.fetchall()
        Bresults=len(resultsB)
        for y in resultsB:
            if y[0]==0:

                b=1
            elif y[0]>0:
                b=0
            if b==1:
                    print("Book is out of Stock")
                    break
        query=("Select * From inventory JOIN cart ON inventory.ISBN = ? AND USerID= ? AND Cart.ISBN = ?")
        data=(ISBN,UserID,ISBN,)
        cursor.execute(query,data,)
        resultsC=cursor.fetchall()
        Cresults=len(resultsC)
        if Cresults!=0:
            for z in range(Cresults,0,-1):
                for z in resultsC:
                    if z[0]==ISBN:
                        c=1
                        
                    elif z[0]!=ISBN:
                        c=0
                        break
                if c==1:
                    print("\tBook already in Cart.\n\tDelete and Add it back to change quantity.")
                    break
        else:
            c=0
        if a==0 and b==0 and c==0:
            bquantity=input("Enter how many you want: ")
            bquantity=int(bquantity)

            while bquantity<=0:
                print("\tInavlid Quantity.\n\tEneter a value over 0")
                bquantity=input("Enter how many you want: ")
            query=("INSERT INTO cart(UserID, ISBN, Quantity) SELECT User.UserID, inventory.ISBN, ? FROM User, inventory WHERE UserID = ? AND ISBN = ?;")
            data=(bquantity,UserID,ISBN,)
            cursor.execute(query,data)
            connection.commit()   
        connection.close()


    def removeFromCart(self,UserID, ISBN):
        try:
            connection = sqlite3.connect("store.db")
        except:
            print("Failed connection.")
            sys.exit()

        cursor=connection.cursor()
        
        removeQuan=input("Enter how many you want to remove: ")
        removeQuantity=int (removeQuan)
        query=("Select * From inventory JOIN cart ON inventory.ISBN = ? AND USerID= ? AND Cart.ISBN = ?")
        data=(ISBN,UserID,ISBN,)
        cursor.execute(query,data)
        results=cursor.fetchall()
        if len(results) !=0:
            for x in results:
                if x[9]<=removeQuantity:
                    query=("Delete  From Cart Where cart.ISBN= ? and UserID = ?")
                    data=(ISBN,UserID,)
                    cursor.execute(query,data)
                elif x[9]> removeQuantity and removeQuantity>0:
                    newQuan=x[9]-removeQuantity
                    query=("Update Cart Set Quantity = ? Where cart.ISBN= ? and UserID = ?")
                    data=(newQuan,ISBN,UserID,)
                    cursor.execute(query,data)
                else:
                        print("\tThe Number Entered is Invalid.")
        elif len(results)==0:
            query=("Select * From inventory JOIN cart ON inventory.ISBN = cart.ISBN AND USerID= ?")
        
            data=(UserID,)
            cursor.execute(query,data,)
            results=cursor.fetchall()
            if(len(results))!=0:
                print("\tThe Book you Entered is not currently in your Cart.")
            else:
                print("\tThere are No books to remove.\n\tCart is Empty.")

        connection.commit()
        connection.close()

    def checkOut(self,UserID):
        try:
            connection = sqlite3.connect("store.db")
        except:
            print("Failed connection.")
            sys.exit()

        cursor=connection.cursor()
        query=("Select * From inventory JOIN cart ON inventory.ISBN = cart.ISBN AND USerID= ?")
        data=(UserID,)
        cursor.execute(query,data,)
        results=cursor.fetchall()
        f=1
        if len(results) !=0:
            print("Are you sure you want to order:")
            for x in results:
                print("Title: ",x[1],"  Quantity: ", x[9])
                print()
                if x[6]<x[9]:
                        print("\tThere aren't enough", x[1],"In stock.")
                        print("\tDeleting book from Cart")
                        ISBN=x[0]
                        query=("Delete  From Cart Where cart.ISBN= ? and UserID = ?")
                        data=(ISBN,UserID,)
                        cursor.execute(query,data)
                        connection.commit()
                        connection.close()
                        f=0
                        break
            if(f==1):
                choice=input("Type 1 to Confirm or 2 to Cancel: ")
                if(choice=='1'):
                    print("Thank you for your purchase!")
                    i=Inventory()
                    query=("Select * From inventory JOIN cart ON inventory.ISBN = cart.ISBN AND USerID= ?")
                    data=(UserID,)
                    cursor.execute(query,data,)
                    results1=cursor.fetchall()
                    for x in results1:
                        ISBN=x[0]
                        Quan=x[9]
                        currentBook=x[0]
                        while Quan!=0:
                            connection = sqlite3.connect("store.db")
                            cursor=connection.cursor()
                            query=("Update Cart Set Quantity = ? Where cart.ISBN= ? and UserID = ?")
                            data=(Quan,ISBN,UserID,)
                            cursor.execute(query,data)
                            Quan=Quan-1
                            connection.commit()
                            connection.close()
                            i.decreaseStock(currentBook)
                        if Quan==0:
                            connection = sqlite3.connect("store.db")
                            cursor=connection.cursor()
                            query=("Delete  From Cart Where cart.ISBN= ? and UserID = ?")
                            data=(ISBN,UserID,)
                            cursor.execute(query,data)
                            connection.commit()
                            connection.close()
                elif(choice=='2'):
                    print("\tLeaving Check Out")
                    connection.commit()
                    connection.close()
        else:
            print("\tNothing in cart to check out.\n\tAdd something to Cart before checking out.")
                        