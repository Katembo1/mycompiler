from lexer import Token  # Make sure you import Token

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.position = 0

    def next_token(self):
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
            self.position += 1
        else:
            self.current_token = None

    def peek(self, offset=0):
        if self.position + offset < len(self.tokens):
            return self.tokens[self.position + offset]
        return None

    def parse(self):
        self.next_token()
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.current_token:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return ASTNode('PROGRAM', children=statements)

    def parse_statement(self):
        if self.current_token and self.current_token.type == 'INT':
            return self.parse_declaration()
        elif self.current_token and self.current_token.type == 'IDENTIFIER':
            # Check for assignment
            if self.peek() and self.peek().type == 'OPERATOR' and self.peek().value == '=':
                return self.parse_assignment()
            else:
                # For now, treat standalone identifiers as expressions
                return self.parse_expression()
        elif self.current_token and self.current_token.type == 'IF':
            return self.parse_if_statement()
        elif self.current_token and self.current_token.type == 'LBRACE':
            return self.parse_block_statement()
        elif self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'printf':
            return self.parse_printf_statement()
        elif self.current_token and self.current_token.type == 'PUNCTUATOR' and self.current_token.value == ';':
            self.next_token() # Consume empty statement (just a semicolon)
            return None
        elif self.current_token:
            return self.parse_expression() # Try parsing as an expression
        return None

    def parse_declaration(self):
        self.next_token()  # Consume 'int'
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            raise Exception("Expected identifier in declaration")
        var_name = self.current_token.value
        self.next_token()

        init_expr = None
        if self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == '=':
            self.next_token()
            init_expr = self.parse_expression()

        if not self.current_token or self.current_token.type != 'PUNCTUATOR' or self.current_token.value != ';':
            raise Exception("Expected ';' at end of declaration")
        self.next_token()  # Consume ';'
        return ASTNode('DECLARATION', value=var_name, children=[init_expr] if init_expr else [])

    def parse_assignment(self):
        var_name = self.current_token.value
        self.next_token()
        if not self.current_token or self.current_token.type != 'OPERATOR' or self.current_token.value != '=':
            raise Exception("Expected '=' in assignment")
        self.next_token()
        expr = self.parse_expression()
        if not self.current_token or self.current_token.type != 'PUNCTUATOR' or self.current_token.value != ';':
            raise Exception("Expected ';' at end of assignment")
        self.next_token()  # Consume the semicolon
        return ASTNode('ASSIGNMENT', value=var_name, children=[expr])

    def parse_expression(self):
        return self.parse_comparison_expression() # Start with comparison

    def parse_comparison_expression(self):
        left = self.parse_additive_expression()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['>=', '<=', '>', '<', '==', '!=']:
            op = self.current_token.value
            self.next_token()
            right = self.parse_additive_expression()
            left = ASTNode('BINARY_OP', value=op, children=[left, right])
        return left

    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-']:
            op = self.current_token.value
            self.next_token()
            right = self.parse_multiplicative_expression()
            left = ASTNode('BINARY_OP', value=op, children=[left, right])
        return left

    def parse_multiplicative_expression(self):
        left = self.parse_primary()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['*', '/']:
            op = self.current_token.value
            self.next_token()
            right = self.parse_primary()
            left = ASTNode('BINARY_OP', value=op, children=[left, right])
        return left

    def parse_primary(self):
        if self.current_token and self.current_token.type == 'INTEGER':
            node = ASTNode('INTEGER', value=self.current_token.value)
            self.next_token()
            return node
        elif self.current_token and self.current_token.type == 'IDENTIFIER':
            node = ASTNode('IDENTIFIER', value=self.current_token.value)
            self.next_token()
            return node
        elif self.current_token and self.current_token.type == 'LPAREN':
            self.next_token()
            expr = self.parse_expression()
            if not self.current_token or self.current_token.type != 'RPAREN':
                raise Exception("Expected ')' after expression")
            self.next_token()
            return expr
        else:
            raise Exception(f"Unexpected token in expression: {self.current_token.type if self.current_token else None}")

    def parse_if_statement(self):
        self.next_token() # Consume 'if'
        if not self.current_token or self.current_token.type != 'LPAREN':
            raise Exception("Expected '(' after 'if'")
        self.next_token()
        condition = self.parse_expression()
        if not self.current_token or self.current_token.type != 'RPAREN':
            raise Exception("Expected ')' after condition")
        self.next_token()
        then_block = self.parse_statement() # Now parse the then block as a statement
        if self.current_token and self.current_token.type == 'ELSE':
            self.next_token()
            else_block = self.parse_statement()
            return ASTNode('IF', children=[condition, then_block, else_block])
        return ASTNode('IF', children=[condition, then_block])

    def parse_block_statement(self):
        self.next_token() # Consume '{'
        statements = []
        while self.current_token and self.current_token.type != 'RBRACE':
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        if not self.current_token or self.current_token.type != 'RBRACE':
            raise Exception("Expected '}' at end of block")
        self.next_token() # Consume '}'
        return ASTNode('BLOCK', children=statements)

    def parse_printf_statement(self):
        self.next_token() # Consume 'printf'
        if not self.current_token or self.current_token.type != 'LPAREN':
            raise Exception("Expected '(' after printf")
        self.next_token()
        if not self.current_token or self.current_token.type != 'STRING':
            raise Exception("Expected string argument in printf")
        string_value = self.current_token.value
        self.next_token()
        if not self.current_token or self.current_token.type != 'RPAREN':
            raise Exception("Expected ')' after printf argument")
        self.next_token()
        if not self.current_token or self.current_token.type != 'PUNCTUATOR' or self.current_token.value != ';':
            raise Exception("Expected ';' after printf statement")
        self.next_token() # Consume ';'
        return ASTNode('PRINTF', children=[ASTNode('STRING_LITERAL', value=string_value)])

if __name__ == '__main__':
    from lexer import lexer
    from test_code import test_code
    tokens = lexer(test_code)
    parser = Parser(tokens)
    ast = parser.parse()

    def print_ast(node, indent=0):
        print('  ' * indent + f"Type: {node.type}, Value: {node.value}, Children: {len(node.children)}")
        for child in node.children:
            print_ast(child, indent + 1)

    print_ast(ast)