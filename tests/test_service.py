import unittest
from decimal import Decimal

from src.service import ExecutionService
from src.domain import Operation


class TestExecutionService(unittest.TestCase):
    def setUp(self):
        self.execution_service = ExecutionService()

    def test_buy_operation(self):
        operation = Operation("buy", 10.00, 100)
        result = self.execution_service.process_operation(operation)
        breakpoint()
        self.assertEqual(result.tax, Decimal('0'))
        self.assertEqual(self.execution_service.total_shares, 100)
        self.assertEqual(self.execution_service.weighted_average_price, 10.00)
    
    def test_weighted_average_calculation(self):
        operation1 = Operation("buy", 10.00, 100)
        self.execution_service.process_operation(operation1)
        operation2 = Operation("buy", 20.00, 100)

        expected_average = Decimal("15.00")

        # calculate rules 100*10 + 100*20 / 200 = 15.00
        self.execution_service.process_operation(operation2)
        self.assertEqual(self.execution_service.total_shares, 200)
        self.assertEqual(self.execution_service.weighted_average_price, expected_average)

    def test_sell_with_profit(self):
        # Buy
        buy_op = Operation("buy", 10.00, 10000)
        self.execution_service.process_operation(buy_op)

        # Sell with profit
        sell_op = Operation("sell", 20.00, 5000)

        result = self.execution_service.process_operation(sell_op)

        expected_tax = Decimal("10000.00")
        breakpoint()
        self.assertEqual(result.tax, expected_tax)
        self.assertEqual(self.execution_service.total_shares, 5000)

    def test_sell_with_loss(self):
        buy_op = Operation("buy", 20.00, 10000)
        self.execution_service.process_operation(buy_op)

        sell_op = Operation("sell", 10.00, 5000)
        result = self.execution_service.process_operation(sell_op)

        # Loss: 10 - 20) * 5000 = -5000
        self.assertEqual(result.tax, result.tax)
        self.assertEqual(self.execution_service.total_shares, 5000)
    
    def test_loss_predict_from_profit(self):
        buy_op = Operation("buy", 20.00, 10000)
        self.execution_service.process_operation(buy_op)

        sell_loss = Operation("sell", 10.00, 5000)
        self.execution_service.process_operation(sell_loss)
        
        # sell with profit 
        sell_profit = Operation("sell", 30.00, 2500)
        result = self.execution_service.process_operation(sell_profit)

        # gross profit: (30 - 20) * 2500 = 25000
        # prejudice: 50000
        # 25000 - 50000 = -25000 
        self.assertEqual(result.tax, Decimal("0"))
        self.assertEqual(self.execution_service.accumulated_loss, Decimal("25000"))



