
# Inventory Management System - Lab 6 (Week 8 OOP)
# Refactored from the Week 5 inventory management system.
# Product manages one product; Inventory manages multiple products.

import json


# =========================================================
# CLASS 1: Product
# =========================================================
class Product:

    # Store information for one product (private attributes).
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Change this product's stock instead of editing it externally.
    def update_stock(self, quantity):
        if quantity < 0:
            print("Error: Stock cannot be negative.")
            return

        self.__stock = quantity

    # Display this product's information.
    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    # Allow Inventory to look up products without accessing private data.
    def get_product_id(self):
        return self.__product_id

    # Convert this object into a dictionary for saving as JSON.
    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


# =========================================================
# CLASS 2: Inventory
# =========================================================
class Inventory:

    # Keep a list of Product objects.
    def __init__(self):
        self.__products = []

    # Add one Product object, rejecting duplicate IDs.
    def add_product(self, product, show_message=True):

        if self.search_product(product.get_product_id()) is not None:
            print("Product ID already exists.")
            return

        self.__products.append(product)

        if show_message:
            print("Product added successfully!")

    # Return a matching Product object, or None if not found.
    def search_product(self, product_id):

        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product

        return None

    # Display all products in the inventory.
    def display_all(self):

        print("Current Inventory")
        print("------------------------------------------------")

        if len(self.__products) == 0:
            print("No products in inventory.")

        else:
            for product in self.__products:
                product.display_information()
                print("------------------------------------------------")

        if len(self.__products) == 0:
            print("------------------------------------------------")

    # Convert all Product objects into dictionaries for saving.
    def to_dict_list(self):

        inventory_data = []

        for product in self.__products:
            inventory_data.append(product.to_dict())

        return inventory_data


# =========================================================
# FILE HANDLING
# =========================================================

# FUNCTION 1: load_inventory()
# Read dictionaries from JSON and turn them into Product objects.
def load_inventory():

    try:
        with open("inventory.json", "r") as file:
            saved_products = json.load(file)

        print("inventory.json found.")

    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
        return Inventory()

    # Create an Inventory object.
    inventory = Inventory()

    # Convert each dictionary into a Product object.
    for product_data in saved_products:

        product = Product(
            product_data["id"],
            product_data["name"],
            product_data["price"],
            product_data["stock"]
        )

        inventory.add_product(product, show_message=False)

    print("Inventory loaded successfully.")
    return inventory


# FUNCTION 2: save_inventory()
# Convert Product objects into dictionaries before writing JSON.
def save_inventory(inventory):

    inventory_data = inventory.to_dict_list()

    with open("inventory.json", "w") as file:
        json.dump(inventory_data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


# =========================================================
# USER INPUT FUNCTIONS
# =========================================================

# FUNCTION 3: handle_add_product()
# Gets user input and creates a new Product object.
def handle_add_product(inventory):

    print("Add New Product")

    product_id = input("Product ID: ").strip()

    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return

    # Check for duplicate Product ID.
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()

    if product_name == "":
        print("Error: Product name cannot be empty.")
        return

    price_input = input("Price: ")

    try:
        price = float(price_input)

        if price < 0:
            print("Error: Price cannot be negative.")
            return

    except ValueError:
        print("Error: Please enter a valid price.")
        return

    stock_input = input("Stock Quantity: ")

    if not stock_input.isdigit():
        print("Error: Please enter a valid stock quantity.")
        return

    stock = int(stock_input)

    # Create a Product object instead of a dictionary.
    new_product = Product(product_id, product_name, price, stock)

    # Add it using the Inventory class.
    inventory.add_product(new_product)


# FUNCTION 4: handle_update_stock()
# Finds a product and updates its stock through its method.
def handle_update_stock(inventory):

    print("Update Stock")

    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    product.display_information()

    stock_input = input("New Stock Quantity: ")

    if not stock_input.isdigit():
        print("Error: Please enter a valid stock quantity.")
        return

    product.update_stock(int(stock_input))

    print("Stock updated successfully!")


# FUNCTION 5: handle_search_product()
# Searches for a product using its ID.
def handle_search_product(inventory):

    print("Search Product")

    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is not None:
        print("Product Found")
        print("------------------------------------------------")
        product.display_information()
        print("------------------------------------------------")

    else:
        print("Product not found.")


# =========================================================
# FUNCTION 6: display_menu()
# =========================================================
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

    # Load existing inventory from JSON.
    inventory = load_inventory()

    # Continue running until the user selects Exit.
    while True:

        display_menu()

        option = input("Enter option: ")

        # OPTION 1 - Display all products.
        if option == "1":
            inventory.display_all()

        # OPTION 2 - Add a new product.
        elif option == "2":
            handle_add_product(inventory)

        # OPTION 3 - Update stock.
        elif option == "3":
            handle_update_stock(inventory)

        # OPTION 4 - Search for a product.
        elif option == "4":
            handle_search_product(inventory)

        # OPTION 5 - Save inventory.
        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        # OPTION 6 - Save and exit.
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)

            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        # Invalid menu option.
        else:
            print("Invalid option. Please select 1 to 6.")


# Run the program.
if __name__ == "__main__":
    main()
