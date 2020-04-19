# test.asm
# by Kamyar Mirzavaziri
# Designed to test hAssembler.py program
mov al, bh
add cl, al
add ecx, eax
add cx, ax
mov dx, 0x1377
mov edx, 0x1377
mov dl, 0x1377
adc dx, 0x3545
and al, al
# TODO al ax eax <- imd
#add al, 0xAA
#add ax, 0x77
#add eax, 0x1377
add bl, 0xAA
# 8-bit addressing
#add bh, [bl]
add edi, [ebx]
add bx, [ebx]
add bh, [ebx]
add edi, [ebx + 0]
add eax, [esi + 0x77]
add bx, [esi + 0x1377]
add edi, [ebx + 0 - 0x77]
add edi, [ebx + 0 - 0x1377]
add ax, [esi + 0x1999]
add ebx, [ebp + 0xABCDE]
# displacement overflow
#add ebx, [ebp + 0xABCDEFABCD]
add bx, [ebp]
add bx, [ebx]
mov edx, [eax + ecx]
add bx, [eax + ebx]
mov edx, [eax + ecx + 0x55]
mov edx, [ebx + ecx * 4]
mov edx, [ecx*2*2+0x06]
mov edx, [ecx * 2 * 2]
mov edx, [ebp + ecx * 4]
mov edx, [ecx * 4 + 0x06]
mov edx, [ebp + ecx * 4 + 0x06]
mov edx, [ecx * 4 + 0x0666]
mov edx, [ebp + ecx * 4 + 0x0666]
mov edx, [ecx * 4 * 2]
mov edx, [ebp + ecx * 8]
mov edx, [ecx * 8 + 0x06]
mov edx, [ebp + ecx * 8 + 0x06]
mov edx, [ecx * 8 + 0x0666]
mov edx, [ebp + ecx * 8 + 0x0666]
mov edx, [0x1]
mov edx, [0x5555551e]
mov edx, [0x99]
add [ebx], bx
mov edx, [0x5555551e]
mov edx, [eax * 8]
mov edx, [ebp + eax * 8]
mov edx, [eax * 8 + 0xAA]
mov edx, [ebp + eax * 8 + 0xAA]
mov edx, [eax * 8 + 0xAABB]
mov edx, [ebp + eax * 8 + 0xAABB]
add bx, [42 + ebx * 2 + 4 + ecx + 5 + 3 - 2 * 3]
add bx, [2*esp]
add bx, [eax]
add bx, [eax + 2]
add bx, [2*eax]
# HERE
add bx, [esp]

#test ax, [ebx]
#test cx, [edx]
#test ebx, [eax]
#test esi, [ecx]



