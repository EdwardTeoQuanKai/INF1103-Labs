
# INF1103 Lab 8 - Section 4.2
# Composition: Order owns and manages its OrderLine objects.

from inventory_manager_lab8 import Product
from order_line import OrderLine


class Order:

    def __init__(self, order_id: str) -> None:

        self.order_id: str = order_id

        # Composition: Each Order manages its own OrderLines.
        self.order_lines: list[OrderLine] = []

    # Create an OrderLine inside the Order.
    def add_order_line(self, product: Product,
                       quantity: int) -> None:

        # OrderLine is created here, not supplied externally.
        order_line = OrderLine(product, quantity)

        self.order_lines.append(order_line)

        print("Order line added successfully!")

    # Remove an OrderLine through the Order.
    def remove_order_line(self, product_id: str) -> bool:

        for index, order_line in enumerate(self.order_lines):

            if (
                order_line.product.get_product_id().lower()
                == product_id.lower()
            ):

                self.order_lines.pop(index)
                print("Order line removed successfully!")
                return True

        print("Order line not found.")
        return False

    # Ask each OrderLine to calculate its subtotal.
    def calculate_total(self) -> float:

        total = 0.0

        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()

        return total

    # Display all OrderLines and the total.
    def display_order(self) -> None:

        print(f"\nOrder ID: {self.order_id}")
        print("----------------------------------------")

        if not self.order_lines:
            print("No order lines.")
        else:
            for index, order_line in enumerate(self.order_lines, 1):

                print(f"Order Line {index}")
                order_line.display_information()
                print("----------------------------------------")

        print(f"Order Total: ${self.calculate_total():.2f}")
