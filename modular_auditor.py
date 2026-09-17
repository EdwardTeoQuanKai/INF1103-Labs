# Smart Inventory Auditor - Week 3
# This program has been refactored into functions.
# Each function has a specific job.


# ---------------------------------------------------------
# FUNCTION 1: get_valid_input()
# ---------------------------------------------------------
# What goes in?
# Nothing.
#
# What comes out?
# - A valid integer if the user enters a number
# - "quit" if the user wants to stop
# - None if the input is invalid
#
# This function handles BOTH the prompt and validation.
def get_valid_input():

    # Ask the user to enter a stock quantity
    stock = input("Enter stock quantity (or 'quit' to stop): ")

    # Check whether the user wants to stop
    if stock.lower() == "quit":
        return "quit"

    # Check whether the input is a valid positive integer
    if not stock.isdigit():
        print("Error: Please enter a valid integer.")
        return None

    # Convert the input from a string into an integer
    quantity = int(stock)

    # Return the valid integer
    return quantity


# ---------------------------------------------------------
# FUNCTION 2: process_delivery(current_total, new_value)
# ---------------------------------------------------------
# What goes in?
# - current_total = current inventory
# - new_value = new delivery
#
# What comes out?
# - The new inventory total
#
# This function ONLY adds the new delivery to the total.
def process_delivery(current_total, new_value):

    # Add the new delivery to the current inventory
    new_total = current_total + new_value

    # Return the updated inventory total
    return new_total


# ---------------------------------------------------------
# FUNCTION 3: calculate_tax(amount)
# ---------------------------------------------------------
# What goes in?
# - amount = delivery amount
#
# What comes out?
# - Tax amount
#
# The assignment says the tax is 10% of the delivery.
def calculate_tax(amount):

    # Calculate 10% tax
    tax = amount * 0.10

    # Return the tax
    return tax


# ---------------------------------------------------------
# FUNCTION 4: generate_report(total_units, failed_attempts)
# ---------------------------------------------------------
# What goes in?
# - total_units = final inventory
# - failed_attempts = number of invalid entries
#
# What comes out?
# - Prints the final report
def generate_report(total_units, failed_attempts):

    # Print the final report heading
    print("\n--- Inventory Report ---")

    # Print the final inventory total
    print("Total Units Processed:", total_units)

    # Print the number of failed/rejected inputs
    print("Number of Failed/Rejected Entries:", failed_attempts)


# =========================================================
# MAIN PROGRAM
# =========================================================

# Initialize inventory to zero
inventory = 0

# Count how many invalid entries the user makes
failed_entries = 0

# Count how many valid deliveries are processed
deliveries_processed = 0


# Keep running until the user enters "quit"
while True:

    # Call get_valid_input() to ask for and validate input
    quantity = get_valid_input()

    # If the user entered "quit", stop the loop
    if quantity == "quit":
        break

    # If the input was invalid, count it as a failed entry
    if quantity is None:
        failed_entries += 1

        # Return to the beginning of the loop
        continue

    # Process the valid delivery
    inventory = process_delivery(inventory, quantity)

    # Calculate 10% tax for THIS delivery
    tax = calculate_tax(quantity)

    # Increase the number of successfully processed deliveries
    deliveries_processed += 1

    # Show the current inventory
    print("Current inventory:", inventory)

    # Show the tax for this delivery
    print("Tax for this delivery:", tax)


# ---------------------------------------------------------
# FINAL REPORT
# ---------------------------------------------------------

# Generate the final report using the required function
generate_report(inventory, failed_entries)

# Print the total number of successful deliveries
print("Total Deliveries Processed:", deliveries_processed)