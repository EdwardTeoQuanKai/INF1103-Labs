
# INF1103 Lab 8 - Sections 6 and 7
# Testing Liskov Substitution Principle and Polymorphism

from supplier import Supplier
from inventory_manager_lab8 import (
    Product,
    PhysicalProduct,
    DigitalProduct,
    Inventory
)


# =========================================================
# SECTION 6: LISKOV SUBSTITUTION PRINCIPLE (LSP)
# =========================================================

# This function accepts the parent Product type.
# Both PhysicalProduct and DigitalProduct should work.
def show_product_details(product: Product) -> None:

    product.display_information()
    print(product.get_fulfilment_info())


# Test a common parent-class operation.
def test_stock_update(product: Product,
                      quantity: int) -> None:

    product.update_stock(quantity)

    print(
        f"Product {product.get_product_id()} "
        f"updated stock: {product.to_dict()['stock']}"
    )

    # Verify that the subclass preserves expected behaviour.
    assert product.to_dict()["stock"] == quantity


# =========================================================
# MAIN TEST
# =========================================================
def main() -> None:

    # Create Supplier independently.
    supplier = Supplier(
        "S001", "ABC Electronics", "abc@example.com"
    )

    # Create PhysicalProduct.
    physical = PhysicalProduct(
        "P001", "Laptop", 1200.0, 20, 2.5, supplier
    )

    # Create DigitalProduct.
    digital = DigitalProduct(
        "D001", "Software License", 99.99, 50, 500.0,
        supplier
    )

    # =====================================================
    # TEST 1: LSP - COMMON PRODUCT FUNCTION
    # =====================================================
    print("=== TEST 1: LISKOV SUBSTITUTION PRINCIPLE ===")

    print("\nPhysical Product:")
    show_product_details(physical)

    print("\nDigital Product:")
    show_product_details(digital)

    print("\nBoth subclasses worked with Product function.")


    # =====================================================
    # TEST 2: LSP - STOCK UPDATE
    # =====================================================
    print("\n=== TEST 2: STOCK UPDATE ===")

    # Both objects support the inherited update_stock().
    test_stock_update(physical, 12)
    test_stock_update(digital, 30)

    print("Both Product subclasses support stock updates.")


    # =====================================================
    # TEST 3: POLYMORPHISM THROUGH INVENTORY
    # =====================================================
    print("\n=== TEST 3: POLYMORPHISM ===")

    inventory = Inventory()

    # Add both subclasses to one Inventory.
    inventory.add_product(physical, show_message=False)
    inventory.add_product(digital, show_message=False)

    print("Both Products added to the same Inventory.")

    # One loop handles both types of Product.
    for product in inventory.products:

        print("\n----------------------------------------")
        product.display_information()

        print(
            "Polymorphic fulfilment:",
            product.get_fulfilment_info()
        )

    print("\n----------------------------------------")


    # =====================================================
    # TEST 4: VERIFY INVENTORY OPERATIONS
    # =====================================================
    print("\n=== TEST 4: INVENTORY OPERATIONS ===")

    print(
        "Physical Product found:",
        inventory.find_product("P001") is physical
    )

    print(
        "Digital Product found:",
        inventory.find_product("D001") is digital
    )

    assert inventory.find_product("P001") is physical
    assert inventory.find_product("D001") is digital

    print("\nAll LSP and Polymorphism tests passed.")


if __name__ == "__main__":
    main()
