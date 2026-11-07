
# INF1103 Lab 8 - Section 3 Aggregation Test

from supplier import Supplier
from inventory_manager_lab8 import Inventory, PhysicalProduct


# STEP 1: Create a Supplier independently.
supplier = Supplier(
    "S001", "ABC Electronics", "abc@example.com"
)

# STEP 2: Create a Product before adding it to an Inventory.
product = PhysicalProduct(
    "P001", "Laptop", 1200.0, 20, 2.5, supplier
)

# STEP 3: Create two separate inventories.
inventory_a = Inventory()
inventory_b = Inventory()

print("=== STEP 1: Product created independently ===")
print("Product ID:", product.get_product_id())


# STEP 4: Add Product to Inventory A.
print("\n=== STEP 2: Add Product to Inventory A ===")
inventory_a.add_product(product)

print(
    "Product exists in Inventory A:",
    inventory_a.find_product("P001") is product
)


# STEP 5: Remove Product from Inventory A.
print("\n=== STEP 3: Remove Product from Inventory A ===")

removed_product = inventory_a.remove_product("P001")

print(
    "Product removed successfully:",
    removed_product is product
)

print(
    "Product in Inventory A:",
    inventory_a.find_product("P001")
)


# STEP 6: Confirm the Product still exists.
print("\n=== STEP 4: Product still exists ===")

product.display_information()


# STEP 7: Transfer Product to Inventory B.
print("\n=== STEP 5: Add Product to Inventory B ===")

inventory_b.add_product(product)

print(
    "Same Product object in Inventory B:",
    inventory_b.find_product("P001") is product
)


# STEP 8: Confirm it is not in Inventory A.
print("\n=== FINAL CHECK ===")

print(
    "Inventory A:",
    inventory_a.find_product("P001")
)

print(
    "Inventory B contains Product:",
    inventory_b.find_product("P001") is product
)
