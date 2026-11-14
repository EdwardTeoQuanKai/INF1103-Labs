# INF1103 Lab 9 - OrderLine with Validation

from inventory_manager_lab9 import Product


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:

        # Order quantity must be a positive whole number.
        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity <= 0
        ):
            raise ValueError(
                "Quantity must be greater than zero (whole number)."
            )

        # Association with an existing Product.
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_information(self) -> None:

        print(f"Product ID: {self.product.get_product_id()}")
        print(f"Unit Price: ${self.product.price:.2f}")
        print(f"Quantity: {self.quantity}")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")