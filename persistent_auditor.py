# Persistent Inventory Auditor - Week 4
# This program uses functions to manage inventory orders.


# ---------------------------------------------------------
# FUNCTION 1: get_product_name()
# ---------------------------------------------------------
# What goes in?
# - Nothing
#
# What comes out?
# - Product name entered by the user
# - "quit" if the user wants to stop
def get_product_name():

    # Ask the user to enter a product name
    product_name = input("Enter Product Name (or 'quit' to stop): ")

    # Check whether the user wants to stop
    if product_name.lower() == "quit":
        return "quit"

    # Check whether the product name is empty
    if product_name.strip() == "":
        print("Error: Please enter a product name.")
        return None

    # Return the product name
    return product_name


# ---------------------------------------------------------
# FUNCTION 2: get_valid_quantity()
# ---------------------------------------------------------
# What goes in?
# - Nothing
#
# What comes out?
# - A valid integer quantity
# - None if the input is invalid
def get_valid_quantity():

    # Ask the user to enter a quantity
    stock = input("Enter Quantity: ")

    # Check whether the quantity is a valid positive integer
    if not stock.isdigit():
        print("Error: Please enter a valid integer.")
        return None

    # Convert the quantity into an integer
    quantity = int(stock)

    # Return the valid quantity
    return quantity


# ---------------------------------------------------------
# FUNCTION 3: load_inventory()
# ---------------------------------------------------------
# What goes in?
# - Nothing
#
# What comes out?
# - Existing orders from inventory.txt
#
# If inventory.txt does not exist, create an empty file
# and continue without producing an error.
def load_inventory():

    # Create an empty list for the current orders
    current_orders = []

    try:
        # Try to open inventory.txt for reading
        with open("inventory.txt", "r") as file:

            # Read each saved order
            for line in file:

                # Remove spaces and newline characters
                line = line.strip()

                # Ignore empty lines
                if line == "":
                    continue

                # Ignore the final total and transaction history
                if line.startswith("Final Total:"):
                    continue

                if line.startswith("Transaction History:"):
                    continue

                # Split the saved order:
                # Product ID, Product Name, Quantity
                parts = line.split(",")

                if len(parts) == 3:

                    product_id = int(parts[0].strip())
                    product_name = parts[1].strip()
                    quantity = int(parts[2].strip())

                    # Add the loaded order into memory
                    current_orders.append(
                        [product_id, product_name, quantity]
                    )

    except FileNotFoundError:

        # inventory.txt does not exist,
        # so create a new empty file
        with open("inventory.txt", "w") as file:
            pass

        print("inventory.txt not found.")
        print("Created a new empty inventory.txt file.")
        print()

    # Return the loaded inventory
    return current_orders


# ---------------------------------------------------------
# FUNCTION 4: display_inventory(orders)
# ---------------------------------------------------------
# What goes in?
# - orders = current inventory orders
#
# What comes out?
# - Displays the current orders
def display_inventory(orders):

    print("Current Orders:")
    print()

    # Check whether there are existing orders
    if len(orders) == 0:
        print("No current orders.")

    else:
        # Display every existing order
        for order in orders:
            print(f"{order[0]}, {order[1]}, {order[2]}")

    print()


# ---------------------------------------------------------
# FUNCTION 5: generate_product_id(orders)
# ---------------------------------------------------------
# What goes in?
# - orders = current inventory orders
#
# What comes out?
# - The next product ID
def generate_product_id(orders):

    # If there are no existing orders, start at 1001
    if len(orders) == 0:
        return 1001

    # Find the highest existing product ID
    highest_id = max(order[0] for order in orders)

    # Return the next product ID
    return highest_id + 1


# ---------------------------------------------------------
# FUNCTION 6: save_inventory()
# ---------------------------------------------------------
# What goes in?
# - orders = current inventory orders
# - history = transaction history list
#
# What comes out?
# - Saves the inventory and transaction history
#   into inventory.txt
def save_inventory(orders, history):

    # Calculate the final total quantity
    final_total = sum(order[2] for order in orders)

    # Open inventory.txt in write mode
    with open("inventory.txt", "w") as file:

        # Save every current order
        for order in orders:
            file.write(
                f"{order[0]},{order[1]},{order[2]}\n"
            )

        # Save the final total
        file.write(f"Final Total: {final_total}\n")

        # Save the transaction history
        file.write(f"Transaction History: {history}\n")

    print()
    print("Inventory successfully saved to inventory.txt.")


# =========================================================
# MAIN PROGRAM
# =========================================================

# Load existing inventory from inventory.txt
current_orders = load_inventory()

# Create an empty list to track every valid transaction
transaction_history = []

# Display the existing orders
display_inventory(current_orders)


# Keep running until the user enters "quit"
while True:

    # Ask for the product name
    product_name = get_product_name()

    # Stop the program if the user enters quit
    if product_name == "quit":

        # Display the transaction history
        print()
        print("Transaction History:")
        print(transaction_history)

        # Save inventory before ending the program
        save_inventory(
            current_orders,
            transaction_history
        )

        break

    # If the product name is invalid, try again
    if product_name is None:
        continue

    # Ask for the product quantity
    quantity = get_valid_quantity()

    # If the quantity is invalid, try again
    if quantity is None:
        continue

    # Generate the next product ID
    product_id = generate_product_id(current_orders)

    # Add the new order to memory
    new_order = [product_id, product_name, quantity]
    current_orders.append(new_order)

    # Add the valid quantity to the transaction history list
    transaction_history.append(quantity)

    # Display the newly added order
    print("\nNew Order Added:")
    print(f"{product_id},{product_name},{quantity}")
    print()