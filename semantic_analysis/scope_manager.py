from .symbol_table import SymbolTable

class ScopeManager:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def enter_scope(self):
        """Enter a new scope (e.g., a block or function)."""
        self.symbol_table.push_scope()

    def exit_scope(self):
        """Exit the current scope."""
        self.symbol_table.pop_scope()

    def declare_variable(self, name, var_type):
        """Declare a new variable in the current scope."""
        self.symbol_table.insert(name, {"type": var_type, "scope": "local"})

    def declare_function(self, name, return_type, parameters):
        """Declare a new function in the current scope."""
        self.symbol_table.insert(name, {"type": "function", "return_type": return_type, "parameters": parameters})

    def resolve_variable(self, name):
        """Resolve a variable's information."""
        return self.symbol_table.lookup(name)

    def resolve_function(self, name):
        """Resolve a function's information."""
        return self.symbol_table.lookup(name)
