# Inventory Management System - Week 5
# This program uses dictionaries and lists to store inventory products.


# =========================================================
# INITIAL INVENTORY
# =========================================================

# Each product is stored as a dictionary.
# The product dictionaries are stored inside a list.

inventory = [
    {
        "id": "P001",
        "name": "Laptop",
        "price": 1200.00,
        "stock": 15
    },
    {
        "id": "P002",
        "name": "Mouse",
        "price": 25.50,
        "stock": 40
    },
    {
        "id": "P003",
        "name": "Keyboard",
        "price": 45.00,
        "stock": 25
    }
]


# =========================================================
# DISPLAY CURRENT INVENTORY
# =========================================================

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")

print("Current Inventory")
print("------------------------------------------------")

# Display every product stored in the inventory list
for product in inventory:
    print(
        f"ID: {product['id']} | "
        f"Name: {product['name']} | "
        f"Price: ${product['price']:.2f} | "
        f"Stock: {product['stock']}"
    )

print("------------------------------------------------")