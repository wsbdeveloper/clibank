from decimal import Decimal
from domain import Operation


class ExecutionService():
    """ Service to process buy and sell operations"""

    def process_operation(self, operation: Operation) -> str:
        if operation.operation == "buy":
            return self._process_buy(operation)
    
    def __init__(self):
        self.total_shares = 0
        self.weighted_average_price = Decimal('0.0')
        self.accumulated_loss = Decimal('0.0')

    def _process_buy(self, operation: Operation) -> str:
        """ Process a buy operation"""
        breakpoint()
        if self.total_shares == 0: # first buy
            self.weighted_average_price = operation.unit_cost
        else:
            total_cost = self.total_shares * self.weighted_average_price
            new_cost = operation.quantity * operation.unit_cost
            self.weighted_average_price = (total_cost + new_cost) / (self.total_shares + operation.quantity)
        
        self.total_shares += operation.quantity
        return "0.00"

    def _process_sell(self, operation: Operation) -> str:
        """ Process a sell operation"""
        if operation.quantity > self.total_shares:
            raise ValueError("Cannot sell more shares than owned")
        
        operation_total = operation.unit_cost * operation.quantity

        profit_loss = (operation.unit_cost - self.weighted_average_price) * operation.quantity

        is_exempt = operation_total <= Decimal('20000.00')

        if profit_loss > 0:
            if is_exempt:
                tax = Decimal('0.00')
            else:
                # operation is taxable at 20%
                taxable_profit = profit_loss - self.accumulated_loss

                if taxable_profit > 0:
                    tax = taxable_profit * Decimal('0.20')
                    self.accumulated_loss = Decimal('0.00')
                else:
                    tax = Decimal('0.00')
                    self.accumulated_loss = abs(taxable_profit)
        else:
            # operation resulted in a loss
            tax = Decimal('0.00')
            self.accumulated_loss += abs(profit_loss)

        self.total_shares -= operation.quantity

        return Decimal(tax).quantize(Decimal('0.00'))

