# Importing necessary modules for the compiler workflow
from lexer import *
from parser_1 import *
from Interpreter import *
from semantic_analysis.symbol_table import SymbolTable
from semantic_analysis.type_checker import TypeChecker
from semantic_analysis.scope_manager import ScopeManager
import sys

# Entry point for the script
def main():
    # Step 1: Retrieve the source code file from the command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_code_file>")
        sys.exit(1)
    source = sys.argv[1]

    # Step 2: Perform lexical analysis (tokenization)
    new_lexer = Lexer(source)
    tokens = new_lexer.getTokens()

    # Step 3: Parse the tokens to generate the Abstract Syntax Tree (AST)
    new_parser = Parser(tokens)
    asts = new_parser.runParse()

    # Step 4: Initialize semantic analysis components
    symbol_table = SymbolTable()
    type_checker = TypeChecker(symbol_table)
    scope_manager = ScopeManager()

    # Step 5: Perform semantic analysis on the AST
    try:
        for ast in asts:
            analyze_ast(ast, symbol_table, type_checker, scope_manager)
        print("Semantic Analysis: Passed")
    except Exception as e:
        print(f"Semantic Analysis Error: {e}")
        sys.exit(1)

    # Step 6: Interpret the AST (execution)
    new_interpreter = Interpreter(asts)
    new_interpreter.execute()

def analyze_ast(ast, symbol_table, type_checker, scope_manager):
    """
    Performs semantic analysis on the given AST node.
    This function traverses the AST to validate declarations, assignments,
    operations, and scope management.
    """
    if isinstance(ast, Assign):
        # Variable assignment
        variable_name = ast.variable
        value_type = ast.value.read(type_checker)  # Infer the type of the value
        if variable_name not in symbol_table.scopes[-1]:
            # Declare the variable in the current scope
            scope_manager.declare_variable(variable_name, value_type)
        else:
            # Validate the assignment type
            type_checker.check_assignment(variable_name, value_type)

    elif isinstance(ast, Print):
        # Print statement (validate the expression type)
        value_type = ast.value.read(type_checker)
        if value_type not in ["int", "float", "string"]:
            raise Exception(f"Cannot print value of type '{value_type}'.")

    elif isinstance(ast, FunctionCall):
        # Function call (validate arguments and return type)
        function_name = ast.function_name
        argument_types = [arg.read(type_checker) for arg in ast.arguments]
        type_checker.check_function_call(function_name, argument_types)

    elif isinstance(ast, Block):
        # Enter a new scope for blocks of code
        scope_manager.enter_scope()
        for stmt in ast.statements:
            analyze_ast(stmt, symbol_table, type_checker, scope_manager)
        scope_manager.exit_scope()

    else:
        # Handle other AST node types (e.g., loops, conditionals)
        pass

if __name__ == "__main__":
    main()