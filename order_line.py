
# INF1103 Lab 8 - Section 4.1
# OrderLine represents one Product and its ordered quantity.

from inventory_manager_lab8 import Product


class OrderLine:

    def __init__(self, product: Product,
                 quantity: int) -> None:

        if quantity <= 0:
            raise ValueError("Order quantity must be positive.")

        # Association: OrderLine refers to an existing Product.
        # It does not own the Product object.
        self.product: Product = product
        self.quantity: int = quantity

    # Calculate the subtotal for this OrderLine.
    def calculate_subtotal(self) -> float:

        return self.product.price * self.quantity

    # Display the OrderLine information.
    def display_information(self) -> None:

        print(f"Product ID: {self.product.get_product_id()}")
        print(f"Unit Price: ${self.product.price:.2f}")
        print(f"Quantity: {self.quantity}")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
