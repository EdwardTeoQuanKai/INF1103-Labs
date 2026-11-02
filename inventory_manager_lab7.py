
# INF1103 Lab 7 - Inventory Management System
# Week 9: Inheritance, Overriding, Abstract Classes, and Interfaces
# Extended from the Lab 6 OOP inventory manager.

import json
import math
from abc import ABC, abstractmethod


# =========================================================
# INTERFACE: CanBeShipped
# =========================================================
# Defines a capability that a class must implement.
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


# =========================================================
# ABSTRACT PARENT CLASS: Product
# =========================================================
# Stores common product information and behaviour.
# A Product cannot be created directly because it is abstract.
class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        if quantity < 0:
            print("Error: Stock cannot be negative.")
            return
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def get_product_id(self):
        return self.__product_id

    @abstractmethod
    def get_fulfilment_info(self):
        # Every child class must implement this method.
        pass

    def to_dict(self):
        # Shared fields for JSON persistence.
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


# =========================================================
# CHILD CLASS: PhysicalProduct
# =========================================================
# PhysicalProduct is-a Product and can be shipped.
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    # Override the parent display method.
    def display_information(self):
        super().display_information()
        print("Type: Physical")
        print(f"Weight: {self.__weight:.2f} kg")
        print(self.get_fulfilment_info())
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "Fulfilment: Requires physical shipping."

    # Implement the shipping interface.
    def calculate_shipping_cost(self):
        # $5 base fee + $2 per kilogram.
        return 5.00 + (2.00 * self.__weight)

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


# =========================================================
# CHILD CLASS: DigitalProduct
# =========================================================
# Digital products do not need physical shipping.
class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    # Override the parent display method.
    def display_information(self):
        super().display_information()
        print("Type: Digital")
        print(f"Download Size: {self.__download_size:.2f} MB")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self):
        return "Fulfilment: Delivered digitally by download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data


# =========================================================
# CLASS: Inventory
# =========================================================
# Manages multiple Product objects.
class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product, show_message=True):

        if self.search_product(product.get_product_id()) is not None:
            print("Product ID already exists.")
            return

        self.__products.append(product)

        if show_message:
            print("Product added successfully!")

    def search_product(self, product_id):

        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product

        return None

    def display_all(self):

        print("Current Inventory")
        print("------------------------------------------------")

        if not self.__products:
            print("No products in inventory.")
            print("------------------------------------------------")
            return

        for product in self.__products:
            product.display_information()
            print("------------------------------------------------")

    def to_dict_list(self):
        return [product.to_dict() for product in self.__products]


# =========================================================
# USER INPUT HELPERS
# =========================================================
def read_nonnegative_float(prompt):

    while True:
        entered = input(prompt).strip()

        try:
            number = float(entered)
        except ValueError:
            print("Error: Please enter a valid number.")
            continue

        if not math.isfinite(number) or number < 0:
            print("Error: Enter a non-negative, finite number.")
            continue

        return number


def ask_product_type():

    while True:
        print("1. Physical Product")
        print("2. Digital Product")

        selection = input("Choose product type (1/2): ").strip()

        if selection == "1":
            weight = read_nonnegative_float("Weight (kg): ")
            return "physical", weight

        if selection == "2":
            download_size = read_nonnegative_float(
                "Download Size (MB): "
            )
            return "digital", download_size

        print("Invalid product type. Please select 1 or 2.")


def create_product(product_id, name, price, stock, product_type, extra):

    if product_type == "physical":
        return PhysicalProduct(
            product_id, name, price, stock, extra
        )

    if product_type == "digital":
        return DigitalProduct(
            product_id, name, price, stock, extra
        )

    raise ValueError(f"Unknown product type: {product_type}")


# =========================================================
# JSON FILE HANDLING
# =========================================================
def load_inventory():

    try:
        with open("inventory.json", "r", encoding="utf-8") as file:
            saved_products = json.load(file)

        print("inventory.json found.")

    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
        return Inventory()

    except json.JSONDecodeError:
        print("Error: inventory.json contains invalid JSON.")
        raise SystemExit(1)

    if not isinstance(saved_products, list):
        print("Error: inventory.json should contain a list of products.")
        raise SystemExit(1)

    inventory = Inventory()

    try:
        for data in saved_products:

            product_type = data.get("type")

            # Convert older Lab 6 records into Lab 7 objects.
            if product_type is None:

                print(
                    f"\nLab 6 product {data['id']} ({data['name']}) "
                    "has no product type."
                )
                print(
                    "Choose its type and provide "
                    "its additional information:"
                )

                product_type, extra = ask_product_type()

            elif product_type == "physical":
                extra = float(data["weight"])

            elif product_type == "digital":
                extra = float(data["download_size"])

            else:
                raise ValueError(f"Unknown type: {product_type}")

            if not math.isfinite(extra) or extra < 0:
                raise ValueError("Invalid weight or download size")

            product = create_product(
                data["id"],
                data["name"],
                float(data["price"]),
                int(data["stock"]),
                product_type,
                extra
            )

            inventory.add_product(product, show_message=False)

    except (KeyError, TypeError, ValueError) as error:
        print(
            f"Error: Invalid product data in inventory.json ({error})."
        )
        raise SystemExit(1)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):

    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(inventory.to_dict_list(), file, indent=4)

    print("Inventory saved successfully to inventory.json.")


# =========================================================
# USER INPUT FUNCTIONS
# =========================================================

# FUNCTION 1: Add Product
def handle_add_product(inventory):

    print("Add New Product")

    product_id = input("Product ID: ").strip()

    if not product_id:
        print("Error: Product ID cannot be empty.")
        return

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()

    if not product_name:
        print("Error: Product name cannot be empty.")
        return

    price = read_nonnegative_float("Price: ")

    stock_input = input("Stock Quantity: ").strip()

    if not stock_input.isdigit():
        print("Error: Please enter a valid stock quantity.")
        return

    stock = int(stock_input)

    # Choose between physical and digital products.
    product_type, extra = ask_product_type()

    # Create the correct subclass object.
    product = create_product(
        product_id,
        product_name,
        price,
        stock,
        product_type,
        extra
    )

    inventory.add_product(product)


# FUNCTION 2: Update Stock
def handle_update_stock(inventory):

    print("Update Stock")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    product.display_information()

    stock_input = input("New Stock Quantity: ").strip()

    if not stock_input.isdigit():
        print("Error: Please enter a valid stock quantity.")
        return

    product.update_stock(int(stock_input))
    print("Stock updated successfully!")


# FUNCTION 3: Search Product
def handle_search_product(inventory):

    print("Search Product")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("------------------------------------------------")
    product.display_information()
    print("------------------------------------------------")


# =========================================================
# MENU
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
    print("INVENTORY MANAGEMENT SYSTEM - LAB 7")
    print("========================================")

    inventory = load_inventory()

    while True:

        display_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            handle_add_product(inventory)

        elif option == "3":
            handle_update_stock(inventory)

        elif option == "4":
            handle_search_product(inventory)

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)

            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please select 1 to 6.")


if __name__ == "__main__":
    main()
