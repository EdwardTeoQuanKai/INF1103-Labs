# INF1103 Lab 9 - Strategy Pattern

import math
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float) -> None:

        if not math.isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError(
                "Discount percentage must be between 0 and 100."
            )

        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float) -> None:

        if not math.isfinite(threshold) or threshold <= 0:
            raise ValueError("Bulk threshold must be greater than zero.")

        if not math.isfinite(amount) or amount < 0:
            raise ValueError("Bulk amount must be non-negative.")

        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:

        if total >= self.threshold:
            return max(0.0, total - self.amount)

        return total


class StudentDiscount(DiscountStrategy):
    # Fourth discount strategy: 5% student discount.

    def apply(self, total: float) -> float:
        return total * 0.95