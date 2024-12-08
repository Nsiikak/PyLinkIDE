class SymbolTable:
    def __init__(self):
        # Stack of scopes (each scope is a dictionary)
        self.scopes = [{}]

    def insert(self, name, symbol_info):
        """Insert a symbol into the current scope."""
        if name in self.scopes[-1]:
            raise Exception(f"Semantic Error: '{name}' already declared in this scope.")
        self.scopes[-1][name] = symbol_info

    def lookup(self, name):
        """Lookup a symbol in the current and parent scopes."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Semantic Error: '{name}' is not declared.")

    def update(self, name, new_info):
        """Update a symbol's information."""
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name].update(new_info)
                return
        raise Exception(f"Semantic Error: '{name}' is not declared.")

    def push_scope(self):
        """Add a new scope for a block."""
        self.scopes.append({})

    def pop_scope(self):
        """Remove the most recent scope after leaving a block."""
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Semantic Error: Cannot pop the global scope.")

    def display(self):
        """Display the current symbol table for debugging."""
        for i, scope in enumerate(self.scopes):
            print(f"Scope {i}: {scope}")
