# INF1103 Lab 9 - Automated Tests

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import tempfile
import unittest

from unittest.mock import patch

from discount_strategy import (
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount
)

from inventory_manager_lab9 import (
    DigitalProduct,
    Inventory,
    PhysicalProduct,
    Product,
    ProductFactory,
    get_positive_float,
    load_products
)

from order_lab9 import Order
from order_line_lab9 import OrderLine
from supplier import Supplier


class Lab9TestCase(unittest.TestCase):

    def setUp(self):

        self.supplier = Supplier(
            "S001",
            "ABC Electronics",
            "abc@example.com"
        )

        self.product = ProductFactory.create(
            "physical",
            "P001",
            "Sample",
            125.0,
            10,
            self.supplier,
            2.0
        )

    def new_order(self, strategy=None):

        order = Order("O001", strategy)

        with redirect_stdout(StringIO()):
            order.add_order_line(self.product, 2)

        return order


# =========================================================
# STRATEGY PATTERN TESTS
# =========================================================
class TestStrategy(Lab9TestCase):

    def test_all_strategies_inherit_abstract_strategy(self):

        for strategy in (
            NoDiscount(),
            PercentageDiscount(10),
            BulkDiscount(200, 20),
            StudentDiscount()
        ):

            self.assertIsInstance(
                strategy,
                DiscountStrategy
            )

    def test_default_no_discount(self):

        self.assertEqual(
            self.new_order().calculate_total(),
            250.0
        )

    def test_bulk_discount_250_becomes_230(self):

        self.assertEqual(
            self.new_order(
                BulkDiscount(200, 20)
            ).calculate_total(),
            230.0
        )

    def test_bulk_discount_below_threshold(self):

        self.assertEqual(
            BulkDiscount(200, 20).apply(199.0),
            199.0
        )

    def test_percentage_discount_250_becomes_225(self):

        self.assertEqual(
            self.new_order(
                PercentageDiscount(10)
            ).calculate_total(),
            225.0
        )

    def test_set_discount_changes_same_order(self):

        order = self.new_order(
            BulkDiscount(200, 20)
        )

        self.assertEqual(
            order.calculate_total(),
            230.0
        )

        order.set_discount(
            PercentageDiscount(10)
        )

        self.assertEqual(
            order.calculate_total(),
            225.0
        )

    def test_fourth_student_discount_without_order_changes(self):

        self.assertEqual(
            self.new_order(
                StudentDiscount()
            ).calculate_total(),
            237.5
        )

    def test_two_orders_can_share_strategy(self):

        strategy = PercentageDiscount(10)

        a = self.new_order(strategy)
        b = self.new_order(strategy)

        self.assertIs(
            a.discount,
            b.discount
        )

    def test_invalid_discount_percent_is_rejected(self):

        for invalid in (
            -1,
            101,
            float("nan")
        ):

            with self.subTest(invalid=invalid):

                with self.assertRaises(ValueError):
                    PercentageDiscount(invalid)

    def test_invalid_bulk_values_are_rejected(self):

        for threshold, amount in (
            (0, 20),
            (200, -1),
            (200, float("inf"))
        ):

            with self.subTest(
                threshold=threshold,
                amount=amount
            ):

                with self.assertRaises(ValueError):
                    BulkDiscount(
                        threshold,
                        amount
                    )

    def test_strategy_must_implement_contract(self):

        with self.assertRaises(TypeError):

            Order(
                "O2",
                discount="ten percent"
            )


# =========================================================
# FACTORY PATTERN TESTS
# =========================================================
class TestFactory(Lab9TestCase):

    def test_physical_product_has_original_weight(self):

        self.assertIsInstance(
            self.product,
            PhysicalProduct
        )

        self.assertEqual(
            self.product.to_dict()["weight"],
            2.0
        )

    def test_digital_product_has_original_download_size(self):

        product = ProductFactory.create(
            "digital",
            "D001",
            "Photo Editor",
            49.90,
            100,
            self.supplier,
            500
        )

        self.assertIsInstance(
            product,
            DigitalProduct
        )

        self.assertEqual(
            product.to_dict()["download_size"],
            500
        )

    def test_factory_returns_product_interface(self):

        product: Product = ProductFactory.create(
            "digital",
            "D001",
            "Photo Editor",
            49.90,
            100,
            self.supplier
        )

        self.assertEqual(
            product.get_fulfilment_info(),
            "Fulfilment: Delivered digitally by download."
        )

    def test_unknown_product_type_raises_value_error(self):

        with self.assertRaisesRegex(
            ValueError,
            "Unknown product type: service"
        ):

            ProductFactory.create(
                "service",
                "S001",
                "Install",
                30,
                5,
                self.supplier
            )

    def test_invalid_extra_rejected(self):

        with self.assertRaises(ValueError):

            ProductFactory.create(
                "physical",
                "P009",
                "Item",
                12,
                1,
                self.supplier,
                -1
            )


