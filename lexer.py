import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def lexer(source_code):
    tokens = []
    position = 0
    while position < len(source_code):
        # Skip whitespace
        if source_code[position].isspace():
            position += 1
            continue

        # String literals
        if source_code[position] == '"':
            start_position = position
            position += 1
            while position < len(source_code) and source_code[position] != '"':
                position += 1
            if position < len(source_code) and source_code[position] == '"':
                value = source_code[start_position + 1:position]
                tokens.append(Token('STRING', value))
                position += 1
                continue
            else:
                print(f"Lexical error: Unterminated string at position {start_position}")
                break

        # Multi-character operators
        if source_code[position:position+2] == '>=':
            tokens.append(Token('OPERATOR', '>='))
            position += 2
            continue
        elif source_code[position:position+2] == '<=':
            tokens.append(Token('OPERATOR', '<='))
            position += 2
            continue
        elif source_code[position:position+2] == '==':
            tokens.append(Token('OPERATOR', '=='))
            position += 2
            continue
        elif source_code[position:position+2] == '!=':
            tokens.append(Token('OPERATOR', '!='))
            position += 2
            continue

        # Keywords
        if re.match(r'int\b', source_code[position:]):
            tokens.append(Token('INT', 'int'))
            position += 3
            continue
        elif re.match(r'if\b', source_code[position:]):
            tokens.append(Token('IF', 'if'))
            position += 2
            continue
        # Add other keywords (like 'printf')
        elif re.match(r'printf\b', source_code[position:]):
            tokens.append(Token('KEYWORD', 'printf')) # Or a specific PRINTF type
            position += 6
            continue

        # Identifiers
        match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*\b', source_code[position:])
        if match:
            identifier = match.group(0)
            tokens.append(Token('IDENTIFIER', identifier))
            position += len(identifier)
            continue

        # Integer literals
        match = re.match(r'\d+\b', source_code[position:])
        if match:
            value = int(match.group(0))
            tokens.append(Token('INTEGER', value))
            position += len(match.group(0))
            continue

        # Single-character operators and symbols
        if source_code[position] == '=':
            tokens.append(Token('OPERATOR', '='))
            position += 1
        elif source_code[position] == ';':
            tokens.append(Token('PUNCTUATOR', ';'))
            position += 1
        elif source_code[position] == '+':
            tokens.append(Token('OPERATOR', '+'))
            position += 1
        elif source_code[position] == '-':
            tokens.append(Token('OPERATOR', '-'))
            position += 1
        elif source_code[position] == '*':
            tokens.append(Token('OPERATOR', '*'))
            position += 1
        elif source_code[position] == '/':
            tokens.append(Token('OPERATOR', '/'))
            position += 1
        elif source_code[position] == '(':
            tokens.append(Token('LPAREN', '('))
            position += 1
        elif source_code[position] == ')':
            tokens.append(Token('RPAREN', ')'))
            position += 1
        elif source_code[position] == '{':
            tokens.append(Token('LBRACE', '{'))
            position += 1
        elif source_code[position] == '}':
            tokens.append(Token('RBRACE', '}'))
            position += 1
        elif source_code[position] == '>':
            tokens.append(Token('OPERATOR', '>'))
            position += 1
        elif source_code[position] == '<':
            tokens.append(Token('OPERATOR', '<'))
            position += 1
        elif source_code[position] == ',':
            tokens.append(Token('COMMA', ',')) # For function arguments
            position += 1
        # Add more single-character operators and symbols as needed

        # Error handling
        else:
            print(f"Lexical error: Unknown character '{source_code[position]}' at position {position}")
            position += 1
    return tokens