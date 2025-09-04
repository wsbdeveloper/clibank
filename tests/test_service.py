import unittest
from decimal import Decimal

from service import ExecutionService
from domain import Operation


class TestExecutionService(unittest.TestCase):
    def setUp(self):
        self.execution_service = ExecutionService()

    def test_buy_operation(self):
        operation = Operation("buy", 10.00, 100)
        result = self.execution_service.process_operation(operation)
        self.assertEqual(result, "0.00")
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