from decimal import Decimal

def IExecutionService():
    def _process_buy(self, operation: Operation) -> str:
        pass

    def _process_sell(self, operation: Operation) -> str:
        pass

class ExecutionService(IExecutionService):
    """
        TODO: realizar processamento de operações dado o requerimento do pdf
    """

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
        return "0.00"
        
    def _process_sell(self, operation: Operation) -> str:
        pass




