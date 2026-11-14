# INF1103 Lab 9 - Inventory Management System
# Extended from Lab 8: Factory, Validation and Exception Handling

import csv
import json
import math

from abc import ABC, abstractmethod
from supplier import Supplier


# =========================================================
# INTERFACE: CanBeShipped
# =========================================================
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


# =========================================================
# ABSTRACT PARENT CLASS: Product
# =========================================================
class Product(ABC):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ) -> None:

        # Validation: Product price must be positive.
        try:
            checked_price = float(price)

        except (TypeError, ValueError) as error:
            raise ValueError(
                "Product price must be a number greater than zero."
            ) from error

        if not math.isfinite(checked_price) or checked_price <= 0:
            raise ValueError(
                "Product price must be greater than zero."
            )

        # Validation: Stock cannot be negative.
        if (
            isinstance(stock, bool)
            or not isinstance(stock, int)
            or stock < 0
        ):
            raise ValueError(
                "Stock quantity must be a non-negative integer."
            )

        self.__product_id = product_id
        self.__name = name
        self.__price = checked_price
        self.__stock = stock

        # Association with Supplier.
        self.supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:

        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity < 0
        ):
            raise ValueError(
                "Stock quantity must be a non-negative integer."
            )

        self.__stock = quantity

    def display_information(self) -> None:

        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

        print("Supplier Information:")
        self.supplier.display_information()

    def get_product_id(self) -> str:
        return self.__product_id

    @property
    def price(self) -> float:
        return self.__price

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def to_dict(self) -> dict:

        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


# =========================================================
# CHILD CLASS: PhysicalProduct
# =========================================================
class PhysicalProduct(Product, CanBeShipped):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        weight: float,
        supplier: Supplier
    ) -> None:

        super().__init__(
            product_id, name, price, stock, supplier
        )

        self.__weight = weight

    def display_information(self) -> None:

        super().display_information()

        print("Type: Physical")
        print(f"Weight: {self.__weight:.2f} kg")
        print(self.get_fulfilment_info())

        print(
            f"Shipping Cost: ${self.calculate_shipping_cost():.2f}"
        )

    def get_fulfilment_info(self) -> str:
        return "Fulfilment: Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (2.00 * self.__weight)

    def to_dict(self) -> dict:

        data = super().to_dict()

        data["type"] = "physical"
        data["weight"] = self.__weight

        return data


# =========================================================
# CHILD CLASS: DigitalProduct
# =========================================================
class DigitalProduct(Product):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        download_size: float,
        supplier: Supplier
    ) -> None:

        super().__init__(
            product_id, name, price, stock, supplier
        )

        self.__download_size = download_size

    def display_information(self) -> None:

        super().display_information()

        print("Type: Digital")
        print(f"Download Size: {self.__download_size:.2f} MB")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self) -> str:
        return "Fulfilment: Delivered digitally by download."

    def to_dict(self) -> dict:

        data = super().to_dict()

        data["type"] = "digital"
        data["download_size"] = self.__download_size

        return data


# =========================================================
# FACTORY PATTERN: ProductFactory
# =========================================================
class ProductFactory:
    """
    Centralises PhysicalProduct and DigitalProduct creation.
    """

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        extra: float = 0.0
    ) -> Product:

        # extra = weight for physical products.
        # extra = download size for digital products.
        # CSV rows do not provide this information.
        if not math.isfinite(extra) or extra < 0:
            raise ValueError(
                "Weight/download size must be non-negative and finite."
            )

        if product_type == "physical":
            return PhysicalProduct(
                product_id,
                name,
                price,
                stock_quantity,
                extra,
                supplier
            )

        if product_type == "digital":
            return DigitalProduct(
                product_id,
                name,
                price,
                stock_quantity,
                extra,
                supplier
            )

        raise ValueError(
            f"Unknown product type: {product_type}"
        )


# =========================================================
# CLASS: Inventory
# =========================================================
# Aggregation: Products exist independently of Inventory.

