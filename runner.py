import subprocess
from lexer import lexer
from parser import Parser
from semantic_analyzer import semantic_analyzer
from intermediate_code_generator import generate_intermediate_code
from code_generator import generate_machine_code

def run_program(assembly_code):
    # 1. Write assembly code to a file
    with open('output.asm', 'w') as f:
        f.write(assembly_code)
"""
    # 2. Assemble using nasm (or your assembler)
    try:
        subprocess.run(['nasm', '-felf', 'output.asm'], check=True)
    except subprocess.CalledProcessError:
        print("Error: Assembler (nasm) failed.")
        return

    # 3. Link using gcc (or your linker)
    try:
        subprocess.run(['gcc', '-m32', 'output.o', '-o', 'output'], check=True)
    except subprocess.CalledProcessError:
        print("Error: Linker (gcc) failed.")
        return

    # 4. Run the executable
    try:
        subprocess.run(['./output'], check=True)
    except subprocess.CalledProcessError:
        print("Error: Running the program failed.")
        return

    print("Program executed successfully.")
"""
if __name__ == '__main__':
    from test_code import test_code
    
    tokens = lexer(test_code)
    parser = Parser(tokens)
    ast = parser.parse()
    symbol_table = semantic_analyzer(ast)
    intermediate_code = generate_intermediate_code(ast)
    assembly_code = generate_machine_code(intermediate_code)
    print("Generated Assembly Code:")
    print(assembly_code)
    run_program(assembly_code)