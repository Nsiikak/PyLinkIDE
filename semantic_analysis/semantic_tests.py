import unittest
from .symbol_table import SymbolTable
from .type_checker import TypeChecker
from .scope_manager import ScopeManager

class TestSemanticAnalysis(unittest.TestCase):
    def test_symbol_table(self):
        table = SymbolTable()
        table.insert("x", {"type": "int", "scope": "global"})
        self.assertEqual(table.lookup("x")["type"], "int")

        with self.assertRaises(Exception):
            table.lookup("y")  # y is not declared

    def test_type_checker(self):
        table = SymbolTable()
        table.insert("x", {"type": "int", "scope": "global"})
        type_checker = TypeChecker(table)

        # Check valid assignment
        type_checker.check_assignment("x", "int")

        # Check invalid assignment
        with self.assertRaises(Exception):
            type_checker.check_assignment("x", "float")

        # Check binary operations
        result = type_checker.check_binary_operation("int", "+", "int")
        self.assertEqual(result, "int")

        with self.assertRaises(Exception):
            type_checker.check_binary_operation("int", "+", "string")

    def test_scope_manager(self):
        manager = ScopeManager()

        # Enter a new scope
        manager.enter_scope()
        manager.declare_variable("x", "int")
        self.assertEqual(manager.resolve_variable("x")["type"], "int")

        # Exit the scope
        manager.exit_scope()
        with self.assertRaises(Exception):
            manager.resolve_variable("x")  # x is not in global scope

if __name__ == "__main__":
    unittest.main()
