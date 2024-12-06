class Interpreter:
    #Constructor used to initialize instances of the Interpreter class.
    def __init__(self, asts):
        #Assigns the list of abstract syntax trees (asts) passed as an argument to the class instance variable
        self.asts = asts
        #Used for storing variables or values during the execution of the ASTs.
        self.storage = {}

    def execute(self):
        #Iterates over each abstract syntax tree (ast) in the list 
        for ast in self.asts:
            # Calls the read method of the current abstract syntax tree (ast) being iterated and passes the self instance of the interpreter
            ast.read(self)
