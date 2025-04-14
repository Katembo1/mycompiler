from parser import ASTNode

def generate_intermediate_code(ast, code=[]):
    if ast.type == 'PROGRAM':
        for child in ast.children:
            generate_intermediate_code(child, code)
    elif ast.type == 'DECLARATION':
        code.append(f'declare {ast.value}')
    elif ast.type == 'ASSIGNMENT':
        generate_intermediate_code(ast.children[0], code)  # Evaluate expression
        code.append(f'store {ast.value}')
    elif ast.type == 'INTEGER':
        code.append(f'push {ast.value}')
    elif ast.type == 'IDENTIFIER':
        code.append(f'load {ast.value}')
    elif ast.type == 'IF':
        generate_intermediate_code(ast.children[0], code)  # Condition
        label_then = f'then_{len(code)}'
        label_else = f'else_{len(code)}'
        label_end = f'endif_{len(code)}'
        code.append(f'jz {label_else}')  # Jump if condition is false
        generate_intermediate_code(ast.children[1], code)  # Then block
        code.append(f'jmp {label_end}')
        code.append(f'{label_else}:')
        if len(ast.children) > 2:
          generate_intermediate_code(ast.children[2], code) # Else block
        code.append(f'{label_end}:')
    return code

if __name__ == '__main__':
    from lexer import lexer
    from parser import Parser

    from test_code import test_code  
    tokens = lexer(test_code)
    parser = Parser(tokens)
    ast = parser.parse()
    intermediate_code = generate_intermediate_code(ast)
    print("Intermediate Code:")
    for instruction in intermediate_code:
        print(instruction)