
# INF1103 Lab 8 - Section 4.3
# Test composition between Order and OrderLine.

from supplier import Supplier
from inventory_manager_lab8 import PhysicalProduct, DigitalProduct
from order import Order


# STEP 1: Create a Supplier independently.
supplier = Supplier(
    "S001", "ABC Electronics", "abc@example.com"
)

# STEP 2: Create two Products independently.
laptop = PhysicalProduct(
    "P001", "Laptop", 1200.0, 20, 2.5, supplier
)

software = DigitalProduct(
    "D001", "Software License", 99.99, 50, 500.0, supplier
)


# STEP 3: Create Order 1.
print("=== STEP 1: Create Order 1 ===")

order1 = Order("O001")

# Order creates its own OrderLine objects.
order1.add_order_line(laptop, 2)
order1.add_order_line(software, 3)

# Display Order 1 and calculate the total.
order1.display_order()


# STEP 4: Create Order 2.
print("\n=== STEP 2: Create Order 2 ===")

order2 = Order("O002")

# Add the same Laptop Product to a different Order.
order2.add_order_line(laptop, 1)

order2.display_order()


# STEP 5: Compare the Product references.
print("\n=== STEP 3: Compare Objects ===")

print(
    "Both orders refer to the same Product:",
    order1.order_lines[0].product
    is order2.order_lines[0].product
)

print(
    "OrderLines are different objects:",
    order1.order_lines[0]
    is not order2.order_lines[0]
)

print(
    "Order 1 OrderLine count:",
    len(order1.order_lines)
)

print(
    "Order 2 OrderLine count:",
    len(order2.order_lines)
)


# STEP 6: Remove a line through Order 1.
print("\n=== STEP 4: Remove OrderLine ===")

order1.remove_order_line("P001")

order1.display_order()


# STEP 7: Confirm Order 2 is unaffected.
print("\n=== STEP 5: Order 2 is unaffected ===")

order2.display_order()


# STEP 8: Confirm that the Product still exists.
print("\n=== FINAL CHECK ===")

print("Laptop still exists:")
laptop.display_information()

print(
    "\nOrder 1 remaining OrderLines:",
    len(order1.order_lines)
)

print(
    "Order 2 remaining OrderLines:",
    len(order2.order_lines)
)
