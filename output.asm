section .data
    x dd 0
    y dd 0
    sum dd 0
section .text
    global main
main:
    push 123
    pop eax
    mov [x], eax
    push 23
    pop eax
    mov [y], eax
    pop eax
    mov [sum], eax
    pop eax
    test eax, eax
    jz else_8
    jmp endif_8
else_8:
endif_8:
    ; Exit program
    mov eax, 1
    xor ebx, ebx
    int 0x80