import unittest

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