.section __TEXT,__text
.globl _main
.p2align 2
_main:
    stp x29, x30, [sp, #-16]!
    stp x19, x20, [sp, #-16]!
    mov x29, sp
    mov x15, #4624
    sub sp, sp, x15
    adrp x0, L_kuro_data_0@PAGE
    add x0, x0, L_kuro_data_0@PAGEOFF
    str x0, [sp, #1208]
    ldr x0, [sp, #1208]
    adrp x2, _kuro_global_203@PAGE
    add x2, x2, _kuro_global_203@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_1@PAGE
    add x0, x0, L_kuro_data_1@PAGEOFF
    str x0, [sp, #1216]
    ldr x0, [sp, #1216]
    adrp x2, _kuro_global_1@PAGE
    add x2, x2, _kuro_global_1@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_2@PAGE
    add x0, x0, L_kuro_data_2@PAGEOFF
    str x0, [sp, #2104]
    ldr x0, [sp, #2104]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_3@PAGE
    add x0, x0, L_kuro_data_3@PAGEOFF
    str x0, [sp, #2992]
    ldr x0, [sp, #2992]
    adrp x2, _kuro_global_209@PAGE
    add x2, x2, _kuro_global_209@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_4@PAGE
    add x0, x0, L_kuro_data_4@PAGEOFF
    str x0, [sp, #3880]
    ldr x0, [sp, #3880]
    adrp x2, _kuro_global_94@PAGE
    add x2, x2, _kuro_global_94@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_5@PAGE
    add x0, x0, L_kuro_data_5@PAGEOFF
    str x0, [sp, #4088]
    ldr x0, [sp, #4088]
    adrp x2, _kuro_global_216@PAGE
    add x2, x2, _kuro_global_216@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_6@PAGE
    add x0, x0, L_kuro_data_6@PAGEOFF
    str x0, [sp, #4176]
    ldr x0, [sp, #4176]
    adrp x2, _kuro_global_7@PAGE
    add x2, x2, _kuro_global_7@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_7@PAGE
    add x0, x0, L_kuro_data_7@PAGEOFF
    str x0, [sp, #4264]
    ldr x0, [sp, #4264]
    adrp x2, _kuro_global_220@PAGE
    add x2, x2, _kuro_global_220@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_8@PAGE
    add x0, x0, L_kuro_data_8@PAGEOFF
    str x0, [sp, #4352]
    ldr x0, [sp, #4352]
    adrp x2, _kuro_global_26@PAGE
    add x2, x2, _kuro_global_26@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_9@PAGE
    add x0, x0, L_kuro_data_9@PAGEOFF
    str x0, [sp, #4440]
    ldr x0, [sp, #4440]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_10@PAGE
    add x0, x0, L_kuro_data_10@PAGEOFF
    str x0, [sp, #1224]
    ldr x0, [sp, #1224]
    adrp x2, _kuro_global_208@PAGE
    add x2, x2, _kuro_global_208@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_11@PAGE
    add x0, x0, L_kuro_data_11@PAGEOFF
    str x0, [sp, #1312]
    ldr x0, [sp, #1312]
    adrp x2, _kuro_global_23@PAGE
    add x2, x2, _kuro_global_23@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_12@PAGE
    add x0, x0, L_kuro_data_12@PAGEOFF
    str x0, [sp, #1400]
    ldr x0, [sp, #1400]
    adrp x2, _kuro_global_46@PAGE
    add x2, x2, _kuro_global_46@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_13@PAGE
    add x0, x0, L_kuro_data_13@PAGEOFF
    str x0, [sp, #1488]
    ldr x0, [sp, #1488]
    adrp x2, _kuro_global_205@PAGE
    add x2, x2, _kuro_global_205@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_14@PAGE
    add x0, x0, L_kuro_data_14@PAGEOFF
    str x0, [sp, #1576]
    ldr x0, [sp, #1576]
    adrp x2, _kuro_global_0@PAGE
    add x2, x2, _kuro_global_0@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_15@PAGE
    add x0, x0, L_kuro_data_15@PAGEOFF
    str x0, [sp, #1664]
    ldr x0, [sp, #1664]
    adrp x2, _kuro_global_201@PAGE
    add x2, x2, _kuro_global_201@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_16@PAGE
    add x0, x0, L_kuro_data_16@PAGEOFF
    str x0, [sp, #1752]
    ldr x0, [sp, #1752]
    adrp x2, _kuro_global_92@PAGE
    add x2, x2, _kuro_global_92@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_17@PAGE
    add x0, x0, L_kuro_data_17@PAGEOFF
    str x0, [sp, #1840]
    ldr x0, [sp, #1840]
    adrp x2, _kuro_global_212@PAGE
    add x2, x2, _kuro_global_212@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_18@PAGE
    add x0, x0, L_kuro_data_18@PAGEOFF
    str x0, [sp, #1928]
    ldr x0, [sp, #1928]
    adrp x2, _kuro_global_10@PAGE
    add x2, x2, _kuro_global_10@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_19@PAGE
    add x0, x0, L_kuro_data_19@PAGEOFF
    str x0, [sp, #2016]
    ldr x0, [sp, #2016]
    adrp x2, _kuro_global_93@PAGE
    add x2, x2, _kuro_global_93@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_20@PAGE
    add x0, x0, L_kuro_data_20@PAGEOFF
    str x0, [sp, #2112]
    ldr x0, [sp, #2112]
    adrp x2, _kuro_global_215@PAGE
    add x2, x2, _kuro_global_215@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_21@PAGE
    add x0, x0, L_kuro_data_21@PAGEOFF
    str x0, [sp, #2200]
    ldr x0, [sp, #2200]
    adrp x2, _kuro_global_204@PAGE
    add x2, x2, _kuro_global_204@PAGEOFF
    str x0, [x2]
    mov x19, #0
    movz x20, #65535
    movk x20, #15, lsl #16
L_kuro_read_0:
    adrp x1, _kuro_input_buffer@PAGE
    add x1, x1, _kuro_input_buffer@PAGEOFF
    add x1, x1, x19
    sub x2, x20, x19
    cbz x2, L_kuro_runtime_error
    mov w0, #0
    bl _read
    cmp x0, #0
    b.lt L_kuro_runtime_error
    cbz x0, L_kuro_read_done_0
    add x19, x19, x0
    b L_kuro_read_0
L_kuro_read_done_0:
    adrp x1, _kuro_input_buffer@PAGE
    add x1, x1, _kuro_input_buffer@PAGEOFF
    strb wzr, [x1, x19]
    mov x0, x1
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_210@PAGE
    add x0, x0, _kuro_global_210@PAGEOFF
    ldr x0, [x0]
    cbz x0, L_kuro_length_zero_t22
    bl _strlen
    b L_kuro_length_done_t22
L_kuro_length_zero_t22:
    mov x0, #0
L_kuro_length_done_t22:
    str x0, [sp, #2288]
    ldr x0, [sp, #2288]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2376]
    ldr x0, [sp, #2376]
    adrp x2, _kuro_global_211@PAGE
    add x2, x2, _kuro_global_211@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2464]
    ldr x0, [sp, #2464]
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2552]
    adrp x0, _kuro_global_38@PAGE
    add x0, x0, _kuro_global_38@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2640]
    mov x0, #0
    str x0, [sp, #2728]
    ldr x0, [sp, #2728]
    str x0, [sp, #520]
L_kuro_repeat_start0:
    ldr x0, [sp, #520]
    str x0, [sp, #2816]
    ldr x0, [sp, #2816]
    ldr x1, [sp, #2552]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #2904]
    ldr x0, [sp, #2904]
    cbz w0, L_kuro_repeat_end1
    ldr x0, [sp, #2816]
    adrp x2, _kuro_global_38@PAGE
    add x2, x2, _kuro_global_38@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3000]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3088]
    ldr x0, [sp, #3000]
    ldr x1, [sp, #3088]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #3176]
    ldr x0, [sp, #3176]
    cbz w0, L_kuro_else2
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3264]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #3264]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #3352]
    ldr x0, [sp, #3352]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3440]
    ldr x0, [sp, #3440]
    adrp x2, _kuro_global_8@PAGE
    add x2, x2, _kuro_global_8@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3528]
    ldr x0, [sp, #3528]
    adrp x2, _kuro_global_219@PAGE
    add x2, x2, _kuro_global_219@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3616]
    ldr x0, [sp, #3616]
    cmp x0, #0
    b.le L_kuro_isclass_invalid_t38
    cmp x0, #0x1000
    b.lo L_kuro_isclass_invalid_t38
    ldrb w0, [x0]
    cmp w0, #32
    cset w1, eq
    cmp w0, #9
    cset w2, eq
    orr w1, w1, w2
    cmp w0, #10
    cset w2, eq
    orr w1, w1, w2
    cmp w0, #13
    cset w0, eq
    orr w0, w1, w0
    b L_kuro_isclass_done_t38
L_kuro_isclass_invalid_t38:
    mov x0, #0
L_kuro_isclass_done_t38:
    str x0, [sp, #3704]
    ldr x0, [sp, #3704]
    cbz w0, L_kuro_else4
    mov x0, #1
    str x0, [sp, #3792]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3792]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif5
L_kuro_else4:
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3888]
    mov x0, #1
    str x0, [sp, #3976]
    ldr x0, [sp, #3888]
    ldr x1, [sp, #3976]
    add x0, x0, x1
    str x0, [sp, #4024]
    ldr x0, [sp, #4024]
    adrp x2, _kuro_global_104@PAGE
    add x2, x2, _kuro_global_104@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_94@PAGE
    add x0, x0, _kuro_global_94@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4032]
    ldr x0, [sp, #4032]
    adrp x2, _kuro_global_103@PAGE
    add x2, x2, _kuro_global_103@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_104@PAGE
    add x0, x0, _kuro_global_104@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4040]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4048]
    ldr x0, [sp, #4040]
    ldr x1, [sp, #4048]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4056]
    ldr x0, [sp, #4056]
    cbz w0, L_kuro_else6
    adrp x0, _kuro_global_104@PAGE
    add x0, x0, _kuro_global_104@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4064]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #4064]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #4072]
    ldr x0, [sp, #4072]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4080]
    ldr x0, [sp, #4080]
    adrp x2, _kuro_global_103@PAGE
    add x2, x2, _kuro_global_103@PAGEOFF
    str x0, [x2]
    b L_kuro_endif7
L_kuro_else6:
L_kuro_endif7:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4096]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4104]
    ldr x0, [sp, #4096]
    ldr x1, [sp, #4104]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4112]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4120]
    adrp x0, _kuro_global_209@PAGE
    add x0, x0, _kuro_global_209@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4128]
    ldr x0, [sp, #4120]
    ldr x1, [sp, #4128]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4136]
    adrp x0, _kuro_global_103@PAGE
    add x0, x0, _kuro_global_103@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4144]
    adrp x0, _kuro_global_209@PAGE
    add x0, x0, _kuro_global_209@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4152]
    ldr x0, [sp, #4144]
    ldr x1, [sp, #4152]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4160]
    ldr x0, [sp, #4136]
    ldr x1, [sp, #4160]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #4168]
    ldr x0, [sp, #4112]
    ldr x1, [sp, #4168]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4184]
    ldr x0, [sp, #4184]
    cbz w0, L_kuro_else8
    mov x0, #1
    str x0, [sp, #4192]
    ldr x0, [sp, #4192]
    adrp x2, _kuro_global_12@PAGE
    add x2, x2, _kuro_global_12@PAGEOFF
    str x0, [x2]
L_kuro_while_start10:
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4200]
    mov x0, #1
    str x0, [sp, #4208]
    ldr x0, [sp, #4200]
    ldr x1, [sp, #4208]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4216]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4224]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4232]
    ldr x0, [sp, #4224]
    ldr x1, [sp, #4232]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4240]
    ldr x0, [sp, #4216]
    ldr x1, [sp, #4240]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #4248]
    ldr x0, [sp, #4248]
    cbz w0, L_kuro_while_end11
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4256]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #4256]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #4272]
    ldr x0, [sp, #4272]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4280]
    ldr x0, [sp, #4280]
    adrp x2, _kuro_global_9@PAGE
    add x2, x2, _kuro_global_9@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4288]
    adrp x0, _kuro_global_94@PAGE
    add x0, x0, _kuro_global_94@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4296]
    ldr x0, [sp, #4288]
    ldr x1, [sp, #4296]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4304]
    ldr x0, [sp, #4304]
    cbz w0, L_kuro_else13
    mov x0, #0
    str x0, [sp, #4312]
    ldr x0, [sp, #4312]
    adrp x2, _kuro_global_12@PAGE
    add x2, x2, _kuro_global_12@PAGEOFF
    str x0, [x2]
    b L_kuro_endif14
L_kuro_else13:
    mov x0, #1
    str x0, [sp, #4320]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4320]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
L_kuro_endif14:
    b L_kuro_while_start10
L_kuro_while_end11:
    b L_kuro_endif9
L_kuro_else8:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4328]
    adrp x0, _kuro_global_203@PAGE
    add x0, x0, _kuro_global_203@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4336]
    ldr x0, [sp, #4328]
    ldr x1, [sp, #4336]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4344]
    ldr x0, [sp, #4344]
    cbz w0, L_kuro_else15
    mov x0, #1
    str x0, [sp, #4360]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4360]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_22@PAGE
    add x0, x0, L_kuro_data_22@PAGEOFF
    str x0, [sp, #4368]
    ldr x0, [sp, #4368]
    adrp x2, _kuro_global_213@PAGE
    add x2, x2, _kuro_global_213@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #4376]
    ldr x0, [sp, #4376]
    adrp x2, _kuro_global_214@PAGE
    add x2, x2, _kuro_global_214@PAGEOFF
    str x0, [x2]
L_kuro_while_start17:
    adrp x0, _kuro_global_214@PAGE
    add x0, x0, _kuro_global_214@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4384]
    mov x0, #1
    str x0, [sp, #4392]
    ldr x0, [sp, #4384]
    ldr x1, [sp, #4392]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4400]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4408]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4416]
    ldr x0, [sp, #4408]
    ldr x1, [sp, #4416]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4424]
    ldr x0, [sp, #4400]
    ldr x1, [sp, #4424]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #4432]
    ldr x0, [sp, #4432]
    cbz w0, L_kuro_while_end18
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4448]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #4448]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #4456]
    ldr x0, [sp, #4456]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4464]
    ldr x0, [sp, #4464]
    adrp x2, _kuro_global_9@PAGE
    add x2, x2, _kuro_global_9@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4472]
    adrp x0, _kuro_global_203@PAGE
    add x0, x0, _kuro_global_203@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4480]
    ldr x0, [sp, #4472]
    ldr x1, [sp, #4480]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4488]
    ldr x0, [sp, #4488]
    cbz w0, L_kuro_else20
    mov x0, #1
    str x0, [sp, #4496]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4496]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4504]
    ldr x0, [sp, #4504]
    adrp x2, _kuro_global_214@PAGE
    add x2, x2, _kuro_global_214@PAGEOFF
    str x0, [x2]
    b L_kuro_endif21
L_kuro_else20:
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4512]
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4520]
    ldr x0, [sp, #4512]
    ldr x1, [sp, #4520]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1232]
    ldr x0, [sp, #1232]
    cbz w0, L_kuro_else22
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1240]
    mov x0, #1
    str x0, [sp, #1248]
    ldr x0, [sp, #1240]
    ldr x1, [sp, #1248]
    add x0, x0, x1
    str x0, [sp, #1256]
    ldr x0, [sp, #1256]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1264]
    ldr x0, [sp, #1264]
    adrp x2, _kuro_global_27@PAGE
    add x2, x2, _kuro_global_27@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_28@PAGE
    add x0, x0, _kuro_global_28@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1272]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1280]
    ldr x0, [sp, #1272]
    ldr x1, [sp, #1280]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #1288]
    ldr x0, [sp, #1288]
    cbz w0, L_kuro_else24
    adrp x0, _kuro_global_28@PAGE
    add x0, x0, _kuro_global_28@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1296]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #1296]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #1304]
    ldr x0, [sp, #1304]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1320]
    ldr x0, [sp, #1320]
    adrp x2, _kuro_global_27@PAGE
    add x2, x2, _kuro_global_27@PAGEOFF
    str x0, [x2]
    b L_kuro_endif25
L_kuro_else24:
L_kuro_endif25:
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1328]
    adrp x0, _kuro_global_93@PAGE
    add x0, x0, _kuro_global_93@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1336]
    ldr x0, [sp, #1328]
    ldr x1, [sp, #1336]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1344]
    ldr x0, [sp, #1344]
    cbz w0, L_kuro_else26
    adrp x0, _kuro_global_213@PAGE
    add x0, x0, _kuro_global_213@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1352]
    adrp x0, _kuro_global_94@PAGE
    add x0, x0, _kuro_global_94@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1360]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1368]
    ldr x0, [sp, #1368]
    ldr x1, [sp, #1352]
    bl _strcpy
    ldr x0, [sp, #1368]
    ldr x1, [sp, #1360]
    bl _strcat
    ldr x0, [sp, #1368]
    adrp x2, _kuro_global_213@PAGE
    add x2, x2, _kuro_global_213@PAGEOFF
    str x0, [x2]
    b L_kuro_endif27
L_kuro_else26:
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1376]
    adrp x0, _kuro_global_215@PAGE
    add x0, x0, _kuro_global_215@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1384]
    ldr x0, [sp, #1376]
    ldr x1, [sp, #1384]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1392]
    ldr x0, [sp, #1392]
    cbz w0, L_kuro_else28
    adrp x0, _kuro_global_213@PAGE
    add x0, x0, _kuro_global_213@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1408]
    adrp x0, _kuro_global_216@PAGE
    add x0, x0, _kuro_global_216@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1416]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1424]
    ldr x0, [sp, #1424]
    ldr x1, [sp, #1408]
    bl _strcpy
    ldr x0, [sp, #1424]
    ldr x1, [sp, #1416]
    bl _strcat
    ldr x0, [sp, #1424]
    adrp x2, _kuro_global_213@PAGE
    add x2, x2, _kuro_global_213@PAGEOFF
    str x0, [x2]
    b L_kuro_endif29
L_kuro_else28:
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1432]
    adrp x0, _kuro_global_204@PAGE
    add x0, x0, _kuro_global_204@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1440]
    ldr x0, [sp, #1432]
    ldr x1, [sp, #1440]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1448]
    ldr x0, [sp, #1448]
    cbz w0, L_kuro_else30
    adrp x0, _kuro_global_213@PAGE
    add x0, x0, _kuro_global_213@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1456]
    adrp x0, _kuro_global_7@PAGE
    add x0, x0, _kuro_global_7@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1464]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1472]
    ldr x0, [sp, #1472]
    ldr x1, [sp, #1456]
    bl _strcpy
    ldr x0, [sp, #1472]
    ldr x1, [sp, #1464]
    bl _strcat
    ldr x0, [sp, #1472]
    adrp x2, _kuro_global_213@PAGE
    add x2, x2, _kuro_global_213@PAGEOFF
    str x0, [x2]
    b L_kuro_endif31
L_kuro_else30:
    adrp x0, _kuro_global_213@PAGE
    add x0, x0, _kuro_global_213@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1480]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1496]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1504]
    ldr x0, [sp, #1504]
    ldr x1, [sp, #1480]
    bl _strcpy
    ldr x0, [sp, #1504]
    ldr x1, [sp, #1496]
    bl _strcat
    ldr x0, [sp, #1504]
    adrp x2, _kuro_global_213@PAGE
    add x2, x2, _kuro_global_213@PAGEOFF
    str x0, [x2]
L_kuro_endif31:
L_kuro_endif29:
L_kuro_endif27:
    mov x0, #2
    str x0, [sp, #1512]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1512]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif23
L_kuro_else22:
    adrp x0, _kuro_global_213@PAGE
    add x0, x0, _kuro_global_213@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1520]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1528]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1536]
    ldr x0, [sp, #1536]
    ldr x1, [sp, #1520]
    bl _strcpy
    ldr x0, [sp, #1536]
    ldr x1, [sp, #1528]
    bl _strcat
    ldr x0, [sp, #1536]
    adrp x2, _kuro_global_213@PAGE
    add x2, x2, _kuro_global_213@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1544]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1544]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
L_kuro_endif23:
L_kuro_endif21:
    b L_kuro_while_start17
L_kuro_while_end18:
    adrp x0, L_kuro_data_23@PAGE
    add x0, x0, L_kuro_data_23@PAGEOFF
    str x0, [sp, #1552]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1552]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1560]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1560]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_213@PAGE
    add x0, x0, _kuro_global_213@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1568]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1568]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    b L_kuro_endif16
L_kuro_else15:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1584]
    ldr x0, [sp, #1584]
    cmp x0, #0
    b.le L_kuro_isclass_invalid_t141
    cmp x0, #0x1000
    b.lo L_kuro_isclass_invalid_t141
    ldrb w0, [x0]
    sub w0, w0, #48
    cmp w0, #9
    cset w0, ls
    b L_kuro_isclass_done_t141
L_kuro_isclass_invalid_t141:
    mov x0, #0
L_kuro_isclass_done_t141:
    str x0, [sp, #1592]
    ldr x0, [sp, #1592]
    cbz w0, L_kuro_else32
    adrp x0, L_kuro_data_24@PAGE
    add x0, x0, L_kuro_data_24@PAGEOFF
    str x0, [sp, #1600]
    ldr x0, [sp, #1600]
    adrp x2, _kuro_global_105@PAGE
    add x2, x2, _kuro_global_105@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #1608]
    ldr x0, [sp, #1608]
    adrp x2, _kuro_global_39@PAGE
    add x2, x2, _kuro_global_39@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1616]
    ldr x0, [sp, #1616]
    adrp x2, _kuro_global_106@PAGE
    add x2, x2, _kuro_global_106@PAGEOFF
    str x0, [x2]
L_kuro_while_start34:
    adrp x0, _kuro_global_106@PAGE
    add x0, x0, _kuro_global_106@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1624]
    mov x0, #1
    str x0, [sp, #1632]
    ldr x0, [sp, #1624]
    ldr x1, [sp, #1632]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1640]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1648]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1656]
    ldr x0, [sp, #1648]
    ldr x1, [sp, #1656]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #1672]
    ldr x0, [sp, #1640]
    ldr x1, [sp, #1672]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #1680]
    ldr x0, [sp, #1680]
    cbz w0, L_kuro_while_end35
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1688]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #1688]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #1696]
    ldr x0, [sp, #1696]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1704]
    ldr x0, [sp, #1704]
    adrp x2, _kuro_global_9@PAGE
    add x2, x2, _kuro_global_9@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1712]
    ldr x0, [sp, #1712]
    cmp x0, #0
    b.le L_kuro_isclass_invalid_t156
    cmp x0, #0x1000
    b.lo L_kuro_isclass_invalid_t156
    ldrb w0, [x0]
    sub w0, w0, #48
    cmp w0, #9
    cset w0, ls
    b L_kuro_isclass_done_t156
L_kuro_isclass_invalid_t156:
    mov x0, #0
L_kuro_isclass_done_t156:
    str x0, [sp, #1720]
    ldr x0, [sp, #1720]
    cbz w0, L_kuro_else37
    adrp x0, _kuro_global_105@PAGE
    add x0, x0, _kuro_global_105@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1728]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1736]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1744]
    ldr x0, [sp, #1744]
    ldr x1, [sp, #1728]
    bl _strcpy
    ldr x0, [sp, #1744]
    ldr x1, [sp, #1736]
    bl _strcat
    ldr x0, [sp, #1744]
    adrp x2, _kuro_global_105@PAGE
    add x2, x2, _kuro_global_105@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1760]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1760]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif38
L_kuro_else37:
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1768]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1776]
    ldr x0, [sp, #1768]
    ldr x1, [sp, #1776]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1784]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1792]
    mov x0, #0
    str x0, [sp, #1800]
    ldr x0, [sp, #1792]
    ldr x1, [sp, #1800]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1808]
    ldr x0, [sp, #1784]
    ldr x1, [sp, #1808]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #1816]
    ldr x0, [sp, #1816]
    cbz w0, L_kuro_else39
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1824]
    mov x0, #1
    str x0, [sp, #1832]
    ldr x0, [sp, #1824]
    ldr x1, [sp, #1832]
    add x0, x0, x1
    str x0, [sp, #1848]
    ldr x0, [sp, #1848]
    adrp x2, _kuro_global_25@PAGE
    add x2, x2, _kuro_global_25@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1856]
    ldr x0, [sp, #1856]
    adrp x2, _kuro_global_24@PAGE
    add x2, x2, _kuro_global_24@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_25@PAGE
    add x0, x0, _kuro_global_25@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1864]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1872]
    ldr x0, [sp, #1864]
    ldr x1, [sp, #1872]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #1880]
    ldr x0, [sp, #1880]
    cbz w0, L_kuro_else41
    adrp x0, _kuro_global_25@PAGE
    add x0, x0, _kuro_global_25@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1888]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #1888]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #1896]
    ldr x0, [sp, #1896]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1904]
    ldr x0, [sp, #1904]
    adrp x2, _kuro_global_24@PAGE
    add x2, x2, _kuro_global_24@PAGEOFF
    str x0, [x2]
    b L_kuro_endif42
L_kuro_else41:
L_kuro_endif42:
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1912]
    ldr x0, [sp, #1912]
    cmp x0, #0
    b.le L_kuro_isclass_invalid_t179
    cmp x0, #0x1000
    b.lo L_kuro_isclass_invalid_t179
    ldrb w0, [x0]
    sub w0, w0, #48
    cmp w0, #9
    cset w0, ls
    b L_kuro_isclass_done_t179
L_kuro_isclass_invalid_t179:
    mov x0, #0
L_kuro_isclass_done_t179:
    str x0, [sp, #1920]
    ldr x0, [sp, #1920]
    cbz w0, L_kuro_else43
    adrp x0, _kuro_global_105@PAGE
    add x0, x0, _kuro_global_105@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1936]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1944]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1952]
    ldr x0, [sp, #1952]
    ldr x1, [sp, #1936]
    bl _strcpy
    ldr x0, [sp, #1952]
    ldr x1, [sp, #1944]
    bl _strcat
    ldr x0, [sp, #1952]
    adrp x2, _kuro_global_105@PAGE
    add x2, x2, _kuro_global_105@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1960]
    ldr x0, [sp, #1960]
    adrp x2, _kuro_global_39@PAGE
    add x2, x2, _kuro_global_39@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1968]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1968]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif44
L_kuro_else43:
    mov x0, #0
    str x0, [sp, #1976]
    ldr x0, [sp, #1976]
    adrp x2, _kuro_global_106@PAGE
    add x2, x2, _kuro_global_106@PAGEOFF
    str x0, [x2]
L_kuro_endif44:
    b L_kuro_endif40
L_kuro_else39:
    mov x0, #0
    str x0, [sp, #1984]
    ldr x0, [sp, #1984]
    adrp x2, _kuro_global_106@PAGE
    add x2, x2, _kuro_global_106@PAGEOFF
    str x0, [x2]
L_kuro_endif40:
L_kuro_endif38:
    b L_kuro_while_start34
L_kuro_while_end35:
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1992]
    mov x0, #1
    str x0, [sp, #2000]
    ldr x0, [sp, #1992]
    ldr x1, [sp, #2000]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2008]
    ldr x0, [sp, #2008]
    cbz w0, L_kuro_else45
    adrp x0, L_kuro_data_25@PAGE
    add x0, x0, L_kuro_data_25@PAGEOFF
    str x0, [sp, #2024]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2024]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2032]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2032]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    b L_kuro_endif46
L_kuro_else45:
    adrp x0, L_kuro_data_26@PAGE
    add x0, x0, L_kuro_data_26@PAGEOFF
    str x0, [sp, #2040]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2040]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2048]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2048]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
L_kuro_endif46:
    adrp x0, _kuro_global_105@PAGE
    add x0, x0, _kuro_global_105@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2056]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2056]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    b L_kuro_endif33
L_kuro_else32:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2064]
    ldr x0, [sp, #2064]
    cmp x0, #0
    b.le L_kuro_isclass_invalid_t196
    cmp x0, #0x1000
    b.lo L_kuro_isclass_invalid_t196
    ldrb w0, [x0]
    sub w1, w0, #48
    cmp w1, #9
    cset w1, ls
    sub w2, w0, #65
    cmp w2, #25
    cset w2, ls
    orr w1, w1, w2
    sub w2, w0, #97
    cmp w2, #25
    cset w2, ls
    orr w1, w1, w2
    mov w0, w1
    b L_kuro_isclass_done_t196
L_kuro_isclass_invalid_t196:
    mov x0, #0
L_kuro_isclass_done_t196:
    str x0, [sp, #2072]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2080]
    adrp x0, _kuro_global_220@PAGE
    add x0, x0, _kuro_global_220@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2088]
    ldr x0, [sp, #2080]
    ldr x1, [sp, #2088]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2096]
    ldr x0, [sp, #2072]
    ldr x1, [sp, #2096]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2120]
    ldr x0, [sp, #2120]
    cbz w0, L_kuro_else47
    adrp x0, L_kuro_data_27@PAGE
    add x0, x0, L_kuro_data_27@PAGEOFF
    str x0, [sp, #2128]
    ldr x0, [sp, #2128]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2136]
    ldr x0, [sp, #2136]
    adrp x2, _kuro_global_37@PAGE
    add x2, x2, _kuro_global_37@PAGEOFF
    str x0, [x2]
L_kuro_while_start49:
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2144]
    mov x0, #1
    str x0, [sp, #2152]
    ldr x0, [sp, #2144]
    ldr x1, [sp, #2152]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2160]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2168]
    adrp x0, _kuro_global_211@PAGE
    add x0, x0, _kuro_global_211@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2176]
    ldr x0, [sp, #2168]
    ldr x1, [sp, #2176]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #2184]
    ldr x0, [sp, #2160]
    ldr x1, [sp, #2184]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #2192]
    ldr x0, [sp, #2192]
    cbz w0, L_kuro_while_end50
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2208]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #2208]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #2216]
    ldr x0, [sp, #2216]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2224]
    ldr x0, [sp, #2224]
    adrp x2, _kuro_global_9@PAGE
    add x2, x2, _kuro_global_9@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2232]
    ldr x0, [sp, #2232]
    cmp x0, #0
    b.le L_kuro_isclass_invalid_t214
    cmp x0, #0x1000
    b.lo L_kuro_isclass_invalid_t214
    ldrb w0, [x0]
    sub w1, w0, #48
    cmp w1, #9
    cset w1, ls
    sub w2, w0, #65
    cmp w2, #25
    cset w2, ls
    orr w1, w1, w2
    sub w2, w0, #97
    cmp w2, #25
    cset w2, ls
    orr w1, w1, w2
    mov w0, w1
    b L_kuro_isclass_done_t214
L_kuro_isclass_invalid_t214:
    mov x0, #0
L_kuro_isclass_done_t214:
    str x0, [sp, #2240]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2248]
    adrp x0, _kuro_global_220@PAGE
    add x0, x0, _kuro_global_220@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2256]
    ldr x0, [sp, #2248]
    ldr x1, [sp, #2256]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2264]
    ldr x0, [sp, #2240]
    ldr x1, [sp, #2264]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2272]
    ldr x0, [sp, #2272]
    cbz w0, L_kuro_else52
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2280]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2296]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2304]
    ldr x0, [sp, #2304]
    ldr x1, [sp, #2280]
    bl _strcpy
    ldr x0, [sp, #2304]
    ldr x1, [sp, #2296]
    bl _strcat
    ldr x0, [sp, #2304]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2312]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2312]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif53
L_kuro_else52:
    mov x0, #0
    str x0, [sp, #2320]
    ldr x0, [sp, #2320]
    adrp x2, _kuro_global_37@PAGE
    add x2, x2, _kuro_global_37@PAGEOFF
    str x0, [x2]
L_kuro_endif53:
    b L_kuro_while_start49
L_kuro_while_end50:
    adrp x0, L_kuro_data_28@PAGE
    add x0, x0, L_kuro_data_28@PAGEOFF
    str x0, [sp, #2328]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2328]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2336]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2336]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2344]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2344]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    b L_kuro_endif48
L_kuro_else47:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2352]
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2360]
    ldr x0, [sp, #2352]
    ldr x1, [sp, #2360]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2368]
    ldr x0, [sp, #2368]
    cbz w0, L_kuro_else54
    adrp x0, L_kuro_data_29@PAGE
    add x0, x0, L_kuro_data_29@PAGEOFF
    str x0, [sp, #2384]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2384]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2392]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2392]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2400]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2400]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2408]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2408]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif55
L_kuro_else54:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2416]
    adrp x0, _kuro_global_11@PAGE
    add x0, x0, _kuro_global_11@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2424]
    ldr x0, [sp, #2416]
    ldr x1, [sp, #2424]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2432]
    ldr x0, [sp, #2432]
    cbz w0, L_kuro_else56
    adrp x0, L_kuro_data_30@PAGE
    add x0, x0, L_kuro_data_30@PAGEOFF
    str x0, [sp, #2440]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2440]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2448]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2448]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2456]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2456]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2472]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2472]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif57
L_kuro_else56:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2480]
    adrp x0, _kuro_global_208@PAGE
    add x0, x0, _kuro_global_208@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2488]
    ldr x0, [sp, #2480]
    ldr x1, [sp, #2488]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2496]
    ldr x0, [sp, #2496]
    cbz w0, L_kuro_else58
    adrp x0, L_kuro_data_31@PAGE
    add x0, x0, L_kuro_data_31@PAGEOFF
    str x0, [sp, #2504]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2504]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2512]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2512]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2520]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2520]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2528]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2528]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif59
L_kuro_else58:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2536]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2544]
    ldr x0, [sp, #2536]
    ldr x1, [sp, #2544]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2560]
    ldr x0, [sp, #2560]
    cbz w0, L_kuro_else60
    adrp x0, L_kuro_data_32@PAGE
    add x0, x0, L_kuro_data_32@PAGEOFF
    str x0, [sp, #2568]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2568]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2576]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2576]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2584]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2584]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2592]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2592]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif61
L_kuro_else60:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2600]
    adrp x0, _kuro_global_46@PAGE
    add x0, x0, _kuro_global_46@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2608]
    ldr x0, [sp, #2600]
    ldr x1, [sp, #2608]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2616]
    ldr x0, [sp, #2616]
    cbz w0, L_kuro_else62
    adrp x0, L_kuro_data_33@PAGE
    add x0, x0, L_kuro_data_33@PAGEOFF
    str x0, [sp, #2624]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2624]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2632]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2632]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2648]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2648]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2656]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2656]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif63
L_kuro_else62:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2664]
    adrp x0, _kuro_global_205@PAGE
    add x0, x0, _kuro_global_205@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2672]
    ldr x0, [sp, #2664]
    ldr x1, [sp, #2672]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2680]
    ldr x0, [sp, #2680]
    cbz w0, L_kuro_else64
    adrp x0, L_kuro_data_34@PAGE
    add x0, x0, L_kuro_data_34@PAGEOFF
    str x0, [sp, #2688]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2688]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2696]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2696]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2704]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2704]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2712]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2712]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif65
L_kuro_else64:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2720]
    adrp x0, _kuro_global_0@PAGE
    add x0, x0, _kuro_global_0@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2736]
    ldr x0, [sp, #2720]
    ldr x1, [sp, #2736]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2744]
    ldr x0, [sp, #2744]
    cbz w0, L_kuro_else66
    adrp x0, L_kuro_data_35@PAGE
    add x0, x0, L_kuro_data_35@PAGEOFF
    str x0, [sp, #2752]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2752]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2760]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2760]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2768]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2768]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2776]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2776]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif67
L_kuro_else66:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2784]
    adrp x0, _kuro_global_201@PAGE
    add x0, x0, _kuro_global_201@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2792]
    ldr x0, [sp, #2784]
    ldr x1, [sp, #2792]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2800]
    ldr x0, [sp, #2800]
    cbz w0, L_kuro_else68
    adrp x0, L_kuro_data_36@PAGE
    add x0, x0, L_kuro_data_36@PAGEOFF
    str x0, [sp, #2808]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2808]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2824]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2824]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2832]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2832]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2840]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2840]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif69
L_kuro_else68:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2848]
    adrp x0, _kuro_global_92@PAGE
    add x0, x0, _kuro_global_92@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2856]
    ldr x0, [sp, #2848]
    ldr x1, [sp, #2856]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2864]
    ldr x0, [sp, #2864]
    cbz w0, L_kuro_else70
    adrp x0, L_kuro_data_37@PAGE
    add x0, x0, L_kuro_data_37@PAGEOFF
    str x0, [sp, #2872]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2872]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2880]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2880]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2888]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2888]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2896]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2896]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif71
L_kuro_else70:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2912]
    adrp x0, _kuro_global_212@PAGE
    add x0, x0, _kuro_global_212@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2920]
    ldr x0, [sp, #2912]
    ldr x1, [sp, #2920]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2928]
    ldr x0, [sp, #2928]
    cbz w0, L_kuro_else72
    adrp x0, L_kuro_data_38@PAGE
    add x0, x0, L_kuro_data_38@PAGEOFF
    str x0, [sp, #2936]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2936]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2944]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2944]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2952]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2952]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #2960]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2960]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif73
L_kuro_else72:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2968]
    adrp x0, _kuro_global_209@PAGE
    add x0, x0, _kuro_global_209@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2976]
    ldr x0, [sp, #2968]
    ldr x1, [sp, #2976]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2984]
    ldr x0, [sp, #2984]
    cbz w0, L_kuro_else74
    adrp x0, L_kuro_data_39@PAGE
    add x0, x0, L_kuro_data_39@PAGEOFF
    str x0, [sp, #3008]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3008]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3016]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3016]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3024]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3024]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #3032]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3032]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif75
L_kuro_else74:
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3040]
    adrp x0, _kuro_global_10@PAGE
    add x0, x0, _kuro_global_10@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3048]
    ldr x0, [sp, #3040]
    ldr x1, [sp, #3048]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3056]
    ldr x0, [sp, #3056]
    cbz w0, L_kuro_else76
    adrp x0, L_kuro_data_40@PAGE
    add x0, x0, L_kuro_data_40@PAGEOFF
    str x0, [sp, #3064]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3064]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_219@PAGE
    add x0, x0, _kuro_global_219@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3072]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3072]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3080]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3080]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #3096]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3096]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
    b L_kuro_endif77
L_kuro_else76:
    mov x0, #1
    str x0, [sp, #3104]
    adrp x0, _kuro_global_202@PAGE
    add x0, x0, _kuro_global_202@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3104]
    add x0, x0, x1
    adrp x2, _kuro_global_202@PAGE
    add x2, x2, _kuro_global_202@PAGEOFF
    str x0, [x2]
L_kuro_endif77:
L_kuro_endif75:
L_kuro_endif73:
L_kuro_endif71:
L_kuro_endif69:
L_kuro_endif67:
L_kuro_endif65:
L_kuro_endif63:
L_kuro_endif61:
L_kuro_endif59:
L_kuro_endif57:
L_kuro_endif55:
L_kuro_endif48:
L_kuro_endif33:
L_kuro_endif16:
L_kuro_endif9:
L_kuro_endif5:
    b L_kuro_endif3
L_kuro_else2:
L_kuro_endif3:
    ldr x0, [sp, #520]
    str x0, [sp, #3112]
    mov x0, #1
    str x0, [sp, #3120]
    ldr x0, [sp, #3112]
    ldr x1, [sp, #3120]
    add x0, x0, x1
    str x0, [sp, #3128]
    ldr x0, [sp, #3128]
    str x0, [sp, #520]
    b L_kuro_repeat_start0
L_kuro_repeat_end1:
    ldr x0, [sp, #2640]
    adrp x2, _kuro_global_38@PAGE
    add x2, x2, _kuro_global_38@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3136]
    ldr x0, [sp, #3136]
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_collection_len_7@PAGE
    add x0, x0, _kuro_collection_len_7@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3144]
    ldr x0, [sp, #3144]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3152]
    ldr x0, [sp, #3152]
    adrp x2, _kuro_global_217@PAGE
    add x2, x2, _kuro_global_217@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3160]
    ldr x0, [sp, #3160]
    adrp x2, _kuro_global_144@PAGE
    add x2, x2, _kuro_global_144@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3168]
    ldr x0, [sp, #3168]
    adrp x2, _kuro_global_141@PAGE
    add x2, x2, _kuro_global_141@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseProgram
    str x0, [sp, #3184]
    ldr x0, [sp, #3184]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3192]
    ldr x0, [sp, #3192]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3200]
    ldr x0, [sp, #3200]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerBlock
    str x0, [sp, #3208]
    ldr x0, [sp, #3208]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3216]
    ldr x0, [sp, #3216]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3224]
    ldr x0, [sp, #3224]
    adrp x2, _kuro_global_3@PAGE
    add x2, x2, _kuro_global_3@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_BytecodeStep
    str x0, [sp, #3232]
    ldr x0, [sp, #3232]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3240]
    ldr x0, [sp, #3240]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3248]
    ldr x0, [sp, #3248]
    adrp x2, _kuro_global_14@PAGE
    add x2, x2, _kuro_global_14@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_CompilerRun
    str x0, [sp, #3256]
    ldr x0, [sp, #3256]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_41@PAGE
    add x0, x0, L_kuro_data_41@PAGEOFF
    str x0, [sp, #3272]
    ldr x0, [sp, #3272]
    adrp x2, _kuro_global_98@PAGE
    add x2, x2, _kuro_global_98@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3280]
    ldr x0, [sp, #3280]
    adrp x2, _kuro_global_99@PAGE
    add x2, x2, _kuro_global_99@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3288]
    mov x0, #0
    str x0, [sp, #3296]
    ldr x0, [sp, #3288]
    ldr x1, [sp, #3296]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3304]
    ldr x0, [sp, #3304]
    cbz w0, L_kuro_else78
    adrp x0, _kuro_collection_len_1@PAGE
    add x0, x0, _kuro_collection_len_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3312]
    ldr x0, [sp, #3312]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3320]
    ldr x0, [sp, #3320]
    adrp x2, _kuro_global_99@PAGE
    add x2, x2, _kuro_global_99@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_99@PAGE
    add x0, x0, _kuro_global_99@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3328]
    mov x0, #65536
    str x0, [sp, #3336]
    ldr x0, [sp, #3328]
    ldr x1, [sp, #3336]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #3344]
    ldr x0, [sp, #3344]
    cbz w0, L_kuro_else80
    mov x0, #1
    str x0, [sp, #3360]
    ldr x0, [sp, #3360]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    b L_kuro_endif81
L_kuro_else80:
L_kuro_endif81:
    b L_kuro_endif79
L_kuro_else78:
L_kuro_endif79:
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3368]
    ldr x0, [sp, #3368]
    adrp x2, _kuro_global_207@PAGE
    add x2, x2, _kuro_global_207@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3376]
    mov x0, #0
    str x0, [sp, #3384]
    ldr x0, [sp, #3376]
    ldr x1, [sp, #3384]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3392]
    ldr x0, [sp, #3392]
    cbz w0, L_kuro_else82
    adrp x0, L_kuro_data_42@PAGE
    add x0, x0, L_kuro_data_42@PAGEOFF
    str x0, [sp, #3400]
    ldr x0, [sp, #3400]
    bl _puts
    mov x0, #0
    str x0, [sp, #3408]
    ldr x0, [sp, #3408]
    adrp x2, _kuro_global_100@PAGE
    add x2, x2, _kuro_global_100@PAGEOFF
    str x0, [x2]
L_kuro_while_start84:
    adrp x0, _kuro_global_100@PAGE
    add x0, x0, _kuro_global_100@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3416]
    adrp x0, _kuro_global_99@PAGE
    add x0, x0, _kuro_global_99@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3424]
    ldr x0, [sp, #3416]
    ldr x1, [sp, #3424]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #3432]
    ldr x0, [sp, #3432]
    cbz w0, L_kuro_while_end85
    adrp x0, _kuro_global_100@PAGE
    add x0, x0, _kuro_global_100@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3448]
    ldr x1, [sp, #3448]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #3456]
    ldr x0, [sp, #3456]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3464]
    ldr x0, [sp, #3464]
    adrp x2, _kuro_global_102@PAGE
    add x2, x2, _kuro_global_102@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_102@PAGE
    add x0, x0, _kuro_global_102@PAGEOFF
    ldr x0, [x0]
    cbz x0, L_kuro_length_zero_t353
    bl _strlen
    b L_kuro_length_done_t353
L_kuro_length_zero_t353:
    mov x0, #0
L_kuro_length_done_t353:
    str x0, [sp, #3472]
    ldr x0, [sp, #3472]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3480]
    ldr x0, [sp, #3480]
    adrp x2, _kuro_global_101@PAGE
    add x2, x2, _kuro_global_101@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_43@PAGE
    add x0, x0, L_kuro_data_43@PAGEOFF
    str x0, [sp, #3488]
    ldr x0, [sp, #3488]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_101@PAGE
    add x0, x0, _kuro_global_101@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3496]
    mov x0, #0
    str x0, [sp, #3504]
    ldr x0, [sp, #3496]
    ldr x1, [sp, #3504]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3512]
    ldr x0, [sp, #3512]
    cbz w0, L_kuro_else87
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3520]
    adrp x0, L_kuro_data_44@PAGE
    add x0, x0, L_kuro_data_44@PAGEOFF
    str x0, [sp, #3536]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3544]
    ldr x0, [sp, #3544]
    ldr x1, [sp, #3520]
    bl _strcpy
    ldr x0, [sp, #3544]
    ldr x1, [sp, #3536]
    bl _strcat
    ldr x0, [sp, #3544]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
    b L_kuro_endif88
L_kuro_else87:
    adrp x0, _kuro_global_102@PAGE
    add x0, x0, _kuro_global_102@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3552]
    adrp x0, L_kuro_data_45@PAGE
    add x0, x0, L_kuro_data_45@PAGEOFF
    str x0, [sp, #3560]
    ldr x0, [sp, #3552]
    ldr x1, [sp, #3560]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3568]
    ldr x0, [sp, #3568]
    cbz w0, L_kuro_else89
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3576]
    adrp x0, L_kuro_data_46@PAGE
    add x0, x0, L_kuro_data_46@PAGEOFF
    str x0, [sp, #3584]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3592]
    ldr x0, [sp, #3592]
    ldr x1, [sp, #3576]
    bl _strcpy
    ldr x0, [sp, #3592]
    ldr x1, [sp, #3584]
    bl _strcat
    ldr x0, [sp, #3592]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_101@PAGE
    add x0, x0, _kuro_global_101@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3600]
    ldr x0, [sp, #3600]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    b L_kuro_endif90
L_kuro_else89:
L_kuro_endif90:
L_kuro_endif88:
    mov x0, #0
    str x0, [sp, #3608]
    ldr x0, [sp, #3608]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
L_kuro_while_start91:
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3624]
    adrp x0, _kuro_global_101@PAGE
    add x0, x0, _kuro_global_101@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3632]
    ldr x0, [sp, #3624]
    ldr x1, [sp, #3632]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #3640]
    ldr x0, [sp, #3640]
    cbz w0, L_kuro_while_end92
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3648]
    adrp x2, _kuro_global_102@PAGE
    add x2, x2, _kuro_global_102@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #3648]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #3656]
    ldr x0, [sp, #3656]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3664]
    ldr x0, [sp, #3664]
    adrp x2, _kuro_global_96@PAGE
    add x2, x2, _kuro_global_96@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_96@PAGE
    add x0, x0, _kuro_global_96@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3672]
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3680]
    ldr x0, [sp, #3672]
    ldr x1, [sp, #3680]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3688]
    ldr x0, [sp, #3688]
    cbz w0, L_kuro_else94
    adrp x0, _kuro_global_97@PAGE
    add x0, x0, _kuro_global_97@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3696]
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3712]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3720]
    ldr x0, [sp, #3720]
    ldr x1, [sp, #3696]
    bl _strcpy
    ldr x0, [sp, #3720]
    ldr x1, [sp, #3712]
    bl _strcat
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3728]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3736]
    ldr x0, [sp, #3736]
    ldr x1, [sp, #3720]
    bl _strcpy
    ldr x0, [sp, #3736]
    ldr x1, [sp, #3728]
    bl _strcat
    ldr x0, [sp, #3736]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
    b L_kuro_endif95
L_kuro_else94:
    adrp x0, _kuro_global_96@PAGE
    add x0, x0, _kuro_global_96@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3744]
    adrp x0, L_kuro_data_47@PAGE
    add x0, x0, L_kuro_data_47@PAGEOFF
    str x0, [sp, #3752]
    ldr x0, [sp, #3744]
    ldr x1, [sp, #3752]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3760]
    ldr x0, [sp, #3760]
    cbz w0, L_kuro_else96
    adrp x0, _kuro_global_97@PAGE
    add x0, x0, _kuro_global_97@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3768]
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3776]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3784]
    ldr x0, [sp, #3784]
    ldr x1, [sp, #3768]
    bl _strcpy
    ldr x0, [sp, #3784]
    ldr x1, [sp, #3776]
    bl _strcat
    adrp x0, L_kuro_data_48@PAGE
    add x0, x0, L_kuro_data_48@PAGEOFF
    str x0, [sp, #3800]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3808]
    ldr x0, [sp, #3808]
    ldr x1, [sp, #3784]
    bl _strcpy
    ldr x0, [sp, #3808]
    ldr x1, [sp, #3800]
    bl _strcat
    ldr x0, [sp, #3808]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
    b L_kuro_endif97
L_kuro_else96:
    adrp x0, _kuro_global_96@PAGE
    add x0, x0, _kuro_global_96@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3816]
    adrp x0, L_kuro_data_49@PAGE
    add x0, x0, L_kuro_data_49@PAGEOFF
    str x0, [sp, #3824]
    ldr x0, [sp, #3816]
    ldr x1, [sp, #3824]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3832]
    ldr x0, [sp, #3832]
    cbz w0, L_kuro_else98
    adrp x0, _kuro_global_97@PAGE
    add x0, x0, _kuro_global_97@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3840]
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3848]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3856]
    ldr x0, [sp, #3856]
    ldr x1, [sp, #3840]
    bl _strcpy
    ldr x0, [sp, #3856]
    ldr x1, [sp, #3848]
    bl _strcat
    adrp x0, L_kuro_data_50@PAGE
    add x0, x0, L_kuro_data_50@PAGEOFF
    str x0, [sp, #3864]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3872]
    ldr x0, [sp, #3872]
    ldr x1, [sp, #3856]
    bl _strcpy
    ldr x0, [sp, #3872]
    ldr x1, [sp, #3864]
    bl _strcat
    ldr x0, [sp, #3872]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
    b L_kuro_endif99
L_kuro_else98:
    adrp x0, _kuro_global_96@PAGE
    add x0, x0, _kuro_global_96@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3896]
    adrp x0, L_kuro_data_51@PAGE
    add x0, x0, L_kuro_data_51@PAGEOFF
    str x0, [sp, #3904]
    ldr x0, [sp, #3896]
    ldr x1, [sp, #3904]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3912]
    ldr x0, [sp, #3912]
    cbz w0, L_kuro_else100
    adrp x0, _kuro_global_97@PAGE
    add x0, x0, _kuro_global_97@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3920]
    adrp x0, _kuro_global_98@PAGE
    add x0, x0, _kuro_global_98@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3928]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3936]
    ldr x0, [sp, #3936]
    ldr x1, [sp, #3920]
    bl _strcpy
    ldr x0, [sp, #3936]
    ldr x1, [sp, #3928]
    bl _strcat
    adrp x0, L_kuro_data_52@PAGE
    add x0, x0, L_kuro_data_52@PAGEOFF
    str x0, [sp, #3944]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3952]
    ldr x0, [sp, #3952]
    ldr x1, [sp, #3936]
    bl _strcpy
    ldr x0, [sp, #3952]
    ldr x1, [sp, #3944]
    bl _strcat
    ldr x0, [sp, #3952]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
    b L_kuro_endif101
L_kuro_else100:
    adrp x0, _kuro_global_97@PAGE
    add x0, x0, _kuro_global_97@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3960]
    adrp x0, _kuro_global_96@PAGE
    add x0, x0, _kuro_global_96@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3968]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3984]
    ldr x0, [sp, #3984]
    ldr x1, [sp, #3960]
    bl _strcpy
    ldr x0, [sp, #3984]
    ldr x1, [sp, #3968]
    bl _strcat
    ldr x0, [sp, #3984]
    adrp x2, _kuro_global_97@PAGE
    add x2, x2, _kuro_global_97@PAGEOFF
    str x0, [x2]
L_kuro_endif101:
L_kuro_endif99:
L_kuro_endif97:
L_kuro_endif95:
    mov x0, #1
    str x0, [sp, #3992]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3992]
    add x0, x0, x1
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    b L_kuro_while_start91
L_kuro_while_end92:
    adrp x0, _kuro_global_97@PAGE
    add x0, x0, _kuro_global_97@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4000]
    ldr x0, [sp, #4000]
    bl _puts
    mov x0, #1
    str x0, [sp, #4008]
    adrp x0, _kuro_global_100@PAGE
    add x0, x0, _kuro_global_100@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4008]
    add x0, x0, x1
    adrp x2, _kuro_global_100@PAGE
    add x2, x2, _kuro_global_100@PAGEOFF
    str x0, [x2]
    b L_kuro_while_start84
L_kuro_while_end85:
    b L_kuro_endif83
L_kuro_else82:
    adrp x0, L_kuro_data_53@PAGE
    add x0, x0, L_kuro_data_53@PAGEOFF
    str x0, [sp, #4016]
    ldr x0, [sp, #4016]
    bl _puts
L_kuro_endif83:
    mov x15, #4624
    add sp, sp, x15
    adrp x0, _kuro_global_207@PAGE
    add x0, x0, _kuro_global_207@PAGEOFF
    ldr x0, [x0]
    ldp x19, x20, [sp], #16
    ldp x29, x30, [sp], #16
    ret
L_kuro_runtime_error:
    mov w0, #1
    mov x15, #4624
    add sp, sp, x15
    ldp x19, x20, [sp], #16
    ldp x29, x30, [sp], #16
    ret
.section __TEXT,__cstring
.section __TEXT,__text
_kuro_fn_ComputeLineCol:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #272
    sub sp, sp, x15
    str x0, [sp, #48]
    mov x0, #0
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    str x0, [sp, #16]
    mov x0, #1
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    str x0, [sp, #24]
    mov x0, #1
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    str x0, [sp, #8]
L_kuro_fn_ComputeLineCol_while_start0:
    ldr x0, [sp, #16]
    str x0, [sp, #200]
    ldr x0, [sp, #48]
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    cbz w0, L_kuro_fn_ComputeLineCol_while_end1
    ldr x0, [sp, #16]
    str x0, [sp, #224]
    adrp x2, _kuro_global_210@PAGE
    add x2, x2, _kuro_global_210@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #224]
    add x2, x2, x1
    ldrb w0, [x2]
    adrp x3, _kuro_char_heap_cursor@PAGE
    add x3, x3, _kuro_char_heap_cursor@PAGEOFF
    ldr x1, [x3]
    cmp x1, #512, lsl #12
    b.hs L_kuro_collection_overflow
    adrp x2, _kuro_char_heap@PAGE
    add x2, x2, _kuro_char_heap@PAGEOFF
    add x2, x2, x1
    strb w0, [x2]
    strb wzr, [x2, #1]
    add x1, x1, #2
    str x1, [x3]
    mov x0, x2
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #248]
    adrp x0, L_kuro_data_54@PAGE
    add x0, x0, L_kuro_data_54@PAGEOFF
    str x0, [sp, #96]
    ldr x0, [sp, #248]
    ldr x1, [sp, #96]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    cbz w0, L_kuro_fn_ComputeLineCol_else3
    ldr x0, [sp, #24]
    str x0, [sp, #112]
    mov x0, #1
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    add x0, x0, x1
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #24]
    mov x0, #1
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    str x0, [sp, #8]
    b L_kuro_fn_ComputeLineCol_endif4
L_kuro_fn_ComputeLineCol_else3:
    ldr x0, [sp, #8]
    str x0, [sp, #144]
    mov x0, #1
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    add x0, x0, x1
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    str x0, [sp, #8]
L_kuro_fn_ComputeLineCol_endif4:
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #16]
    ldr x1, [sp, #168]
    add x0, x0, x1
    str x0, [sp, #16]
    b L_kuro_fn_ComputeLineCol_while_start0
L_kuro_fn_ComputeLineCol_while_end1:
    ldr x0, [sp, #24]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_22@PAGE
    add x2, x2, _kuro_global_22@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_21@PAGE
    add x2, x2, _kuro_global_21@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #272
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_CurDiagPos:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #144
    sub sp, sp, x15
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #48]
    adrp x0, _kuro_global_217@PAGE
    add x0, x0, _kuro_global_217@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    ldr x0, [sp, #48]
    ldr x1, [sp, #56]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #80]
    mov x0, #1
    str x0, [sp, #88]
    ldr x0, [sp, #80]
    ldr x1, [sp, #88]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    cbz w0, L_kuro_fn_CurDiagPos_else0
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    ldr x1, [sp, #104]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    mov x15, #144
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_CurDiagPos_endif1
L_kuro_fn_CurDiagPos_else0:
    adrp x0, _kuro_global_210@PAGE
    add x0, x0, _kuro_global_210@PAGEOFF
    ldr x0, [x0]
    cbz x0, L_kuro_fn_CurDiagPos_length_zero_t9
    bl _strlen
    b L_kuro_fn_CurDiagPos_length_done_t9
L_kuro_fn_CurDiagPos_length_zero_t9:
    mov x0, #0
L_kuro_fn_CurDiagPos_length_done_t9:
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    mov x15, #144
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_CurDiagPos_endif1:
    mov x0, #0
    mov x15, #144
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_RecordDiag:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #72]
    bl _kuro_fn_CurDiagPos
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    bl _kuro_fn_ComputeLineCol
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #0]
    str x0, [sp, #136]
    adrp x1, _kuro_collection_len_2@PAGE
    add x1, x1, _kuro_collection_len_2@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_2@PAGE
    add x2, x2, _kuro_collection_2@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #136]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_2@PAGE
    add x2, x2, _kuro_collection_len_2@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_22@PAGE
    add x0, x0, _kuro_global_22@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    adrp x1, _kuro_collection_len_4@PAGE
    add x1, x1, _kuro_collection_len_4@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #144]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_4@PAGE
    add x2, x2, _kuro_collection_len_4@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    adrp x1, _kuro_collection_len_3@PAGE
    add x1, x1, _kuro_collection_len_3@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #152]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_3@PAGE
    add x2, x2, _kuro_collection_len_3@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #72]
    str x0, [sp, #160]
    adrp x1, _kuro_collection_len_5@PAGE
    add x1, x1, _kuro_collection_len_5@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #160]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_5@PAGE
    add x2, x2, _kuro_collection_len_5@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    adrp x2, _kuro_global_144@PAGE
    add x2, x2, _kuro_global_144@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_PeekKind:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    str x0, [sp, #0]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    ldr x0, [sp, #0]
    str x0, [sp, #72]
    ldr x0, [sp, #64]
    ldr x1, [sp, #72]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #112]
    adrp x0, _kuro_global_217@PAGE
    add x0, x0, _kuro_global_217@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #136]
    mov x0, #1
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_PeekKind_else0
    ldr x0, [sp, #16]
    str x0, [sp, #160]
    ldr x1, [sp, #160]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_PeekKind_endif1
L_kuro_fn_PeekKind_else0:
    adrp x0, L_kuro_data_55@PAGE
    add x0, x0, L_kuro_data_55@PAGEOFF
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_PeekKind_endif1:
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_PeekValue:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    str x0, [sp, #0]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    ldr x0, [sp, #0]
    str x0, [sp, #72]
    ldr x0, [sp, #64]
    ldr x1, [sp, #72]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #112]
    adrp x0, _kuro_global_217@PAGE
    add x0, x0, _kuro_global_217@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #136]
    mov x0, #1
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_PeekValue_else0
    ldr x0, [sp, #16]
    str x0, [sp, #160]
    ldr x1, [sp, #160]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_PeekValue_endif1
L_kuro_fn_PeekValue_else0:
    adrp x0, L_kuro_data_56@PAGE
    add x0, x0, L_kuro_data_56@PAGEOFF
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_PeekValue_endif1:
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_CurKind:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #48
    sub sp, sp, x15
    mov x0, #0
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    bl _kuro_fn_PeekKind
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_CurValue:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #48
    sub sp, sp, x15
    mov x0, #0
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    bl _kuro_fn_PeekValue
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_IsWord:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #192
    sub sp, sp, x15
    str x0, [sp, #16]
    bl _kuro_fn_CurKind
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #120]
    adrp x0, L_kuro_data_57@PAGE
    add x0, x0, L_kuro_data_57@PAGEOFF
    str x0, [sp, #128]
    ldr x0, [sp, #120]
    ldr x1, [sp, #128]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    cbz w0, L_kuro_fn_IsWord_else0
    bl _kuro_fn_CurValue
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #160]
    ldr x0, [sp, #16]
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    cbz w0, L_kuro_fn_IsWord_else2
    mov x0, #1
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_IsWord_endif3
L_kuro_fn_IsWord_else2:
    mov x0, #0
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_IsWord_endif3:
    b L_kuro_fn_IsWord_endif1
L_kuro_fn_IsWord_else0:
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_IsWord_endif1:
    mov x0, #0
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ExpectKind:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #192
    sub sp, sp, x15
    str x0, [sp, #24]
    bl _kuro_fn_CurKind
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #120]
    ldr x0, [sp, #24]
    str x0, [sp, #128]
    ldr x0, [sp, #120]
    ldr x1, [sp, #128]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    cbz w0, L_kuro_fn_ExpectKind_else0
    mov x0, #1
    str x0, [sp, #144]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #144]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ExpectKind_endif1
L_kuro_fn_ExpectKind_else0:
    adrp x0, L_kuro_data_58@PAGE
    add x0, x0, L_kuro_data_58@PAGEOFF
    str x0, [sp, #160]
    ldr x0, [sp, #24]
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    ldr x1, [sp, #160]
    bl _strcpy
    ldr x0, [sp, #176]
    ldr x1, [sp, #168]
    bl _strcat
    ldr x0, [sp, #176]
    str x0, [sp, #16]
    adrp x0, L_kuro_data_59@PAGE
    add x0, x0, L_kuro_data_59@PAGEOFF
    str x0, [sp, #88]
    ldr x0, [sp, #16]
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    bl _kuro_fn_RecordDiag
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_ExpectKind_endif1:
    mov x0, #0
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ExpectWord:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #192
    sub sp, sp, x15
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    bl _kuro_fn_IsWord
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #136]
    mov x0, #1
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_ExpectWord_else0
    mov x0, #1
    str x0, [sp, #160]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #160]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ExpectWord_endif1
L_kuro_fn_ExpectWord_else0:
    adrp x0, L_kuro_data_60@PAGE
    add x0, x0, L_kuro_data_60@PAGEOFF
    str x0, [sp, #176]
    ldr x0, [sp, #16]
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    ldr x1, [sp, #176]
    bl _strcpy
    ldr x0, [sp, #88]
    ldr x1, [sp, #184]
    bl _strcat
    ldr x0, [sp, #88]
    str x0, [sp, #0]
    adrp x0, L_kuro_data_61@PAGE
    add x0, x0, L_kuro_data_61@PAGEOFF
    str x0, [sp, #96]
    ldr x0, [sp, #0]
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    bl _kuro_fn_RecordDiag
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_ExpectWord_endif1:
    mov x0, #0
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ExpectIdent:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #112]
    adrp x0, L_kuro_data_62@PAGE
    add x0, x0, L_kuro_data_62@PAGEOFF
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    cbz w0, L_kuro_fn_ExpectIdent_else0
    bl _kuro_fn_CurValue
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #24]
    mov x0, #1
    str x0, [sp, #152]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #152]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #24]
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ExpectIdent_endif1
L_kuro_fn_ExpectIdent_else0:
    adrp x0, L_kuro_data_63@PAGE
    add x0, x0, L_kuro_data_63@PAGEOFF
    str x0, [sp, #168]
    adrp x0, L_kuro_data_64@PAGE
    add x0, x0, L_kuro_data_64@PAGEOFF
    str x0, [sp, #88]
    ldr x0, [sp, #168]
    ldr x1, [sp, #88]
    bl _kuro_fn_RecordDiag
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_65@PAGE
    add x0, x0, L_kuro_data_65@PAGEOFF
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_ExpectIdent_endif1:
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseAtom:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #784
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #304]
    adrp x0, L_kuro_data_66@PAGE
    add x0, x0, L_kuro_data_66@PAGEOFF
    str x0, [sp, #392]
    ldr x0, [sp, #304]
    ldr x1, [sp, #392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #480]
    ldr x0, [sp, #480]
    cbz w0, L_kuro_fn_ParseAtom_else0
    mov x0, #1
    str x0, [sp, #568]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #568]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #656]
    ldr x0, [sp, #656]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_67@PAGE
    add x0, x0, L_kuro_data_67@PAGEOFF
    str x0, [sp, #744]
    ldr x0, [sp, #744]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #760]
    ldr x0, [sp, #760]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #768]
    ldr x0, [sp, #768]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseAtom_endif1
L_kuro_fn_ParseAtom_else0:
L_kuro_fn_ParseAtom_endif1:
    ldr x0, [sp, #48]
    str x0, [sp, #224]
    adrp x0, L_kuro_data_68@PAGE
    add x0, x0, L_kuro_data_68@PAGEOFF
    str x0, [sp, #232]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_ParseAtom_else2
    bl _kuro_fn_CurValue
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #56]
    mov x0, #1
    str x0, [sp, #264]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #264]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_69@PAGE
    add x0, x0, L_kuro_data_69@PAGEOFF
    str x0, [sp, #272]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #272]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #56]
    str x0, [sp, #280]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #280]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseAtom_endif3
L_kuro_fn_ParseAtom_else2:
L_kuro_fn_ParseAtom_endif3:
    ldr x0, [sp, #48]
    str x0, [sp, #296]
    adrp x0, L_kuro_data_70@PAGE
    add x0, x0, L_kuro_data_70@PAGEOFF
    str x0, [sp, #312]
    ldr x0, [sp, #296]
    ldr x1, [sp, #312]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    cbz w0, L_kuro_fn_ParseAtom_else4
    bl _kuro_fn_CurValue
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    str x0, [sp, #56]
    mov x0, #1
    str x0, [sp, #344]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #344]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_71@PAGE
    add x0, x0, L_kuro_data_71@PAGEOFF
    str x0, [sp, #352]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #352]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #56]
    str x0, [sp, #360]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #360]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #368]
    ldr x0, [sp, #368]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseAtom_endif5
L_kuro_fn_ParseAtom_else4:
L_kuro_fn_ParseAtom_endif5:
    ldr x0, [sp, #48]
    str x0, [sp, #376]
    adrp x0, L_kuro_data_72@PAGE
    add x0, x0, L_kuro_data_72@PAGEOFF
    str x0, [sp, #384]
    ldr x0, [sp, #376]
    ldr x1, [sp, #384]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    cbz w0, L_kuro_fn_ParseAtom_else6
    bl _kuro_fn_CurValue
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    str x0, [sp, #56]
    mov x0, #1
    str x0, [sp, #424]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #424]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_73@PAGE
    add x0, x0, L_kuro_data_73@PAGEOFF
    str x0, [sp, #432]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #432]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #56]
    str x0, [sp, #440]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #440]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #448]
    ldr x0, [sp, #448]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseAtom_endif7
L_kuro_fn_ParseAtom_else6:
L_kuro_fn_ParseAtom_endif7:
    ldr x0, [sp, #48]
    str x0, [sp, #456]
    adrp x0, L_kuro_data_74@PAGE
    add x0, x0, L_kuro_data_74@PAGEOFF
    str x0, [sp, #464]
    ldr x0, [sp, #456]
    ldr x1, [sp, #464]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #472]
    ldr x0, [sp, #472]
    cbz w0, L_kuro_fn_ParseAtom_else8
    mov x0, #1
    str x0, [sp, #488]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #488]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #504]
    ldr x0, [sp, #504]
    str x0, [sp, #56]
    adrp x0, L_kuro_data_75@PAGE
    add x0, x0, L_kuro_data_75@PAGEOFF
    str x0, [sp, #512]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #512]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_76@PAGE
    add x0, x0, L_kuro_data_76@PAGEOFF
    str x0, [sp, #520]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #520]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #56]
    str x0, [sp, #528]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #528]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseAtom_endif9
L_kuro_fn_ParseAtom_else8:
L_kuro_fn_ParseAtom_endif9:
    ldr x0, [sp, #48]
    str x0, [sp, #544]
    adrp x0, L_kuro_data_77@PAGE
    add x0, x0, L_kuro_data_77@PAGEOFF
    str x0, [sp, #552]
    ldr x0, [sp, #544]
    ldr x1, [sp, #552]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #560]
    ldr x0, [sp, #560]
    cbz w0, L_kuro_fn_ParseAtom_else10
    mov x0, #1
    str x0, [sp, #576]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #576]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_78@PAGE
    add x0, x0, L_kuro_data_78@PAGEOFF
    str x0, [sp, #584]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #584]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_79@PAGE
    add x0, x0, L_kuro_data_79@PAGEOFF
    str x0, [sp, #592]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #592]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseAtom
    str x0, [sp, #600]
    ldr x0, [sp, #600]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_80@PAGE
    add x0, x0, L_kuro_data_80@PAGEOFF
    str x0, [sp, #608]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #608]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_81@PAGE
    add x0, x0, L_kuro_data_81@PAGEOFF
    str x0, [sp, #616]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #616]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #624]
    ldr x0, [sp, #624]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseAtom_endif11
L_kuro_fn_ParseAtom_else10:
L_kuro_fn_ParseAtom_endif11:
    ldr x0, [sp, #48]
    str x0, [sp, #632]
    adrp x0, L_kuro_data_82@PAGE
    add x0, x0, L_kuro_data_82@PAGEOFF
    str x0, [sp, #640]
    ldr x0, [sp, #632]
    ldr x1, [sp, #640]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #648]
    ldr x0, [sp, #648]
    cbz w0, L_kuro_fn_ParseAtom_else12
    bl _kuro_fn_CurValue
    str x0, [sp, #664]
    ldr x0, [sp, #664]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #672]
    ldr x0, [sp, #672]
    str x0, [sp, #56]
    mov x0, #1
    str x0, [sp, #680]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #680]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_83@PAGE
    add x0, x0, L_kuro_data_83@PAGEOFF
    str x0, [sp, #688]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #688]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_84@PAGE
    add x0, x0, L_kuro_data_84@PAGEOFF
    str x0, [sp, #696]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #696]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #56]
    str x0, [sp, #704]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #704]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #712]
    ldr x0, [sp, #712]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseAtom_endif13
L_kuro_fn_ParseAtom_else12:
L_kuro_fn_ParseAtom_endif13:
    adrp x0, L_kuro_data_85@PAGE
    add x0, x0, L_kuro_data_85@PAGEOFF
    str x0, [sp, #720]
    adrp x0, L_kuro_data_86@PAGE
    add x0, x0, L_kuro_data_86@PAGEOFF
    str x0, [sp, #728]
    ldr x0, [sp, #720]
    ldr x1, [sp, #728]
    bl _kuro_fn_RecordDiag
    str x0, [sp, #736]
    ldr x0, [sp, #736]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #752]
    ldr x0, [sp, #752]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseFactor:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #48
    sub sp, sp, x15
    bl _kuro_fn_ParseAtom
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseFactorTail
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseFactorTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #304
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #216]
    adrp x0, L_kuro_data_87@PAGE
    add x0, x0, L_kuro_data_87@PAGEOFF
    str x0, [sp, #240]
    ldr x0, [sp, #216]
    ldr x1, [sp, #240]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #248]
    ldr x0, [sp, #32]
    str x0, [sp, #256]
    adrp x0, L_kuro_data_88@PAGE
    add x0, x0, L_kuro_data_88@PAGEOFF
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #272]
    ldr x0, [sp, #248]
    ldr x1, [sp, #272]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    cbz w0, L_kuro_fn_ParseFactorTail_else0
    adrp x0, L_kuro_data_89@PAGE
    add x0, x0, L_kuro_data_89@PAGEOFF
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    str x0, [sp, #40]
    ldr x0, [sp, #32]
    str x0, [sp, #136]
    adrp x0, L_kuro_data_90@PAGE
    add x0, x0, L_kuro_data_90@PAGEOFF
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_ParseFactorTail_else2
    adrp x0, L_kuro_data_91@PAGE
    add x0, x0, L_kuro_data_91@PAGEOFF
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    str x0, [sp, #40]
    b L_kuro_fn_ParseFactorTail_endif3
L_kuro_fn_ParseFactorTail_else2:
L_kuro_fn_ParseFactorTail_endif3:
    mov x0, #1
    str x0, [sp, #168]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #168]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseAtom
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_92@PAGE
    add x0, x0, L_kuro_data_92@PAGEOFF
    str x0, [sp, #184]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #184]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #40]
    str x0, [sp, #192]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #192]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    mov x0, #0
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_ParseFactorTail_else4
    bl _kuro_fn_ParseFactorTail
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseFactorTail_endif5
L_kuro_fn_ParseFactorTail_else4:
L_kuro_fn_ParseFactorTail_endif5:
    b L_kuro_fn_ParseFactorTail_endif1
L_kuro_fn_ParseFactorTail_else0:
L_kuro_fn_ParseFactorTail_endif1:
    mov x0, #0
    mov x15, #304
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseTerm:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #48
    sub sp, sp, x15
    bl _kuro_fn_ParseFactor
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseTermTail
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseTermTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #304
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #216]
    adrp x0, L_kuro_data_93@PAGE
    add x0, x0, L_kuro_data_93@PAGEOFF
    str x0, [sp, #240]
    ldr x0, [sp, #216]
    ldr x1, [sp, #240]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #248]
    ldr x0, [sp, #40]
    str x0, [sp, #256]
    adrp x0, L_kuro_data_94@PAGE
    add x0, x0, L_kuro_data_94@PAGEOFF
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #272]
    ldr x0, [sp, #248]
    ldr x1, [sp, #272]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    cbz w0, L_kuro_fn_ParseTermTail_else0
    adrp x0, L_kuro_data_95@PAGE
    add x0, x0, L_kuro_data_95@PAGEOFF
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    str x0, [sp, #48]
    ldr x0, [sp, #40]
    str x0, [sp, #136]
    adrp x0, L_kuro_data_96@PAGE
    add x0, x0, L_kuro_data_96@PAGEOFF
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_ParseTermTail_else2
    adrp x0, L_kuro_data_97@PAGE
    add x0, x0, L_kuro_data_97@PAGEOFF
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    str x0, [sp, #48]
    b L_kuro_fn_ParseTermTail_endif3
L_kuro_fn_ParseTermTail_else2:
L_kuro_fn_ParseTermTail_endif3:
    mov x0, #1
    str x0, [sp, #168]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #168]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseFactor
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_98@PAGE
    add x0, x0, L_kuro_data_98@PAGEOFF
    str x0, [sp, #184]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #184]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #48]
    str x0, [sp, #192]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #192]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    mov x0, #0
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_ParseTermTail_else4
    bl _kuro_fn_ParseTermTail
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseTermTail_endif5
L_kuro_fn_ParseTermTail_else4:
L_kuro_fn_ParseTermTail_endif5:
    b L_kuro_fn_ParseTermTail_endif1
L_kuro_fn_ParseTermTail_else0:
L_kuro_fn_ParseTermTail_endif1:
    mov x0, #0
    mov x15, #304
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseExpr:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #128
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #48]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #48]
    add x0, x0, x1
    adrp x2, _kuro_global_141@PAGE
    add x2, x2, _kuro_global_141@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseTerm
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #64]
    mov x0, #1
    str x0, [sp, #72]
    ldr x0, [sp, #64]
    ldr x1, [sp, #72]
    sub x0, x0, x1
    str x0, [sp, #80]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #80]
    add x0, x0, x1
    adrp x2, _kuro_global_141@PAGE
    add x2, x2, _kuro_global_141@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    mov x0, #0
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    cbz w0, L_kuro_fn_ParseExpr_else0
    adrp x0, L_kuro_data_99@PAGE
    add x0, x0, L_kuro_data_99@PAGEOFF
    str x0, [sp, #112]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #112]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_ParseExpr_endif1
L_kuro_fn_ParseExpr_else0:
L_kuro_fn_ParseExpr_endif1:
    mov x0, #0
    mov x15, #128
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseComparisonOp:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #1440
    sub sp, sp, x15
    adrp x0, L_kuro_data_100@PAGE
    add x0, x0, L_kuro_data_100@PAGEOFF
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    bl _kuro_fn_IsWord
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #720]
    ldr x0, [sp, #720]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #808]
    mov x0, #1
    str x0, [sp, #896]
    ldr x0, [sp, #808]
    ldr x1, [sp, #896]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #984]
    ldr x0, [sp, #984]
    cbz w0, L_kuro_fn_ParseComparisonOp_else0
    mov x0, #1
    str x0, [sp, #1072]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1072]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_101@PAGE
    add x0, x0, L_kuro_data_101@PAGEOFF
    str x0, [sp, #1160]
    ldr x0, [sp, #1160]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #1248]
    ldr x0, [sp, #1248]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_102@PAGE
    add x0, x0, L_kuro_data_102@PAGEOFF
    str x0, [sp, #1336]
    ldr x0, [sp, #1336]
    bl _kuro_fn_IsWord
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #504]
    ldr x0, [sp, #504]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #592]
    mov x0, #1
    str x0, [sp, #664]
    ldr x0, [sp, #592]
    ldr x1, [sp, #664]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #672]
    ldr x0, [sp, #672]
    cbz w0, L_kuro_fn_ParseComparisonOp_else2
    mov x0, #1
    str x0, [sp, #680]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #680]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_103@PAGE
    add x0, x0, L_kuro_data_103@PAGEOFF
    str x0, [sp, #688]
    ldr x0, [sp, #688]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #696]
    ldr x0, [sp, #696]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_104@PAGE
    add x0, x0, L_kuro_data_104@PAGEOFF
    str x0, [sp, #704]
    ldr x0, [sp, #704]
    bl _kuro_fn_IsWord
    str x0, [sp, #712]
    ldr x0, [sp, #712]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #728]
    ldr x0, [sp, #728]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #736]
    mov x0, #1
    str x0, [sp, #744]
    ldr x0, [sp, #736]
    ldr x1, [sp, #744]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #752]
    ldr x0, [sp, #752]
    cbz w0, L_kuro_fn_ParseComparisonOp_else4
    mov x0, #1
    str x0, [sp, #760]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #760]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseComparisonOp_endif5
L_kuro_fn_ParseComparisonOp_else4:
L_kuro_fn_ParseComparisonOp_endif5:
    adrp x0, L_kuro_data_105@PAGE
    add x0, x0, L_kuro_data_105@PAGEOFF
    str x0, [sp, #768]
    ldr x0, [sp, #768]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseComparisonOp_endif3
L_kuro_fn_ParseComparisonOp_else2:
    adrp x0, L_kuro_data_106@PAGE
    add x0, x0, L_kuro_data_106@PAGEOFF
    str x0, [sp, #776]
    ldr x0, [sp, #776]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_ParseComparisonOp_endif3:
    b L_kuro_fn_ParseComparisonOp_endif1
L_kuro_fn_ParseComparisonOp_else0:
L_kuro_fn_ParseComparisonOp_endif1:
    adrp x0, L_kuro_data_107@PAGE
    add x0, x0, L_kuro_data_107@PAGEOFF
    str x0, [sp, #784]
    ldr x0, [sp, #784]
    bl _kuro_fn_IsWord
    str x0, [sp, #792]
    ldr x0, [sp, #792]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #800]
    ldr x0, [sp, #800]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #816]
    mov x0, #1
    str x0, [sp, #824]
    ldr x0, [sp, #816]
    ldr x1, [sp, #824]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #832]
    ldr x0, [sp, #832]
    cbz w0, L_kuro_fn_ParseComparisonOp_else6
    mov x0, #1
    str x0, [sp, #840]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #840]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_108@PAGE
    add x0, x0, L_kuro_data_108@PAGEOFF
    str x0, [sp, #848]
    ldr x0, [sp, #848]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #856]
    ldr x0, [sp, #856]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_109@PAGE
    add x0, x0, L_kuro_data_109@PAGEOFF
    str x0, [sp, #864]
    ldr x0, [sp, #864]
    bl _kuro_fn_IsWord
    str x0, [sp, #872]
    ldr x0, [sp, #872]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #880]
    ldr x0, [sp, #880]
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #888]
    mov x0, #1
    str x0, [sp, #904]
    ldr x0, [sp, #888]
    ldr x1, [sp, #904]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #912]
    ldr x0, [sp, #912]
    cbz w0, L_kuro_fn_ParseComparisonOp_else8
    mov x0, #1
    str x0, [sp, #920]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #920]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_110@PAGE
    add x0, x0, L_kuro_data_110@PAGEOFF
    str x0, [sp, #928]
    ldr x0, [sp, #928]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #936]
    ldr x0, [sp, #936]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_111@PAGE
    add x0, x0, L_kuro_data_111@PAGEOFF
    str x0, [sp, #944]
    ldr x0, [sp, #944]
    bl _kuro_fn_IsWord
    str x0, [sp, #952]
    ldr x0, [sp, #952]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #960]
    ldr x0, [sp, #960]
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    str x0, [sp, #968]
    mov x0, #1
    str x0, [sp, #976]
    ldr x0, [sp, #968]
    ldr x1, [sp, #976]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #992]
    ldr x0, [sp, #992]
    cbz w0, L_kuro_fn_ParseComparisonOp_else10
    mov x0, #1
    str x0, [sp, #1000]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1000]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseComparisonOp_endif11
L_kuro_fn_ParseComparisonOp_else10:
L_kuro_fn_ParseComparisonOp_endif11:
    adrp x0, L_kuro_data_112@PAGE
    add x0, x0, L_kuro_data_112@PAGEOFF
    str x0, [sp, #1008]
    ldr x0, [sp, #1008]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseComparisonOp_endif9
L_kuro_fn_ParseComparisonOp_else8:
    adrp x0, L_kuro_data_113@PAGE
    add x0, x0, L_kuro_data_113@PAGEOFF
    str x0, [sp, #1016]
    ldr x0, [sp, #1016]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_ParseComparisonOp_endif9:
    b L_kuro_fn_ParseComparisonOp_endif7
L_kuro_fn_ParseComparisonOp_else6:
L_kuro_fn_ParseComparisonOp_endif7:
    adrp x0, L_kuro_data_114@PAGE
    add x0, x0, L_kuro_data_114@PAGEOFF
    str x0, [sp, #1024]
    ldr x0, [sp, #1024]
    bl _kuro_fn_IsWord
    str x0, [sp, #1032]
    ldr x0, [sp, #1032]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1040]
    ldr x0, [sp, #1040]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    str x0, [sp, #1048]
    mov x0, #1
    str x0, [sp, #1056]
    ldr x0, [sp, #1048]
    ldr x1, [sp, #1056]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1064]
    ldr x0, [sp, #1064]
    cbz w0, L_kuro_fn_ParseComparisonOp_else12
    mov x0, #1
    str x0, [sp, #1080]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1080]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_115@PAGE
    add x0, x0, L_kuro_data_115@PAGEOFF
    str x0, [sp, #1088]
    ldr x0, [sp, #1088]
    bl _kuro_fn_IsWord
    str x0, [sp, #1096]
    ldr x0, [sp, #1096]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1104]
    ldr x0, [sp, #1104]
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    str x0, [sp, #1112]
    mov x0, #1
    str x0, [sp, #1120]
    ldr x0, [sp, #1112]
    ldr x1, [sp, #1120]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1128]
    ldr x0, [sp, #1128]
    cbz w0, L_kuro_fn_ParseComparisonOp_else14
    mov x0, #1
    str x0, [sp, #1136]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1136]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseComparisonOp_endif15
L_kuro_fn_ParseComparisonOp_else14:
L_kuro_fn_ParseComparisonOp_endif15:
    adrp x0, L_kuro_data_116@PAGE
    add x0, x0, L_kuro_data_116@PAGEOFF
    str x0, [sp, #1144]
    ldr x0, [sp, #1144]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseComparisonOp_endif13
L_kuro_fn_ParseComparisonOp_else12:
L_kuro_fn_ParseComparisonOp_endif13:
    adrp x0, L_kuro_data_117@PAGE
    add x0, x0, L_kuro_data_117@PAGEOFF
    str x0, [sp, #1152]
    ldr x0, [sp, #1152]
    bl _kuro_fn_IsWord
    str x0, [sp, #1168]
    ldr x0, [sp, #1168]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1176]
    ldr x0, [sp, #1176]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    str x0, [sp, #1184]
    mov x0, #1
    str x0, [sp, #1192]
    ldr x0, [sp, #1184]
    ldr x1, [sp, #1192]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1200]
    ldr x0, [sp, #1200]
    cbz w0, L_kuro_fn_ParseComparisonOp_else16
    mov x0, #1
    str x0, [sp, #1208]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1208]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_118@PAGE
    add x0, x0, L_kuro_data_118@PAGEOFF
    str x0, [sp, #1216]
    ldr x0, [sp, #1216]
    bl _kuro_fn_IsWord
    str x0, [sp, #1224]
    ldr x0, [sp, #1224]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1232]
    ldr x0, [sp, #1232]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    str x0, [sp, #1240]
    mov x0, #1
    str x0, [sp, #1256]
    ldr x0, [sp, #1240]
    ldr x1, [sp, #1256]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1264]
    ldr x0, [sp, #1264]
    cbz w0, L_kuro_fn_ParseComparisonOp_else18
    mov x0, #1
    str x0, [sp, #1272]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1272]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseComparisonOp_endif19
L_kuro_fn_ParseComparisonOp_else18:
L_kuro_fn_ParseComparisonOp_endif19:
    adrp x0, L_kuro_data_119@PAGE
    add x0, x0, L_kuro_data_119@PAGEOFF
    str x0, [sp, #1280]
    ldr x0, [sp, #1280]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseComparisonOp_endif17
L_kuro_fn_ParseComparisonOp_else16:
L_kuro_fn_ParseComparisonOp_endif17:
    adrp x0, L_kuro_data_120@PAGE
    add x0, x0, L_kuro_data_120@PAGEOFF
    str x0, [sp, #1288]
    ldr x0, [sp, #1288]
    bl _kuro_fn_IsWord
    str x0, [sp, #1296]
    ldr x0, [sp, #1296]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1304]
    ldr x0, [sp, #1304]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    str x0, [sp, #1312]
    mov x0, #1
    str x0, [sp, #1320]
    ldr x0, [sp, #1312]
    ldr x1, [sp, #1320]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1328]
    ldr x0, [sp, #1328]
    cbz w0, L_kuro_fn_ParseComparisonOp_else20
    mov x0, #1
    str x0, [sp, #1344]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1344]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_121@PAGE
    add x0, x0, L_kuro_data_121@PAGEOFF
    str x0, [sp, #1352]
    ldr x0, [sp, #1352]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #1360]
    ldr x0, [sp, #1360]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_122@PAGE
    add x0, x0, L_kuro_data_122@PAGEOFF
    str x0, [sp, #1368]
    ldr x0, [sp, #1368]
    bl _kuro_fn_IsWord
    str x0, [sp, #1376]
    ldr x0, [sp, #1376]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1384]
    ldr x0, [sp, #1384]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #1392]
    mov x0, #1
    str x0, [sp, #1400]
    ldr x0, [sp, #1392]
    ldr x1, [sp, #1400]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1408]
    ldr x0, [sp, #1408]
    cbz w0, L_kuro_fn_ParseComparisonOp_else22
    mov x0, #1
    str x0, [sp, #1416]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1416]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseComparisonOp_endif23
L_kuro_fn_ParseComparisonOp_else22:
L_kuro_fn_ParseComparisonOp_endif23:
    adrp x0, L_kuro_data_123@PAGE
    add x0, x0, L_kuro_data_123@PAGEOFF
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseComparisonOp_endif21
L_kuro_fn_ParseComparisonOp_else20:
L_kuro_fn_ParseComparisonOp_endif21:
    adrp x0, L_kuro_data_124@PAGE
    add x0, x0, L_kuro_data_124@PAGEOFF
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    bl _kuro_fn_IsWord
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #448]
    ldr x0, [sp, #448]
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #456]
    mov x0, #1
    str x0, [sp, #464]
    ldr x0, [sp, #456]
    ldr x1, [sp, #464]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #472]
    ldr x0, [sp, #472]
    cbz w0, L_kuro_fn_ParseComparisonOp_else24
    mov x0, #1
    str x0, [sp, #480]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #480]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_125@PAGE
    add x0, x0, L_kuro_data_125@PAGEOFF
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    bl _kuro_fn_IsWord
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #512]
    ldr x0, [sp, #512]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #520]
    mov x0, #1
    str x0, [sp, #528]
    ldr x0, [sp, #520]
    ldr x1, [sp, #528]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    cbz w0, L_kuro_fn_ParseComparisonOp_else26
    mov x0, #1
    str x0, [sp, #544]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #544]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_126@PAGE
    add x0, x0, L_kuro_data_126@PAGEOFF
    str x0, [sp, #552]
    ldr x0, [sp, #552]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseComparisonOp_endif27
L_kuro_fn_ParseComparisonOp_else26:
L_kuro_fn_ParseComparisonOp_endif27:
    adrp x0, L_kuro_data_127@PAGE
    add x0, x0, L_kuro_data_127@PAGEOFF
    str x0, [sp, #560]
    ldr x0, [sp, #560]
    bl _kuro_fn_IsWord
    str x0, [sp, #568]
    ldr x0, [sp, #568]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #576]
    ldr x0, [sp, #576]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #584]
    mov x0, #1
    str x0, [sp, #600]
    ldr x0, [sp, #584]
    ldr x1, [sp, #600]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #608]
    ldr x0, [sp, #608]
    cbz w0, L_kuro_fn_ParseComparisonOp_else28
    mov x0, #1
    str x0, [sp, #616]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #616]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_128@PAGE
    add x0, x0, L_kuro_data_128@PAGEOFF
    str x0, [sp, #624]
    ldr x0, [sp, #624]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseComparisonOp_endif29
L_kuro_fn_ParseComparisonOp_else28:
L_kuro_fn_ParseComparisonOp_endif29:
    b L_kuro_fn_ParseComparisonOp_endif25
L_kuro_fn_ParseComparisonOp_else24:
L_kuro_fn_ParseComparisonOp_endif25:
    adrp x0, L_kuro_data_129@PAGE
    add x0, x0, L_kuro_data_129@PAGEOFF
    str x0, [sp, #632]
    adrp x0, L_kuro_data_130@PAGE
    add x0, x0, L_kuro_data_130@PAGEOFF
    str x0, [sp, #640]
    ldr x0, [sp, #632]
    ldr x1, [sp, #640]
    bl _kuro_fn_RecordDiag
    str x0, [sp, #648]
    ldr x0, [sp, #648]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_131@PAGE
    add x0, x0, L_kuro_data_131@PAGEOFF
    str x0, [sp, #656]
    ldr x0, [sp, #656]
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #1440
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseComparison:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #608
    sub sp, sp, x15
    bl _kuro_fn_ParseExpr
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_132@PAGE
    add x0, x0, L_kuro_data_132@PAGEOFF
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    bl _kuro_fn_IsWord
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #504]
    mov x0, #1
    str x0, [sp, #568]
    ldr x0, [sp, #504]
    ldr x1, [sp, #568]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #576]
    ldr x0, [sp, #576]
    cbz w0, L_kuro_fn_ParseComparison_else0
    mov x0, #1
    str x0, [sp, #584]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #584]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseComparison_endif1
L_kuro_fn_ParseComparison_else0:
L_kuro_fn_ParseComparison_endif1:
    bl _kuro_fn_CurKind
    str x0, [sp, #592]
    ldr x0, [sp, #592]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #600]
    ldr x0, [sp, #600]
    str x0, [sp, #56]
    bl _kuro_fn_CurValue
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #72]
    mov x0, #0
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #48]
    ldr x0, [sp, #56]
    str x0, [sp, #272]
    adrp x0, L_kuro_data_133@PAGE
    add x0, x0, L_kuro_data_133@PAGEOFF
    str x0, [sp, #280]
    ldr x0, [sp, #272]
    ldr x1, [sp, #280]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    cbz w0, L_kuro_fn_ParseComparison_else2
    ldr x0, [sp, #72]
    str x0, [sp, #296]
    adrp x0, L_kuro_data_134@PAGE
    add x0, x0, L_kuro_data_134@PAGEOFF
    str x0, [sp, #304]
    ldr x0, [sp, #296]
    ldr x1, [sp, #304]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    cbz w0, L_kuro_fn_ParseComparison_else4
    mov x0, #1
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    str x0, [sp, #48]
    b L_kuro_fn_ParseComparison_endif5
L_kuro_fn_ParseComparison_else4:
L_kuro_fn_ParseComparison_endif5:
    ldr x0, [sp, #72]
    str x0, [sp, #336]
    adrp x0, L_kuro_data_135@PAGE
    add x0, x0, L_kuro_data_135@PAGEOFF
    str x0, [sp, #344]
    ldr x0, [sp, #336]
    ldr x1, [sp, #344]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    cbz w0, L_kuro_fn_ParseComparison_else6
    mov x0, #1
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    str x0, [sp, #48]
    b L_kuro_fn_ParseComparison_endif7
L_kuro_fn_ParseComparison_else6:
L_kuro_fn_ParseComparison_endif7:
    ldr x0, [sp, #72]
    str x0, [sp, #368]
    adrp x0, L_kuro_data_136@PAGE
    add x0, x0, L_kuro_data_136@PAGEOFF
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    cbz w0, L_kuro_fn_ParseComparison_else8
    mov x0, #1
    str x0, [sp, #392]
    ldr x0, [sp, #392]
    str x0, [sp, #48]
    b L_kuro_fn_ParseComparison_endif9
L_kuro_fn_ParseComparison_else8:
L_kuro_fn_ParseComparison_endif9:
    ldr x0, [sp, #72]
    str x0, [sp, #400]
    adrp x0, L_kuro_data_137@PAGE
    add x0, x0, L_kuro_data_137@PAGEOFF
    str x0, [sp, #408]
    ldr x0, [sp, #400]
    ldr x1, [sp, #408]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    cbz w0, L_kuro_fn_ParseComparison_else10
    mov x0, #1
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    str x0, [sp, #48]
    b L_kuro_fn_ParseComparison_endif11
L_kuro_fn_ParseComparison_else10:
L_kuro_fn_ParseComparison_endif11:
    ldr x0, [sp, #72]
    str x0, [sp, #440]
    adrp x0, L_kuro_data_138@PAGE
    add x0, x0, L_kuro_data_138@PAGEOFF
    str x0, [sp, #448]
    ldr x0, [sp, #440]
    ldr x1, [sp, #448]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #456]
    ldr x0, [sp, #456]
    cbz w0, L_kuro_fn_ParseComparison_else12
    mov x0, #1
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    str x0, [sp, #48]
    b L_kuro_fn_ParseComparison_endif13
L_kuro_fn_ParseComparison_else12:
L_kuro_fn_ParseComparison_endif13:
    b L_kuro_fn_ParseComparison_endif3
L_kuro_fn_ParseComparison_else2:
L_kuro_fn_ParseComparison_endif3:
    ldr x0, [sp, #48]
    str x0, [sp, #472]
    mov x0, #1
    str x0, [sp, #480]
    ldr x0, [sp, #472]
    ldr x1, [sp, #480]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    cbz w0, L_kuro_fn_ParseComparison_else14
    mov x0, #1
    str x0, [sp, #496]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #496]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_139@PAGE
    add x0, x0, L_kuro_data_139@PAGEOFF
    str x0, [sp, #512]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #512]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #72]
    str x0, [sp, #520]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #520]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_ParseComparison_endif15
L_kuro_fn_ParseComparison_else14:
    bl _kuro_fn_ParseComparisonOp
    str x0, [sp, #528]
    ldr x0, [sp, #528]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    str x0, [sp, #64]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #544]
    ldr x0, [sp, #544]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_140@PAGE
    add x0, x0, L_kuro_data_140@PAGEOFF
    str x0, [sp, #552]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #552]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #64]
    str x0, [sp, #560]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #560]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
L_kuro_fn_ParseComparison_endif15:
    mov x0, #0
    mov x15, #608
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseAndCondition:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #48
    sub sp, sp, x15
    bl _kuro_fn_ParseComparison
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseAndConditionTail
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseAndConditionTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #208
    sub sp, sp, x15
    adrp x0, L_kuro_data_141@PAGE
    add x0, x0, L_kuro_data_141@PAGEOFF
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    bl _kuro_fn_IsWord
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #144]
    mov x0, #1
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_ParseAndConditionTail_else0
    mov x0, #1
    str x0, [sp, #168]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #168]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseComparison
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_142@PAGE
    add x0, x0, L_kuro_data_142@PAGEOFF
    str x0, [sp, #184]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #184]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #192]
    ldr x1, [sp, #112]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    cbz w0, L_kuro_fn_ParseAndConditionTail_else2
    bl _kuro_fn_ParseAndConditionTail
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseAndConditionTail_endif3
L_kuro_fn_ParseAndConditionTail_else2:
L_kuro_fn_ParseAndConditionTail_endif3:
    b L_kuro_fn_ParseAndConditionTail_endif1
L_kuro_fn_ParseAndConditionTail_else0:
L_kuro_fn_ParseAndConditionTail_endif1:
    mov x0, #0
    mov x15, #208
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseCondition:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #48
    sub sp, sp, x15
    bl _kuro_fn_ParseAndCondition
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseConditionTail
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #48
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseConditionTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #208
    sub sp, sp, x15
    adrp x0, L_kuro_data_143@PAGE
    add x0, x0, L_kuro_data_143@PAGEOFF
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    bl _kuro_fn_IsWord
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #144]
    mov x0, #1
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_ParseConditionTail_else0
    mov x0, #1
    str x0, [sp, #168]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #168]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseAndCondition
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_144@PAGE
    add x0, x0, L_kuro_data_144@PAGEOFF
    str x0, [sp, #184]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #184]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #192]
    ldr x1, [sp, #112]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    cbz w0, L_kuro_fn_ParseConditionTail_else2
    bl _kuro_fn_ParseConditionTail
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseConditionTail_endif3
L_kuro_fn_ParseConditionTail_else2:
L_kuro_fn_ParseConditionTail_endif3:
    b L_kuro_fn_ParseConditionTail_endif1
L_kuro_fn_ParseConditionTail_else0:
L_kuro_fn_ParseConditionTail_endif1:
    mov x0, #0
    mov x15, #208
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseOneParam:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #192
    sub sp, sp, x15
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    str x0, [sp, #32]
    adrp x0, L_kuro_data_145@PAGE
    add x0, x0, L_kuro_data_145@PAGEOFF
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #40]
    bl _kuro_fn_CurKind
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #144]
    adrp x0, L_kuro_data_146@PAGE
    add x0, x0, L_kuro_data_146@PAGEOFF
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_ParseOneParam_else0
    mov x0, #1
    str x0, [sp, #168]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #168]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    str x0, [sp, #40]
    b L_kuro_fn_ParseOneParam_endif1
L_kuro_fn_ParseOneParam_else0:
L_kuro_fn_ParseOneParam_endif1:
    ldr x0, [sp, #32]
    str x0, [sp, #104]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #104]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #40]
    str x0, [sp, #112]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #112]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseParamsTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #112]
    adrp x0, L_kuro_data_147@PAGE
    add x0, x0, L_kuro_data_147@PAGEOFF
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    cbz w0, L_kuro_fn_ParseParamsTail_else0
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseOneParam
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    mov x0, #0
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_ParseParamsTail_else2
    bl _kuro_fn_ParseParamsTail
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseParamsTail_endif3
L_kuro_fn_ParseParamsTail_else2:
L_kuro_fn_ParseParamsTail_endif3:
    b L_kuro_fn_ParseParamsTail_endif1
L_kuro_fn_ParseParamsTail_else0:
L_kuro_fn_ParseParamsTail_endif1:
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseParams:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #336
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #232]
    adrp x0, L_kuro_data_148@PAGE
    add x0, x0, L_kuro_data_148@PAGEOFF
    str x0, [sp, #280]
    ldr x0, [sp, #232]
    ldr x1, [sp, #280]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    cbz w0, L_kuro_fn_ParseParams_else0
    mov x0, #1
    str x0, [sp, #296]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #296]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_CurKind
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #320]
    adrp x0, L_kuro_data_149@PAGE
    add x0, x0, L_kuro_data_149@PAGEOFF
    str x0, [sp, #328]
    ldr x0, [sp, #320]
    ldr x1, [sp, #328]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_ParseParams_else2
    mov x0, #1
    str x0, [sp, #160]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #160]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseParams_endif3
L_kuro_fn_ParseParams_else2:
    bl _kuro_fn_ParseOneParam
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseParamsTail
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_150@PAGE
    add x0, x0, L_kuro_data_150@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
L_kuro_fn_ParseParams_endif3:
    b L_kuro_fn_ParseParams_endif1
L_kuro_fn_ParseParams_else0:
    bl _kuro_fn_CurKind
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    str x0, [sp, #216]
    adrp x0, L_kuro_data_151@PAGE
    add x0, x0, L_kuro_data_151@PAGEOFF
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_ParseParams_else4
    mov x0, #0
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    str x0, [sp, #64]
    b L_kuro_fn_ParseParams_endif5
L_kuro_fn_ParseParams_else4:
    bl _kuro_fn_ParseOneParam
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseParamsTail
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
L_kuro_fn_ParseParams_endif5:
L_kuro_fn_ParseParams_endif1:
    adrp x0, L_kuro_data_152@PAGE
    add x0, x0, L_kuro_data_152@PAGEOFF
    str x0, [sp, #272]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #272]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #336
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseArgsTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #112]
    adrp x0, L_kuro_data_153@PAGE
    add x0, x0, L_kuro_data_153@PAGEOFF
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    cbz w0, L_kuro_fn_ParseArgsTail_else0
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    mov x0, #0
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_ParseArgsTail_else2
    bl _kuro_fn_ParseArgsTail
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseArgsTail_endif3
L_kuro_fn_ParseArgsTail_else2:
L_kuro_fn_ParseArgsTail_endif3:
    b L_kuro_fn_ParseArgsTail_endif1
L_kuro_fn_ParseArgsTail_else0:
L_kuro_fn_ParseArgsTail_endif1:
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseArgs:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #336
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #232]
    adrp x0, L_kuro_data_154@PAGE
    add x0, x0, L_kuro_data_154@PAGEOFF
    str x0, [sp, #280]
    ldr x0, [sp, #232]
    ldr x1, [sp, #280]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    cbz w0, L_kuro_fn_ParseArgs_else0
    mov x0, #1
    str x0, [sp, #296]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #296]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_CurKind
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #320]
    adrp x0, L_kuro_data_155@PAGE
    add x0, x0, L_kuro_data_155@PAGEOFF
    str x0, [sp, #328]
    ldr x0, [sp, #320]
    ldr x1, [sp, #328]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_ParseArgs_else2
    mov x0, #1
    str x0, [sp, #160]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #160]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseArgs_endif3
L_kuro_fn_ParseArgs_else2:
    bl _kuro_fn_ParseExpr
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseArgsTail
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_156@PAGE
    add x0, x0, L_kuro_data_156@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
L_kuro_fn_ParseArgs_endif3:
    b L_kuro_fn_ParseArgs_endif1
L_kuro_fn_ParseArgs_else0:
    bl _kuro_fn_CurKind
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #216]
    adrp x0, L_kuro_data_157@PAGE
    add x0, x0, L_kuro_data_157@PAGEOFF
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_ParseArgs_else4
    mov x0, #0
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    str x0, [sp, #56]
    b L_kuro_fn_ParseArgs_endif5
L_kuro_fn_ParseArgs_else4:
    bl _kuro_fn_ParseExpr
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseArgsTail
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
L_kuro_fn_ParseArgs_endif5:
L_kuro_fn_ParseArgs_endif1:
    adrp x0, L_kuro_data_158@PAGE
    add x0, x0, L_kuro_data_158@PAGEOFF
    str x0, [sp, #272]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #272]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #336
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_IsDeclAhead:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #512
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    bl _kuro_fn_PeekKind
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #8]
    mov x0, #1
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    bl _kuro_fn_PeekValue
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #472]
    ldr x0, [sp, #472]
    str x0, [sp, #16]
    ldr x0, [sp, #8]
    str x0, [sp, #480]
    adrp x0, L_kuro_data_159@PAGE
    add x0, x0, L_kuro_data_159@PAGEOFF
    str x0, [sp, #488]
    ldr x0, [sp, #480]
    ldr x1, [sp, #488]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #496]
    ldr x0, [sp, #16]
    str x0, [sp, #504]
    adrp x0, L_kuro_data_160@PAGE
    add x0, x0, L_kuro_data_160@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #504]
    ldr x1, [sp, #184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #496]
    ldr x1, [sp, #192]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    cbz w0, L_kuro_fn_IsDeclAhead_else0
    mov x0, #2
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    bl _kuro_fn_PeekValue
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    str x0, [sp, #24]
    mov x0, #0
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    str x0, [sp, #0]
    ldr x0, [sp, #24]
    str x0, [sp, #240]
    adrp x0, L_kuro_data_161@PAGE
    add x0, x0, L_kuro_data_161@PAGEOFF
    str x0, [sp, #248]
    ldr x0, [sp, #240]
    ldr x1, [sp, #248]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    cbz w0, L_kuro_fn_IsDeclAhead_else2
    mov x0, #1
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    str x0, [sp, #0]
    b L_kuro_fn_IsDeclAhead_endif3
L_kuro_fn_IsDeclAhead_else2:
L_kuro_fn_IsDeclAhead_endif3:
    ldr x0, [sp, #24]
    str x0, [sp, #280]
    adrp x0, L_kuro_data_162@PAGE
    add x0, x0, L_kuro_data_162@PAGEOFF
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    cbz w0, L_kuro_fn_IsDeclAhead_else4
    mov x0, #1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    str x0, [sp, #0]
    b L_kuro_fn_IsDeclAhead_endif5
L_kuro_fn_IsDeclAhead_else4:
L_kuro_fn_IsDeclAhead_endif5:
    ldr x0, [sp, #24]
    str x0, [sp, #312]
    adrp x0, L_kuro_data_163@PAGE
    add x0, x0, L_kuro_data_163@PAGEOFF
    str x0, [sp, #320]
    ldr x0, [sp, #312]
    ldr x1, [sp, #320]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    cbz w0, L_kuro_fn_IsDeclAhead_else6
    mov x0, #1
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    str x0, [sp, #0]
    b L_kuro_fn_IsDeclAhead_endif7
L_kuro_fn_IsDeclAhead_else6:
L_kuro_fn_IsDeclAhead_endif7:
    ldr x0, [sp, #24]
    str x0, [sp, #344]
    adrp x0, L_kuro_data_164@PAGE
    add x0, x0, L_kuro_data_164@PAGEOFF
    str x0, [sp, #360]
    ldr x0, [sp, #344]
    ldr x1, [sp, #360]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #368]
    ldr x0, [sp, #368]
    cbz w0, L_kuro_fn_IsDeclAhead_else8
    mov x0, #1
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    str x0, [sp, #0]
    b L_kuro_fn_IsDeclAhead_endif9
L_kuro_fn_IsDeclAhead_else8:
L_kuro_fn_IsDeclAhead_endif9:
    ldr x0, [sp, #24]
    str x0, [sp, #384]
    adrp x0, L_kuro_data_165@PAGE
    add x0, x0, L_kuro_data_165@PAGEOFF
    str x0, [sp, #392]
    ldr x0, [sp, #384]
    ldr x1, [sp, #392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    cbz w0, L_kuro_fn_IsDeclAhead_else10
    mov x0, #1
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    str x0, [sp, #0]
    b L_kuro_fn_IsDeclAhead_endif11
L_kuro_fn_IsDeclAhead_else10:
L_kuro_fn_IsDeclAhead_endif11:
    ldr x0, [sp, #0]
    str x0, [sp, #416]
    mov x0, #1
    str x0, [sp, #424]
    ldr x0, [sp, #416]
    ldr x1, [sp, #424]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    cbz w0, L_kuro_fn_IsDeclAhead_else12
    mov x0, #0
    str x0, [sp, #448]
    ldr x0, [sp, #448]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_IsDeclAhead_endif13
L_kuro_fn_IsDeclAhead_else12:
    mov x0, #1
    str x0, [sp, #456]
    ldr x0, [sp, #456]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_IsDeclAhead_endif13:
    b L_kuro_fn_IsDeclAhead_endif1
L_kuro_fn_IsDeclAhead_else0:
    mov x0, #0
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_IsDeclAhead_endif1:
    mov x0, #0
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseTakeNamesTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #224
    sub sp, sp, x15
    adrp x0, L_kuro_data_166@PAGE
    add x0, x0, L_kuro_data_166@PAGEOFF
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    bl _kuro_fn_IsWord
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #160]
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    cbz w0, L_kuro_fn_ParseTakeNamesTail_else0
    mov x0, #1
    str x0, [sp, #184]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #184]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #208]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #208]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    mov x0, #0
    str x0, [sp, #128]
    ldr x0, [sp, #120]
    ldr x1, [sp, #128]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    cbz w0, L_kuro_fn_ParseTakeNamesTail_else2
    bl _kuro_fn_ParseTakeNamesTail
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseTakeNamesTail_endif3
L_kuro_fn_ParseTakeNamesTail_else2:
L_kuro_fn_ParseTakeNamesTail_endif3:
    b L_kuro_fn_ParseTakeNamesTail_endif1
L_kuro_fn_ParseTakeNamesTail_else0:
L_kuro_fn_ParseTakeNamesTail_endif1:
    mov x0, #0
    mov x15, #224
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseValueListTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #112]
    adrp x0, L_kuro_data_167@PAGE
    add x0, x0, L_kuro_data_167@PAGEOFF
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    cbz w0, L_kuro_fn_ParseValueListTail_else0
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    mov x0, #0
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_ParseValueListTail_else2
    bl _kuro_fn_ParseValueListTail
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseValueListTail_endif3
L_kuro_fn_ParseValueListTail_else2:
L_kuro_fn_ParseValueListTail_endif3:
    b L_kuro_fn_ParseValueListTail_endif1
L_kuro_fn_ParseValueListTail_else0:
L_kuro_fn_ParseValueListTail_endif1:
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseValueList:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #64
    sub sp, sp, x15
    bl _kuro_fn_ParseExpr
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseValueListTail
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_168@PAGE
    add x0, x0, L_kuro_data_168@PAGEOFF
    str x0, [sp, #48]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #48]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #64
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseStatement:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #3856
    sub sp, sp, x15
    bl _kuro_fn_CurKind
    str x0, [sp, #840]
    ldr x0, [sp, #840]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #848]
    ldr x0, [sp, #848]
    str x0, [sp, #336]
    bl _kuro_fn_CurValue
    str x0, [sp, #1736]
    ldr x0, [sp, #1736]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2624]
    ldr x0, [sp, #2624]
    str x0, [sp, #416]
    ldr x0, [sp, #336]
    str x0, [sp, #3312]
    adrp x0, L_kuro_data_169@PAGE
    add x0, x0, L_kuro_data_169@PAGEOFF
    str x0, [sp, #3400]
    ldr x0, [sp, #3312]
    ldr x1, [sp, #3400]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3488]
    ldr x0, [sp, #3488]
    cbz w0, L_kuro_fn_ParseStatement_else0
    bl _kuro_fn_IsDeclAhead
    str x0, [sp, #3576]
    ldr x0, [sp, #3576]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3664]
    ldr x0, [sp, #3664]
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    str x0, [sp, #3752]
    mov x0, #1
    str x0, [sp, #856]
    ldr x0, [sp, #3752]
    ldr x1, [sp, #856]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #944]
    ldr x0, [sp, #944]
    cbz w0, L_kuro_fn_ParseStatement_else2
    mov x0, #1
    str x0, [sp, #1032]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1032]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1120]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1120]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #1208]
    ldr x0, [sp, #1208]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1296]
    ldr x0, [sp, #1296]
    str x0, [sp, #392]
    adrp x0, L_kuro_data_170@PAGE
    add x0, x0, L_kuro_data_170@PAGEOFF
    str x0, [sp, #1384]
    ldr x0, [sp, #1384]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #1472]
    ldr x0, [sp, #1472]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_171@PAGE
    add x0, x0, L_kuro_data_171@PAGEOFF
    str x0, [sp, #1560]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1560]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #416]
    str x0, [sp, #1648]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1648]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #392]
    str x0, [sp, #1744]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1744]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #1832]
    ldr x0, [sp, #1832]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif3
L_kuro_fn_ParseStatement_else2:
L_kuro_fn_ParseStatement_endif3:
    mov x0, #1
    str x0, [sp, #1920]
    ldr x0, [sp, #1920]
    bl _kuro_fn_PeekKind
    str x0, [sp, #2008]
    ldr x0, [sp, #2008]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2096]
    ldr x0, [sp, #2096]
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    str x0, [sp, #2184]
    adrp x0, L_kuro_data_172@PAGE
    add x0, x0, L_kuro_data_172@PAGEOFF
    str x0, [sp, #2272]
    ldr x0, [sp, #2184]
    ldr x1, [sp, #2272]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2360]
    ldr x0, [sp, #2360]
    cbz w0, L_kuro_fn_ParseStatement_else4
    mov x0, #1
    str x0, [sp, #2448]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2448]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2536]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2536]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #2632]
    ldr x0, [sp, #2632]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2720]
    ldr x0, [sp, #2720]
    str x0, [sp, #400]
    adrp x0, L_kuro_data_173@PAGE
    add x0, x0, L_kuro_data_173@PAGEOFF
    str x0, [sp, #2808]
    ldr x0, [sp, #2808]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2896]
    ldr x0, [sp, #2896]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_174@PAGE
    add x0, x0, L_kuro_data_174@PAGEOFF
    str x0, [sp, #2984]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2984]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #416]
    str x0, [sp, #3072]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3072]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #400]
    str x0, [sp, #3160]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3160]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseValueList
    str x0, [sp, #3248]
    ldr x0, [sp, #3248]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_175@PAGE
    add x0, x0, L_kuro_data_175@PAGEOFF
    str x0, [sp, #3296]
    ldr x0, [sp, #3296]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3304]
    ldr x0, [sp, #3304]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3320]
    ldr x0, [sp, #3320]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif5
L_kuro_fn_ParseStatement_else4:
L_kuro_fn_ParseStatement_endif5:
    ldr x0, [sp, #360]
    str x0, [sp, #3328]
    adrp x0, L_kuro_data_176@PAGE
    add x0, x0, L_kuro_data_176@PAGEOFF
    str x0, [sp, #3336]
    ldr x0, [sp, #3328]
    ldr x1, [sp, #3336]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3344]
    ldr x0, [sp, #3344]
    cbz w0, L_kuro_fn_ParseStatement_else6
    mov x0, #1
    str x0, [sp, #3352]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3352]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3360]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3360]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_177@PAGE
    add x0, x0, L_kuro_data_177@PAGEOFF
    str x0, [sp, #3368]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3368]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #416]
    str x0, [sp, #3376]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3376]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_178@PAGE
    add x0, x0, L_kuro_data_178@PAGEOFF
    str x0, [sp, #3384]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3384]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseValueList
    str x0, [sp, #3392]
    ldr x0, [sp, #3392]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_179@PAGE
    add x0, x0, L_kuro_data_179@PAGEOFF
    str x0, [sp, #3408]
    ldr x0, [sp, #3408]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3416]
    ldr x0, [sp, #3416]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3424]
    ldr x0, [sp, #3424]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif7
L_kuro_fn_ParseStatement_else6:
L_kuro_fn_ParseStatement_endif7:
    b L_kuro_fn_ParseStatement_endif1
L_kuro_fn_ParseStatement_else0:
L_kuro_fn_ParseStatement_endif1:
    adrp x0, L_kuro_data_180@PAGE
    add x0, x0, L_kuro_data_180@PAGEOFF
    str x0, [sp, #3432]
    ldr x0, [sp, #3432]
    bl _kuro_fn_IsWord
    str x0, [sp, #3440]
    ldr x0, [sp, #3440]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3448]
    ldr x0, [sp, #3448]
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    str x0, [sp, #3456]
    mov x0, #1
    str x0, [sp, #3464]
    ldr x0, [sp, #3456]
    ldr x1, [sp, #3464]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3472]
    ldr x0, [sp, #3472]
    cbz w0, L_kuro_fn_ParseStatement_else8
    mov x0, #1
    str x0, [sp, #3480]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3480]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_181@PAGE
    add x0, x0, L_kuro_data_181@PAGEOFF
    str x0, [sp, #3496]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3496]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #3504]
    ldr x0, [sp, #3504]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_182@PAGE
    add x0, x0, L_kuro_data_182@PAGEOFF
    str x0, [sp, #3512]
    ldr x0, [sp, #3512]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3520]
    ldr x0, [sp, #3520]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3528]
    ldr x0, [sp, #3528]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif9
L_kuro_fn_ParseStatement_else8:
L_kuro_fn_ParseStatement_endif9:
    adrp x0, L_kuro_data_183@PAGE
    add x0, x0, L_kuro_data_183@PAGEOFF
    str x0, [sp, #3536]
    ldr x0, [sp, #3536]
    bl _kuro_fn_IsWord
    str x0, [sp, #3544]
    ldr x0, [sp, #3544]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3552]
    ldr x0, [sp, #3552]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    str x0, [sp, #3560]
    mov x0, #1
    str x0, [sp, #3568]
    ldr x0, [sp, #3560]
    ldr x1, [sp, #3568]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3584]
    ldr x0, [sp, #3584]
    cbz w0, L_kuro_fn_ParseStatement_else10
    mov x0, #1
    str x0, [sp, #3592]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3592]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_184@PAGE
    add x0, x0, L_kuro_data_184@PAGEOFF
    str x0, [sp, #3600]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3600]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #3608]
    ldr x0, [sp, #3608]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_185@PAGE
    add x0, x0, L_kuro_data_185@PAGEOFF
    str x0, [sp, #3616]
    ldr x0, [sp, #3616]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #3624]
    ldr x0, [sp, #3624]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #3632]
    ldr x0, [sp, #3632]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3640]
    ldr x0, [sp, #3640]
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    str x0, [sp, #3648]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3648]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_186@PAGE
    add x0, x0, L_kuro_data_186@PAGEOFF
    str x0, [sp, #3656]
    ldr x0, [sp, #3656]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3672]
    ldr x0, [sp, #3672]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3680]
    ldr x0, [sp, #3680]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif11
L_kuro_fn_ParseStatement_else10:
L_kuro_fn_ParseStatement_endif11:
    adrp x0, L_kuro_data_187@PAGE
    add x0, x0, L_kuro_data_187@PAGEOFF
    str x0, [sp, #3688]
    ldr x0, [sp, #3688]
    bl _kuro_fn_IsWord
    str x0, [sp, #3696]
    ldr x0, [sp, #3696]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3704]
    ldr x0, [sp, #3704]
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    str x0, [sp, #3712]
    mov x0, #1
    str x0, [sp, #3720]
    ldr x0, [sp, #3712]
    ldr x1, [sp, #3720]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3728]
    ldr x0, [sp, #3728]
    cbz w0, L_kuro_fn_ParseStatement_else12
    mov x0, #1
    str x0, [sp, #3736]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3736]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #3744]
    ldr x0, [sp, #3744]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3760]
    ldr x0, [sp, #3760]
    str x0, [sp, #408]
    adrp x0, L_kuro_data_188@PAGE
    add x0, x0, L_kuro_data_188@PAGEOFF
    str x0, [sp, #3768]
    ldr x0, [sp, #3768]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #3776]
    ldr x0, [sp, #3776]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_189@PAGE
    add x0, x0, L_kuro_data_189@PAGEOFF
    str x0, [sp, #3784]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3784]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #408]
    str x0, [sp, #3792]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3792]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #3800]
    ldr x0, [sp, #3800]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_190@PAGE
    add x0, x0, L_kuro_data_190@PAGEOFF
    str x0, [sp, #3808]
    ldr x0, [sp, #3808]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3816]
    ldr x0, [sp, #3816]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3824]
    ldr x0, [sp, #3824]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif13
L_kuro_fn_ParseStatement_else12:
L_kuro_fn_ParseStatement_endif13:
    adrp x0, L_kuro_data_191@PAGE
    add x0, x0, L_kuro_data_191@PAGEOFF
    str x0, [sp, #3832]
    ldr x0, [sp, #3832]
    bl _kuro_fn_IsWord
    str x0, [sp, #864]
    ldr x0, [sp, #864]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #872]
    ldr x0, [sp, #872]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    str x0, [sp, #880]
    mov x0, #1
    str x0, [sp, #888]
    ldr x0, [sp, #880]
    ldr x1, [sp, #888]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #896]
    ldr x0, [sp, #896]
    cbz w0, L_kuro_fn_ParseStatement_else14
    mov x0, #1
    str x0, [sp, #904]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #904]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_192@PAGE
    add x0, x0, L_kuro_data_192@PAGEOFF
    str x0, [sp, #912]
    ldr x0, [sp, #912]
    bl _kuro_fn_IsWord
    str x0, [sp, #920]
    ldr x0, [sp, #920]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #928]
    ldr x0, [sp, #928]
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    str x0, [sp, #936]
    mov x0, #1
    str x0, [sp, #952]
    ldr x0, [sp, #936]
    ldr x1, [sp, #952]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #960]
    ldr x0, [sp, #960]
    cbz w0, L_kuro_fn_ParseStatement_else16
    mov x0, #1
    str x0, [sp, #968]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #968]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseStatement_endif17
L_kuro_fn_ParseStatement_else16:
L_kuro_fn_ParseStatement_endif17:
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #976]
    ldr x0, [sp, #976]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #984]
    ldr x0, [sp, #984]
    str x0, [sp, #376]
    adrp x0, L_kuro_data_193@PAGE
    add x0, x0, L_kuro_data_193@PAGEOFF
    str x0, [sp, #992]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #992]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #376]
    str x0, [sp, #1000]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1000]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseTakeNamesTail
    str x0, [sp, #1008]
    ldr x0, [sp, #1008]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_194@PAGE
    add x0, x0, L_kuro_data_194@PAGEOFF
    str x0, [sp, #1016]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1016]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_195@PAGE
    add x0, x0, L_kuro_data_195@PAGEOFF
    str x0, [sp, #1024]
    ldr x0, [sp, #1024]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #1040]
    ldr x0, [sp, #1040]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1048]
    ldr x0, [sp, #1048]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif15
L_kuro_fn_ParseStatement_else14:
L_kuro_fn_ParseStatement_endif15:
    adrp x0, L_kuro_data_196@PAGE
    add x0, x0, L_kuro_data_196@PAGEOFF
    str x0, [sp, #1056]
    ldr x0, [sp, #1056]
    bl _kuro_fn_IsWord
    str x0, [sp, #1064]
    ldr x0, [sp, #1064]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1072]
    ldr x0, [sp, #1072]
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #1080]
    mov x0, #1
    str x0, [sp, #1088]
    ldr x0, [sp, #1080]
    ldr x1, [sp, #1088]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1096]
    ldr x0, [sp, #1096]
    cbz w0, L_kuro_fn_ParseStatement_else18
    mov x0, #1
    str x0, [sp, #1104]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1104]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #1112]
    ldr x0, [sp, #1112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1128]
    ldr x0, [sp, #1128]
    str x0, [sp, #176]
    adrp x0, L_kuro_data_197@PAGE
    add x0, x0, L_kuro_data_197@PAGEOFF
    str x0, [sp, #1136]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1136]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #176]
    str x0, [sp, #1144]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1144]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_CurKind
    str x0, [sp, #1152]
    ldr x0, [sp, #1152]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1160]
    ldr x0, [sp, #1160]
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    str x0, [sp, #1168]
    adrp x0, L_kuro_data_198@PAGE
    add x0, x0, L_kuro_data_198@PAGEOFF
    str x0, [sp, #1176]
    ldr x0, [sp, #1168]
    ldr x1, [sp, #1176]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1184]
    ldr x0, [sp, #1184]
    cbz w0, L_kuro_fn_ParseStatement_else20
    adrp x0, L_kuro_data_199@PAGE
    add x0, x0, L_kuro_data_199@PAGEOFF
    str x0, [sp, #1192]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1192]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_ParseStatement_endif21
L_kuro_fn_ParseStatement_else20:
    adrp x0, L_kuro_data_200@PAGE
    add x0, x0, L_kuro_data_200@PAGEOFF
    str x0, [sp, #1200]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1200]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #1216]
    ldr x0, [sp, #1216]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
L_kuro_fn_ParseStatement_endif21:
    adrp x0, L_kuro_data_201@PAGE
    add x0, x0, L_kuro_data_201@PAGEOFF
    str x0, [sp, #1224]
    ldr x0, [sp, #1224]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #1232]
    ldr x0, [sp, #1232]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1240]
    ldr x0, [sp, #1240]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif19
L_kuro_fn_ParseStatement_else18:
L_kuro_fn_ParseStatement_endif19:
    adrp x0, L_kuro_data_202@PAGE
    add x0, x0, L_kuro_data_202@PAGEOFF
    str x0, [sp, #1248]
    ldr x0, [sp, #1248]
    bl _kuro_fn_IsWord
    str x0, [sp, #1256]
    ldr x0, [sp, #1256]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1264]
    ldr x0, [sp, #1264]
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    str x0, [sp, #1272]
    mov x0, #1
    str x0, [sp, #1280]
    ldr x0, [sp, #1272]
    ldr x1, [sp, #1280]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1288]
    ldr x0, [sp, #1288]
    cbz w0, L_kuro_fn_ParseStatement_else22
    mov x0, #1
    str x0, [sp, #1304]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1304]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #1312]
    ldr x0, [sp, #1312]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1320]
    ldr x0, [sp, #1320]
    str x0, [sp, #344]
    adrp x0, L_kuro_data_203@PAGE
    add x0, x0, L_kuro_data_203@PAGEOFF
    str x0, [sp, #1328]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1328]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #344]
    str x0, [sp, #1336]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1336]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_204@PAGE
    add x0, x0, L_kuro_data_204@PAGEOFF
    str x0, [sp, #1344]
    ldr x0, [sp, #1344]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #1352]
    ldr x0, [sp, #1352]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1360]
    ldr x0, [sp, #1360]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif23
L_kuro_fn_ParseStatement_else22:
L_kuro_fn_ParseStatement_endif23:
    adrp x0, L_kuro_data_205@PAGE
    add x0, x0, L_kuro_data_205@PAGEOFF
    str x0, [sp, #1368]
    ldr x0, [sp, #1368]
    bl _kuro_fn_IsWord
    str x0, [sp, #1376]
    ldr x0, [sp, #1376]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1392]
    ldr x0, [sp, #1392]
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    str x0, [sp, #1400]
    mov x0, #1
    str x0, [sp, #1408]
    ldr x0, [sp, #1400]
    ldr x1, [sp, #1408]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1416]
    ldr x0, [sp, #1416]
    cbz w0, L_kuro_fn_ParseStatement_else24
    mov x0, #1
    str x0, [sp, #1424]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1424]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #1432]
    ldr x0, [sp, #1432]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1440]
    ldr x0, [sp, #1440]
    str x0, [sp, #368]
    adrp x0, L_kuro_data_206@PAGE
    add x0, x0, L_kuro_data_206@PAGEOFF
    str x0, [sp, #1448]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1448]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #368]
    str x0, [sp, #1456]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1456]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #1464]
    ldr x0, [sp, #1464]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_207@PAGE
    add x0, x0, L_kuro_data_207@PAGEOFF
    str x0, [sp, #1480]
    ldr x0, [sp, #1480]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #1488]
    ldr x0, [sp, #1488]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #1496]
    ldr x0, [sp, #1496]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_208@PAGE
    add x0, x0, L_kuro_data_208@PAGEOFF
    str x0, [sp, #1504]
    ldr x0, [sp, #1504]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #1512]
    ldr x0, [sp, #1512]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1520]
    ldr x0, [sp, #1520]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif25
L_kuro_fn_ParseStatement_else24:
L_kuro_fn_ParseStatement_endif25:
    adrp x0, L_kuro_data_209@PAGE
    add x0, x0, L_kuro_data_209@PAGEOFF
    str x0, [sp, #1528]
    ldr x0, [sp, #1528]
    bl _kuro_fn_IsWord
    str x0, [sp, #1536]
    ldr x0, [sp, #1536]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1544]
    ldr x0, [sp, #1544]
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    str x0, [sp, #1552]
    mov x0, #1
    str x0, [sp, #1568]
    ldr x0, [sp, #1552]
    ldr x1, [sp, #1568]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1576]
    ldr x0, [sp, #1576]
    cbz w0, L_kuro_fn_ParseStatement_else26
    mov x0, #1
    str x0, [sp, #1584]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1584]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_210@PAGE
    add x0, x0, L_kuro_data_210@PAGEOFF
    str x0, [sp, #1592]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1592]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #1600]
    ldr x0, [sp, #1600]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_211@PAGE
    add x0, x0, L_kuro_data_211@PAGEOFF
    str x0, [sp, #1608]
    ldr x0, [sp, #1608]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #1616]
    ldr x0, [sp, #1616]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #1624]
    ldr x0, [sp, #1624]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1632]
    ldr x0, [sp, #1632]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #1640]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1640]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_212@PAGE
    add x0, x0, L_kuro_data_212@PAGEOFF
    str x0, [sp, #1656]
    ldr x0, [sp, #1656]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #1664]
    ldr x0, [sp, #1664]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1672]
    ldr x0, [sp, #1672]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif27
L_kuro_fn_ParseStatement_else26:
L_kuro_fn_ParseStatement_endif27:
    adrp x0, L_kuro_data_213@PAGE
    add x0, x0, L_kuro_data_213@PAGEOFF
    str x0, [sp, #1680]
    ldr x0, [sp, #1680]
    bl _kuro_fn_IsWord
    str x0, [sp, #1688]
    ldr x0, [sp, #1688]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1696]
    ldr x0, [sp, #1696]
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    str x0, [sp, #1704]
    mov x0, #1
    str x0, [sp, #1712]
    ldr x0, [sp, #1704]
    ldr x1, [sp, #1712]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1720]
    ldr x0, [sp, #1720]
    cbz w0, L_kuro_fn_ParseStatement_else28
    mov x0, #1
    str x0, [sp, #1728]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1728]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #1752]
    ldr x0, [sp, #1752]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1760]
    ldr x0, [sp, #1760]
    str x0, [sp, #144]
    adrp x0, L_kuro_data_214@PAGE
    add x0, x0, L_kuro_data_214@PAGEOFF
    str x0, [sp, #1768]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1768]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #144]
    str x0, [sp, #1776]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1776]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseCondition
    str x0, [sp, #1784]
    ldr x0, [sp, #1784]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_215@PAGE
    add x0, x0, L_kuro_data_215@PAGEOFF
    str x0, [sp, #1792]
    ldr x0, [sp, #1792]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #1800]
    ldr x0, [sp, #1800]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1808]
    ldr x0, [sp, #1808]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif29
L_kuro_fn_ParseStatement_else28:
L_kuro_fn_ParseStatement_endif29:
    adrp x0, L_kuro_data_216@PAGE
    add x0, x0, L_kuro_data_216@PAGEOFF
    str x0, [sp, #1816]
    ldr x0, [sp, #1816]
    bl _kuro_fn_IsWord
    str x0, [sp, #1824]
    ldr x0, [sp, #1824]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1840]
    ldr x0, [sp, #1840]
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    str x0, [sp, #1848]
    mov x0, #1
    str x0, [sp, #1856]
    ldr x0, [sp, #1848]
    ldr x1, [sp, #1856]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1864]
    ldr x0, [sp, #1864]
    cbz w0, L_kuro_fn_ParseStatement_else30
    mov x0, #1
    str x0, [sp, #1872]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1872]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #1880]
    ldr x0, [sp, #1880]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1888]
    ldr x0, [sp, #1888]
    str x0, [sp, #152]
    adrp x0, L_kuro_data_217@PAGE
    add x0, x0, L_kuro_data_217@PAGEOFF
    str x0, [sp, #1896]
    ldr x0, [sp, #1896]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #1904]
    ldr x0, [sp, #1904]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ParseComparisonOp
    str x0, [sp, #1912]
    ldr x0, [sp, #1912]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1928]
    ldr x0, [sp, #1928]
    str x0, [sp, #160]
    adrp x0, L_kuro_data_218@PAGE
    add x0, x0, L_kuro_data_218@PAGEOFF
    str x0, [sp, #1936]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1936]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_219@PAGE
    add x0, x0, L_kuro_data_219@PAGEOFF
    str x0, [sp, #1944]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1944]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_220@PAGE
    add x0, x0, L_kuro_data_220@PAGEOFF
    str x0, [sp, #1952]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1952]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #152]
    str x0, [sp, #1960]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1960]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_221@PAGE
    add x0, x0, L_kuro_data_221@PAGEOFF
    str x0, [sp, #1968]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1968]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #1976]
    ldr x0, [sp, #1976]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_222@PAGE
    add x0, x0, L_kuro_data_222@PAGEOFF
    str x0, [sp, #1984]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1984]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #160]
    str x0, [sp, #1992]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #1992]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_223@PAGE
    add x0, x0, L_kuro_data_223@PAGEOFF
    str x0, [sp, #2000]
    ldr x0, [sp, #2000]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #2016]
    ldr x0, [sp, #2016]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_224@PAGE
    add x0, x0, L_kuro_data_224@PAGEOFF
    str x0, [sp, #2024]
    ldr x0, [sp, #2024]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #2032]
    ldr x0, [sp, #2032]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_225@PAGE
    add x0, x0, L_kuro_data_225@PAGEOFF
    str x0, [sp, #2040]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2040]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #2048]
    ldr x0, [sp, #2048]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_226@PAGE
    add x0, x0, L_kuro_data_226@PAGEOFF
    str x0, [sp, #2056]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2056]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_227@PAGE
    add x0, x0, L_kuro_data_227@PAGEOFF
    str x0, [sp, #2064]
    ldr x0, [sp, #2064]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #2072]
    ldr x0, [sp, #2072]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_228@PAGE
    add x0, x0, L_kuro_data_228@PAGEOFF
    str x0, [sp, #2080]
    ldr x0, [sp, #2080]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #2088]
    ldr x0, [sp, #2088]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_229@PAGE
    add x0, x0, L_kuro_data_229@PAGEOFF
    str x0, [sp, #2104]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2104]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #2112]
    ldr x0, [sp, #2112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_230@PAGE
    add x0, x0, L_kuro_data_230@PAGEOFF
    str x0, [sp, #2120]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2120]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_231@PAGE
    add x0, x0, L_kuro_data_231@PAGEOFF
    str x0, [sp, #2128]
    ldr x0, [sp, #2128]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2136]
    ldr x0, [sp, #2136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2144]
    ldr x0, [sp, #2144]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif31
L_kuro_fn_ParseStatement_else30:
L_kuro_fn_ParseStatement_endif31:
    adrp x0, L_kuro_data_232@PAGE
    add x0, x0, L_kuro_data_232@PAGEOFF
    str x0, [sp, #2152]
    ldr x0, [sp, #2152]
    bl _kuro_fn_IsWord
    str x0, [sp, #2160]
    ldr x0, [sp, #2160]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2168]
    ldr x0, [sp, #2168]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    str x0, [sp, #2176]
    mov x0, #1
    str x0, [sp, #2192]
    ldr x0, [sp, #2176]
    ldr x1, [sp, #2192]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2200]
    ldr x0, [sp, #2200]
    cbz w0, L_kuro_fn_ParseStatement_else32
    mov x0, #1
    str x0, [sp, #2208]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2208]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_233@PAGE
    add x0, x0, L_kuro_data_233@PAGEOFF
    str x0, [sp, #2216]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2216]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #2224]
    ldr x0, [sp, #2224]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_234@PAGE
    add x0, x0, L_kuro_data_234@PAGEOFF
    str x0, [sp, #2232]
    ldr x0, [sp, #2232]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2240]
    ldr x0, [sp, #2240]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2248]
    ldr x0, [sp, #2248]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif33
L_kuro_fn_ParseStatement_else32:
L_kuro_fn_ParseStatement_endif33:
    adrp x0, L_kuro_data_235@PAGE
    add x0, x0, L_kuro_data_235@PAGEOFF
    str x0, [sp, #2256]
    ldr x0, [sp, #2256]
    bl _kuro_fn_IsWord
    str x0, [sp, #2264]
    ldr x0, [sp, #2264]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2280]
    ldr x0, [sp, #2280]
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    str x0, [sp, #2288]
    mov x0, #1
    str x0, [sp, #2296]
    ldr x0, [sp, #2288]
    ldr x1, [sp, #2296]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2304]
    ldr x0, [sp, #2304]
    cbz w0, L_kuro_fn_ParseStatement_else34
    mov x0, #1
    str x0, [sp, #2312]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2312]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #2320]
    ldr x0, [sp, #2320]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2328]
    ldr x0, [sp, #2328]
    str x0, [sp, #136]
    adrp x0, L_kuro_data_236@PAGE
    add x0, x0, L_kuro_data_236@PAGEOFF
    str x0, [sp, #2336]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2336]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #136]
    str x0, [sp, #2344]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2344]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseArgs
    str x0, [sp, #2352]
    ldr x0, [sp, #2352]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_237@PAGE
    add x0, x0, L_kuro_data_237@PAGEOFF
    str x0, [sp, #2368]
    ldr x0, [sp, #2368]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2376]
    ldr x0, [sp, #2376]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2384]
    ldr x0, [sp, #2384]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif35
L_kuro_fn_ParseStatement_else34:
L_kuro_fn_ParseStatement_endif35:
    adrp x0, L_kuro_data_238@PAGE
    add x0, x0, L_kuro_data_238@PAGEOFF
    str x0, [sp, #2392]
    ldr x0, [sp, #2392]
    bl _kuro_fn_IsWord
    str x0, [sp, #2400]
    ldr x0, [sp, #2400]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2408]
    ldr x0, [sp, #2408]
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    str x0, [sp, #2416]
    mov x0, #1
    str x0, [sp, #2424]
    ldr x0, [sp, #2416]
    ldr x1, [sp, #2424]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2432]
    ldr x0, [sp, #2432]
    cbz w0, L_kuro_fn_ParseStatement_else36
    mov x0, #1
    str x0, [sp, #2440]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2440]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_ExpectIdent
    str x0, [sp, #2456]
    ldr x0, [sp, #2456]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2464]
    ldr x0, [sp, #2464]
    str x0, [sp, #112]
    adrp x0, L_kuro_data_239@PAGE
    add x0, x0, L_kuro_data_239@PAGEOFF
    str x0, [sp, #2472]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2472]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #112]
    str x0, [sp, #2480]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2480]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseParams
    str x0, [sp, #2488]
    ldr x0, [sp, #2488]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_240@PAGE
    add x0, x0, L_kuro_data_240@PAGEOFF
    str x0, [sp, #2496]
    ldr x0, [sp, #2496]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2504]
    ldr x0, [sp, #2504]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_241@PAGE
    add x0, x0, L_kuro_data_241@PAGEOFF
    str x0, [sp, #2512]
    adrp x0, L_kuro_data_242@PAGE
    add x0, x0, L_kuro_data_242@PAGEOFF
    str x0, [sp, #2520]
    ldr x0, [sp, #2512]
    ldr x1, [sp, #2520]
    bl _kuro_fn_ParseBlock
    str x0, [sp, #2528]
    ldr x0, [sp, #2528]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_243@PAGE
    add x0, x0, L_kuro_data_243@PAGEOFF
    str x0, [sp, #2544]
    ldr x0, [sp, #2544]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #2552]
    ldr x0, [sp, #2552]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_244@PAGE
    add x0, x0, L_kuro_data_244@PAGEOFF
    str x0, [sp, #2560]
    ldr x0, [sp, #2560]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2568]
    ldr x0, [sp, #2568]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2576]
    ldr x0, [sp, #2576]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif37
L_kuro_fn_ParseStatement_else36:
L_kuro_fn_ParseStatement_endif37:
    adrp x0, L_kuro_data_245@PAGE
    add x0, x0, L_kuro_data_245@PAGEOFF
    str x0, [sp, #2584]
    ldr x0, [sp, #2584]
    bl _kuro_fn_IsWord
    str x0, [sp, #2592]
    ldr x0, [sp, #2592]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2600]
    ldr x0, [sp, #2600]
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #2608]
    mov x0, #1
    str x0, [sp, #2616]
    ldr x0, [sp, #2608]
    ldr x1, [sp, #2616]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2640]
    ldr x0, [sp, #2640]
    cbz w0, L_kuro_fn_ParseStatement_else38
    mov x0, #1
    str x0, [sp, #2648]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2648]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_246@PAGE
    add x0, x0, L_kuro_data_246@PAGEOFF
    str x0, [sp, #2656]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2656]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseCondition
    str x0, [sp, #2664]
    ldr x0, [sp, #2664]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_247@PAGE
    add x0, x0, L_kuro_data_247@PAGEOFF
    str x0, [sp, #2672]
    ldr x0, [sp, #2672]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2680]
    ldr x0, [sp, #2680]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_248@PAGE
    add x0, x0, L_kuro_data_248@PAGEOFF
    str x0, [sp, #2688]
    adrp x0, L_kuro_data_249@PAGE
    add x0, x0, L_kuro_data_249@PAGEOFF
    str x0, [sp, #2696]
    ldr x0, [sp, #2688]
    ldr x1, [sp, #2696]
    bl _kuro_fn_ParseBlock
    str x0, [sp, #2704]
    ldr x0, [sp, #2704]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_250@PAGE
    add x0, x0, L_kuro_data_250@PAGEOFF
    str x0, [sp, #2712]
    ldr x0, [sp, #2712]
    bl _kuro_fn_IsWord
    str x0, [sp, #2728]
    ldr x0, [sp, #2728]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2736]
    ldr x0, [sp, #2736]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    str x0, [sp, #2744]
    mov x0, #1
    str x0, [sp, #2752]
    ldr x0, [sp, #2744]
    ldr x1, [sp, #2752]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2760]
    ldr x0, [sp, #2760]
    cbz w0, L_kuro_fn_ParseStatement_else40
    mov x0, #1
    str x0, [sp, #2768]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2768]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_251@PAGE
    add x0, x0, L_kuro_data_251@PAGEOFF
    str x0, [sp, #2776]
    ldr x0, [sp, #2776]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2784]
    ldr x0, [sp, #2784]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_252@PAGE
    add x0, x0, L_kuro_data_252@PAGEOFF
    str x0, [sp, #2792]
    adrp x0, L_kuro_data_253@PAGE
    add x0, x0, L_kuro_data_253@PAGEOFF
    str x0, [sp, #2800]
    ldr x0, [sp, #2792]
    ldr x1, [sp, #2800]
    bl _kuro_fn_ParseBlock
    str x0, [sp, #2816]
    ldr x0, [sp, #2816]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseStatement_endif41
L_kuro_fn_ParseStatement_else40:
    adrp x0, L_kuro_data_254@PAGE
    add x0, x0, L_kuro_data_254@PAGEOFF
    str x0, [sp, #2824]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2824]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
L_kuro_fn_ParseStatement_endif41:
    adrp x0, L_kuro_data_255@PAGE
    add x0, x0, L_kuro_data_255@PAGEOFF
    str x0, [sp, #2832]
    ldr x0, [sp, #2832]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #2840]
    ldr x0, [sp, #2840]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_256@PAGE
    add x0, x0, L_kuro_data_256@PAGEOFF
    str x0, [sp, #2848]
    ldr x0, [sp, #2848]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2856]
    ldr x0, [sp, #2856]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2864]
    ldr x0, [sp, #2864]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif39
L_kuro_fn_ParseStatement_else38:
L_kuro_fn_ParseStatement_endif39:
    adrp x0, L_kuro_data_257@PAGE
    add x0, x0, L_kuro_data_257@PAGEOFF
    str x0, [sp, #2872]
    ldr x0, [sp, #2872]
    bl _kuro_fn_IsWord
    str x0, [sp, #2880]
    ldr x0, [sp, #2880]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2888]
    ldr x0, [sp, #2888]
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    str x0, [sp, #2904]
    mov x0, #1
    str x0, [sp, #2912]
    ldr x0, [sp, #2904]
    ldr x1, [sp, #2912]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2920]
    ldr x0, [sp, #2920]
    cbz w0, L_kuro_fn_ParseStatement_else42
    mov x0, #1
    str x0, [sp, #2928]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2928]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_258@PAGE
    add x0, x0, L_kuro_data_258@PAGEOFF
    str x0, [sp, #2936]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #2936]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseExpr
    str x0, [sp, #2944]
    ldr x0, [sp, #2944]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_259@PAGE
    add x0, x0, L_kuro_data_259@PAGEOFF
    str x0, [sp, #2952]
    ldr x0, [sp, #2952]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #2960]
    ldr x0, [sp, #2960]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_260@PAGE
    add x0, x0, L_kuro_data_260@PAGEOFF
    str x0, [sp, #2968]
    adrp x0, L_kuro_data_261@PAGE
    add x0, x0, L_kuro_data_261@PAGEOFF
    str x0, [sp, #2976]
    ldr x0, [sp, #2968]
    ldr x1, [sp, #2976]
    bl _kuro_fn_ParseBlock
    str x0, [sp, #2992]
    ldr x0, [sp, #2992]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_262@PAGE
    add x0, x0, L_kuro_data_262@PAGEOFF
    str x0, [sp, #3000]
    ldr x0, [sp, #3000]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #3008]
    ldr x0, [sp, #3008]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_263@PAGE
    add x0, x0, L_kuro_data_263@PAGEOFF
    str x0, [sp, #3016]
    ldr x0, [sp, #3016]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3024]
    ldr x0, [sp, #3024]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3032]
    ldr x0, [sp, #3032]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif43
L_kuro_fn_ParseStatement_else42:
L_kuro_fn_ParseStatement_endif43:
    adrp x0, L_kuro_data_264@PAGE
    add x0, x0, L_kuro_data_264@PAGEOFF
    str x0, [sp, #3040]
    ldr x0, [sp, #3040]
    bl _kuro_fn_IsWord
    str x0, [sp, #3048]
    ldr x0, [sp, #3048]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3056]
    ldr x0, [sp, #3056]
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    str x0, [sp, #3064]
    mov x0, #1
    str x0, [sp, #3080]
    ldr x0, [sp, #3064]
    ldr x1, [sp, #3080]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3088]
    ldr x0, [sp, #3088]
    cbz w0, L_kuro_fn_ParseStatement_else44
    mov x0, #1
    str x0, [sp, #3096]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3096]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_265@PAGE
    add x0, x0, L_kuro_data_265@PAGEOFF
    str x0, [sp, #3104]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #3104]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_ParseCondition
    str x0, [sp, #3112]
    ldr x0, [sp, #3112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_266@PAGE
    add x0, x0, L_kuro_data_266@PAGEOFF
    str x0, [sp, #3120]
    ldr x0, [sp, #3120]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3128]
    ldr x0, [sp, #3128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_267@PAGE
    add x0, x0, L_kuro_data_267@PAGEOFF
    str x0, [sp, #3136]
    adrp x0, L_kuro_data_268@PAGE
    add x0, x0, L_kuro_data_268@PAGEOFF
    str x0, [sp, #3144]
    ldr x0, [sp, #3136]
    ldr x1, [sp, #3144]
    bl _kuro_fn_ParseBlock
    str x0, [sp, #3152]
    ldr x0, [sp, #3152]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_269@PAGE
    add x0, x0, L_kuro_data_269@PAGEOFF
    str x0, [sp, #3168]
    ldr x0, [sp, #3168]
    bl _kuro_fn_ExpectWord
    str x0, [sp, #3176]
    ldr x0, [sp, #3176]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_270@PAGE
    add x0, x0, L_kuro_data_270@PAGEOFF
    str x0, [sp, #3184]
    ldr x0, [sp, #3184]
    bl _kuro_fn_ExpectKind
    str x0, [sp, #3192]
    ldr x0, [sp, #3192]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3200]
    ldr x0, [sp, #3200]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ParseStatement_endif45
L_kuro_fn_ParseStatement_else44:
L_kuro_fn_ParseStatement_endif45:
    bl _kuro_fn_CurValue
    str x0, [sp, #3208]
    ldr x0, [sp, #3208]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3216]
    ldr x0, [sp, #3216]
    str x0, [sp, #128]
    adrp x0, L_kuro_data_271@PAGE
    add x0, x0, L_kuro_data_271@PAGEOFF
    str x0, [sp, #3224]
    ldr x0, [sp, #128]
    str x0, [sp, #3232]
    ldr x0, [sp, #3224]
    ldr x1, [sp, #3232]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3240]
    ldr x0, [sp, #3240]
    ldr x1, [sp, #3224]
    bl _strcpy
    ldr x0, [sp, #3240]
    ldr x1, [sp, #3232]
    bl _strcat
    ldr x0, [sp, #3240]
    str x0, [sp, #352]
    adrp x0, L_kuro_data_272@PAGE
    add x0, x0, L_kuro_data_272@PAGEOFF
    str x0, [sp, #3256]
    ldr x0, [sp, #352]
    str x0, [sp, #3264]
    ldr x0, [sp, #3256]
    ldr x1, [sp, #3264]
    bl _kuro_fn_RecordDiag
    str x0, [sp, #3272]
    ldr x0, [sp, #3272]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3280]
    adrp x0, _kuro_global_218@PAGE
    add x0, x0, _kuro_global_218@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3280]
    add x0, x0, x1
    adrp x2, _kuro_global_218@PAGE
    add x2, x2, _kuro_global_218@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3288]
    ldr x0, [sp, #3288]
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #3856
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseBlockLoop:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #448
    sub sp, sp, x15
    str x0, [sp, #80]
    str x1, [sp, #88]
    bl _kuro_fn_CurKind
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #296]
    adrp x0, L_kuro_data_273@PAGE
    add x0, x0, L_kuro_data_273@PAGEOFF
    str x0, [sp, #384]
    ldr x0, [sp, #296]
    ldr x1, [sp, #384]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    cbz w0, L_kuro_fn_ParseBlockLoop_else0
    mov x0, #0
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    str x0, [sp, #40]
    b L_kuro_fn_ParseBlockLoop_endif1
L_kuro_fn_ParseBlockLoop_else0:
    bl _kuro_fn_CurValue
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    str x0, [sp, #56]
    mov x0, #0
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    str x0, [sp, #24]
    ldr x0, [sp, #32]
    str x0, [sp, #440]
    adrp x0, L_kuro_data_274@PAGE
    add x0, x0, L_kuro_data_274@PAGEOFF
    str x0, [sp, #216]
    ldr x0, [sp, #440]
    ldr x1, [sp, #216]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_ParseBlockLoop_else2
    ldr x0, [sp, #56]
    str x0, [sp, #232]
    ldr x0, [sp, #80]
    str x0, [sp, #240]
    ldr x0, [sp, #232]
    ldr x1, [sp, #240]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    cbz w0, L_kuro_fn_ParseBlockLoop_else4
    mov x0, #1
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #24]
    b L_kuro_fn_ParseBlockLoop_endif5
L_kuro_fn_ParseBlockLoop_else4:
L_kuro_fn_ParseBlockLoop_endif5:
    ldr x0, [sp, #56]
    str x0, [sp, #264]
    ldr x0, [sp, #88]
    str x0, [sp, #272]
    ldr x0, [sp, #264]
    ldr x1, [sp, #272]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    cbz w0, L_kuro_fn_ParseBlockLoop_else6
    mov x0, #1
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    str x0, [sp, #24]
    b L_kuro_fn_ParseBlockLoop_endif7
L_kuro_fn_ParseBlockLoop_else6:
L_kuro_fn_ParseBlockLoop_endif7:
    b L_kuro_fn_ParseBlockLoop_endif3
L_kuro_fn_ParseBlockLoop_else2:
L_kuro_fn_ParseBlockLoop_endif3:
    ldr x0, [sp, #24]
    str x0, [sp, #304]
    mov x0, #1
    str x0, [sp, #312]
    ldr x0, [sp, #304]
    ldr x1, [sp, #312]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    cbz w0, L_kuro_fn_ParseBlockLoop_else8
    mov x0, #0
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    str x0, [sp, #48]
    b L_kuro_fn_ParseBlockLoop_endif9
L_kuro_fn_ParseBlockLoop_else8:
    bl _kuro_fn_ParseStatement
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #344]
    mov x0, #0
    str x0, [sp, #352]
    ldr x0, [sp, #344]
    ldr x1, [sp, #352]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    cbz w0, L_kuro_fn_ParseBlockLoop_else10
    ldr x0, [sp, #80]
    str x0, [sp, #368]
    ldr x0, [sp, #88]
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    bl _kuro_fn_ParseBlockLoop
    str x0, [sp, #392]
    ldr x0, [sp, #392]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ParseBlockLoop_endif11
L_kuro_fn_ParseBlockLoop_else10:
L_kuro_fn_ParseBlockLoop_endif11:
L_kuro_fn_ParseBlockLoop_endif9:
L_kuro_fn_ParseBlockLoop_endif1:
    mov x0, #0
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseBlock:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #80
    sub sp, sp, x15
    str x0, [sp, #16]
    str x1, [sp, #24]
    ldr x0, [sp, #16]
    str x0, [sp, #40]
    ldr x0, [sp, #24]
    str x0, [sp, #48]
    ldr x0, [sp, #40]
    ldr x1, [sp, #48]
    bl _kuro_fn_ParseBlockLoop
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_275@PAGE
    add x0, x0, L_kuro_data_275@PAGEOFF
    str x0, [sp, #64]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #64]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #80
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ParseProgram:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #64
    sub sp, sp, x15
    adrp x0, L_kuro_data_276@PAGE
    add x0, x0, L_kuro_data_276@PAGEOFF
    str x0, [sp, #24]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #24]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_277@PAGE
    add x0, x0, L_kuro_data_277@PAGEOFF
    str x0, [sp, #32]
    adrp x0, L_kuro_data_278@PAGE
    add x0, x0, L_kuro_data_278@PAGEOFF
    str x0, [sp, #40]
    ldr x0, [sp, #32]
    ldr x1, [sp, #40]
    bl _kuro_fn_ParseBlock
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #64
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerAtom:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #400
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    ldr x1, [sp, #88]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #272]
    adrp x0, L_kuro_data_279@PAGE
    add x0, x0, L_kuro_data_279@PAGEOFF
    str x0, [sp, #344]
    ldr x0, [sp, #272]
    ldr x1, [sp, #344]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #352]
    ldr x0, [sp, #16]
    str x0, [sp, #360]
    adrp x0, L_kuro_data_280@PAGE
    add x0, x0, L_kuro_data_280@PAGEOFF
    str x0, [sp, #368]
    ldr x0, [sp, #360]
    ldr x1, [sp, #368]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #376]
    ldr x0, [sp, #352]
    ldr x1, [sp, #376]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #384]
    ldr x0, [sp, #16]
    str x0, [sp, #104]
    adrp x0, L_kuro_data_281@PAGE
    add x0, x0, L_kuro_data_281@PAGEOFF
    str x0, [sp, #112]
    ldr x0, [sp, #104]
    ldr x1, [sp, #112]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #120]
    ldr x0, [sp, #384]
    ldr x1, [sp, #120]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    cbz w0, L_kuro_fn_LowerAtom_else0
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    mov x0, #1
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    add x0, x0, x1
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #160]
    ldr x1, [sp, #160]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_282@PAGE
    add x0, x0, L_kuro_data_282@PAGEOFF
    str x0, [sp, #176]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #176]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #192]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    mov x0, #2
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    add x0, x0, x1
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerAtom_endif1
L_kuro_fn_LowerAtom_else0:
    ldr x0, [sp, #16]
    str x0, [sp, #224]
    adrp x0, L_kuro_data_283@PAGE
    add x0, x0, L_kuro_data_283@PAGEOFF
    str x0, [sp, #232]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_LowerAtom_else2
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    mov x0, #2
    str x0, [sp, #256]
    ldr x0, [sp, #248]
    ldr x1, [sp, #256]
    add x0, x0, x1
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #280]
    ldr x1, [sp, #280]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_284@PAGE
    add x0, x0, L_kuro_data_284@PAGEOFF
    str x0, [sp, #296]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #296]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #304]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #304]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    mov x0, #3
    str x0, [sp, #320]
    ldr x0, [sp, #312]
    ldr x1, [sp, #320]
    add x0, x0, x1
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerAtom_endif3
L_kuro_fn_LowerAtom_else2:
    mov x0, #1
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
L_kuro_fn_LowerAtom_endif3:
L_kuro_fn_LowerAtom_endif1:
    mov x0, #0
    mov x15, #400
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerValue:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #96
    sub sp, sp, x15
    bl _kuro_fn_LowerAtom
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    mov x0, #0
    str x0, [sp, #64]
    ldr x0, [sp, #56]
    ldr x1, [sp, #64]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    cbz w0, L_kuro_fn_LowerValue_else0
    bl _kuro_fn_LowerValueTail
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerValue_endif1
L_kuro_fn_LowerValue_else0:
L_kuro_fn_LowerValue_endif1:
    mov x0, #0
    mov x15, #96
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerValueTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #544
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    ldr x1, [sp, #112]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #296]
    adrp x0, L_kuro_data_285@PAGE
    add x0, x0, L_kuro_data_285@PAGEOFF
    str x0, [sp, #384]
    ldr x0, [sp, #296]
    ldr x1, [sp, #384]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #472]
    ldr x0, [sp, #40]
    str x0, [sp, #504]
    adrp x0, L_kuro_data_286@PAGE
    add x0, x0, L_kuro_data_286@PAGEOFF
    str x0, [sp, #512]
    ldr x0, [sp, #504]
    ldr x1, [sp, #512]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #520]
    ldr x0, [sp, #472]
    ldr x1, [sp, #520]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #528]
    ldr x0, [sp, #40]
    str x0, [sp, #128]
    adrp x0, L_kuro_data_287@PAGE
    add x0, x0, L_kuro_data_287@PAGEOFF
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #144]
    ldr x0, [sp, #528]
    ldr x1, [sp, #144]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_LowerValueTail_else0
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #160]
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    add x0, x0, x1
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #184]
    ldr x1, [sp, #184]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_288@PAGE
    add x0, x0, L_kuro_data_288@PAGEOFF
    str x0, [sp, #200]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #200]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #216]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    mov x0, #2
    str x0, [sp, #232]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    add x0, x0, x1
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValueTail
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerValueTail_endif1
L_kuro_fn_LowerValueTail_else0:
    ldr x0, [sp, #40]
    str x0, [sp, #256]
    adrp x0, L_kuro_data_289@PAGE
    add x0, x0, L_kuro_data_289@PAGEOFF
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    cbz w0, L_kuro_fn_LowerValueTail_else2
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #280]
    mov x0, #2
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    add x0, x0, x1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #312]
    ldr x1, [sp, #312]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_290@PAGE
    add x0, x0, L_kuro_data_290@PAGEOFF
    str x0, [sp, #328]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #328]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #336]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #336]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #344]
    mov x0, #3
    str x0, [sp, #352]
    ldr x0, [sp, #344]
    ldr x1, [sp, #352]
    add x0, x0, x1
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValueTail
    str x0, [sp, #368]
    ldr x0, [sp, #368]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerValueTail_endif3
L_kuro_fn_LowerValueTail_else2:
    ldr x0, [sp, #40]
    str x0, [sp, #376]
    adrp x0, L_kuro_data_291@PAGE
    add x0, x0, L_kuro_data_291@PAGEOFF
    str x0, [sp, #392]
    ldr x0, [sp, #376]
    ldr x1, [sp, #392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    cbz w0, L_kuro_fn_LowerValueTail_else4
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #408]
    mov x0, #1
    str x0, [sp, #416]
    ldr x0, [sp, #408]
    ldr x1, [sp, #416]
    add x0, x0, x1
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #432]
    ldr x1, [sp, #432]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_292@PAGE
    add x0, x0, L_kuro_data_292@PAGEOFF
    str x0, [sp, #448]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #448]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #456]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #456]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #464]
    mov x0, #2
    str x0, [sp, #480]
    ldr x0, [sp, #464]
    ldr x1, [sp, #480]
    add x0, x0, x1
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValueTail
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerValueTail_endif5
L_kuro_fn_LowerValueTail_else4:
L_kuro_fn_LowerValueTail_endif5:
L_kuro_fn_LowerValueTail_endif3:
L_kuro_fn_LowerValueTail_endif1:
    mov x0, #0
    mov x15, #544
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerCondition:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #560
    sub sp, sp, x15
    bl _kuro_fn_LowerValue
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    ldr x1, [sp, #224]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #488]
    adrp x0, L_kuro_data_293@PAGE
    add x0, x0, L_kuro_data_293@PAGEOFF
    str x0, [sp, #520]
    ldr x0, [sp, #488]
    ldr x1, [sp, #520]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #528]
    ldr x0, [sp, #528]
    cbz w0, L_kuro_fn_LowerCondition_else0
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #536]
    mov x0, #1
    str x0, [sp, #544]
    ldr x0, [sp, #536]
    ldr x1, [sp, #544]
    add x0, x0, x1
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #152]
    ldr x1, [sp, #152]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_294@PAGE
    add x0, x0, L_kuro_data_294@PAGEOFF
    str x0, [sp, #168]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #168]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #176]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #176]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #184]
    mov x0, #2
    str x0, [sp, #192]
    ldr x0, [sp, #184]
    ldr x1, [sp, #192]
    add x0, x0, x1
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerConditionTail
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerCondition_endif1
L_kuro_fn_LowerCondition_else0:
    ldr x0, [sp, #40]
    str x0, [sp, #216]
    adrp x0, L_kuro_data_295@PAGE
    add x0, x0, L_kuro_data_295@PAGEOFF
    str x0, [sp, #232]
    ldr x0, [sp, #216]
    ldr x1, [sp, #232]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_LowerCondition_else2
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    mov x0, #1
    str x0, [sp, #256]
    ldr x0, [sp, #248]
    ldr x1, [sp, #256]
    add x0, x0, x1
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #272]
    ldr x1, [sp, #272]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_296@PAGE
    add x0, x0, L_kuro_data_296@PAGEOFF
    str x0, [sp, #288]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #288]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #296]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #296]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #304]
    mov x0, #2
    str x0, [sp, #320]
    ldr x0, [sp, #304]
    ldr x1, [sp, #320]
    add x0, x0, x1
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerConditionTail
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerCondition_endif3
L_kuro_fn_LowerCondition_else2:
    bl _kuro_fn_LowerValue
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #352]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #352]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #360]
    ldr x1, [sp, #360]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #368]
    ldr x0, [sp, #368]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #384]
    adrp x0, L_kuro_data_297@PAGE
    add x0, x0, L_kuro_data_297@PAGEOFF
    str x0, [sp, #392]
    ldr x0, [sp, #384]
    ldr x1, [sp, #392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    cbz w0, L_kuro_fn_LowerCondition_else4
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #416]
    mov x0, #1
    str x0, [sp, #424]
    ldr x0, [sp, #416]
    ldr x1, [sp, #424]
    add x0, x0, x1
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #440]
    ldr x1, [sp, #440]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #448]
    ldr x0, [sp, #448]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_298@PAGE
    add x0, x0, L_kuro_data_298@PAGEOFF
    str x0, [sp, #456]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #456]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #464]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #464]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #472]
    mov x0, #2
    str x0, [sp, #480]
    ldr x0, [sp, #472]
    ldr x1, [sp, #480]
    add x0, x0, x1
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerConditionTail
    str x0, [sp, #504]
    ldr x0, [sp, #504]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerCondition_endif5
L_kuro_fn_LowerCondition_else4:
    mov x0, #1
    str x0, [sp, #512]
    ldr x0, [sp, #512]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
L_kuro_fn_LowerCondition_endif5:
L_kuro_fn_LowerCondition_endif3:
L_kuro_fn_LowerCondition_endif1:
    mov x0, #0
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerConditionTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #416
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    ldr x1, [sp, #112]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #296]
    adrp x0, L_kuro_data_299@PAGE
    add x0, x0, L_kuro_data_299@PAGEOFF
    str x0, [sp, #368]
    ldr x0, [sp, #296]
    ldr x1, [sp, #368]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #376]
    ldr x0, [sp, #32]
    str x0, [sp, #384]
    adrp x0, L_kuro_data_300@PAGE
    add x0, x0, L_kuro_data_300@PAGEOFF
    str x0, [sp, #392]
    ldr x0, [sp, #384]
    ldr x1, [sp, #392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #400]
    ldr x0, [sp, #376]
    ldr x1, [sp, #400]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #408]
    ldr x0, [sp, #32]
    str x0, [sp, #128]
    adrp x0, L_kuro_data_301@PAGE
    add x0, x0, L_kuro_data_301@PAGEOFF
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #144]
    ldr x0, [sp, #408]
    ldr x1, [sp, #144]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #152]
    ldr x0, [sp, #32]
    str x0, [sp, #160]
    adrp x0, L_kuro_data_302@PAGE
    add x0, x0, L_kuro_data_302@PAGEOFF
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #152]
    ldr x1, [sp, #176]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    cbz w0, L_kuro_fn_LowerConditionTail_else0
    bl _kuro_fn_LowerCondition
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #200]
    ldr x1, [sp, #216]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_LowerConditionTail_else2
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    ldr x1, [sp, #232]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #256]
    adrp x0, L_kuro_data_303@PAGE
    add x0, x0, L_kuro_data_303@PAGEOFF
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #272]
    ldr x0, [sp, #24]
    str x0, [sp, #280]
    adrp x0, L_kuro_data_304@PAGE
    add x0, x0, L_kuro_data_304@PAGEOFF
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #304]
    ldr x0, [sp, #272]
    ldr x1, [sp, #304]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    cbz w0, L_kuro_fn_LowerConditionTail_else4
    adrp x0, L_kuro_data_305@PAGE
    add x0, x0, L_kuro_data_305@PAGEOFF
    str x0, [sp, #320]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #320]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #24]
    str x0, [sp, #328]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #328]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #336]
    mov x0, #1
    str x0, [sp, #344]
    ldr x0, [sp, #336]
    ldr x1, [sp, #344]
    add x0, x0, x1
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerConditionTail
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerConditionTail_endif5
L_kuro_fn_LowerConditionTail_else4:
L_kuro_fn_LowerConditionTail_endif5:
    b L_kuro_fn_LowerConditionTail_endif3
L_kuro_fn_LowerConditionTail_else2:
L_kuro_fn_LowerConditionTail_endif3:
    b L_kuro_fn_LowerConditionTail_endif1
L_kuro_fn_LowerConditionTail_else0:
L_kuro_fn_LowerConditionTail_endif1:
    mov x0, #0
    mov x15, #416
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerPrintExpr:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #112
    sub sp, sp, x15
    bl _kuro_fn_LowerValue
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    mov x0, #0
    str x0, [sp, #72]
    ldr x0, [sp, #64]
    ldr x1, [sp, #72]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    cbz w0, L_kuro_fn_LowerPrintExpr_else0
    mov x0, #1
    str x0, [sp, #88]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #88]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_306@PAGE
    add x0, x0, L_kuro_data_306@PAGEOFF
    str x0, [sp, #96]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #96]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerPrintExpr_endif1
L_kuro_fn_LowerPrintExpr_else0:
L_kuro_fn_LowerPrintExpr_endif1:
    mov x0, #0
    mov x15, #112
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerAssign:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #256
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    mov x0, #1
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    add x0, x0, x1
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #200]
    ldr x1, [sp, #200]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    str x0, [sp, #16]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    mov x0, #3
    str x0, [sp, #232]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    add x0, x0, x1
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    mov x0, #0
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    cbz w0, L_kuro_fn_LowerAssign_else0
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerAssignTail
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerAssign_endif1
L_kuro_fn_LowerAssign_else0:
L_kuro_fn_LowerAssign_endif1:
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    mov x0, #0
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_LowerAssign_else2
    adrp x0, L_kuro_data_307@PAGE
    add x0, x0, L_kuro_data_307@PAGEOFF
    str x0, [sp, #176]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #176]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #16]
    str x0, [sp, #184]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #184]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerAssign_endif3
L_kuro_fn_LowerAssign_else2:
L_kuro_fn_LowerAssign_endif3:
    mov x0, #0
    mov x15, #256
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerAssignTail:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #192
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x1, [sp, #80]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #128]
    adrp x0, L_kuro_data_308@PAGE
    add x0, x0, L_kuro_data_308@PAGEOFF
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    cbz w0, L_kuro_fn_LowerAssignTail_else0
    mov x0, #1
    str x0, [sp, #152]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #152]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerAssignTail_endif1
L_kuro_fn_LowerAssignTail_else0:
    bl _kuro_fn_LowerValue
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    mov x0, #0
    str x0, [sp, #176]
    ldr x0, [sp, #168]
    ldr x1, [sp, #176]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    cbz w0, L_kuro_fn_LowerAssignTail_else2
    mov x0, #1
    str x0, [sp, #104]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #104]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerAssignTail
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerAssignTail_endif3
L_kuro_fn_LowerAssignTail_else2:
L_kuro_fn_LowerAssignTail_endif3:
L_kuro_fn_LowerAssignTail_endif1:
    mov x0, #0
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerUpdate:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #208
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #72]
    mov x0, #1
    str x0, [sp, #80]
    ldr x0, [sp, #72]
    ldr x1, [sp, #80]
    add x0, x0, x1
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #144]
    ldr x1, [sp, #144]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    str x0, [sp, #24]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    mov x0, #2
    str x0, [sp, #176]
    ldr x0, [sp, #168]
    ldr x1, [sp, #176]
    add x0, x0, x1
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    mov x0, #0
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    cbz w0, L_kuro_fn_LowerUpdate_else0
    mov x0, #1
    str x0, [sp, #112]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #112]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_309@PAGE
    add x0, x0, L_kuro_data_309@PAGEOFF
    str x0, [sp, #120]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #120]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #24]
    str x0, [sp, #128]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #128]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerUpdate_endif1
L_kuro_fn_LowerUpdate_else0:
L_kuro_fn_LowerUpdate_endif1:
    mov x0, #0
    mov x15, #208
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerAdd:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #64]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #64]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    mov x0, #0
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    cbz w0, L_kuro_fn_LowerAdd_else0
    mov x0, #1
    str x0, [sp, #120]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #120]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x1, [sp, #128]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #8]
    adrp x0, L_kuro_data_310@PAGE
    add x0, x0, L_kuro_data_310@PAGEOFF
    str x0, [sp, #152]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #152]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #80]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #80]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #88]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #88]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerAdd_endif1
L_kuro_fn_LowerAdd_else0:
L_kuro_fn_LowerAdd_endif1:
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerAppend:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #64]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #64]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    mov x0, #0
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    cbz w0, L_kuro_fn_LowerAppend_else0
    mov x0, #1
    str x0, [sp, #120]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #120]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x1, [sp, #128]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #8]
    adrp x0, L_kuro_data_311@PAGE
    add x0, x0, L_kuro_data_311@PAGEOFF
    str x0, [sp, #152]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #152]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #80]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #80]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #88]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #88]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerAppend_endif1
L_kuro_fn_LowerAppend_else0:
L_kuro_fn_LowerAppend_endif1:
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerInputFrom:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #208
    sub sp, sp, x15
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #64]
    ldr x1, [sp, #64]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_77@PAGE
    add x2, x2, _kuro_global_77@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    adrp x0, L_kuro_data_312@PAGE
    add x0, x0, L_kuro_data_312@PAGEOFF
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_LowerInputFrom_else0
    ldr x0, [sp, #32]
    str x0, [sp, #168]
    mov x0, #1
    str x0, [sp, #176]
    ldr x0, [sp, #168]
    ldr x1, [sp, #176]
    add x0, x0, x1
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    mov x15, #208
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_LowerInputFrom_endif1
L_kuro_fn_LowerInputFrom_else0:
    adrp x0, L_kuro_data_313@PAGE
    add x0, x0, L_kuro_data_313@PAGEOFF
    str x0, [sp, #192]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #192]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #80]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #32]
    str x0, [sp, #88]
    mov x0, #1
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_78@PAGE
    add x2, x2, _kuro_global_78@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    bl _kuro_fn_LowerInputFrom
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    mov x15, #208
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_LowerInputFrom_endif1:
    mov x0, #0
    mov x15, #208
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerGet:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #288
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    mov x0, #1
    str x0, [sp, #88]
    ldr x0, [sp, #80]
    ldr x1, [sp, #88]
    add x0, x0, x1
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #232]
    ldr x1, [sp, #232]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    str x0, [sp, #24]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #256]
    mov x0, #2
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    add x0, x0, x1
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #280]
    ldr x1, [sp, #280]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #8]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    mov x0, #3
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    add x0, x0, x1
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #136]
    adrp x0, L_kuro_data_314@PAGE
    add x0, x0, L_kuro_data_314@PAGEOFF
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_LowerGet_else0
    bl _kuro_fn_LowerValue
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #168]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #168]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_315@PAGE
    add x0, x0, L_kuro_data_315@PAGEOFF
    str x0, [sp, #184]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #184]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #24]
    str x0, [sp, #192]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #192]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_316@PAGE
    add x0, x0, L_kuro_data_316@PAGEOFF
    str x0, [sp, #200]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #200]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerGet_endif1
L_kuro_fn_LowerGet_else0:
    adrp x0, L_kuro_data_317@PAGE
    add x0, x0, L_kuro_data_317@PAGEOFF
    str x0, [sp, #208]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #208]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #24]
    str x0, [sp, #216]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #216]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, L_kuro_data_318@PAGE
    add x0, x0, L_kuro_data_318@PAGEOFF
    str x0, [sp, #224]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #224]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
L_kuro_fn_LowerGet_endif1:
    mov x0, #0
    mov x15, #288
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerLength:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #112
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #32]
    mov x0, #1
    str x0, [sp, #40]
    ldr x0, [sp, #32]
    ldr x1, [sp, #40]
    add x0, x0, x1
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #56]
    ldr x1, [sp, #56]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_319@PAGE
    add x0, x0, L_kuro_data_319@PAGEOFF
    str x0, [sp, #72]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #72]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #80]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    mov x0, #2
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #112
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerDecl:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #192
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #48]
    mov x0, #1
    str x0, [sp, #56]
    ldr x0, [sp, #48]
    ldr x1, [sp, #56]
    add x0, x0, x1
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #128]
    ldr x1, [sp, #128]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #8]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    mov x0, #2
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    add x0, x0, x1
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #176]
    ldr x1, [sp, #176]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_320@PAGE
    add x0, x0, L_kuro_data_320@PAGEOFF
    str x0, [sp, #72]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #72]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #80]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #80]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #88]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    mov x0, #3
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    add x0, x0, x1
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerSet:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #48]
    mov x0, #1
    str x0, [sp, #56]
    ldr x0, [sp, #48]
    ldr x1, [sp, #56]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #112]
    ldr x1, [sp, #112]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #16]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    mov x0, #2
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    add x0, x0, x1
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #64]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #64]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #80]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #80]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_321@PAGE
    add x0, x0, L_kuro_data_321@PAGEOFF
    str x0, [sp, #88]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #88]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #16]
    str x0, [sp, #96]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #96]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerCompare:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #144
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #48]
    mov x0, #1
    str x0, [sp, #56]
    ldr x0, [sp, #48]
    ldr x1, [sp, #56]
    add x0, x0, x1
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #88]
    ldr x1, [sp, #88]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #8]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    mov x0, #2
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    add x0, x0, x1
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerCondition
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_322@PAGE
    add x0, x0, L_kuro_data_322@PAGEOFF
    str x0, [sp, #64]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #64]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #72]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #72]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #144
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerCallArgs:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #192
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x1, [sp, #80]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #128]
    adrp x0, L_kuro_data_323@PAGE
    add x0, x0, L_kuro_data_323@PAGEOFF
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    cbz w0, L_kuro_fn_LowerCallArgs_else0
    mov x0, #1
    str x0, [sp, #152]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #152]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerCallArgs_endif1
L_kuro_fn_LowerCallArgs_else0:
    bl _kuro_fn_LowerValue
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #168]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #168]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #176]
    mov x0, #0
    str x0, [sp, #96]
    ldr x0, [sp, #176]
    ldr x1, [sp, #96]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    cbz w0, L_kuro_fn_LowerCallArgs_else2
    bl _kuro_fn_LowerCallArgs
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerCallArgs_endif3
L_kuro_fn_LowerCallArgs_else2:
L_kuro_fn_LowerCallArgs_endif3:
L_kuro_fn_LowerCallArgs_endif1:
    mov x0, #0
    mov x15, #192
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerReturn:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #112
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #56]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #56]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #72]
    mov x0, #0
    str x0, [sp, #80]
    ldr x0, [sp, #72]
    ldr x1, [sp, #80]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    cbz w0, L_kuro_fn_LowerReturn_else0
    mov x0, #1
    str x0, [sp, #96]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #96]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_324@PAGE
    add x0, x0, L_kuro_data_324@PAGEOFF
    str x0, [sp, #104]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #104]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerReturn_endif1
L_kuro_fn_LowerReturn_else0:
L_kuro_fn_LowerReturn_endif1:
    mov x0, #0
    mov x15, #112
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerCall:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #48]
    mov x0, #1
    str x0, [sp, #56]
    ldr x0, [sp, #48]
    ldr x1, [sp, #56]
    add x0, x0, x1
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    str x0, [sp, #96]
    ldr x1, [sp, #96]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #16]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    mov x0, #2
    str x0, [sp, #128]
    ldr x0, [sp, #120]
    ldr x1, [sp, #128]
    add x0, x0, x1
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_325@PAGE
    add x0, x0, L_kuro_data_325@PAGEOFF
    str x0, [sp, #144]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #144]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #16]
    str x0, [sp, #64]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #64]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_LowerCallArgs
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_326@PAGE
    add x0, x0, L_kuro_data_326@PAGEOFF
    str x0, [sp, #80]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #80]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerParams:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #256
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #72]
    ldr x1, [sp, #72]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #192]
    adrp x0, L_kuro_data_327@PAGE
    add x0, x0, L_kuro_data_327@PAGEOFF
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    cbz w0, L_kuro_fn_LowerParams_else0
    mov x0, #1
    str x0, [sp, #216]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #216]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerParams_endif1
L_kuro_fn_LowerParams_else0:
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    mov x0, #1
    str x0, [sp, #232]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    add x0, x0, x1
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #88]
    ldr x1, [sp, #88]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #24]
    adrp x0, L_kuro_data_328@PAGE
    add x0, x0, L_kuro_data_328@PAGEOFF
    str x0, [sp, #112]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #112]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x1, [sp, #120]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #136]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #24]
    str x0, [sp, #144]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #144]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    mov x0, #2
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    add x0, x0, x1
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerParams
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
L_kuro_fn_LowerParams_endif1:
    mov x0, #0
    mov x15, #256
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerAction:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    mov x0, #1
    str x0, [sp, #64]
    ldr x0, [sp, #56]
    ldr x1, [sp, #64]
    add x0, x0, x1
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #120]
    ldr x1, [sp, #120]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    str x0, [sp, #8]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    mov x0, #2
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    add x0, x0, x1
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_329@PAGE
    add x0, x0, L_kuro_data_329@PAGEOFF
    str x0, [sp, #168]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #168]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #72]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #72]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_LowerParams
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerBlock
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #96]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #96]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_330@PAGE
    add x0, x0, L_kuro_data_330@PAGEOFF
    str x0, [sp, #104]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #104]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerIf:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #64]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #64]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerCondition
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    mov x0, #0
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    cbz w0, L_kuro_fn_LowerIf_else0
    adrp x0, L_kuro_data_331@PAGE
    add x0, x0, L_kuro_data_331@PAGEOFF
    str x0, [sp, #120]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #120]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_LowerBlock
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_332@PAGE
    add x0, x0, L_kuro_data_332@PAGEOFF
    str x0, [sp, #144]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #144]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_LowerBlock
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #80]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #80]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_333@PAGE
    add x0, x0, L_kuro_data_333@PAGEOFF
    str x0, [sp, #88]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #88]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerIf_endif1
L_kuro_fn_LowerIf_else0:
L_kuro_fn_LowerIf_endif1:
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerRepeat:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #144
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #64]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #64]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerValue
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    mov x0, #0
    str x0, [sp, #88]
    ldr x0, [sp, #80]
    ldr x1, [sp, #88]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    cbz w0, L_kuro_fn_LowerRepeat_else0
    mov x0, #1
    str x0, [sp, #104]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #104]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_334@PAGE
    add x0, x0, L_kuro_data_334@PAGEOFF
    str x0, [sp, #112]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #112]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_LowerBlock
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #128]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #128]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_335@PAGE
    add x0, x0, L_kuro_data_335@PAGEOFF
    str x0, [sp, #136]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #136]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerRepeat_endif1
L_kuro_fn_LowerRepeat_else0:
L_kuro_fn_LowerRepeat_endif1:
    mov x0, #0
    mov x15, #144
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerWhile:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #144
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #64]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #64]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_336@PAGE
    add x0, x0, L_kuro_data_336@PAGEOFF
    str x0, [sp, #72]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #72]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_LowerCondition
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    mov x0, #0
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    cbz w0, L_kuro_fn_LowerWhile_else0
    adrp x0, L_kuro_data_337@PAGE
    add x0, x0, L_kuro_data_337@PAGEOFF
    str x0, [sp, #112]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #112]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    bl _kuro_fn_LowerBlock
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #128]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #128]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_338@PAGE
    add x0, x0, L_kuro_data_338@PAGEOFF
    str x0, [sp, #136]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #136]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    b L_kuro_fn_LowerWhile_endif1
L_kuro_fn_LowerWhile_else0:
L_kuro_fn_LowerWhile_endif1:
    mov x0, #0
    mov x15, #144
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_LowerBlock:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #1152
    sub sp, sp, x15
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #480]
    ldr x1, [sp, #480]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #576]
    ldr x0, [sp, #576]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    str x0, [sp, #664]
    adrp x0, L_kuro_data_339@PAGE
    add x0, x0, L_kuro_data_339@PAGEOFF
    str x0, [sp, #752]
    ldr x0, [sp, #664]
    ldr x1, [sp, #752]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #840]
    ldr x0, [sp, #840]
    cbz w0, L_kuro_fn_LowerBlock_else0
    mov x0, #1
    str x0, [sp, #928]
    ldr x0, [sp, #928]
    mov x15, #1152
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_LowerBlock_endif1
L_kuro_fn_LowerBlock_else0:
    ldr x0, [sp, #40]
    str x0, [sp, #1016]
    adrp x0, L_kuro_data_340@PAGE
    add x0, x0, L_kuro_data_340@PAGEOFF
    str x0, [sp, #1104]
    ldr x0, [sp, #1016]
    ldr x1, [sp, #1104]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1144]
    ldr x0, [sp, #1144]
    cbz w0, L_kuro_fn_LowerBlock_else2
    bl _kuro_fn_LowerDecl
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif3
L_kuro_fn_LowerBlock_else2:
    ldr x0, [sp, #40]
    str x0, [sp, #504]
    adrp x0, L_kuro_data_341@PAGE
    add x0, x0, L_kuro_data_341@PAGEOFF
    str x0, [sp, #512]
    ldr x0, [sp, #504]
    ldr x1, [sp, #512]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #520]
    ldr x0, [sp, #520]
    cbz w0, L_kuro_fn_LowerBlock_else4
    mov x0, #1
    str x0, [sp, #528]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #528]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_LowerPrintExpr
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif5
L_kuro_fn_LowerBlock_else4:
    ldr x0, [sp, #40]
    str x0, [sp, #544]
    adrp x0, L_kuro_data_342@PAGE
    add x0, x0, L_kuro_data_342@PAGEOFF
    str x0, [sp, #552]
    ldr x0, [sp, #544]
    ldr x1, [sp, #552]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #560]
    ldr x0, [sp, #560]
    cbz w0, L_kuro_fn_LowerBlock_else6
    bl _kuro_fn_LowerAssign
    str x0, [sp, #568]
    ldr x0, [sp, #568]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif7
L_kuro_fn_LowerBlock_else6:
    ldr x0, [sp, #40]
    str x0, [sp, #584]
    adrp x0, L_kuro_data_343@PAGE
    add x0, x0, L_kuro_data_343@PAGEOFF
    str x0, [sp, #592]
    ldr x0, [sp, #584]
    ldr x1, [sp, #592]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #600]
    ldr x0, [sp, #600]
    cbz w0, L_kuro_fn_LowerBlock_else8
    bl _kuro_fn_LowerUpdate
    str x0, [sp, #608]
    ldr x0, [sp, #608]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif9
L_kuro_fn_LowerBlock_else8:
    ldr x0, [sp, #40]
    str x0, [sp, #616]
    adrp x0, L_kuro_data_344@PAGE
    add x0, x0, L_kuro_data_344@PAGEOFF
    str x0, [sp, #624]
    ldr x0, [sp, #616]
    ldr x1, [sp, #624]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #632]
    ldr x0, [sp, #632]
    cbz w0, L_kuro_fn_LowerBlock_else10
    bl _kuro_fn_LowerAdd
    str x0, [sp, #640]
    ldr x0, [sp, #640]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif11
L_kuro_fn_LowerBlock_else10:
    ldr x0, [sp, #40]
    str x0, [sp, #648]
    adrp x0, L_kuro_data_345@PAGE
    add x0, x0, L_kuro_data_345@PAGEOFF
    str x0, [sp, #656]
    ldr x0, [sp, #648]
    ldr x1, [sp, #656]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #672]
    ldr x0, [sp, #672]
    cbz w0, L_kuro_fn_LowerBlock_else12
    bl _kuro_fn_LowerAppend
    str x0, [sp, #680]
    ldr x0, [sp, #680]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif13
L_kuro_fn_LowerBlock_else12:
    ldr x0, [sp, #40]
    str x0, [sp, #688]
    adrp x0, L_kuro_data_346@PAGE
    add x0, x0, L_kuro_data_346@PAGEOFF
    str x0, [sp, #696]
    ldr x0, [sp, #688]
    ldr x1, [sp, #696]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #704]
    ldr x0, [sp, #704]
    cbz w0, L_kuro_fn_LowerBlock_else14
    bl _kuro_fn_LowerIf
    str x0, [sp, #712]
    ldr x0, [sp, #712]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif15
L_kuro_fn_LowerBlock_else14:
    ldr x0, [sp, #40]
    str x0, [sp, #720]
    adrp x0, L_kuro_data_347@PAGE
    add x0, x0, L_kuro_data_347@PAGEOFF
    str x0, [sp, #728]
    ldr x0, [sp, #720]
    ldr x1, [sp, #728]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #736]
    ldr x0, [sp, #736]
    cbz w0, L_kuro_fn_LowerBlock_else16
    bl _kuro_fn_LowerRepeat
    str x0, [sp, #744]
    ldr x0, [sp, #744]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif17
L_kuro_fn_LowerBlock_else16:
    ldr x0, [sp, #40]
    str x0, [sp, #760]
    adrp x0, L_kuro_data_348@PAGE
    add x0, x0, L_kuro_data_348@PAGEOFF
    str x0, [sp, #768]
    ldr x0, [sp, #760]
    ldr x1, [sp, #768]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #776]
    ldr x0, [sp, #776]
    cbz w0, L_kuro_fn_LowerBlock_else18
    bl _kuro_fn_LowerWhile
    str x0, [sp, #784]
    ldr x0, [sp, #784]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif19
L_kuro_fn_LowerBlock_else18:
    ldr x0, [sp, #40]
    str x0, [sp, #792]
    adrp x0, L_kuro_data_349@PAGE
    add x0, x0, L_kuro_data_349@PAGEOFF
    str x0, [sp, #800]
    ldr x0, [sp, #792]
    ldr x1, [sp, #800]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #808]
    ldr x0, [sp, #808]
    cbz w0, L_kuro_fn_LowerBlock_else20
    bl _kuro_fn_LowerReturn
    str x0, [sp, #816]
    ldr x0, [sp, #816]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif21
L_kuro_fn_LowerBlock_else20:
    ldr x0, [sp, #40]
    str x0, [sp, #824]
    adrp x0, L_kuro_data_350@PAGE
    add x0, x0, L_kuro_data_350@PAGEOFF
    str x0, [sp, #832]
    ldr x0, [sp, #824]
    ldr x1, [sp, #832]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #848]
    ldr x0, [sp, #848]
    cbz w0, L_kuro_fn_LowerBlock_else22
    bl _kuro_fn_LowerCall
    str x0, [sp, #856]
    ldr x0, [sp, #856]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif23
L_kuro_fn_LowerBlock_else22:
    ldr x0, [sp, #40]
    str x0, [sp, #864]
    adrp x0, L_kuro_data_351@PAGE
    add x0, x0, L_kuro_data_351@PAGEOFF
    str x0, [sp, #872]
    ldr x0, [sp, #864]
    ldr x1, [sp, #872]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #880]
    ldr x0, [sp, #880]
    cbz w0, L_kuro_fn_LowerBlock_else24
    bl _kuro_fn_LowerAction
    str x0, [sp, #888]
    ldr x0, [sp, #888]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif25
L_kuro_fn_LowerBlock_else24:
    ldr x0, [sp, #40]
    str x0, [sp, #896]
    adrp x0, L_kuro_data_352@PAGE
    add x0, x0, L_kuro_data_352@PAGEOFF
    str x0, [sp, #904]
    ldr x0, [sp, #896]
    ldr x1, [sp, #904]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #912]
    ldr x0, [sp, #912]
    cbz w0, L_kuro_fn_LowerBlock_else26
    mov x0, #1
    str x0, [sp, #920]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #920]
    add x0, x0, x1
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #936]
    ldr x0, [sp, #936]
    bl _kuro_fn_LowerInputFrom
    str x0, [sp, #944]
    ldr x0, [sp, #944]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #952]
    ldr x0, [sp, #952]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif27
L_kuro_fn_LowerBlock_else26:
    ldr x0, [sp, #40]
    str x0, [sp, #960]
    adrp x0, L_kuro_data_353@PAGE
    add x0, x0, L_kuro_data_353@PAGEOFF
    str x0, [sp, #968]
    ldr x0, [sp, #960]
    ldr x1, [sp, #968]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #976]
    ldr x0, [sp, #976]
    cbz w0, L_kuro_fn_LowerBlock_else28
    bl _kuro_fn_LowerGet
    str x0, [sp, #984]
    ldr x0, [sp, #984]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif29
L_kuro_fn_LowerBlock_else28:
    ldr x0, [sp, #40]
    str x0, [sp, #992]
    adrp x0, L_kuro_data_354@PAGE
    add x0, x0, L_kuro_data_354@PAGEOFF
    str x0, [sp, #1000]
    ldr x0, [sp, #992]
    ldr x1, [sp, #1000]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1008]
    ldr x0, [sp, #1008]
    cbz w0, L_kuro_fn_LowerBlock_else30
    bl _kuro_fn_LowerLength
    str x0, [sp, #1024]
    ldr x0, [sp, #1024]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif31
L_kuro_fn_LowerBlock_else30:
    ldr x0, [sp, #40]
    str x0, [sp, #1032]
    adrp x0, L_kuro_data_355@PAGE
    add x0, x0, L_kuro_data_355@PAGEOFF
    str x0, [sp, #1040]
    ldr x0, [sp, #1032]
    ldr x1, [sp, #1040]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1048]
    ldr x0, [sp, #1048]
    cbz w0, L_kuro_fn_LowerBlock_else32
    bl _kuro_fn_LowerSet
    str x0, [sp, #1056]
    ldr x0, [sp, #1056]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif33
L_kuro_fn_LowerBlock_else32:
    ldr x0, [sp, #40]
    str x0, [sp, #1064]
    adrp x0, L_kuro_data_356@PAGE
    add x0, x0, L_kuro_data_356@PAGEOFF
    str x0, [sp, #1072]
    ldr x0, [sp, #1064]
    ldr x1, [sp, #1072]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1080]
    ldr x0, [sp, #1080]
    cbz w0, L_kuro_fn_LowerBlock_else34
    bl _kuro_fn_LowerCompare
    str x0, [sp, #1088]
    ldr x0, [sp, #1088]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif35
L_kuro_fn_LowerBlock_else34:
    mov x0, #1
    str x0, [sp, #1096]
    ldr x0, [sp, #1096]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
L_kuro_fn_LowerBlock_endif35:
L_kuro_fn_LowerBlock_endif33:
L_kuro_fn_LowerBlock_endif31:
L_kuro_fn_LowerBlock_endif29:
L_kuro_fn_LowerBlock_endif27:
L_kuro_fn_LowerBlock_endif25:
L_kuro_fn_LowerBlock_endif23:
L_kuro_fn_LowerBlock_endif21:
L_kuro_fn_LowerBlock_endif19:
L_kuro_fn_LowerBlock_endif17:
L_kuro_fn_LowerBlock_endif15:
L_kuro_fn_LowerBlock_endif13:
L_kuro_fn_LowerBlock_endif11:
L_kuro_fn_LowerBlock_endif9:
L_kuro_fn_LowerBlock_endif7:
L_kuro_fn_LowerBlock_endif5:
L_kuro_fn_LowerBlock_endif3:
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1112]
    mov x0, #0
    str x0, [sp, #1120]
    ldr x0, [sp, #1112]
    ldr x1, [sp, #1120]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1128]
    ldr x0, [sp, #1128]
    cbz w0, L_kuro_fn_LowerBlock_else36
    bl _kuro_fn_LowerBlock
    str x0, [sp, #1136]
    ldr x0, [sp, #1136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_LowerBlock_endif37
L_kuro_fn_LowerBlock_else36:
L_kuro_fn_LowerBlock_endif37:
L_kuro_fn_LowerBlock_endif1:
    mov x0, #0
    mov x15, #1152
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_BytecodeConsume:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    str x0, [sp, #32]
    ldr x0, [sp, #32]
    str x0, [sp, #64]
    mov x0, #0
    str x0, [sp, #72]
    ldr x0, [sp, #64]
    ldr x1, [sp, #72]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    cbz w0, L_kuro_fn_BytecodeConsume_else0
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    ldr x1, [sp, #104]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    adrp x1, _kuro_collection_len_1@PAGE
    add x1, x1, _kuro_collection_len_1@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #120]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_1@PAGE
    add x2, x2, _kuro_collection_len_1@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #128]
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #128]
    add x0, x0, x1
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #32]
    str x0, [sp, #136]
    mov x0, #1
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    sub x0, x0, x1
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    str x0, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    bl _kuro_fn_BytecodeConsume
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_BytecodeConsume_endif1
L_kuro_fn_BytecodeConsume_else0:
L_kuro_fn_BytecodeConsume_endif1:
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_BytecodeStep:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #1248
    sub sp, sp, x15
    adrp x0, _kuro_collection_len_6@PAGE
    add x0, x0, _kuro_collection_len_6@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_4@PAGE
    add x2, x2, _kuro_global_4@PAGEOFF
    str x0, [x2]
L_kuro_fn_BytecodeStep_while_start0:
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #528]
    adrp x0, _kuro_global_4@PAGE
    add x0, x0, _kuro_global_4@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #616]
    ldr x0, [sp, #528]
    ldr x1, [sp, #616]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #704]
    adrp x0, _kuro_global_3@PAGE
    add x0, x0, _kuro_global_3@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #792]
    mov x0, #0
    str x0, [sp, #880]
    ldr x0, [sp, #792]
    ldr x1, [sp, #880]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #968]
    ldr x0, [sp, #704]
    ldr x1, [sp, #968]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #1056]
    ldr x0, [sp, #1056]
    cbz w0, L_kuro_fn_BytecodeStep_while_end1
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1144]
    ldr x1, [sp, #1144]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    str x0, [sp, #40]
    adrp x0, L_kuro_data_357@PAGE
    add x0, x0, L_kuro_data_357@PAGEOFF
    str x0, [sp, #312]
    ldr x0, [sp, #40]
    str x0, [sp, #400]
    ldr x0, [sp, #312]
    ldr x1, [sp, #400]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #480]
    ldr x0, [sp, #480]
    ldr x1, [sp, #312]
    bl _strcpy
    ldr x0, [sp, #480]
    ldr x1, [sp, #400]
    bl _strcat
    adrp x1, _kuro_collection_len_1@PAGE
    add x1, x1, _kuro_collection_len_1@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #480]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_1@PAGE
    add x2, x2, _kuro_collection_len_1@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #488]
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #488]
    add x0, x0, x1
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #40]
    str x0, [sp, #496]
    adrp x0, L_kuro_data_358@PAGE
    add x0, x0, L_kuro_data_358@PAGEOFF
    str x0, [sp, #504]
    ldr x0, [sp, #496]
    ldr x1, [sp, #504]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #512]
    ldr x0, [sp, #40]
    str x0, [sp, #520]
    adrp x0, L_kuro_data_359@PAGE
    add x0, x0, L_kuro_data_359@PAGEOFF
    str x0, [sp, #536]
    ldr x0, [sp, #520]
    ldr x1, [sp, #536]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #544]
    ldr x0, [sp, #512]
    ldr x1, [sp, #544]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #552]
    ldr x0, [sp, #40]
    str x0, [sp, #560]
    adrp x0, L_kuro_data_360@PAGE
    add x0, x0, L_kuro_data_360@PAGEOFF
    str x0, [sp, #568]
    ldr x0, [sp, #560]
    ldr x1, [sp, #568]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #576]
    ldr x0, [sp, #552]
    ldr x1, [sp, #576]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #584]
    ldr x0, [sp, #40]
    str x0, [sp, #592]
    adrp x0, L_kuro_data_361@PAGE
    add x0, x0, L_kuro_data_361@PAGEOFF
    str x0, [sp, #600]
    ldr x0, [sp, #592]
    ldr x1, [sp, #600]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #608]
    ldr x0, [sp, #584]
    ldr x1, [sp, #608]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #624]
    ldr x0, [sp, #40]
    str x0, [sp, #632]
    adrp x0, L_kuro_data_362@PAGE
    add x0, x0, L_kuro_data_362@PAGEOFF
    str x0, [sp, #640]
    ldr x0, [sp, #632]
    ldr x1, [sp, #640]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #648]
    ldr x0, [sp, #624]
    ldr x1, [sp, #648]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #656]
    ldr x0, [sp, #40]
    str x0, [sp, #664]
    adrp x0, L_kuro_data_363@PAGE
    add x0, x0, L_kuro_data_363@PAGEOFF
    str x0, [sp, #672]
    ldr x0, [sp, #664]
    ldr x1, [sp, #672]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #680]
    ldr x0, [sp, #656]
    ldr x1, [sp, #680]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #688]
    ldr x0, [sp, #40]
    str x0, [sp, #696]
    adrp x0, L_kuro_data_364@PAGE
    add x0, x0, L_kuro_data_364@PAGEOFF
    str x0, [sp, #712]
    ldr x0, [sp, #696]
    ldr x1, [sp, #712]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #720]
    ldr x0, [sp, #688]
    ldr x1, [sp, #720]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #728]
    ldr x0, [sp, #40]
    str x0, [sp, #736]
    adrp x0, L_kuro_data_365@PAGE
    add x0, x0, L_kuro_data_365@PAGEOFF
    str x0, [sp, #744]
    ldr x0, [sp, #736]
    ldr x1, [sp, #744]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #752]
    ldr x0, [sp, #728]
    ldr x1, [sp, #752]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #760]
    ldr x0, [sp, #40]
    str x0, [sp, #768]
    adrp x0, L_kuro_data_366@PAGE
    add x0, x0, L_kuro_data_366@PAGEOFF
    str x0, [sp, #776]
    ldr x0, [sp, #768]
    ldr x1, [sp, #776]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #784]
    ldr x0, [sp, #760]
    ldr x1, [sp, #784]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #800]
    ldr x0, [sp, #40]
    str x0, [sp, #808]
    adrp x0, L_kuro_data_367@PAGE
    add x0, x0, L_kuro_data_367@PAGEOFF
    str x0, [sp, #816]
    ldr x0, [sp, #808]
    ldr x1, [sp, #816]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #824]
    ldr x0, [sp, #800]
    ldr x1, [sp, #824]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #832]
    ldr x0, [sp, #40]
    str x0, [sp, #840]
    adrp x0, L_kuro_data_368@PAGE
    add x0, x0, L_kuro_data_368@PAGEOFF
    str x0, [sp, #848]
    ldr x0, [sp, #840]
    ldr x1, [sp, #848]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #856]
    ldr x0, [sp, #832]
    ldr x1, [sp, #856]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #864]
    ldr x0, [sp, #40]
    str x0, [sp, #872]
    adrp x0, L_kuro_data_369@PAGE
    add x0, x0, L_kuro_data_369@PAGEOFF
    str x0, [sp, #888]
    ldr x0, [sp, #872]
    ldr x1, [sp, #888]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #896]
    ldr x0, [sp, #864]
    ldr x1, [sp, #896]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #904]
    ldr x0, [sp, #40]
    str x0, [sp, #912]
    adrp x0, L_kuro_data_370@PAGE
    add x0, x0, L_kuro_data_370@PAGEOFF
    str x0, [sp, #920]
    ldr x0, [sp, #912]
    ldr x1, [sp, #920]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #928]
    ldr x0, [sp, #904]
    ldr x1, [sp, #928]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #936]
    ldr x0, [sp, #40]
    str x0, [sp, #944]
    adrp x0, L_kuro_data_371@PAGE
    add x0, x0, L_kuro_data_371@PAGEOFF
    str x0, [sp, #952]
    ldr x0, [sp, #944]
    ldr x1, [sp, #952]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #960]
    ldr x0, [sp, #936]
    ldr x1, [sp, #960]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #976]
    ldr x0, [sp, #40]
    str x0, [sp, #984]
    adrp x0, L_kuro_data_372@PAGE
    add x0, x0, L_kuro_data_372@PAGEOFF
    str x0, [sp, #992]
    ldr x0, [sp, #984]
    ldr x1, [sp, #992]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1000]
    ldr x0, [sp, #976]
    ldr x1, [sp, #1000]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1008]
    ldr x0, [sp, #1008]
    cbz w0, L_kuro_fn_BytecodeStep_else3
    mov x0, #1
    str x0, [sp, #1016]
    ldr x0, [sp, #1016]
    bl _kuro_fn_BytecodeConsume
    str x0, [sp, #1024]
    ldr x0, [sp, #1024]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_BytecodeStep_endif4
L_kuro_fn_BytecodeStep_else3:
    ldr x0, [sp, #40]
    str x0, [sp, #1032]
    adrp x0, L_kuro_data_373@PAGE
    add x0, x0, L_kuro_data_373@PAGEOFF
    str x0, [sp, #1040]
    ldr x0, [sp, #1032]
    ldr x1, [sp, #1040]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1048]
    ldr x0, [sp, #1048]
    cbz w0, L_kuro_fn_BytecodeStep_else5
    mov x0, #2
    str x0, [sp, #1064]
    ldr x0, [sp, #1064]
    bl _kuro_fn_BytecodeConsume
    str x0, [sp, #1072]
    ldr x0, [sp, #1072]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_BytecodeStep_endif6
L_kuro_fn_BytecodeStep_else5:
    ldr x0, [sp, #40]
    str x0, [sp, #1080]
    adrp x0, L_kuro_data_374@PAGE
    add x0, x0, L_kuro_data_374@PAGEOFF
    str x0, [sp, #1088]
    ldr x0, [sp, #1080]
    ldr x1, [sp, #1088]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1096]
    ldr x0, [sp, #40]
    str x0, [sp, #1104]
    adrp x0, L_kuro_data_375@PAGE
    add x0, x0, L_kuro_data_375@PAGEOFF
    str x0, [sp, #1112]
    ldr x0, [sp, #1104]
    ldr x1, [sp, #1112]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1120]
    ldr x0, [sp, #1096]
    ldr x1, [sp, #1120]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1128]
    ldr x0, [sp, #1128]
    cbz w0, L_kuro_fn_BytecodeStep_else7
    mov x0, #2
    str x0, [sp, #1136]
    ldr x0, [sp, #1136]
    bl _kuro_fn_BytecodeConsume
    str x0, [sp, #1152]
    ldr x0, [sp, #1152]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_BytecodeStep_endif8
L_kuro_fn_BytecodeStep_else7:
    ldr x0, [sp, #40]
    str x0, [sp, #1160]
    adrp x0, L_kuro_data_376@PAGE
    add x0, x0, L_kuro_data_376@PAGEOFF
    str x0, [sp, #1168]
    ldr x0, [sp, #1160]
    ldr x1, [sp, #1168]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1176]
    ldr x0, [sp, #40]
    str x0, [sp, #1184]
    adrp x0, L_kuro_data_377@PAGE
    add x0, x0, L_kuro_data_377@PAGEOFF
    str x0, [sp, #1192]
    ldr x0, [sp, #1184]
    ldr x1, [sp, #1192]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1200]
    ldr x0, [sp, #1176]
    ldr x1, [sp, #1200]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1208]
    ldr x0, [sp, #40]
    str x0, [sp, #1216]
    adrp x0, L_kuro_data_378@PAGE
    add x0, x0, L_kuro_data_378@PAGEOFF
    str x0, [sp, #1224]
    ldr x0, [sp, #1216]
    ldr x1, [sp, #1224]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #144]
    ldr x0, [sp, #1208]
    ldr x1, [sp, #144]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #152]
    ldr x0, [sp, #40]
    str x0, [sp, #160]
    adrp x0, L_kuro_data_379@PAGE
    add x0, x0, L_kuro_data_379@PAGEOFF
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #152]
    ldr x1, [sp, #176]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #184]
    ldr x0, [sp, #40]
    str x0, [sp, #192]
    adrp x0, L_kuro_data_380@PAGE
    add x0, x0, L_kuro_data_380@PAGEOFF
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #208]
    ldr x0, [sp, #184]
    ldr x1, [sp, #208]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #216]
    ldr x0, [sp, #40]
    str x0, [sp, #232]
    adrp x0, L_kuro_data_381@PAGE
    add x0, x0, L_kuro_data_381@PAGEOFF
    str x0, [sp, #240]
    ldr x0, [sp, #232]
    ldr x1, [sp, #240]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #248]
    ldr x0, [sp, #216]
    ldr x1, [sp, #248]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #256]
    ldr x0, [sp, #40]
    str x0, [sp, #264]
    adrp x0, L_kuro_data_382@PAGE
    add x0, x0, L_kuro_data_382@PAGEOFF
    str x0, [sp, #272]
    ldr x0, [sp, #264]
    ldr x1, [sp, #272]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #280]
    ldr x0, [sp, #256]
    ldr x1, [sp, #280]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #288]
    ldr x0, [sp, #40]
    str x0, [sp, #296]
    adrp x0, L_kuro_data_383@PAGE
    add x0, x0, L_kuro_data_383@PAGEOFF
    str x0, [sp, #304]
    ldr x0, [sp, #296]
    ldr x1, [sp, #304]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #320]
    ldr x0, [sp, #288]
    ldr x1, [sp, #320]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #328]
    ldr x0, [sp, #40]
    str x0, [sp, #336]
    adrp x0, L_kuro_data_384@PAGE
    add x0, x0, L_kuro_data_384@PAGEOFF
    str x0, [sp, #344]
    ldr x0, [sp, #336]
    ldr x1, [sp, #344]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #352]
    ldr x0, [sp, #328]
    ldr x1, [sp, #352]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #360]
    ldr x0, [sp, #40]
    str x0, [sp, #368]
    adrp x0, L_kuro_data_385@PAGE
    add x0, x0, L_kuro_data_385@PAGEOFF
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #384]
    ldr x0, [sp, #360]
    ldr x1, [sp, #384]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #392]
    ldr x0, [sp, #40]
    str x0, [sp, #408]
    adrp x0, L_kuro_data_386@PAGE
    add x0, x0, L_kuro_data_386@PAGEOFF
    str x0, [sp, #416]
    ldr x0, [sp, #408]
    ldr x1, [sp, #416]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #424]
    ldr x0, [sp, #392]
    ldr x1, [sp, #424]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #432]
    ldr x0, [sp, #40]
    str x0, [sp, #440]
    adrp x0, L_kuro_data_387@PAGE
    add x0, x0, L_kuro_data_387@PAGEOFF
    str x0, [sp, #448]
    ldr x0, [sp, #440]
    ldr x1, [sp, #448]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #456]
    ldr x0, [sp, #432]
    ldr x1, [sp, #456]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    cbz w0, L_kuro_fn_BytecodeStep_else9
    b L_kuro_fn_BytecodeStep_endif10
L_kuro_fn_BytecodeStep_else9:
    mov x0, #1
    str x0, [sp, #472]
    ldr x0, [sp, #472]
    adrp x2, _kuro_global_3@PAGE
    add x2, x2, _kuro_global_3@PAGEOFF
    str x0, [x2]
L_kuro_fn_BytecodeStep_endif10:
L_kuro_fn_BytecodeStep_endif8:
L_kuro_fn_BytecodeStep_endif6:
L_kuro_fn_BytecodeStep_endif4:
    b L_kuro_fn_BytecodeStep_while_start0
L_kuro_fn_BytecodeStep_while_end1:
    mov x0, #0
    mov x15, #1248
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_CompilerRun:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #272
    sub sp, sp, x15
    adrp x0, _kuro_global_144@PAGE
    add x0, x0, _kuro_global_144@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    mov x0, #0
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    cbz w0, L_kuro_fn_CompilerRun_else0
    mov x0, #1
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_CompilerRun_endif1
L_kuro_fn_CompilerRun_else0:
L_kuro_fn_CompilerRun_endif1:
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    mov x0, #0
    str x0, [sp, #232]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_CompilerRun_else2
    mov x0, #1
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_CompilerRun_endif3
L_kuro_fn_CompilerRun_else2:
L_kuro_fn_CompilerRun_endif3:
    adrp x0, _kuro_global_3@PAGE
    add x0, x0, _kuro_global_3@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #256]
    mov x0, #0
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    cbz w0, L_kuro_fn_CompilerRun_else4
    mov x0, #1
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_CompilerRun_endif5
L_kuro_fn_CompilerRun_else4:
L_kuro_fn_CompilerRun_endif5:
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #160]
    mov x0, #0
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    cbz w0, L_kuro_fn_CompilerRun_else6
    adrp x0, _kuro_collection_len_1@PAGE
    add x0, x0, _kuro_collection_len_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_221@PAGE
    add x2, x2, _kuro_global_221@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_221@PAGE
    add x0, x0, _kuro_global_221@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_14@PAGE
    add x2, x2, _kuro_global_14@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_collection_1@PAGE
    add x0, x0, _kuro_collection_1@PAGEOFF
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_15@PAGE
    add x2, x2, _kuro_global_15@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_CompilerRun_endif7
L_kuro_fn_CompilerRun_else6:
L_kuro_fn_CompilerRun_endif7:
    mov x0, #0
    mov x15, #272
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
.section __TEXT,__cstring
L_kuro_data_0: .asciz "\""
L_kuro_data_1: .asciz "\\"
L_kuro_data_2: .asciz "#"
L_kuro_data_3: .asciz "/"
L_kuro_data_4: .asciz "\n"
L_kuro_data_5: .asciz "\t"
L_kuro_data_6: .asciz "\r"
L_kuro_data_7: .asciz "_"
L_kuro_data_8: .asciz "="
L_kuro_data_9: .asciz ","
L_kuro_data_10: .asciz ";"
L_kuro_data_11: .asciz "."
L_kuro_data_12: .asciz "("
L_kuro_data_13: .asciz ")"
L_kuro_data_14: .asciz "@"
L_kuro_data_15: .asciz "+"
L_kuro_data_16: .asciz "-"
L_kuro_data_17: .asciz "*"
L_kuro_data_18: .asciz ":"
L_kuro_data_19: .asciz "n"
L_kuro_data_20: .asciz "t"
L_kuro_data_21: .asciz "r"
L_kuro_data_22: .asciz ""
L_kuro_data_23: .asciz "STRING"
L_kuro_data_24: .asciz ""
L_kuro_data_25: .asciz "DECIMAL"
L_kuro_data_26: .asciz "INTEGER"
L_kuro_data_27: .asciz ""
L_kuro_data_28: .asciz "IDENT"
L_kuro_data_29: .asciz "EQUAL"
L_kuro_data_30: .asciz "COMMA"
L_kuro_data_31: .asciz "SEMI"
L_kuro_data_32: .asciz "DOT"
L_kuro_data_33: .asciz "LPAREN"
L_kuro_data_34: .asciz "RPAREN"
L_kuro_data_35: .asciz "AT"
L_kuro_data_36: .asciz "PLUS"
L_kuro_data_37: .asciz "MINUS"
L_kuro_data_38: .asciz "STAR"
L_kuro_data_39: .asciz "SLASH"
L_kuro_data_40: .asciz "COLON"
L_kuro_data_41: .asciz "\\"
L_kuro_data_42: .asciz "kuro.bytecode/1"
L_kuro_data_43: .asciz ""
L_kuro_data_44: .asciz "e"
L_kuro_data_45: .asciz "kuro.input/1"
L_kuro_data_46: .asciz "i"
L_kuro_data_47: .asciz "\n"
L_kuro_data_48: .asciz "n"
L_kuro_data_49: .asciz "\r"
L_kuro_data_50: .asciz "r"
L_kuro_data_51: .asciz "\t"
L_kuro_data_52: .asciz "t"
L_kuro_data_53: .asciz "kuro.compile-error/1"
L_kuro_data_54: .asciz "\n"
L_kuro_data_55: .asciz "EOF"
L_kuro_data_56: .asciz ""
L_kuro_data_57: .asciz "IDENT"
L_kuro_data_58: .asciz "expected "
L_kuro_data_59: .asciz "E2002"
L_kuro_data_60: .asciz "expected '"
L_kuro_data_61: .asciz "E2002"
L_kuro_data_62: .asciz "IDENT"
L_kuro_data_63: .asciz "E2001"
L_kuro_data_64: .asciz "expected an identifier"
L_kuro_data_65: .asciz ""
L_kuro_data_66: .asciz "LPAREN"
L_kuro_data_67: .asciz "RPAREN"
L_kuro_data_68: .asciz "STRING"
L_kuro_data_69: .asciz "LIT_STR"
L_kuro_data_70: .asciz "INTEGER"
L_kuro_data_71: .asciz "LIT_INT"
L_kuro_data_72: .asciz "DECIMAL"
L_kuro_data_73: .asciz "LIT_DEC"
L_kuro_data_74: .asciz "AT"
L_kuro_data_75: .asciz "VAR"
L_kuro_data_76: .asciz "1"
L_kuro_data_77: .asciz "MINUS"
L_kuro_data_78: .asciz "LIT_INT"
L_kuro_data_79: .asciz "0"
L_kuro_data_80: .asciz "BIN"
L_kuro_data_81: .asciz "-"
L_kuro_data_82: .asciz "IDENT"
L_kuro_data_83: .asciz "VAR"
L_kuro_data_84: .asciz "0"
L_kuro_data_85: .asciz "E2003"
L_kuro_data_86: .asciz "expected a value"
L_kuro_data_87: .asciz "STAR"
L_kuro_data_88: .asciz "SLASH"
L_kuro_data_89: .asciz "*"
L_kuro_data_90: .asciz "SLASH"
L_kuro_data_91: .asciz "/"
L_kuro_data_92: .asciz "BIN"
L_kuro_data_93: .asciz "PLUS"
L_kuro_data_94: .asciz "MINUS"
L_kuro_data_95: .asciz "+"
L_kuro_data_96: .asciz "MINUS"
L_kuro_data_97: .asciz "-"
L_kuro_data_98: .asciz "BIN"
L_kuro_data_99: .asciz "END_EXPR"
L_kuro_data_100: .asciz "greater"
L_kuro_data_101: .asciz "than"
L_kuro_data_102: .asciz "or"
L_kuro_data_103: .asciz "equal"
L_kuro_data_104: .asciz "to"
L_kuro_data_105: .asciz "ge"
L_kuro_data_106: .asciz "gt"
L_kuro_data_107: .asciz "less"
L_kuro_data_108: .asciz "than"
L_kuro_data_109: .asciz "or"
L_kuro_data_110: .asciz "equal"
L_kuro_data_111: .asciz "to"
L_kuro_data_112: .asciz "le"
L_kuro_data_113: .asciz "lt"
L_kuro_data_114: .asciz "equal"
L_kuro_data_115: .asciz "to"
L_kuro_data_116: .asciz "eq"
L_kuro_data_117: .asciz "equals"
L_kuro_data_118: .asciz "to"
L_kuro_data_119: .asciz "eq"
L_kuro_data_120: .asciz "not"
L_kuro_data_121: .asciz "equal"
L_kuro_data_122: .asciz "to"
L_kuro_data_123: .asciz "ne"
L_kuro_data_124: .asciz "at"
L_kuro_data_125: .asciz "least"
L_kuro_data_126: .asciz "ge"
L_kuro_data_127: .asciz "most"
L_kuro_data_128: .asciz "le"
L_kuro_data_129: .asciz "E2004"
L_kuro_data_130: .asciz "expected a comparison operator"
L_kuro_data_131: .asciz ""
L_kuro_data_132: .asciz "is"
L_kuro_data_133: .asciz "IDENT"
L_kuro_data_134: .asciz "digit"
L_kuro_data_135: .asciz "alpha"
L_kuro_data_136: .asciz "space"
L_kuro_data_137: .asciz "alnum"
L_kuro_data_138: .asciz "quote"
L_kuro_data_139: .asciz "ISCLASS"
L_kuro_data_140: .asciz "CMP"
L_kuro_data_141: .asciz "and"
L_kuro_data_142: .asciz "AND"
L_kuro_data_143: .asciz "or"
L_kuro_data_144: .asciz "OR"
L_kuro_data_145: .asciz "NONE"
L_kuro_data_146: .asciz "COLON"
L_kuro_data_147: .asciz "COMMA"
L_kuro_data_148: .asciz "LPAREN"
L_kuro_data_149: .asciz "RPAREN"
L_kuro_data_150: .asciz "RPAREN"
L_kuro_data_151: .asciz "SEMI"
L_kuro_data_152: .asciz "END_PARAMS"
L_kuro_data_153: .asciz "COMMA"
L_kuro_data_154: .asciz "LPAREN"
L_kuro_data_155: .asciz "RPAREN"
L_kuro_data_156: .asciz "RPAREN"
L_kuro_data_157: .asciz "SEMI"
L_kuro_data_158: .asciz "END_ARGS"
L_kuro_data_159: .asciz "IDENT"
L_kuro_data_160: .asciz "is"
L_kuro_data_161: .asciz "greater"
L_kuro_data_162: .asciz "less"
L_kuro_data_163: .asciz "equal"
L_kuro_data_164: .asciz "equals"
L_kuro_data_165: .asciz "not"
L_kuro_data_166: .asciz "and"
L_kuro_data_167: .asciz "COMMA"
L_kuro_data_168: .asciz "END_VALUES"
L_kuro_data_169: .asciz "IDENT"
L_kuro_data_170: .asciz "SEMI"
L_kuro_data_171: .asciz "DECL"
L_kuro_data_172: .asciz "COLON"
L_kuro_data_173: .asciz "EQUAL"
L_kuro_data_174: .asciz "ASSIGN"
L_kuro_data_175: .asciz "SEMI"
L_kuro_data_176: .asciz "EQUAL"
L_kuro_data_177: .asciz "ASSIGN"
L_kuro_data_178: .asciz "NONE"
L_kuro_data_179: .asciz "SEMI"
L_kuro_data_180: .asciz "Print"
L_kuro_data_181: .asciz "PRINT"
L_kuro_data_182: .asciz "DOT"
L_kuro_data_183: .asciz "Add"
L_kuro_data_184: .asciz "ADD"
L_kuro_data_185: .asciz "to"
L_kuro_data_186: .asciz "SEMI"
L_kuro_data_187: .asciz "Update"
L_kuro_data_188: .asciz "to"
L_kuro_data_189: .asciz "UPDATE"
L_kuro_data_190: .asciz "SEMI"
L_kuro_data_191: .asciz "Take"
L_kuro_data_192: .asciz "user"
L_kuro_data_193: .asciz "INPUT"
L_kuro_data_194: .asciz "END_NAMES"
L_kuro_data_195: .asciz "SEMI"
L_kuro_data_196: .asciz "Get"
L_kuro_data_197: .asciz "GET"
L_kuro_data_198: .asciz "SEMI"
L_kuro_data_199: .asciz "0"
L_kuro_data_200: .asciz "1"
L_kuro_data_201: .asciz "SEMI"
L_kuro_data_202: .asciz "Length"
L_kuro_data_203: .asciz "LENGTH"
L_kuro_data_204: .asciz "SEMI"
L_kuro_data_205: .asciz "Set"
L_kuro_data_206: .asciz "SET"
L_kuro_data_207: .asciz "to"
L_kuro_data_208: .asciz "SEMI"
L_kuro_data_209: .asciz "Append"
L_kuro_data_210: .asciz "APPEND"
L_kuro_data_211: .asciz "to"
L_kuro_data_212: .asciz "SEMI"
L_kuro_data_213: .asciz "Compare"
L_kuro_data_214: .asciz "COMPARE"
L_kuro_data_215: .asciz "SEMI"
L_kuro_data_216: .asciz "Entered"
L_kuro_data_217: .asciz "is"
L_kuro_data_218: .asciz "IF"
L_kuro_data_219: .asciz "VAR"
L_kuro_data_220: .asciz "0"
L_kuro_data_221: .asciz "END_EXPR"
L_kuro_data_222: .asciz "CMP"
L_kuro_data_223: .asciz "then"
L_kuro_data_224: .asciz "Print"
L_kuro_data_225: .asciz "PRINT"
L_kuro_data_226: .asciz "END_BLOCK"
L_kuro_data_227: .asciz "otherwise"
L_kuro_data_228: .asciz "Print"
L_kuro_data_229: .asciz "PRINT"
L_kuro_data_230: .asciz "END_BLOCK"
L_kuro_data_231: .asciz "SEMI"
L_kuro_data_232: .asciz "Return"
L_kuro_data_233: .asciz "RETURN"
L_kuro_data_234: .asciz "SEMI"
L_kuro_data_235: .asciz "Call"
L_kuro_data_236: .asciz "CALL"
L_kuro_data_237: .asciz "SEMI"
L_kuro_data_238: .asciz "Action"
L_kuro_data_239: .asciz "ACTION"
L_kuro_data_240: .asciz "SEMI"
L_kuro_data_241: .asciz "Done"
L_kuro_data_242: .asciz ""
L_kuro_data_243: .asciz "Done"
L_kuro_data_244: .asciz "DOT"
L_kuro_data_245: .asciz "If"
L_kuro_data_246: .asciz "IF"
L_kuro_data_247: .asciz "SEMI"
L_kuro_data_248: .asciz "Else"
L_kuro_data_249: .asciz "Done"
L_kuro_data_250: .asciz "Else"
L_kuro_data_251: .asciz "SEMI"
L_kuro_data_252: .asciz "Done"
L_kuro_data_253: .asciz ""
L_kuro_data_254: .asciz "END_BLOCK"
L_kuro_data_255: .asciz "Done"
L_kuro_data_256: .asciz "DOT"
L_kuro_data_257: .asciz "Repeat"
L_kuro_data_258: .asciz "REPEAT"
L_kuro_data_259: .asciz "SEMI"
L_kuro_data_260: .asciz "Done"
L_kuro_data_261: .asciz ""
L_kuro_data_262: .asciz "Done"
L_kuro_data_263: .asciz "DOT"
L_kuro_data_264: .asciz "While"
L_kuro_data_265: .asciz "WHILE"
L_kuro_data_266: .asciz "SEMI"
L_kuro_data_267: .asciz "Done"
L_kuro_data_268: .asciz ""
L_kuro_data_269: .asciz "Done"
L_kuro_data_270: .asciz "DOT"
L_kuro_data_271: .asciz "unknown statement starting with "
L_kuro_data_272: .asciz "E2001"
L_kuro_data_273: .asciz "EOF"
L_kuro_data_274: .asciz "IDENT"
L_kuro_data_275: .asciz "END_BLOCK"
L_kuro_data_276: .asciz "PROGRAM"
L_kuro_data_277: .asciz ""
L_kuro_data_278: .asciz ""
L_kuro_data_279: .asciz "LIT_STR"
L_kuro_data_280: .asciz "LIT_INT"
L_kuro_data_281: .asciz "LIT_DEC"
L_kuro_data_282: .asciz "CONST"
L_kuro_data_283: .asciz "VAR"
L_kuro_data_284: .asciz "LOADVAR"
L_kuro_data_285: .asciz "LIT_STR"
L_kuro_data_286: .asciz "LIT_INT"
L_kuro_data_287: .asciz "LIT_DEC"
L_kuro_data_288: .asciz "CONST"
L_kuro_data_289: .asciz "VAR"
L_kuro_data_290: .asciz "LOADVAR"
L_kuro_data_291: .asciz "BIN"
L_kuro_data_292: .asciz "BINOP"
L_kuro_data_293: .asciz "CMP"
L_kuro_data_294: .asciz "CMP"
L_kuro_data_295: .asciz "ISCLASS"
L_kuro_data_296: .asciz "ISCLASS"
L_kuro_data_297: .asciz "CMP"
L_kuro_data_298: .asciz "CMP"
L_kuro_data_299: .asciz "LIT_STR"
L_kuro_data_300: .asciz "LIT_INT"
L_kuro_data_301: .asciz "LIT_DEC"
L_kuro_data_302: .asciz "VAR"
L_kuro_data_303: .asciz "AND"
L_kuro_data_304: .asciz "OR"
L_kuro_data_305: .asciz "BOOL"
L_kuro_data_306: .asciz "PRINT"
L_kuro_data_307: .asciz "STORE_LIST"
L_kuro_data_308: .asciz "END_VALUES"
L_kuro_data_309: .asciz "UPDATE"
L_kuro_data_310: .asciz "ADD"
L_kuro_data_311: .asciz "APPEND"
L_kuro_data_312: .asciz "END_NAMES"
L_kuro_data_313: .asciz "INPUT"
L_kuro_data_314: .asciz "1"
L_kuro_data_315: .asciz "GET"
L_kuro_data_316: .asciz "1"
L_kuro_data_317: .asciz "GET"
L_kuro_data_318: .asciz "0"
L_kuro_data_319: .asciz "LENGTH"
L_kuro_data_320: .asciz "DECLTYPE"
L_kuro_data_321: .asciz "SET"
L_kuro_data_322: .asciz "STORE_LIST"
L_kuro_data_323: .asciz "END_ARGS"
L_kuro_data_324: .asciz "RETURN"
L_kuro_data_325: .asciz "CALL_BEGIN"
L_kuro_data_326: .asciz "CALL_END"
L_kuro_data_327: .asciz "END_PARAMS"
L_kuro_data_328: .asciz "PARAM"
L_kuro_data_329: .asciz "FUNC_BEGIN"
L_kuro_data_330: .asciz "FUNC_END"
L_kuro_data_331: .asciz "IF_BEGIN"
L_kuro_data_332: .asciz "ELSE_BEGIN"
L_kuro_data_333: .asciz "IF_END"
L_kuro_data_334: .asciz "REPEAT_BEGIN"
L_kuro_data_335: .asciz "REPEAT_END"
L_kuro_data_336: .asciz "WHILE_BEGIN"
L_kuro_data_337: .asciz "WHILE_TEST"
L_kuro_data_338: .asciz "WHILE_END"
L_kuro_data_339: .asciz "END_BLOCK"
L_kuro_data_340: .asciz "DECL"
L_kuro_data_341: .asciz "PRINT"
L_kuro_data_342: .asciz "ASSIGN"
L_kuro_data_343: .asciz "UPDATE"
L_kuro_data_344: .asciz "ADD"
L_kuro_data_345: .asciz "APPEND"
L_kuro_data_346: .asciz "IF"
L_kuro_data_347: .asciz "REPEAT"
L_kuro_data_348: .asciz "WHILE"
L_kuro_data_349: .asciz "RETURN"
L_kuro_data_350: .asciz "CALL"
L_kuro_data_351: .asciz "ACTION"
L_kuro_data_352: .asciz "INPUT"
L_kuro_data_353: .asciz "GET"
L_kuro_data_354: .asciz "LENGTH"
L_kuro_data_355: .asciz "SET"
L_kuro_data_356: .asciz "COMPARE"
L_kuro_data_357: .asciz "BC_"
L_kuro_data_358: .asciz "CONST"
L_kuro_data_359: .asciz "LOADVAR"
L_kuro_data_360: .asciz "STORE_LIST"
L_kuro_data_361: .asciz "UPDATE"
L_kuro_data_362: .asciz "ADD"
L_kuro_data_363: .asciz "APPEND"
L_kuro_data_364: .asciz "FUNC_BEGIN"
L_kuro_data_365: .asciz "CALL_BEGIN"
L_kuro_data_366: .asciz "BINOP"
L_kuro_data_367: .asciz "CMP"
L_kuro_data_368: .asciz "BOOL"
L_kuro_data_369: .asciz "ISCLASS"
L_kuro_data_370: .asciz "LENGTH"
L_kuro_data_371: .asciz "SET"
L_kuro_data_372: .asciz "INPUT"
L_kuro_data_373: .asciz "GET"
L_kuro_data_374: .asciz "PARAM"
L_kuro_data_375: .asciz "DECLTYPE"
L_kuro_data_376: .asciz "PRINT"
L_kuro_data_377: .asciz "RETURN"
L_kuro_data_378: .asciz "IF_BEGIN"
L_kuro_data_379: .asciz "ELSE_BEGIN"
L_kuro_data_380: .asciz "IF_END"
L_kuro_data_381: .asciz "REPEAT_BEGIN"
L_kuro_data_382: .asciz "REPEAT_END"
L_kuro_data_383: .asciz "WHILE_BEGIN"
L_kuro_data_384: .asciz "WHILE_TEST"
L_kuro_data_385: .asciz "WHILE_END"
L_kuro_data_386: .asciz "FUNC_END"
L_kuro_data_387: .asciz "CALL_END"
L_kuro_float_format: .asciz "%g\n"
.section __TEXT,__text
_kuro_print_int:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    adrp x10, _kuro_int_buffer@PAGE
    add x10, x10, _kuro_int_buffer@PAGEOFF
    add x10, x10, #31
    mov w11, #0
    strb w11, [x10]
    mov x11, #10
    cbnz x0, L_kuro_print_int_loop
    mov w12, #48
    strb w12, [x10, #-1]!
    b L_kuro_print_int_done
L_kuro_print_int_loop:
    udiv x12, x0, x11
    msub x13, x12, x11, x0
    add x13, x13, #48
    strb w13, [x10, #-1]!
    mov x0, x12
    cbnz x0, L_kuro_print_int_loop
L_kuro_print_int_done:
    mov x0, x10
    bl _puts
    ldp x29, x30, [sp], #16
    ret
L_kuro_collection_overflow:
    mov w0, #1
    bl _exit
    brk #0
L_kuro_collection_bounds:
    mov w0, #1
    bl _exit
    brk #0
.zerofill __DATA,__bss,_kuro_collection_0,524288,3
.zerofill __DATA,__bss,_kuro_collection_1,524288,3
.zerofill __DATA,__bss,_kuro_collection_2,524288,3
.zerofill __DATA,__bss,_kuro_collection_3,524288,3
.zerofill __DATA,__bss,_kuro_collection_4,524288,3
.zerofill __DATA,__bss,_kuro_collection_5,524288,3
.zerofill __DATA,__bss,_kuro_collection_6,524288,3
.zerofill __DATA,__bss,_kuro_collection_7,524288,3
.zerofill __DATA,__bss,_kuro_collection_8,524288,3
.zerofill __DATA,__bss,_kuro_collection_9,524288,3
.zerofill __DATA,__bss,_kuro_collection_len_0,8,3
.zerofill __DATA,__bss,_kuro_collection_len_1,8,3
.zerofill __DATA,__bss,_kuro_collection_len_2,8,3
.zerofill __DATA,__bss,_kuro_collection_len_3,8,3
.zerofill __DATA,__bss,_kuro_collection_len_4,8,3
.zerofill __DATA,__bss,_kuro_collection_len_5,8,3
.zerofill __DATA,__bss,_kuro_collection_len_6,8,3
.zerofill __DATA,__bss,_kuro_collection_len_7,8,3
.zerofill __DATA,__bss,_kuro_collection_len_8,8,3
.zerofill __DATA,__bss,_kuro_collection_len_9,8,3
.zerofill __DATA,__bss,_kuro_global_0,8,3
.zerofill __DATA,__bss,_kuro_global_1,8,3
.zerofill __DATA,__bss,_kuro_global_2,8,3
.zerofill __DATA,__bss,_kuro_global_3,8,3
.zerofill __DATA,__bss,_kuro_global_4,8,3
.zerofill __DATA,__bss,_kuro_global_5,8,3
.zerofill __DATA,__bss,_kuro_global_6,8,3
.zerofill __DATA,__bss,_kuro_global_7,8,3
.zerofill __DATA,__bss,_kuro_global_8,8,3
.zerofill __DATA,__bss,_kuro_global_9,8,3
.zerofill __DATA,__bss,_kuro_global_10,8,3
.zerofill __DATA,__bss,_kuro_global_11,8,3
.zerofill __DATA,__bss,_kuro_global_12,8,3
.zerofill __DATA,__bss,_kuro_global_13,8,3
.zerofill __DATA,__bss,_kuro_global_14,8,3
.zerofill __DATA,__bss,_kuro_global_15,8,3
.zerofill __DATA,__bss,_kuro_global_16,8,3
.zerofill __DATA,__bss,_kuro_global_17,8,3
.zerofill __DATA,__bss,_kuro_global_18,8,3
.zerofill __DATA,__bss,_kuro_global_19,8,3
.zerofill __DATA,__bss,_kuro_global_20,8,3
.zerofill __DATA,__bss,_kuro_global_21,8,3
.zerofill __DATA,__bss,_kuro_global_22,8,3
.zerofill __DATA,__bss,_kuro_global_23,8,3
.zerofill __DATA,__bss,_kuro_global_24,8,3
.zerofill __DATA,__bss,_kuro_global_25,8,3
.zerofill __DATA,__bss,_kuro_global_26,8,3
.zerofill __DATA,__bss,_kuro_global_27,8,3
.zerofill __DATA,__bss,_kuro_global_28,8,3
.zerofill __DATA,__bss,_kuro_global_29,8,3
.zerofill __DATA,__bss,_kuro_global_30,8,3
.zerofill __DATA,__bss,_kuro_global_31,8,3
.zerofill __DATA,__bss,_kuro_global_32,8,3
.zerofill __DATA,__bss,_kuro_global_33,8,3
.zerofill __DATA,__bss,_kuro_global_34,8,3
.zerofill __DATA,__bss,_kuro_global_35,8,3
.zerofill __DATA,__bss,_kuro_global_36,8,3
.zerofill __DATA,__bss,_kuro_global_37,8,3
.zerofill __DATA,__bss,_kuro_global_38,8,3
.zerofill __DATA,__bss,_kuro_global_39,8,3
.zerofill __DATA,__bss,_kuro_global_40,8,3
.zerofill __DATA,__bss,_kuro_global_41,8,3
.zerofill __DATA,__bss,_kuro_global_42,8,3
.zerofill __DATA,__bss,_kuro_global_43,8,3
.zerofill __DATA,__bss,_kuro_global_44,8,3
.zerofill __DATA,__bss,_kuro_global_45,8,3
.zerofill __DATA,__bss,_kuro_global_46,8,3
.zerofill __DATA,__bss,_kuro_global_47,8,3
.zerofill __DATA,__bss,_kuro_global_48,8,3
.zerofill __DATA,__bss,_kuro_global_49,8,3
.zerofill __DATA,__bss,_kuro_global_50,8,3
.zerofill __DATA,__bss,_kuro_global_51,8,3
.zerofill __DATA,__bss,_kuro_global_52,8,3
.zerofill __DATA,__bss,_kuro_global_53,8,3
.zerofill __DATA,__bss,_kuro_global_54,8,3
.zerofill __DATA,__bss,_kuro_global_55,8,3
.zerofill __DATA,__bss,_kuro_global_56,8,3
.zerofill __DATA,__bss,_kuro_global_57,8,3
.zerofill __DATA,__bss,_kuro_global_58,8,3
.zerofill __DATA,__bss,_kuro_global_59,8,3
.zerofill __DATA,__bss,_kuro_global_60,8,3
.zerofill __DATA,__bss,_kuro_global_61,8,3
.zerofill __DATA,__bss,_kuro_global_62,8,3
.zerofill __DATA,__bss,_kuro_global_63,8,3
.zerofill __DATA,__bss,_kuro_global_64,8,3
.zerofill __DATA,__bss,_kuro_global_65,8,3
.zerofill __DATA,__bss,_kuro_global_66,8,3
.zerofill __DATA,__bss,_kuro_global_67,8,3
.zerofill __DATA,__bss,_kuro_global_68,8,3
.zerofill __DATA,__bss,_kuro_global_69,8,3
.zerofill __DATA,__bss,_kuro_global_70,8,3
.zerofill __DATA,__bss,_kuro_global_71,8,3
.zerofill __DATA,__bss,_kuro_global_72,8,3
.zerofill __DATA,__bss,_kuro_global_73,8,3
.zerofill __DATA,__bss,_kuro_global_74,8,3
.zerofill __DATA,__bss,_kuro_global_75,8,3
.zerofill __DATA,__bss,_kuro_global_76,8,3
.zerofill __DATA,__bss,_kuro_global_77,8,3
.zerofill __DATA,__bss,_kuro_global_78,8,3
.zerofill __DATA,__bss,_kuro_global_79,8,3
.zerofill __DATA,__bss,_kuro_global_80,8,3
.zerofill __DATA,__bss,_kuro_global_81,8,3
.zerofill __DATA,__bss,_kuro_global_82,8,3
.zerofill __DATA,__bss,_kuro_global_83,8,3
.zerofill __DATA,__bss,_kuro_global_84,8,3
.zerofill __DATA,__bss,_kuro_global_85,8,3
.zerofill __DATA,__bss,_kuro_global_86,8,3
.zerofill __DATA,__bss,_kuro_global_87,8,3
.zerofill __DATA,__bss,_kuro_global_88,8,3
.zerofill __DATA,__bss,_kuro_global_89,8,3
.zerofill __DATA,__bss,_kuro_global_90,8,3
.zerofill __DATA,__bss,_kuro_global_91,8,3
.zerofill __DATA,__bss,_kuro_global_92,8,3
.zerofill __DATA,__bss,_kuro_global_93,8,3
.zerofill __DATA,__bss,_kuro_global_94,8,3
.zerofill __DATA,__bss,_kuro_global_95,8,3
.zerofill __DATA,__bss,_kuro_global_96,8,3
.zerofill __DATA,__bss,_kuro_global_97,8,3
.zerofill __DATA,__bss,_kuro_global_98,8,3
.zerofill __DATA,__bss,_kuro_global_99,8,3
.zerofill __DATA,__bss,_kuro_global_100,8,3
.zerofill __DATA,__bss,_kuro_global_101,8,3
.zerofill __DATA,__bss,_kuro_global_102,8,3
.zerofill __DATA,__bss,_kuro_global_103,8,3
.zerofill __DATA,__bss,_kuro_global_104,8,3
.zerofill __DATA,__bss,_kuro_global_105,8,3
.zerofill __DATA,__bss,_kuro_global_106,8,3
.zerofill __DATA,__bss,_kuro_global_107,8,3
.zerofill __DATA,__bss,_kuro_global_108,8,3
.zerofill __DATA,__bss,_kuro_global_109,8,3
.zerofill __DATA,__bss,_kuro_global_110,8,3
.zerofill __DATA,__bss,_kuro_global_111,8,3
.zerofill __DATA,__bss,_kuro_global_112,8,3
.zerofill __DATA,__bss,_kuro_global_113,8,3
.zerofill __DATA,__bss,_kuro_global_114,8,3
.zerofill __DATA,__bss,_kuro_global_115,8,3
.zerofill __DATA,__bss,_kuro_global_116,8,3
.zerofill __DATA,__bss,_kuro_global_117,8,3
.zerofill __DATA,__bss,_kuro_global_118,8,3
.zerofill __DATA,__bss,_kuro_global_119,8,3
.zerofill __DATA,__bss,_kuro_global_120,8,3
.zerofill __DATA,__bss,_kuro_global_121,8,3
.zerofill __DATA,__bss,_kuro_global_122,8,3
.zerofill __DATA,__bss,_kuro_global_123,8,3
.zerofill __DATA,__bss,_kuro_global_124,8,3
.zerofill __DATA,__bss,_kuro_global_125,8,3
.zerofill __DATA,__bss,_kuro_global_126,8,3
.zerofill __DATA,__bss,_kuro_global_127,8,3
.zerofill __DATA,__bss,_kuro_global_128,8,3
.zerofill __DATA,__bss,_kuro_global_129,8,3
.zerofill __DATA,__bss,_kuro_global_130,8,3
.zerofill __DATA,__bss,_kuro_global_131,8,3
.zerofill __DATA,__bss,_kuro_global_132,8,3
.zerofill __DATA,__bss,_kuro_global_133,8,3
.zerofill __DATA,__bss,_kuro_global_134,8,3
.zerofill __DATA,__bss,_kuro_global_135,8,3
.zerofill __DATA,__bss,_kuro_global_136,8,3
.zerofill __DATA,__bss,_kuro_global_137,8,3
.zerofill __DATA,__bss,_kuro_global_138,8,3
.zerofill __DATA,__bss,_kuro_global_139,8,3
.zerofill __DATA,__bss,_kuro_global_140,8,3
.zerofill __DATA,__bss,_kuro_global_141,8,3
.zerofill __DATA,__bss,_kuro_global_142,8,3
.zerofill __DATA,__bss,_kuro_global_143,8,3
.zerofill __DATA,__bss,_kuro_global_144,8,3
.zerofill __DATA,__bss,_kuro_global_145,8,3
.zerofill __DATA,__bss,_kuro_global_146,8,3
.zerofill __DATA,__bss,_kuro_global_147,8,3
.zerofill __DATA,__bss,_kuro_global_148,8,3
.zerofill __DATA,__bss,_kuro_global_149,8,3
.zerofill __DATA,__bss,_kuro_global_150,8,3
.zerofill __DATA,__bss,_kuro_global_151,8,3
.zerofill __DATA,__bss,_kuro_global_152,8,3
.zerofill __DATA,__bss,_kuro_global_153,8,3
.zerofill __DATA,__bss,_kuro_global_154,8,3
.zerofill __DATA,__bss,_kuro_global_155,8,3
.zerofill __DATA,__bss,_kuro_global_156,8,3
.zerofill __DATA,__bss,_kuro_global_157,8,3
.zerofill __DATA,__bss,_kuro_global_158,8,3
.zerofill __DATA,__bss,_kuro_global_159,8,3
.zerofill __DATA,__bss,_kuro_global_160,8,3
.zerofill __DATA,__bss,_kuro_global_161,8,3
.zerofill __DATA,__bss,_kuro_global_162,8,3
.zerofill __DATA,__bss,_kuro_global_163,8,3
.zerofill __DATA,__bss,_kuro_global_164,8,3
.zerofill __DATA,__bss,_kuro_global_165,8,3
.zerofill __DATA,__bss,_kuro_global_166,8,3
.zerofill __DATA,__bss,_kuro_global_167,8,3
.zerofill __DATA,__bss,_kuro_global_168,8,3
.zerofill __DATA,__bss,_kuro_global_169,8,3
.zerofill __DATA,__bss,_kuro_global_170,8,3
.zerofill __DATA,__bss,_kuro_global_171,8,3
.zerofill __DATA,__bss,_kuro_global_172,8,3
.zerofill __DATA,__bss,_kuro_global_173,8,3
.zerofill __DATA,__bss,_kuro_global_174,8,3
.zerofill __DATA,__bss,_kuro_global_175,8,3
.zerofill __DATA,__bss,_kuro_global_176,8,3
.zerofill __DATA,__bss,_kuro_global_177,8,3
.zerofill __DATA,__bss,_kuro_global_178,8,3
.zerofill __DATA,__bss,_kuro_global_179,8,3
.zerofill __DATA,__bss,_kuro_global_180,8,3
.zerofill __DATA,__bss,_kuro_global_181,8,3
.zerofill __DATA,__bss,_kuro_global_182,8,3
.zerofill __DATA,__bss,_kuro_global_183,8,3
.zerofill __DATA,__bss,_kuro_global_184,8,3
.zerofill __DATA,__bss,_kuro_global_185,8,3
.zerofill __DATA,__bss,_kuro_global_186,8,3
.zerofill __DATA,__bss,_kuro_global_187,8,3
.zerofill __DATA,__bss,_kuro_global_188,8,3
.zerofill __DATA,__bss,_kuro_global_189,8,3
.zerofill __DATA,__bss,_kuro_global_190,8,3
.zerofill __DATA,__bss,_kuro_global_191,8,3
.zerofill __DATA,__bss,_kuro_global_192,8,3
.zerofill __DATA,__bss,_kuro_global_193,8,3
.zerofill __DATA,__bss,_kuro_global_194,8,3
.zerofill __DATA,__bss,_kuro_global_195,8,3
.zerofill __DATA,__bss,_kuro_global_196,8,3
.zerofill __DATA,__bss,_kuro_global_197,8,3
.zerofill __DATA,__bss,_kuro_global_198,8,3
.zerofill __DATA,__bss,_kuro_global_199,8,3
.zerofill __DATA,__bss,_kuro_global_200,8,3
.zerofill __DATA,__bss,_kuro_global_201,8,3
.zerofill __DATA,__bss,_kuro_global_202,8,3
.zerofill __DATA,__bss,_kuro_global_203,8,3
.zerofill __DATA,__bss,_kuro_global_204,8,3
.zerofill __DATA,__bss,_kuro_global_205,8,3
.zerofill __DATA,__bss,_kuro_global_206,8,3
.zerofill __DATA,__bss,_kuro_global_207,8,3
.zerofill __DATA,__bss,_kuro_global_208,8,3
.zerofill __DATA,__bss,_kuro_global_209,8,3
.zerofill __DATA,__bss,_kuro_global_210,8,3
.zerofill __DATA,__bss,_kuro_global_211,8,3
.zerofill __DATA,__bss,_kuro_global_212,8,3
.zerofill __DATA,__bss,_kuro_global_213,8,3
.zerofill __DATA,__bss,_kuro_global_214,8,3
.zerofill __DATA,__bss,_kuro_global_215,8,3
.zerofill __DATA,__bss,_kuro_global_216,8,3
.zerofill __DATA,__bss,_kuro_global_217,8,3
.zerofill __DATA,__bss,_kuro_global_218,8,3
.zerofill __DATA,__bss,_kuro_global_219,8,3
.zerofill __DATA,__bss,_kuro_global_220,8,3
.zerofill __DATA,__bss,_kuro_global_221,8,3
.zerofill __DATA,__bss,_kuro_char_70,2,1
.zerofill __DATA,__bss,_kuro_char_94,2,1
.zerofill __DATA,__bss,_kuro_char_126,2,1
.zerofill __DATA,__bss,_kuro_char_166,2,1
.zerofill __DATA,__bss,_kuro_char_195,2,1
.zerofill __DATA,__bss,_kuro_char_281,2,1
.zerofill __DATA,__bss,_kuro_char_315,2,1
.zerofill __DATA,__bss,_kuro_char_387,2,1
.zerofill __DATA,__bss,_kuro_char_738,2,1
.zerofill __DATA,__bss,_kuro_char_9,2,1
.zerofill __DATA,__bss,_kuro_char_heap,2097152,4
.zerofill __DATA,__bss,_kuro_char_heap_cursor,8,3
.zerofill __DATA,__bss,_kuro_int_buffer,32,3
.zerofill __DATA,__bss,_kuro_input_buffer,1048576,4