# =========================================================
# VALIDATION TESTS
# =========================================================
class TestValidation(Lab9TestCase):

    def test_invalid_product_price_zero(self):

        with self.assertRaisesRegex(
            ValueError,
            "price"
        ):

            ProductFactory.create(
                "physical",
                "P002",
                "Bad",
                0,
                1,
                self.supplier
            )

    def test_invalid_product_price_negative(self):

        with self.assertRaises(ValueError):

            ProductFactory.create(
                "digital",
                "D002",
                "Bad",
                -2,
                1,
                self.supplier
            )

    def test_invalid_product_price_nan(self):

        with self.assertRaises(ValueError):

            ProductFactory.create(
                "digital",
                "D002",
                "Bad",
                float("nan"),
                1,
                self.supplier
            )

    def test_invalid_stock_on_creation(self):

        with self.assertRaisesRegex(
            ValueError,
            "Stock"
        ):

            ProductFactory.create(
                "physical",
                "P002",
                "Bad",
                10,
                -1,
                self.supplier
            )

    def test_zero_stock_is_valid(self):

        item = ProductFactory.create(
            "digital",
            "D003",
            "Valid",
            10,
            0,
            self.supplier
        )

        self.assertEqual(
            item.to_dict()["stock"],
            0
        )

    def test_invalid_stock_update_rejected_without_changing_stock(self):

        with self.assertRaises(ValueError):
            self.product.update_stock(-5)

        self.assertEqual(
            self.product.to_dict()["stock"],
            10
        )

    def test_valid_stock_update(self):

        self.product.update_stock(0)

        self.assertEqual(
            self.product.to_dict()["stock"],
            0
        )

    def test_lsp_rule_same_for_digital_and_physical(self):

        products = [
            self.product,

            ProductFactory.create(
                "digital",
                "D2",
                "Digital",
                10,
                1,
                self.supplier
            )
        ]

        for product in products:

            with self.subTest(
                type=type(product).__name__
            ):

                with self.assertRaises(ValueError):
                    product.update_stock(-1)

    def test_invalid_order_line_quantity_zero(self):

        with self.assertRaises(ValueError):
            OrderLine(self.product, 0)

    def test_invalid_order_line_quantity_negative(self):

        with self.assertRaises(ValueError):

            self.new_order().add_order_line(
                self.product,
                -1
            )

    def test_valid_order_line_subtotal(self):

        self.assertEqual(
            OrderLine(
                self.product,
                2
            ).calculate_subtotal(),
            250
        )

    def test_order_line_does_not_own_product(self):

        order = self.new_order()

        with redirect_stdout(StringIO()):
            order.remove_order_line("P001")

        self.assertIsNotNone(self.product)

        self.assertEqual(
            order.order_lines,
            []
        )


# =========================================================
# EXCEPTION HANDLING TESTS
# =========================================================
class TestExceptionHandling(Lab9TestCase):

    def test_input_abc_negative_then_12_50(self):

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=["abc", "-5", "12.50"]
        ):

            with redirect_stdout(output):
                returned = get_positive_float(
                    "Price: "
                )

        self.assertEqual(
            returned,
            12.5
        )

        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "Please enter a valid number, e.g. 12.50",
                "Please enter a number greater than zero."
            ]
        )

    def test_input_nonfinite_then_valid(self):

        with patch(
            "builtins.input",
            side_effect=["nan", "inf", "5"]
        ):

            with redirect_stdout(StringIO()):

                self.assertEqual(
                    get_positive_float("Price: "),
                    5.0
                )

    def test_missing_csv_has_except_and_finally_messages(self):

        output = StringIO()
        inventory = Inventory()

        with redirect_stdout(output):

            load_products(
                "missing_products_example.csv",
                inventory,
                self.supplier
            )

        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "Products file not found: missing_products_example.csv",
                "Load attempt finished."
            ]
        )

        self.assertEqual(
            len(inventory.products),
            0
        )

    def test_csv_sample_has_three_valid_products(self):

        csv_path = (
            Path(__file__).resolve().parents[1]
            / "products.csv"
        )

        inventory = Inventory()
        output = StringIO()

        with redirect_stdout(output):

            load_products(
                str(csv_path),
                inventory,
                self.supplier
            )

        self.assertEqual(
            [
                p.get_product_id()
                for p in inventory.products
            ],
            ["P001", "D001", "P003"]
        )

        lines = output.getvalue().splitlines()

        self.assertIn(
            "Skipping row 4: Unknown product type: service",
            lines
        )

        self.assertIn(
            "Skipping row 5: could not convert string to float: 'abc'",
            lines
        )

        self.assertEqual(
            lines[-2:],
            [
                "3 products loaded.",
                "Load attempt finished."
            ]
        )

    def test_file_load_skips_bad_row_and_continues(self):

        content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P1,Good,10,3\n"
            "digital,D1,Bad,-2,3\n"
            "digital,D2,Valid,15,2\n"
        )

        with tempfile.TemporaryDirectory() as directory:

            path = Path(directory) / "products.csv"
            path.write_text(content)

            inventory = Inventory()
            output = StringIO()

            with redirect_stdout(output):

                load_products(
                    str(path),
                    inventory,
                    self.supplier
                )

            self.assertEqual(
                len(inventory.products),
                2
            )

            self.assertIn(
                "Skipping row 3",
                output.getvalue()
            )

    def test_csv_invalid_stock_skipped(self):

        content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "digital,D1,Bad,10,-1\n"
            "physical,P1,Good,10,2\n"
        )

        with tempfile.TemporaryDirectory() as directory:

            path = Path(directory) / "products.csv"
            path.write_text(content)

            inventory = Inventory()

            with redirect_stdout(StringIO()):

                load_products(
                    str(path),
                    inventory,
                    self.supplier
                )

            self.assertEqual(
                [
                    p.get_product_id()
                    for p in inventory.products
                ],
                ["P1"]
            )

    def test_duplicate_csv_product_skipped(self):

        content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "digital,D1,First,10,1\n"
            "digital,D1,Duplicate,20,2\n"
        )

        with tempfile.TemporaryDirectory() as directory:

            path = Path(directory) / "products.csv"
            path.write_text(content)

            inventory = Inventory()
            output = StringIO()

            with redirect_stdout(output):

                load_products(
                    str(path),
                    inventory,
                    self.supplier
                )

            self.assertEqual(
                len(inventory.products),
                1
            )

            self.assertIn(
                "Duplicate product ID",
                output.getvalue()
            )


if __name__ == "__main__":
    unittest.main()