class Inventory:

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(
        self,
        product: Product,
        show_message: bool = True
    ) -> None:

        if self.find_product(product.get_product_id()) is not None:
            print("Product ID already exists.")
            return

        self.products.append(product)

        if show_message:
            print("Product added successfully!")

    def remove_product(self, product_id: str) -> Product | None:

        for index, product in enumerate(self.products):

            if (
                product.get_product_id().lower()
                == product_id.lower()
            ):
                return self.products.pop(index)

        return None

    def find_product(self, product_id: str) -> Product | None:

        for product in self.products:

            if (
                product.get_product_id().lower()
                == product_id.lower()
            ):
                return product

        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all(self) -> None:

        print("Current Inventory")
        print("------------------------------------------------")

        if not self.products:
            print("No products in inventory.")
            print("------------------------------------------------")
            return

        for product in self.products:

            product.display_information()
            print("------------------------------------------------")

    def to_dict_list(self) -> list[dict]:

        return [
            product.to_dict()
            for product in self.products
        ]


# =========================================================
# INPUT HELPER: Non-Negative Float
# =========================================================
def read_nonnegative_float(prompt: str) -> float:

    while True:

        entered = input(prompt).strip()

        try:
            number = float(entered)

        except ValueError:
            print("Error: Please enter a valid number.")
            continue

        if not math.isfinite(number) or number < 0:
            print("Error: Enter a non-negative, finite number.")
            continue

        return number


# =========================================================
# INPUT HELPER: Product Type
# =========================================================
def ask_product_type() -> tuple[str, float]:

    while True:

        print("1. Physical Product")
        print("2. Digital Product")

        selection = input(
            "Choose product type (1/2): "
        ).strip()

        if selection == "1":

            weight = read_nonnegative_float(
                "Weight (kg): "
            )

            return "physical", weight

        if selection == "2":

            download_size = read_nonnegative_float(
                "Download Size (MB): "
            )

            return "digital", download_size

        print("Invalid product type. Please select 1 or 2.")


# =========================================================
# LAB 9: Positive Float Validation
# =========================================================
def get_positive_float(prompt: str) -> float:

    while True:

        try:
            value = float(input(prompt))

            if not math.isfinite(value) or value <= 0:

                print(
                    "Please enter a number greater than zero."
                )
                continue

            return value

        except ValueError:

            print(
                "Please enter a valid number, e.g. 12.50"
            )


# =========================================================
# PRODUCT CREATION HELPER
# =========================================================
def create_product(
    product_id: str,
    name: str,
    price: float,
    stock: int,
    product_type: str,
    extra: float,
    supplier: Supplier
) -> Product:

    # All creation is now handled by the Factory.
    return ProductFactory.create(
        product_type,
        product_id,
        name,
        price,
        stock,
        supplier,
        extra
    )


# =========================================================
# JSON FILE HANDLING
# =========================================================
def load_inventory(supplier: Supplier) -> Inventory:

    try:

        with open(
            "inventory.json",
            "r",
            encoding="utf-8"
        ) as file:

            saved_products = json.load(file)

        print("inventory.json found.")

    except FileNotFoundError:

        print("inventory.json not found.")
        print("Starting with an empty inventory.")

        return Inventory()

    except json.JSONDecodeError:

        print("Error: inventory.json contains invalid JSON.")
        raise SystemExit(1)

    if not isinstance(saved_products, list):

        print(
            "Error: inventory.json should contain a list of products."
        )
        raise SystemExit(1)

    inventory = Inventory()

    try:

        for data in saved_products:

            product_type = data.get("type")

            # Support older Lab 6 records.
            if product_type is None:

                print(
                    f"\nLab 6 product {data['id']} "
                    f"({data['name']}) has no product type."
                )

                print(
                    "Choose its type and provide "
                    "its additional information:"
                )

                product_type, extra = ask_product_type()

            elif product_type == "physical":

                extra = float(data["weight"])

            elif product_type == "digital":

                extra = float(data["download_size"])

            else:

                raise ValueError(
                    f"Unknown type: {product_type}"
                )

            if not math.isfinite(extra) or extra < 0:
                raise ValueError(
                    "Invalid weight or download size"
                )

            product = ProductFactory.create(
                product_type,
                data["id"],
                data["name"],
                float(data["price"]),
                int(data["stock"]),
                supplier,
                extra
            )

            inventory.add_product(
                product,
                show_message=False
            )

    except (KeyError, TypeError, ValueError) as error:

        print(
            f"Error: Invalid product data in "
            f"inventory.json ({error})."
        )

        raise SystemExit(1)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory) -> None:

    with open(
        "inventory.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            inventory.to_dict_list(),
            file,
            indent=4
        )

    print("Inventory saved successfully to inventory.json.")


