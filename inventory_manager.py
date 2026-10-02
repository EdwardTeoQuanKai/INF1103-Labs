# Inventory Management System - Week 5
# This program uses dictionaries, lists and JSON
# to manage inventory products.

import json


# ---------------------------------------------------------
# FUNCTION 1: load_inventory()
# ---------------------------------------------------------
# What goes in?
# - Nothing
#
# What comes out?
# - Existing inventory products from inventory.json
#
# If inventory.json does not exist,
# begin with an empty inventory.
def load_inventory():

    try:
        # Try to open inventory.json for reading
        with open("inventory.json", "r") as file:

            # Load JSON data into a Python list
            inventory = json.load(file)

        print("inventory.json found.")
        print("Inventory loaded successfully.")

        return inventory

    except FileNotFoundError:

        # If inventory.json does not exist,
        # begin with an empty inventory
        print("inventory.json not found.")
        print("Starting with an empty inventory.")

        return []


# ---------------------------------------------------------
# FUNCTION 2: display_all(inventory)
# ---------------------------------------------------------
# What goes in?
# - inventory = list containing all product dictionaries
#
# What comes out?
# - Displays all products currently in inventory
def display_all(inventory):

    print("Current Inventory")
    print("------------------------------------------------")

    # Check whether inventory is empty
    if len(inventory) == 0:
        print("No products in inventory.")

    else:

        # Display every product
        for product in inventory:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

    print("------------------------------------------------")


# ---------------------------------------------------------
# FUNCTION 3: add_product(inventory)
# ---------------------------------------------------------
# What goes in?
# - inventory = current inventory list
#
# What comes out?
# - Adds a new product dictionary into inventory
def add_product(inventory):

    print("Add New Product")

    # Ask for Product ID
    product_id = input("Product ID: ").strip()

    # Check whether the Product ID already exists
    for product in inventory:

        if product["id"].lower() == product_id.lower():
            print("Product ID already exists.")
            return

    # Ask for Product Name
    product_name = input("Product Name: ").strip()

    # Check whether product name is empty
    if product_name == "":
        print("Error: Product name cannot be empty.")
        return

    # Ask for product price
    price_input = input("Price: ")

    try:
        price = float(price_input)

        if price < 0:
            print("Error: Price cannot be negative.")
            return

    except ValueError:
        print("Error: Please enter a valid price.")
        return

    # Ask for stock quantity
    stock_input = input("Stock Quantity: ")

    if not stock_input.isdigit():
        print("Error: Please enter a valid stock quantity.")
        return

    stock = int(stock_input)

    # Create a dictionary for the new product
    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    # Add the new dictionary into the inventory list
    inventory.append(new_product)

    print("Product added successfully!")


# ---------------------------------------------------------
# FUNCTION 4: update_stock(inventory)
# ---------------------------------------------------------
# What goes in?
# - inventory = current inventory list
#
# What comes out?
# - Updates the stock quantity of an existing product
def update_stock(inventory):

    print("Update Stock")

    # Ask for Product ID
    product_id = input("Enter Product ID: ").strip()

    # Search for the product
    for product in inventory:

        if product["id"].lower() == product_id.lower():

            print("Product Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")

            # Ask for new stock quantity
            stock_input = input("New Stock Quantity: ")

            if not stock_input.isdigit():
                print("Error: Please enter a valid stock quantity.")
                return

            # Update the product stock
            product["stock"] = int(stock_input)

            print("Stock updated successfully!")
            return

    # Product ID was not found
    print("Product not found.")


# ---------------------------------------------------------
# FUNCTION 5: search_product(inventory)
# ---------------------------------------------------------
# What goes in?
# - inventory = current inventory list
#
# What comes out?
# - Searches and displays one product
def search_product(inventory):

    print("Search Product")

    # Ask for Product ID
    product_id = input("Enter Product ID: ").strip()

    # Search through the inventory
    for product in inventory:

        if product["id"].lower() == product_id.lower():

            print("Product Found")
            print("------------------------------------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("------------------------------------------------")

            return

    # Product ID was not found
    print("Product not found.")


# ---------------------------------------------------------
# FUNCTION 6: save_inventory(inventory)
# ---------------------------------------------------------
# What goes in?
# - inventory = current inventory list
#
# What comes out?
# - Saves all inventory data into inventory.json
def save_inventory(inventory):

    # Open inventory.json in write mode
    with open("inventory.json", "w") as file:

        # Save the inventory list in JSON format
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


# ---------------------------------------------------------
# FUNCTION 7: display_menu()
# ---------------------------------------------------------
# What goes in?
# - Nothing
#
# What comes out?
# - Displays the inventory menu
def display_menu():

    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# =========================================================
# MAIN PROGRAM
# =========================================================
def main():

    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    # Load existing inventory
    inventory = load_inventory()

    # Keep running until the user selects Exit
    while True:

        display_menu()

        option = input("Enter option: ")

        # OPTION 1 - Display all products
        if option == "1":
            display_all(inventory)

        # OPTION 2 - Add a product
        elif option == "2":
            add_product(inventory)

        # OPTION 3 - Update stock
        elif option == "3":
            update_stock(inventory)

        # OPTION 4 - Search for a product
        elif option == "4":
            search_product(inventory)

        # OPTION 5 - Save inventory
        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        # OPTION 6 - Save and exit
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)

            print("Thank you for using Inventory Management System.")
            print("Program terminated.")

            break

        # Invalid menu option
        else:
            print("Invalid option. Please select 1 to 6.")


# Run the program
main()