def generate_machine_code(intermediate_code):
    assembly_code = []
    assembly_code.append('section .data')
    declared_vars = set()
    for instruction in intermediate_code:
        if instruction.startswith('declare'):
            var_name = instruction.split()[1]
            assembly_code.append(f'    {var_name} dd 0')  # Declare integer variable
            declared_vars.add(var_name)

    assembly_code.append('section .text')
    assembly_code.append('    global main')
    assembly_code.append('main:')
    for instruction in intermediate_code:
        if instruction.startswith('push'):
            value = instruction.split()[1]
            assembly_code.append(f'    push {value}')
        elif instruction.startswith('load'):
            var_name = instruction.split()[1]
            assembly_code.append(f'    mov eax, [{var_name}]')
            assembly_code.append('    push eax')
        elif instruction.startswith('store'):
            var_name = instruction.split()[1]
            assembly_code.append('    pop eax')
            assembly_code.append(f'    mov [{var_name}], eax')
        elif instruction.startswith('jz'):
            label = instruction.split()[1]
            assembly_code.append('    pop eax')
            assembly_code.append('    test eax, eax')
            assembly_code.append(f'    jz {label}')
        elif instruction.startswith('jmp'):
            label = instruction.split()[1]
            assembly_code.append(f'    jmp {label}')
        elif instruction.endswith(':'):
            assembly_code.append(instruction)

    assembly_code.append('    ; Exit program')
    assembly_code.append('    mov eax, 1')  # sys_exit
    assembly_code.append('    xor ebx, ebx')  # exit code 0
    assembly_code.append('    int 0x80')  # Linux system call
    return '\n'.join(assembly_code)

if __name__ == '__main__':
    from lexer import lexer
    from parser import Parser
    from intermediate_code_generator import generate_intermediate_code

    from test_code import test_code
    tokens = lexer(test_code)
    parser = Parser(tokens)
    ast = parser.parse()
    intermediate = generate_intermediate_code(ast)
    assembly = generate_machine_code(intermediate)
    print("Assembly Output:")
    print(assembly)