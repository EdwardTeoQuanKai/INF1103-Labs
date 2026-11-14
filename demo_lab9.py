# INF1103 Lab 9 - Demonstration

from discount_strategy import (
    BulkDiscount,
    PercentageDiscount,
    StudentDiscount
)

from inventory_manager_lab9 import (
    Inventory,
    ProductFactory,
    load_products
)

from order_lab9 import Order
from supplier import Supplier


def main() -> None:

    supplier = Supplier(
        "S001",
        "ABC Electronics",
        "abc@example.com"
    )

    product = ProductFactory.create(
        "physical",
        "DEMO001",
        "Sample Product",
        125.0,
        10,
        supplier,
        1.0
    )

    order = Order(
        "O001",
        BulkDiscount(200, 20)
    )

    order.add_order_line(product, 2)

    print("=== STRATEGY PATTERN ===")

    print(
        f"BulkDiscount(200, 20): "
        f"${order.calculate_total():.2f}"
    )

    order.set_discount(
        PercentageDiscount(10)
    )

    print(
        f"PercentageDiscount(10): "
        f"${order.calculate_total():.2f}"
    )

    order.set_discount(
        StudentDiscount()
    )

    print(
        f"StudentDiscount(): "
        f"${order.calculate_total():.2f}"
    )

    print("\n=== FACTORY PATTERN ===")

    try:

        ProductFactory.create(
            "service",
            "S001",
            "Installation",
            30,
            5,
            supplier
        )

    except ValueError as error:

        print(f"Factory error handled: {error}")

    print("\n=== CSV LOADING ===")

    inventory = Inventory()

    load_products(
        "products.csv",
        inventory,
        supplier
    )

    print(
        "Imported IDs:",
        ", ".join(
            p.get_product_id()
            for p in inventory.products
        )
    )


if __name__ == "__main__":
    main()