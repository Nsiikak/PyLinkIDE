#Imports the sys module, which provides access to some variables maintained by the Python interpreter and to functions that interact with the interpreter.
import sys
class Parser:
    #Constructor to initialize instances of the Parser class
    def __init__(self, tokens):
        self.tokens = tokens #for the list of tokens
        self.currentPosition = -1 #to keep track of the current position
        self.currentToken = None #to keep track of the current token
        self.advance()
    #A method that is used to move to the next position and current token
    def advance(self):
        self.currentPosition += 1
        if self.currentPosition < len(self.tokens):
            self.currentToken = self.tokens[self.currentPosition]

    #A method that processes tokens until the end of the file ("TT_EOF") is reached and skips newline tokens.
    def runParse(self):
        statements = []

        while self.currentToken.type != "TT_EOF":

            if self.currentToken.type == "TT_NWL":
                self.advance()
                continue

            statement = self.isStatement()
            if statement:
                #If it is a statement, add to the list of statements
                statements.append(statement)
            else:
                sys.exit("Statement not supported")

            if self.tokens[self.currentPosition].type != "TT_NWL":
                sys.exit("Parsing Error: expected newline")

        #Returns all statements found
        return statements
    
    #A method to check if the current token represents a statement by identifying and parsing different types of statements.
    def isStatement(self):
        if self.currentToken.type == "TT_IDENT":  # assignment statement
            identifier = self.currentToken
            self.advance()
            if self.currentToken.type == "TT_EQ":
                self.advance()
                expression = self.expression()
                return Assign(identifier, expression)

        elif self.currentToken.type == "TT_KEYW" and self.currentToken.value == "print":  # print statement
            self.advance()
            if self.currentToken.type == "TT_LPAREN":
                self.advance()
                expression = self.expression()

                if self.currentToken.type == "TT_RPAREN":
                    self.advance()
                    return Print(expression)
                else:
                    sys.exit("Parsing Error: expected ')' ")
            else:
                sys.exit("Parsing Error: expected '(' ")
    #A method which calls the BiOptn method to handle binary operations (addition and subtraction)
    def expression(self):
        return  self.BiOptn(self.term, ["TT_PLUS", "TT_MINUS"])
    #A method which calls the BiOptn method to handle binary operations (multiplication and division).
    def term(self):
        return  self.BiOptn(self.exponent, ["TT_MULT", "TT_DIV"])
    #A method which calls the BiOptn method to handle binary operations (exponentiation).
    def exponent(self):
        return self.BiOptn(self.factor, ["TT_POW"])

    #A method for parsing factors in mathematical expressions. It handles numbers, identifiers, parentheses, and exits with an error message for unexpected tokens.
    def factor(self):
        tok = self.currentToken

        if self.currentToken.type == "TT_NUMBER":
            self.advance()
            return Node(tok)
        elif self.currentToken.type == "TT_IDENT":
            self.advance()
            return Node(tok)
        elif self.currentToken.type == "TT_LPAREN":
            self.advance()
            expr = self.expression()
            if self.currentToken.type == "TT_RPAREN":
                self.advance()
                return expr
            else:
                sys.exit("Parsing Error: Expected a )")
        elif self.currentToken.type == "TT_EOF":
            return Node(tok)
        else:
            sys.exit(f"Parsing Error: Expected a number, but got {self.currentToken.value}")

    #A generic function used to handle binary operations
    def BiOptn(self, func, opts):

        left = func()

        while self.currentToken.type in opts:
            optn = self.currentToken
            self.advance()
            right = func()
            left = BiNode(left, optn, right)

        return left

#A class used for representing a generic node in the abstract syntax tree (AST)
class Node:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok.value}'

    def read(self, obj):
        return self.tok.read(obj)

#A class used for representing a node in the AST for binary operations. It has left and right nodes and an operator token
class BiNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node} {self.op_tok.value} {self.right_node})'
    #A method used to perform binary operations based on the operator
    def read(self, obj):

        if self.op_tok.type == "TT_PLUS":
            return self.left_node.read(obj) + self.right_node.read(obj)
        if self.op_tok.type == "TT_MINUS":
            return self.left_node.read(obj) - self.right_node.read(obj)
        if self.op_tok.type == "TT_DIV":
            return self.left_node.read(obj) / self.right_node.read(obj)
        if self.op_tok.type == "TT_MULT":
            return self.left_node.read(obj) * self.right_node.read(obj)
        if self.op_tok.type == "TT_POW":
            return self.left_node.read(obj) ** self.right_node.read(obj)

#A class used to represent the assignment statement.
class Assign:

    def __init__(self, ident, value):
        self.variable = ident.value
        self.value = value

    def __repr__(self):
        return f"{self.variable} = {self.value}"

    def read(self, obj):
        obj.storage[self.variable] = self.value.read(obj)

#A class used to represent the print statement
class Print:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"print({self.value})"

    def read(self, obj):
         print(self.value.read(obj))
