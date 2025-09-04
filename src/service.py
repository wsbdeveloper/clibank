import json
from typing import List

from decimal import Decimal
from domain import Operation, TaxResult


class ExecutionService:
    """ Service to process buy and sell operations"""

    def process_operation(self, operation: Operation) -> str:
        if operation.operation == "buy":
            return self._process_buy(operation)
        elif operation.operation == "sell":
            return self._process_sell(operation)
        else:
            raise ValueError("Invalid operation type")
    
    def __init__(self):
        self.total_shares = 0
        self.weighted_average_price = Decimal('0.0')
        self.accumulated_loss = Decimal('0.0')

    def _process_buy(self, operation: Operation) -> str:
        """ Process a buy operation"""
        if self.total_shares == 0: # first buy
            self.weighted_average_price = operation.unit_cost
        else:
            total_cost = self.total_shares * self.weighted_average_price
            new_cost = operation.quantity * operation.unit_cost
            self.weighted_average_price = (total_cost + new_cost) / (self.total_shares + operation.quantity)
        
        self.total_shares += operation.quantity
        return TaxResult(0)

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
                taxable_profit = Decimal(profit_loss) - self.accumulated_loss

                if taxable_profit > 0:
                    tax = taxable_profit * Decimal('0.20')
                    self.accumulated_loss = Decimal('0.00')
                else:
                    tax = Decimal('0.00')
                    self.accumulated_loss = abs(taxable_profit)
        else:
            # operation resulted in a loss
            tax = Decimal('0.00')
            self.accumulated_loss += abs(Decimal(profit_loss))

        self.total_shares -= operation.quantity

        return TaxResult(tax)

class TaxCalculation:

    def __init__(self):
        self.service = ExecutionService()

    def process_lines(self, lines: str) -> List:
        try:

            data_operations = json.loads(lines.strip())

            if not isinstance(data_operations, list):
                raise ValueError("Entrada deve ser uma lista de operações")
            
            results = []
            
            # Process the operations
            for op_data in data_operations:
                operation = Operation.from_dict(op_data)
                result = self.service.process_operation(operation)
                results.append(result)
            
            return results
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {e}")
        except Exception as e:
            raise ValueError(f"Error processing lines: {e}")
