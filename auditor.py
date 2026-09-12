# Smart Inventory Auditor

# 1. Initialize inventory to zero
inventory = 0

# Count failed/rejected entries
failed_entries = 0

# 2. Keep asking until the user types "quit"
while True:
    stock = input("Enter stock quantity (or 'quit' to stop): ")

    # Stop the loop when the user types quit
    if stock.lower() == "quit":
        break

    # 4. Handle invalid input
    if not stock.isdigit():
        print("Error: Please enter a valid integer.")
        failed_entries += 1
        continue

    # Convert the input from string to integer
    quantity = int(stock)

    # 5. Reject negative numbers
    # Note: .isdigit() already prevents normal negative input such as -5
    if quantity < 0:
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    # 6. Keep a running total
    inventory += quantity
    print("Current inventory:", inventory)

    # 7. Check for overstock
    if inventory > 500:
        print("OVERSTOCK ALERT! Inventory exceeds 500 units.")
        break

# 8. Reporting
print("\n--- Inventory Report ---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)