# =========================================================
# LAB 9: CSV LOADING WITH EXCEPTION HANDLING
# =========================================================
def load_products(
    path: str,
    inventory: Inventory,
    supplier: Supplier
) -> None:

    try:

        file = open(
            path,
            newline="",
            encoding="utf-8"
        )

    except FileNotFoundError:

        print(f"Products file not found: {path}")

    else:

        loaded = 0

        with file:

            reader = csv.reader(file)

            # Skip CSV header.
            next(reader, None)

            for row_number, row in enumerate(
                reader,
                start=2
            ):

                try:

                    if len(row) != 5:
                        raise ValueError(
                            "Expected 5 CSV columns."
                        )

                    product_type, product_id, name, price, stock = [
                        cell.strip() for cell in row
                    ]

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        float(price),
                        int(stock),
                        supplier
                    )

                    # Avoid duplicate products.
                    if inventory.find_product(product_id) is not None:

                        raise ValueError(
                            f"Duplicate product ID: {product_id}"
                        )

                    inventory.add_product(
                        product,
                        show_message=False
                    )

                    loaded += 1

                except ValueError as error:

                    print(
                        f"Skipping row {row_number}: {error}"
                    )

        print(f"{loaded} products loaded.")

    finally:

        print("Load attempt finished.")


# =========================================================
# FUNCTION 1: Add Product
# =========================================================
def handle_add_product(
    inventory: Inventory,
    supplier: Supplier
) -> None:

    print("Add New Product")

    product_id = input(
        "Product ID: "
    ).strip()

    if not product_id:
        print("Error: Product ID cannot be empty.")
        return

    if inventory.find_product(product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input(
        "Product Name: "
    ).strip()

    if not product_name:
        print("Error: Product name cannot be empty.")
        return

    price = get_positive_float("Price: ")

    stock_input = input(
        "Stock Quantity: "
    ).strip()

    if not stock_input.isdigit():
        print("Error: Please enter a valid stock quantity.")
        return

    stock = int(stock_input)

    product_type, extra = ask_product_type()

    product = ProductFactory.create(
        product_type,
        product_id,
        product_name,
        price,
        stock,
        supplier,
        extra
    )

    inventory.add_product(product)


# =========================================================
# FUNCTION 2: Update Stock
# =========================================================
def handle_update_stock(inventory: Inventory) -> None:

    print("Update Stock")

    product_id = input(
        "Enter Product ID: "
    ).strip()

    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    product.display_information()

    stock_input = input(
        "New Stock Quantity: "
    ).strip()

    if not stock_input.isdigit():
        print("Error: Please enter a valid stock quantity.")
        return

    try:

        product.update_stock(
            int(stock_input)
        )

    except ValueError as error:

        print(f"Error: {error}")

    else:

        print("Stock updated successfully!")


# =========================================================
# FUNCTION 3: Search Product
# =========================================================
def handle_search_product(inventory: Inventory) -> None:

    print("Search Product")

    product_id = input(
        "Enter Product ID: "
    ).strip()

    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("------------------------------------------------")

    product.display_information()

    print("------------------------------------------------")


# =========================================================
# MENU
# =========================================================
def display_menu() -> None:

    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Load Products from CSV")
    print("7. Exit")
    print("----------------------------")


# =========================================================
# MAIN PROGRAM
# =========================================================
def main() -> None:

    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM - LAB 9")
    print("========================================")

    supplier = Supplier(
        "S001",
        "ABC Electronics",
        "abc@example.com"
    )

    inventory = load_inventory(supplier)

    while True:

        display_menu()

        option = input(
            "Enter option: "
        ).strip()

        if option == "1":

            inventory.display_all()

        elif option == "2":

            handle_add_product(
                inventory,
                supplier
            )

        elif option == "3":

            handle_update_stock(inventory)

        elif option == "4":

            handle_search_product(inventory)

        elif option == "5":

            print("Saving inventory...")
            save_inventory(inventory)

        elif option == "6":

            filename = input(
                "CSV filename (e.g. products.csv): "
            ).strip()

            if not filename:
                filename = "products.csv"

            load_products(
                filename,
                inventory,
                supplier
            )

        elif option == "7":

            print("Saving inventory before exit...")
            save_inventory(inventory)

            print(
                "Thank you for using Inventory Management System."
            )
            print("Program terminated.")

            break

        else:

            print("Invalid option. Please select 1 to 7.")


if __name__ == "__main__":
    main()