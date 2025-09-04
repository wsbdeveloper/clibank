from decimal import Decimal


class Operation:
    """ Domain the operations transaction"""

    def __init__(self, operation: str, unit_cost: float, quantity: int):
        self.operation = operation
        self.unit_cost = unit_cost
        self.quantity = quantity
    
class TaxResult:
    """ Domain for tax result"""

    def __init__(self, tax: str):
        self.tax = Decimal(str(tax))
    
    def to_dict(self):
        return {"tax": float(self.tax)}
    