# INF1103 Lab 9 - Order with Strategy Pattern
# Composition: Order owns its OrderLine objects.

from inventory_manager_lab9 import Product
from discount_strategy import DiscountStrategy, NoDiscount
from order_line_lab9 import OrderLine


class Order:

    def __init__(
        self,
        order_id: str,
        discount: DiscountStrategy | None = None
    ) -> None:

        self.order_id: str = order_id

        # Validate the supplied discount strategy.
        if discount is not None and not isinstance(
            discount, DiscountStrategy
        ):
            raise TypeError("Discount must implement DiscountStrategy.")

        # Default strategy if none is provided.
        self.discount: DiscountStrategy = (
            discount if discount is not None else NoDiscount()
        )

        # Composition: Order manages its OrderLines.
        self.order_lines: list[OrderLine] = []

    def add_order_line(
        self,
        product: Product,
        quantity: int
    ) -> None:

        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

        print("Order line added successfully!")

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

    def set_discount(self, discount: DiscountStrategy) -> None:

        if not isinstance(discount, DiscountStrategy):
            raise TypeError("Discount must implement DiscountStrategy.")

        self.discount = discount

    def calculate_total(self) -> float:

        total = sum(
            line.calculate_subtotal()
            for line in self.order_lines
        )

        # Strategy decides how the discount is applied.
        return self.discount.apply(total)

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