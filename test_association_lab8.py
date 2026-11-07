
from supplier import Supplier
from inventory_manager_lab8 import PhysicalProduct, DigitalProduct

# Create the supplier independently.
supplier = Supplier("S001", "ABC Electronics", "abc@example.com")

# Create two products using the same supplier.
physical = PhysicalProduct("P001", "Laptop", 1200.0, 20, 2.5, supplier)
digital = DigitalProduct("D001", "Software License", 99.99, 50, 500.0, supplier)

print("BEFORE deleting supplier variable:")
physical.supplier.display_information()
digital.supplier.display_information()

# Delete the original variable referencing the supplier.
del supplier

print("\nAFTER deleting supplier variable:")
physical.supplier.display_information()
digital.supplier.display_information()
