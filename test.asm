PRIME:
	; if the number is prime the rdx will be 1, else it'll be zero
	mov r8, rax
	mov rbx, 2

	; iterate all numbers
	main_loop_start:
	cmp rbx, rax
	jge main_loop_end
		mov rdx, 0
		div rbx
		mov rax, r8
		cmp rdx, 0
		je no_case
		inc rbx
	jmp main_loop_start
	main_loop_end:

	mov rdx, 1
	ret

	no_case:
		mov rdx, 0
		ret
section .data:
	a dq 37
section .text:
	global _start
_start:
	mov rax, [a]
	call PRIME
exit:
	mov ebx, 0
	mov eax, 1
	int 80h
