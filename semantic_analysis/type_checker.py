class TypeChecker:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def check_binary_operation(self, left_type, operator, right_type):
        """Validate binary operations."""
        if left_type == right_type:
            if operator in ["+", "-", "*", "/"] and left_type in ["int", "float"]:
                return left_type
            if operator in ["&&", "||"] and left_type == "bool":
                return "bool"
            raise Exception(f"Semantic Error: Invalid operator '{operator}' for type '{left_type}'.")

        raise Exception(f"Semantic Error: Type mismatch: '{left_type}' and '{right_type}'.")

    def check_assignment(self, variable_name, value_type):
        """Validate variable assignments."""
        variable_info = self.symbol_table.lookup(variable_name)
        if variable_info["type"] != value_type:
            raise Exception(f"Semantic Error: Cannot assign '{value_type}' to '{variable_name}' of type '{variable_info['type']}'.")

    def check_function_call(self, function_name, argument_types):
        """Validate function calls."""
        function_info = self.symbol_table.lookup(function_name)
        if "parameters" not in function_info:
            raise Exception(f"Semantic Error: '{function_name}' is not a function.")

        expected_types = function_info["parameters"]
        if len(expected_types) != len(argument_types):
            raise Exception(f"Semantic Error: Function '{function_name}' expects {len(expected_types)} arguments but got {len(argument_types)}.")

        for expected, actual in zip(expected_types, argument_types):
            if expected != actual:
                raise Exception(f"Semantic Error: Argument type mismatch. Expected '{expected}', got '{actual}'.")
