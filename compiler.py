#Importing the lexer needed for lexical analysis
from lexer import *
#Importing the parser for parsing the tokenized source code
from parser_1 import *
#Importing the interpreter used to Interprete the AST and execute the corresponding actions
from Interpreter import *
#Imports the sys module, which provides access to some variables maintained by the Python interpreter and to functions that interact with the interpreter.
import sys

#Entry point for the script
def main():
    #Retrieving the source code file from the command line arguments
    source = sys.argv[1]
    #Creating a new instance of the lexer class and passing the source code as an argument
    new_lexer = Lexer(source)
    #Obtaining a list of tokens from the lexer after lexical analysis
    tokens = new_lexer.getTokens()
    #Craeting a new instance of the parser class and passing the tokens gotten from the lexer as an argument
    new_parser = Parser(tokens)
    #Obtaining a list of ASTs from the parsing process
    asts = new_parser.runParse()
    #Creating a new instance of the interpreter class and passing the list of ASTs as an argument
    new_interpreter = Interpreter(asts)
    #Interpreting and executing the actions specified by the ASTs
    new_interpreter.execute()

main()