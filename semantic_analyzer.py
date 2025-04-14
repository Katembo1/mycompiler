from parser import ASTNode  # Import the ASTNode

class SymbolTable:
    def __init__(self):
        self.table = {}

    def declare(self, name, type):
        if name in self.table:
            raise Exception(f"Variable '{name}' already declared")
        self.table[name] = type

    def lookup(self, name):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared")
        return self.table[name]

def semantic_analyzer(ast, symbol_table=None):
    if symbol_table is None:
        symbol_table = SymbolTable()

    if ast.type == 'PROGRAM':
        for child in ast.children:
            semantic_analyzer(child, symbol_table)
    elif ast.type == 'DECLARATION':
        if ast.value in symbol_table.table:
            raise Exception(f"Variable '{ast.value}' already declared")
        symbol_table.declare(ast.value, 'int')  # Simplified: All ints for now
    elif ast.type == 'ASSIGNMENT':
        if ast.value not in symbol_table.table:
            raise Exception(f"Variable '{ast.value}' not declared")
        semantic_analyzer(ast.children[0], symbol_table) # Analyze expression
    elif ast.type == 'IF':
        semantic_analyzer(ast.children[0], symbol_table) # Analyze condition
        semantic_analyzer(ast.children[1], symbol_table) # Analyze then block
        if len(ast.children) > 2:
            semantic_analyzer(ast.children[2], symbol_table) # Analyze else block
    elif ast.type == 'INTEGER':
        pass # Fine
    elif ast.type == 'IDENTIFIER':
        if ast.value not in symbol_table.table:
            raise Exception(f"Variable '{ast.value}' not declared")
    return symbol_table

if __name__ == '__main__':
    from lexer import lexer
    from parser import Parser

    test_code = """
    int x;
    x = 10;
    y = x;
    """
    tokens = lexer(test_code)
    parser = Parser(tokens)
    ast = parser.parse()
    symbol_table = semantic_analyzer(ast)
    print("Symbol Table:", symbol_table.table)

    from test_code import test_code
    tokens_error = lexer(test_code)
    parser_error = Parser(tokens_error)
    ast_error = parser_error.parse()
    try:
        semantic_analyzer(ast_error)
    except Exception as e:
        print("Semantic Error:", e)