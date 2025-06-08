# Online_Store_Simulation

A Python-based user interface with an inventory system and shopping cart for a bookstore, backed by an SQLite database.

## Description

This project was created in a collaborative effort with a class group. It manages a bookstore’s inventory and user shopping carts using SQLite and Python classes. It supports account creation and login, viewing and searching the inventory, adding/removing books from a cart, and checking out with stock updates. The system handles multiple users with separate carts through a stored User ID.

## Contributors
- **Store Menu** (`main.py`): Developed by Entire Team
- **User Interface** (`user.py`): Developed by Grant Hayes
- **Inventory Management** (`inventory.py`): Developed by Hunter Morgan  
- **Cart System & Checkout Logic** (`CartCode.py`): Developed by Gabe Alpha  
- **Database Design** (`store.db`): Developed by Hunter Morgan
  
## Files
- `main.py` – Defines the store menu logic and acts as a driver program
- `user.py` – Defines the `User` class for storing and handling user information
- `inventory.py` – Defines the `Inventory` class for interacting with and updating the book inventory database  
- `CartCode.py` – Defines the `Cart` class for managing user carts, including add, remove, view, and checkout functions  
- `store.db` – SQLite database storing inventory, users, and cart tables 

## How to Run

Run the main script in a Python environment:

```bash
python main.py
```
