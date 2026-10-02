# Inventory Management System - Week 5
# This program uses dictionaries and lists to manage inventory products.

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

            # Load the JSON data into a Python list
            inventory = json.load(file)

        print("inventory.json found.")
        print("Inventory loaded successfully.")

        # Return the loaded inventory
        return inventory

    except FileNotFoundError:

        # If inventory.json does not exist,
        # begin with an empty inventory
        print("inventory.json not found.")
        print("Starting with an empty inventory.")

        return []


# =========================================================
# MAIN PROGRAM
# =========================================================

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")

# Load existing inventory from inventory.json
inventory = load_inventory()

print()

# Display the current inventory
print("Current Inventory")
print("------------------------------------------------")

# Check whether there are products
if len(inventory) == 0:
    print("No products in inventory.")

else:

    # Display every product in the inventory
    for product in inventory:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | "
            f"Stock: {product['stock']}"
        )

print("------------------------------------------------")