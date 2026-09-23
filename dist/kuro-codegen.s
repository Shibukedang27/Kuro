.section __TEXT,__text
.globl _main
.p2align 2
_main:
    stp x29, x30, [sp, #-16]!
    stp x19, x20, [sp, #-16]!
    mov x29, sp
    mov x15, #4752
    sub sp, sp, x15
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
    adrp x2, _kuro_global_25@PAGE
    add x2, x2, _kuro_global_25@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_0@PAGE
    add x0, x0, L_kuro_data_0@PAGEOFF
    str x0, [sp, #864]
    ldr x0, [sp, #864]
    adrp x2, _kuro_global_20@PAGE
    add x2, x2, _kuro_global_20@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_1@PAGE
    add x0, x0, L_kuro_data_1@PAGEOFF
    str x0, [sp, #872]
    ldr x0, [sp, #872]
    adrp x2, _kuro_global_18@PAGE
    add x2, x2, _kuro_global_18@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #1760]
    ldr x0, [sp, #1760]
    adrp x2, _kuro_global_19@PAGE
    add x2, x2, _kuro_global_19@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2648]
    ldr x0, [sp, #2648]
    adrp x2, _kuro_global_14@PAGE
    add x2, x2, _kuro_global_14@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3536]
    ldr x0, [sp, #3536]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4272]
    ldr x0, [sp, #4272]
    adrp x2, _kuro_global_26@PAGE
    add x2, x2, _kuro_global_26@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_2@PAGE
    add x0, x0, L_kuro_data_2@PAGEOFF
    str x0, [sp, #4360]
    ldr x0, [sp, #4360]
    adrp x2, _kuro_global_9@PAGE
    add x2, x2, _kuro_global_9@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_3@PAGE
    add x0, x0, L_kuro_data_3@PAGEOFF
    str x0, [sp, #4448]
    ldr x0, [sp, #4448]
    adrp x2, _kuro_global_15@PAGE
    add x2, x2, _kuro_global_15@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4536]
    ldr x0, [sp, #4536]
    adrp x2, _kuro_global_22@PAGE
    add x2, x2, _kuro_global_22@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_4@PAGE
    add x0, x0, L_kuro_data_4@PAGEOFF
    str x0, [sp, #4624]
    ldr x0, [sp, #4624]
    adrp x2, _kuro_global_94@PAGE
    add x2, x2, _kuro_global_94@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_25@PAGE
    add x0, x0, _kuro_global_25@PAGEOFF
    ldr x0, [x0]
    cbz x0, L_kuro_length_zero_t10
    bl _strlen
    b L_kuro_length_done_t10
L_kuro_length_zero_t10:
    mov x0, #0
L_kuro_length_done_t10:
    str x0, [sp, #880]
    ldr x0, [sp, #880]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #968]
    ldr x0, [sp, #968]
    adrp x2, _kuro_global_17@PAGE
    add x2, x2, _kuro_global_17@PAGEOFF
    str x0, [x2]
L_kuro_while_start0:
    adrp x0, _kuro_global_14@PAGE
    add x0, x0, _kuro_global_14@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1056]
    adrp x0, _kuro_global_17@PAGE
    add x0, x0, _kuro_global_17@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1144]
    ldr x0, [sp, #1056]
    ldr x1, [sp, #1144]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #1232]
    ldr x0, [sp, #1232]
    cbz w0, L_kuro_while_end1
    adrp x0, _kuro_global_14@PAGE
    add x0, x0, _kuro_global_14@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1320]
    adrp x2, _kuro_global_25@PAGE
    add x2, x2, _kuro_global_25@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #1320]
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
    str x0, [sp, #1408]
    ldr x0, [sp, #1408]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1496]
    ldr x0, [sp, #1496]
    adrp x2, _kuro_global_2@PAGE
    add x2, x2, _kuro_global_2@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_22@PAGE
    add x0, x0, _kuro_global_22@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1584]
    mov x0, #1
    str x0, [sp, #1672]
    ldr x0, [sp, #1584]
    ldr x1, [sp, #1672]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1768]
    ldr x0, [sp, #1768]
    cbz w0, L_kuro_else3
    adrp x0, _kuro_global_94@PAGE
    add x0, x0, _kuro_global_94@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1856]
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1944]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2032]
    ldr x0, [sp, #2032]
    ldr x1, [sp, #1856]
    bl _strcpy
    ldr x0, [sp, #2032]
    ldr x1, [sp, #1944]
    bl _strcat
    ldr x0, [sp, #2032]
    adrp x2, _kuro_global_94@PAGE
    add x2, x2, _kuro_global_94@PAGEOFF
    str x0, [x2]
    b L_kuro_endif4
L_kuro_else3:
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2120]
    adrp x0, L_kuro_data_5@PAGE
    add x0, x0, L_kuro_data_5@PAGEOFF
    str x0, [sp, #2208]
    ldr x0, [sp, #2120]
    ldr x1, [sp, #2208]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2296]
    ldr x0, [sp, #2296]
    cbz w0, L_kuro_else5
    bl _kuro_fn_ArtifactCommitLine
    str x0, [sp, #2384]
    ldr x0, [sp, #2384]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    b L_kuro_endif6
L_kuro_else5:
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2472]
    adrp x0, L_kuro_data_6@PAGE
    add x0, x0, L_kuro_data_6@PAGEOFF
    str x0, [sp, #2560]
    ldr x0, [sp, #2472]
    ldr x1, [sp, #2560]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2656]
    ldr x0, [sp, #2656]
    cbz w0, L_kuro_else7
    mov x0, #1
    str x0, [sp, #2744]
    ldr x0, [sp, #2744]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif8
L_kuro_else7:
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2832]
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2920]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3008]
    ldr x0, [sp, #3008]
    ldr x1, [sp, #2832]
    bl _strcpy
    ldr x0, [sp, #3008]
    ldr x1, [sp, #2920]
    bl _strcat
    ldr x0, [sp, #3008]
    adrp x2, _kuro_global_18@PAGE
    add x2, x2, _kuro_global_18@PAGEOFF
    str x0, [x2]
L_kuro_endif8:
L_kuro_endif6:
L_kuro_endif4:
    mov x0, #1
    str x0, [sp, #3096]
    adrp x0, _kuro_global_14@PAGE
    add x0, x0, _kuro_global_14@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3096]
    add x0, x0, x1
    adrp x2, _kuro_global_14@PAGE
    add x2, x2, _kuro_global_14@PAGEOFF
    str x0, [x2]
    b L_kuro_while_start0
L_kuro_while_end1:
    adrp x0, _kuro_global_22@PAGE
    add x0, x0, _kuro_global_22@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3184]
    mov x0, #0
    str x0, [sp, #3272]
    ldr x0, [sp, #3184]
    ldr x1, [sp, #3272]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3360]
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3448]
    adrp x0, L_kuro_data_7@PAGE
    add x0, x0, L_kuro_data_7@PAGEOFF
    str x0, [sp, #3544]
    ldr x0, [sp, #3448]
    ldr x1, [sp, #3544]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #3632]
    ldr x0, [sp, #3360]
    ldr x1, [sp, #3632]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #3720]
    ldr x0, [sp, #3720]
    cbz w0, L_kuro_else9
    bl _kuro_fn_ArtifactCommitLine
    str x0, [sp, #3808]
    ldr x0, [sp, #3808]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    b L_kuro_endif10
L_kuro_else9:
L_kuro_endif10:
    adrp x0, _kuro_global_19@PAGE
    add x0, x0, _kuro_global_19@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3896]
    mov x0, #2
    str x0, [sp, #3984]
    ldr x0, [sp, #3896]
    ldr x1, [sp, #3984]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4072]
    ldr x0, [sp, #4072]
    cbz w0, L_kuro_else11
    mov x0, #1
    str x0, [sp, #4160]
    ldr x0, [sp, #4160]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif12
L_kuro_else11:
L_kuro_endif12:
    mov x0, #0
    str x0, [sp, #4248]
    ldr x0, [sp, #4248]
    adrp x2, _kuro_global_24@PAGE
    add x2, x2, _kuro_global_24@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4264]
    ldr x0, [sp, #4264]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4280]
    ldr x0, [sp, #4280]
    adrp x2, _kuro_global_23@PAGE
    add x2, x2, _kuro_global_23@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4288]
    ldr x0, [sp, #4288]
    adrp x2, _kuro_global_27@PAGE
    add x2, x2, _kuro_global_27@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4296]
    ldr x0, [sp, #4296]
    adrp x2, _kuro_global_12@PAGE
    add x2, x2, _kuro_global_12@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4304]
    ldr x0, [sp, #4304]
    adrp x2, _kuro_global_1@PAGE
    add x2, x2, _kuro_global_1@PAGEOFF
    str x0, [x2]
L_kuro_while_start13:
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4312]
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4320]
    ldr x0, [sp, #4312]
    ldr x1, [sp, #4320]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4328]
    adrp x0, _kuro_global_11@PAGE
    add x0, x0, _kuro_global_11@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4336]
    mov x0, #0
    str x0, [sp, #4344]
    ldr x0, [sp, #4336]
    ldr x1, [sp, #4344]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4352]
    ldr x0, [sp, #4328]
    ldr x1, [sp, #4352]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #4368]
    ldr x0, [sp, #4368]
    cbz w0, L_kuro_while_end14
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4376]
    ldr x1, [sp, #4376]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #4384]
    ldr x0, [sp, #4384]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4392]
    ldr x0, [sp, #4392]
    adrp x2, _kuro_global_21@PAGE
    add x2, x2, _kuro_global_21@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4400]
    ldr x0, [sp, #4400]
    adrp x2, _kuro_global_0@PAGE
    add x2, x2, _kuro_global_0@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4408]
    ldr x0, [sp, #4408]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4416]
    adrp x0, L_kuro_data_8@PAGE
    add x0, x0, L_kuro_data_8@PAGEOFF
    str x0, [sp, #4424]
    ldr x0, [sp, #4416]
    ldr x1, [sp, #4424]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4432]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4440]
    adrp x0, L_kuro_data_9@PAGE
    add x0, x0, L_kuro_data_9@PAGEOFF
    str x0, [sp, #4456]
    ldr x0, [sp, #4440]
    ldr x1, [sp, #4456]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4464]
    ldr x0, [sp, #4432]
    ldr x1, [sp, #4464]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4472]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4480]
    adrp x0, L_kuro_data_10@PAGE
    add x0, x0, L_kuro_data_10@PAGEOFF
    str x0, [sp, #4488]
    ldr x0, [sp, #4480]
    ldr x1, [sp, #4488]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4496]
    ldr x0, [sp, #4472]
    ldr x1, [sp, #4496]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4504]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4512]
    adrp x0, L_kuro_data_11@PAGE
    add x0, x0, L_kuro_data_11@PAGEOFF
    str x0, [sp, #4520]
    ldr x0, [sp, #4512]
    ldr x1, [sp, #4520]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4528]
    ldr x0, [sp, #4504]
    ldr x1, [sp, #4528]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4544]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4552]
    adrp x0, L_kuro_data_12@PAGE
    add x0, x0, L_kuro_data_12@PAGEOFF
    str x0, [sp, #4560]
    ldr x0, [sp, #4552]
    ldr x1, [sp, #4560]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4568]
    ldr x0, [sp, #4544]
    ldr x1, [sp, #4568]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4576]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4584]
    adrp x0, L_kuro_data_13@PAGE
    add x0, x0, L_kuro_data_13@PAGEOFF
    str x0, [sp, #4592]
    ldr x0, [sp, #4584]
    ldr x1, [sp, #4592]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4600]
    ldr x0, [sp, #4576]
    ldr x1, [sp, #4600]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4608]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4616]
    adrp x0, L_kuro_data_14@PAGE
    add x0, x0, L_kuro_data_14@PAGEOFF
    str x0, [sp, #4632]
    ldr x0, [sp, #4616]
    ldr x1, [sp, #4632]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4640]
    ldr x0, [sp, #4608]
    ldr x1, [sp, #4640]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4648]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4656]
    adrp x0, L_kuro_data_15@PAGE
    add x0, x0, L_kuro_data_15@PAGEOFF
    str x0, [sp, #4664]
    ldr x0, [sp, #4656]
    ldr x1, [sp, #4664]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4672]
    ldr x0, [sp, #4648]
    ldr x1, [sp, #4672]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4680]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4688]
    adrp x0, L_kuro_data_16@PAGE
    add x0, x0, L_kuro_data_16@PAGEOFF
    str x0, [sp, #4696]
    ldr x0, [sp, #4688]
    ldr x1, [sp, #4696]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4704]
    ldr x0, [sp, #4680]
    ldr x1, [sp, #4704]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #888]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #896]
    adrp x0, L_kuro_data_17@PAGE
    add x0, x0, L_kuro_data_17@PAGEOFF
    str x0, [sp, #904]
    ldr x0, [sp, #896]
    ldr x1, [sp, #904]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #912]
    ldr x0, [sp, #888]
    ldr x1, [sp, #912]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #920]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #928]
    adrp x0, L_kuro_data_18@PAGE
    add x0, x0, L_kuro_data_18@PAGEOFF
    str x0, [sp, #936]
    ldr x0, [sp, #928]
    ldr x1, [sp, #936]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #944]
    ldr x0, [sp, #920]
    ldr x1, [sp, #944]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #952]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #960]
    adrp x0, L_kuro_data_19@PAGE
    add x0, x0, L_kuro_data_19@PAGEOFF
    str x0, [sp, #976]
    ldr x0, [sp, #960]
    ldr x1, [sp, #976]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #984]
    ldr x0, [sp, #952]
    ldr x1, [sp, #984]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #992]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1000]
    adrp x0, L_kuro_data_20@PAGE
    add x0, x0, L_kuro_data_20@PAGEOFF
    str x0, [sp, #1008]
    ldr x0, [sp, #1000]
    ldr x1, [sp, #1008]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1016]
    ldr x0, [sp, #992]
    ldr x1, [sp, #1016]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1024]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1032]
    adrp x0, L_kuro_data_21@PAGE
    add x0, x0, L_kuro_data_21@PAGEOFF
    str x0, [sp, #1040]
    ldr x0, [sp, #1032]
    ldr x1, [sp, #1040]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1048]
    ldr x0, [sp, #1024]
    ldr x1, [sp, #1048]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1064]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1072]
    adrp x0, L_kuro_data_22@PAGE
    add x0, x0, L_kuro_data_22@PAGEOFF
    str x0, [sp, #1080]
    ldr x0, [sp, #1072]
    ldr x1, [sp, #1080]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1088]
    ldr x0, [sp, #1064]
    ldr x1, [sp, #1088]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1096]
    ldr x0, [sp, #1096]
    cbz w0, L_kuro_else16
    mov x0, #1
    str x0, [sp, #1104]
    ldr x0, [sp, #1104]
    adrp x2, _kuro_global_0@PAGE
    add x2, x2, _kuro_global_0@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1112]
    ldr x0, [sp, #1112]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    b L_kuro_endif17
L_kuro_else16:
L_kuro_endif17:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1120]
    adrp x0, L_kuro_data_23@PAGE
    add x0, x0, L_kuro_data_23@PAGEOFF
    str x0, [sp, #1128]
    ldr x0, [sp, #1120]
    ldr x1, [sp, #1128]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1136]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1152]
    adrp x0, L_kuro_data_24@PAGE
    add x0, x0, L_kuro_data_24@PAGEOFF
    str x0, [sp, #1160]
    ldr x0, [sp, #1152]
    ldr x1, [sp, #1160]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1168]
    ldr x0, [sp, #1136]
    ldr x1, [sp, #1168]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1176]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1184]
    adrp x0, L_kuro_data_25@PAGE
    add x0, x0, L_kuro_data_25@PAGEOFF
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
    ldr x0, [sp, #1208]
    cbz w0, L_kuro_else18
    mov x0, #2
    str x0, [sp, #1216]
    ldr x0, [sp, #1216]
    adrp x2, _kuro_global_0@PAGE
    add x2, x2, _kuro_global_0@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1224]
    ldr x0, [sp, #1224]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    b L_kuro_endif19
L_kuro_else18:
L_kuro_endif19:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1240]
    adrp x0, L_kuro_data_26@PAGE
    add x0, x0, L_kuro_data_26@PAGEOFF
    str x0, [sp, #1248]
    ldr x0, [sp, #1240]
    ldr x1, [sp, #1248]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1256]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1264]
    adrp x0, L_kuro_data_27@PAGE
    add x0, x0, L_kuro_data_27@PAGEOFF
    str x0, [sp, #1272]
    ldr x0, [sp, #1264]
    ldr x1, [sp, #1272]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1280]
    ldr x0, [sp, #1256]
    ldr x1, [sp, #1280]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1288]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1296]
    adrp x0, L_kuro_data_28@PAGE
    add x0, x0, L_kuro_data_28@PAGEOFF
    str x0, [sp, #1304]
    ldr x0, [sp, #1296]
    ldr x1, [sp, #1304]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1312]
    ldr x0, [sp, #1288]
    ldr x1, [sp, #1312]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1328]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1336]
    adrp x0, L_kuro_data_29@PAGE
    add x0, x0, L_kuro_data_29@PAGEOFF
    str x0, [sp, #1344]
    ldr x0, [sp, #1336]
    ldr x1, [sp, #1344]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1352]
    ldr x0, [sp, #1328]
    ldr x1, [sp, #1352]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1360]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1368]
    adrp x0, L_kuro_data_30@PAGE
    add x0, x0, L_kuro_data_30@PAGEOFF
    str x0, [sp, #1376]
    ldr x0, [sp, #1368]
    ldr x1, [sp, #1376]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1384]
    ldr x0, [sp, #1360]
    ldr x1, [sp, #1384]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1392]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1400]
    adrp x0, L_kuro_data_31@PAGE
    add x0, x0, L_kuro_data_31@PAGEOFF
    str x0, [sp, #1416]
    ldr x0, [sp, #1400]
    ldr x1, [sp, #1416]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1424]
    ldr x0, [sp, #1392]
    ldr x1, [sp, #1424]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1432]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1440]
    adrp x0, L_kuro_data_32@PAGE
    add x0, x0, L_kuro_data_32@PAGEOFF
    str x0, [sp, #1448]
    ldr x0, [sp, #1440]
    ldr x1, [sp, #1448]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1456]
    ldr x0, [sp, #1432]
    ldr x1, [sp, #1456]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1464]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1472]
    adrp x0, L_kuro_data_33@PAGE
    add x0, x0, L_kuro_data_33@PAGEOFF
    str x0, [sp, #1480]
    ldr x0, [sp, #1472]
    ldr x1, [sp, #1480]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1488]
    ldr x0, [sp, #1464]
    ldr x1, [sp, #1488]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1504]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1512]
    adrp x0, L_kuro_data_34@PAGE
    add x0, x0, L_kuro_data_34@PAGEOFF
    str x0, [sp, #1520]
    ldr x0, [sp, #1512]
    ldr x1, [sp, #1520]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1528]
    ldr x0, [sp, #1504]
    ldr x1, [sp, #1528]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1536]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1544]
    adrp x0, L_kuro_data_35@PAGE
    add x0, x0, L_kuro_data_35@PAGEOFF
    str x0, [sp, #1552]
    ldr x0, [sp, #1544]
    ldr x1, [sp, #1552]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1560]
    ldr x0, [sp, #1536]
    ldr x1, [sp, #1560]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1568]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1576]
    adrp x0, L_kuro_data_36@PAGE
    add x0, x0, L_kuro_data_36@PAGEOFF
    str x0, [sp, #1592]
    ldr x0, [sp, #1576]
    ldr x1, [sp, #1592]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1600]
    ldr x0, [sp, #1568]
    ldr x1, [sp, #1600]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1608]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1616]
    adrp x0, L_kuro_data_37@PAGE
    add x0, x0, L_kuro_data_37@PAGEOFF
    str x0, [sp, #1624]
    ldr x0, [sp, #1616]
    ldr x1, [sp, #1624]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1632]
    ldr x0, [sp, #1608]
    ldr x1, [sp, #1632]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1640]
    ldr x0, [sp, #1640]
    cbz w0, L_kuro_else20
    mov x0, #1
    str x0, [sp, #1648]
    ldr x0, [sp, #1648]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    b L_kuro_endif21
L_kuro_else20:
L_kuro_endif21:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1656]
    adrp x0, L_kuro_data_38@PAGE
    add x0, x0, L_kuro_data_38@PAGEOFF
    str x0, [sp, #1664]
    ldr x0, [sp, #1656]
    ldr x1, [sp, #1664]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1680]
    ldr x0, [sp, #1680]
    cbz w0, L_kuro_else22
    mov x0, #1
    str x0, [sp, #1688]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1688]
    add x0, x0, x1
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    b L_kuro_endif23
L_kuro_else22:
L_kuro_endif23:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1696]
    adrp x0, L_kuro_data_39@PAGE
    add x0, x0, L_kuro_data_39@PAGEOFF
    str x0, [sp, #1704]
    ldr x0, [sp, #1696]
    ldr x1, [sp, #1704]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1712]
    ldr x0, [sp, #1712]
    cbz w0, L_kuro_else24
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1720]
    mov x0, #0
    str x0, [sp, #1728]
    ldr x0, [sp, #1720]
    ldr x1, [sp, #1728]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1736]
    ldr x0, [sp, #1736]
    cbz w0, L_kuro_else26
    mov x0, #1
    str x0, [sp, #1744]
    ldr x0, [sp, #1744]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif27
L_kuro_else26:
L_kuro_endif27:
    b L_kuro_endif25
L_kuro_else24:
L_kuro_endif25:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1752]
    adrp x0, L_kuro_data_40@PAGE
    add x0, x0, L_kuro_data_40@PAGEOFF
    str x0, [sp, #1776]
    ldr x0, [sp, #1752]
    ldr x1, [sp, #1776]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1784]
    ldr x0, [sp, #1784]
    cbz w0, L_kuro_else28
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1792]
    mov x0, #0
    str x0, [sp, #1800]
    ldr x0, [sp, #1792]
    ldr x1, [sp, #1800]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1808]
    ldr x0, [sp, #1808]
    cbz w0, L_kuro_else30
    mov x0, #1
    str x0, [sp, #1816]
    ldr x0, [sp, #1816]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif31
L_kuro_else30:
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1824]
    mov x0, #1
    str x0, [sp, #1832]
    ldr x0, [sp, #1824]
    ldr x1, [sp, #1832]
    sub x0, x0, x1
    str x0, [sp, #1840]
    ldr x0, [sp, #1840]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
L_kuro_endif31:
    b L_kuro_endif29
L_kuro_else28:
L_kuro_endif29:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1848]
    adrp x0, L_kuro_data_41@PAGE
    add x0, x0, L_kuro_data_41@PAGEOFF
    str x0, [sp, #1864]
    ldr x0, [sp, #1848]
    ldr x1, [sp, #1864]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1872]
    ldr x0, [sp, #1872]
    cbz w0, L_kuro_else32
    mov x0, #1
    str x0, [sp, #1880]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1880]
    add x0, x0, x1
    adrp x2, _kuro_global_23@PAGE
    add x2, x2, _kuro_global_23@PAGEOFF
    str x0, [x2]
    b L_kuro_endif33
L_kuro_else32:
L_kuro_endif33:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1888]
    adrp x0, L_kuro_data_42@PAGE
    add x0, x0, L_kuro_data_42@PAGEOFF
    str x0, [sp, #1896]
    ldr x0, [sp, #1888]
    ldr x1, [sp, #1896]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1904]
    ldr x0, [sp, #1904]
    cbz w0, L_kuro_else34
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1912]
    mov x0, #0
    str x0, [sp, #1920]
    ldr x0, [sp, #1912]
    ldr x1, [sp, #1920]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1928]
    ldr x0, [sp, #1928]
    cbz w0, L_kuro_else36
    mov x0, #1
    str x0, [sp, #1936]
    ldr x0, [sp, #1936]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif37
L_kuro_else36:
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1952]
    mov x0, #1
    str x0, [sp, #1960]
    ldr x0, [sp, #1952]
    ldr x1, [sp, #1960]
    sub x0, x0, x1
    str x0, [sp, #1968]
    ldr x0, [sp, #1968]
    adrp x2, _kuro_global_23@PAGE
    add x2, x2, _kuro_global_23@PAGEOFF
    str x0, [x2]
L_kuro_endif37:
    b L_kuro_endif35
L_kuro_else34:
L_kuro_endif35:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1976]
    adrp x0, L_kuro_data_43@PAGE
    add x0, x0, L_kuro_data_43@PAGEOFF
    str x0, [sp, #1984]
    ldr x0, [sp, #1976]
    ldr x1, [sp, #1984]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1992]
    ldr x0, [sp, #1992]
    cbz w0, L_kuro_else38
    mov x0, #1
    str x0, [sp, #2000]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2000]
    add x0, x0, x1
    adrp x2, _kuro_global_27@PAGE
    add x2, x2, _kuro_global_27@PAGEOFF
    str x0, [x2]
    b L_kuro_endif39
L_kuro_else38:
L_kuro_endif39:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2008]
    adrp x0, L_kuro_data_44@PAGE
    add x0, x0, L_kuro_data_44@PAGEOFF
    str x0, [sp, #2016]
    ldr x0, [sp, #2008]
    ldr x1, [sp, #2016]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2024]
    ldr x0, [sp, #2024]
    cbz w0, L_kuro_else40
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2040]
    mov x0, #0
    str x0, [sp, #2048]
    ldr x0, [sp, #2040]
    ldr x1, [sp, #2048]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2056]
    ldr x0, [sp, #2056]
    cbz w0, L_kuro_else42
    mov x0, #1
    str x0, [sp, #2064]
    ldr x0, [sp, #2064]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif43
L_kuro_else42:
L_kuro_endif43:
    b L_kuro_endif41
L_kuro_else40:
L_kuro_endif41:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2072]
    adrp x0, L_kuro_data_45@PAGE
    add x0, x0, L_kuro_data_45@PAGEOFF
    str x0, [sp, #2080]
    ldr x0, [sp, #2072]
    ldr x1, [sp, #2080]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2088]
    ldr x0, [sp, #2088]
    cbz w0, L_kuro_else44
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2096]
    mov x0, #0
    str x0, [sp, #2104]
    ldr x0, [sp, #2096]
    ldr x1, [sp, #2104]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2112]
    ldr x0, [sp, #2112]
    cbz w0, L_kuro_else46
    mov x0, #1
    str x0, [sp, #2128]
    ldr x0, [sp, #2128]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif47
L_kuro_else46:
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2136]
    mov x0, #1
    str x0, [sp, #2144]
    ldr x0, [sp, #2136]
    ldr x1, [sp, #2144]
    sub x0, x0, x1
    str x0, [sp, #2152]
    ldr x0, [sp, #2152]
    adrp x2, _kuro_global_27@PAGE
    add x2, x2, _kuro_global_27@PAGEOFF
    str x0, [x2]
L_kuro_endif47:
    b L_kuro_endif45
L_kuro_else44:
L_kuro_endif45:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2160]
    adrp x0, L_kuro_data_46@PAGE
    add x0, x0, L_kuro_data_46@PAGEOFF
    str x0, [sp, #2168]
    ldr x0, [sp, #2160]
    ldr x1, [sp, #2168]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2176]
    ldr x0, [sp, #2176]
    cbz w0, L_kuro_else48
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2184]
    mov x0, #0
    str x0, [sp, #2192]
    ldr x0, [sp, #2184]
    ldr x1, [sp, #2192]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2200]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2216]
    mov x0, #0
    str x0, [sp, #2224]
    ldr x0, [sp, #2216]
    ldr x1, [sp, #2224]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2232]
    ldr x0, [sp, #2200]
    ldr x1, [sp, #2232]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2240]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2248]
    mov x0, #0
    str x0, [sp, #2256]
    ldr x0, [sp, #2248]
    ldr x1, [sp, #2256]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2264]
    ldr x0, [sp, #2240]
    ldr x1, [sp, #2264]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2272]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2280]
    mov x0, #0
    str x0, [sp, #2288]
    ldr x0, [sp, #2280]
    ldr x1, [sp, #2288]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2304]
    ldr x0, [sp, #2272]
    ldr x1, [sp, #2304]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2312]
    ldr x0, [sp, #2312]
    cbz w0, L_kuro_else50
    mov x0, #1
    str x0, [sp, #2320]
    ldr x0, [sp, #2320]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif51
L_kuro_else50:
    mov x0, #1
    str x0, [sp, #2328]
    ldr x0, [sp, #2328]
    adrp x2, _kuro_global_12@PAGE
    add x2, x2, _kuro_global_12@PAGEOFF
    str x0, [x2]
L_kuro_endif51:
    b L_kuro_endif49
L_kuro_else48:
L_kuro_endif49:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2336]
    adrp x0, L_kuro_data_47@PAGE
    add x0, x0, L_kuro_data_47@PAGEOFF
    str x0, [sp, #2344]
    ldr x0, [sp, #2336]
    ldr x1, [sp, #2344]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2352]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2360]
    adrp x0, L_kuro_data_48@PAGE
    add x0, x0, L_kuro_data_48@PAGEOFF
    str x0, [sp, #2368]
    ldr x0, [sp, #2360]
    ldr x1, [sp, #2368]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2376]
    ldr x0, [sp, #2352]
    ldr x1, [sp, #2376]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2392]
    ldr x0, [sp, #2392]
    cbz w0, L_kuro_else52
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2400]
    mov x0, #0
    str x0, [sp, #2408]
    ldr x0, [sp, #2400]
    ldr x1, [sp, #2408]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2416]
    ldr x0, [sp, #2416]
    cbz w0, L_kuro_else54
    mov x0, #1
    str x0, [sp, #2424]
    ldr x0, [sp, #2424]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif55
L_kuro_else54:
L_kuro_endif55:
    b L_kuro_endif53
L_kuro_else52:
L_kuro_endif53:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2432]
    adrp x0, L_kuro_data_49@PAGE
    add x0, x0, L_kuro_data_49@PAGEOFF
    str x0, [sp, #2440]
    ldr x0, [sp, #2432]
    ldr x1, [sp, #2440]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2448]
    ldr x0, [sp, #2448]
    cbz w0, L_kuro_else56
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2456]
    mov x0, #1
    str x0, [sp, #2464]
    ldr x0, [sp, #2456]
    ldr x1, [sp, #2464]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2480]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2488]
    mov x0, #0
    str x0, [sp, #2496]
    ldr x0, [sp, #2488]
    ldr x1, [sp, #2496]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2504]
    ldr x0, [sp, #2480]
    ldr x1, [sp, #2504]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2512]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2520]
    mov x0, #0
    str x0, [sp, #2528]
    ldr x0, [sp, #2520]
    ldr x1, [sp, #2528]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2536]
    ldr x0, [sp, #2512]
    ldr x1, [sp, #2536]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2544]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2552]
    mov x0, #0
    str x0, [sp, #2568]
    ldr x0, [sp, #2552]
    ldr x1, [sp, #2568]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2576]
    ldr x0, [sp, #2544]
    ldr x1, [sp, #2576]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2584]
    ldr x0, [sp, #2584]
    cbz w0, L_kuro_else58
    mov x0, #1
    str x0, [sp, #2592]
    ldr x0, [sp, #2592]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif59
L_kuro_else58:
    mov x0, #0
    str x0, [sp, #2600]
    ldr x0, [sp, #2600]
    adrp x2, _kuro_global_12@PAGE
    add x2, x2, _kuro_global_12@PAGEOFF
    str x0, [x2]
L_kuro_endif59:
    b L_kuro_endif57
L_kuro_else56:
L_kuro_endif57:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2608]
    adrp x0, L_kuro_data_50@PAGE
    add x0, x0, L_kuro_data_50@PAGEOFF
    str x0, [sp, #2616]
    ldr x0, [sp, #2608]
    ldr x1, [sp, #2616]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2624]
    ldr x0, [sp, #2624]
    cbz w0, L_kuro_else60
    mov x0, #1
    str x0, [sp, #2632]
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2632]
    add x0, x0, x1
    adrp x2, _kuro_global_1@PAGE
    add x2, x2, _kuro_global_1@PAGEOFF
    str x0, [x2]
    b L_kuro_endif61
L_kuro_else60:
L_kuro_endif61:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2640]
    adrp x0, L_kuro_data_51@PAGE
    add x0, x0, L_kuro_data_51@PAGEOFF
    str x0, [sp, #2664]
    ldr x0, [sp, #2640]
    ldr x1, [sp, #2664]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2672]
    ldr x0, [sp, #2672]
    cbz w0, L_kuro_else62
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2680]
    mov x0, #0
    str x0, [sp, #2688]
    ldr x0, [sp, #2680]
    ldr x1, [sp, #2688]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2696]
    ldr x0, [sp, #2696]
    cbz w0, L_kuro_else64
    mov x0, #1
    str x0, [sp, #2704]
    ldr x0, [sp, #2704]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif65
L_kuro_else64:
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2712]
    mov x0, #1
    str x0, [sp, #2720]
    ldr x0, [sp, #2712]
    ldr x1, [sp, #2720]
    sub x0, x0, x1
    str x0, [sp, #2728]
    ldr x0, [sp, #2728]
    adrp x2, _kuro_global_1@PAGE
    add x2, x2, _kuro_global_1@PAGEOFF
    str x0, [x2]
L_kuro_endif65:
    b L_kuro_endif63
L_kuro_else62:
L_kuro_endif63:
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2736]
    mov x0, #1
    str x0, [sp, #2752]
    ldr x0, [sp, #2736]
    ldr x1, [sp, #2752]
    add x0, x0, x1
    str x0, [sp, #2760]
    adrp x0, _kuro_global_0@PAGE
    add x0, x0, _kuro_global_0@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2768]
    ldr x0, [sp, #2760]
    ldr x1, [sp, #2768]
    add x0, x0, x1
    str x0, [sp, #2776]
    ldr x0, [sp, #2776]
    adrp x2, _kuro_global_24@PAGE
    add x2, x2, _kuro_global_24@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_16@PAGE
    add x0, x0, _kuro_global_16@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2784]
    mov x0, #0
    str x0, [sp, #2792]
    ldr x0, [sp, #2784]
    ldr x1, [sp, #2792]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2800]
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2808]
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2816]
    ldr x0, [sp, #2808]
    ldr x1, [sp, #2816]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #2824]
    ldr x0, [sp, #2800]
    ldr x1, [sp, #2824]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2840]
    ldr x0, [sp, #2840]
    cbz w0, L_kuro_else66
    mov x0, #1
    str x0, [sp, #2848]
    ldr x0, [sp, #2848]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif67
L_kuro_else66:
L_kuro_endif67:
    b L_kuro_while_start13
L_kuro_while_end14:
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2856]
    mov x0, #0
    str x0, [sp, #2864]
    ldr x0, [sp, #2856]
    ldr x1, [sp, #2864]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2872]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2880]
    mov x0, #0
    str x0, [sp, #2888]
    ldr x0, [sp, #2880]
    ldr x1, [sp, #2888]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2896]
    ldr x0, [sp, #2872]
    ldr x1, [sp, #2896]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2904]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2912]
    mov x0, #0
    str x0, [sp, #2928]
    ldr x0, [sp, #2912]
    ldr x1, [sp, #2928]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2936]
    ldr x0, [sp, #2904]
    ldr x1, [sp, #2936]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2944]
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2952]
    mov x0, #0
    str x0, [sp, #2960]
    ldr x0, [sp, #2952]
    ldr x1, [sp, #2960]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2968]
    ldr x0, [sp, #2944]
    ldr x1, [sp, #2968]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2976]
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2984]
    mov x0, #0
    str x0, [sp, #2992]
    ldr x0, [sp, #2984]
    ldr x1, [sp, #2992]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #3000]
    ldr x0, [sp, #2976]
    ldr x1, [sp, #3000]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3016]
    ldr x0, [sp, #3016]
    cbz w0, L_kuro_else68
    mov x0, #1
    str x0, [sp, #3024]
    ldr x0, [sp, #3024]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif69
L_kuro_else68:
L_kuro_endif69:
    adrp x0, _kuro_global_11@PAGE
    add x0, x0, _kuro_global_11@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3032]
    mov x0, #1
    str x0, [sp, #3040]
    ldr x0, [sp, #3032]
    ldr x1, [sp, #3040]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3048]
    ldr x0, [sp, #3048]
    cbz w0, L_kuro_else70
    adrp x0, L_kuro_data_52@PAGE
    add x0, x0, L_kuro_data_52@PAGEOFF
    str x0, [sp, #3056]
    adrp x0, L_kuro_data_53@PAGE
    add x0, x0, L_kuro_data_53@PAGEOFF
    str x0, [sp, #3064]
    ldr x0, [sp, #3056]
    adrp x1, _kuro_collection_0@PAGE
    add x1, x1, _kuro_collection_0@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3064]
    adrp x1, _kuro_collection_0@PAGE
    add x1, x1, _kuro_collection_0@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x0, [x2]
    b L_kuro_endif71
L_kuro_else70:
L_kuro_endif71:
    mov x0, #0
    str x0, [sp, #3072]
    ldr x0, [sp, #3072]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3080]
    ldr x0, [sp, #3080]
    adrp x2, _kuro_global_60@PAGE
    add x2, x2, _kuro_global_60@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_54@PAGE
    add x0, x0, L_kuro_data_54@PAGEOFF
    str x0, [sp, #3088]
    ldr x0, [sp, #3088]
    adrp x2, _kuro_global_53@PAGE
    add x2, x2, _kuro_global_53@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_55@PAGE
    add x0, x0, L_kuro_data_55@PAGEOFF
    str x0, [sp, #3104]
    ldr x0, [sp, #3104]
    adrp x2, _kuro_global_29@PAGE
    add x2, x2, _kuro_global_29@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_56@PAGE
    add x0, x0, L_kuro_data_56@PAGEOFF
    str x0, [sp, #3112]
    ldr x0, [sp, #3112]
    adrp x2, _kuro_global_62@PAGE
    add x2, x2, _kuro_global_62@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3120]
    ldr x0, [sp, #3120]
    adrp x2, _kuro_global_82@PAGE
    add x2, x2, _kuro_global_82@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3128]
    mov x0, #0
    str x0, [sp, #3136]
    mov x0, #0
    str x0, [sp, #3144]
    mov x0, #0
    str x0, [sp, #3152]
    mov x0, #0
    str x0, [sp, #3160]
    mov x0, #0
    str x0, [sp, #3168]
    mov x0, #0
    str x0, [sp, #3176]
    mov x0, #0
    str x0, [sp, #3192]
    mov x0, #0
    str x0, [sp, #3200]
    mov x0, #0
    str x0, [sp, #3208]
    mov x0, #0
    str x0, [sp, #3216]
    mov x0, #0
    str x0, [sp, #3224]
    mov x0, #0
    str x0, [sp, #3232]
    mov x0, #0
    str x0, [sp, #3240]
    mov x0, #0
    str x0, [sp, #3248]
    mov x0, #0
    str x0, [sp, #3256]
    ldr x0, [sp, #3128]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3136]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3144]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3152]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3160]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3168]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3176]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3192]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3200]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3208]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #72]
    ldr x0, [sp, #3216]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #80]
    ldr x0, [sp, #3224]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #88]
    ldr x0, [sp, #3232]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #96]
    ldr x0, [sp, #3240]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #104]
    ldr x0, [sp, #3248]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #112]
    ldr x0, [sp, #3256]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #120]
    mov x0, #16
    adrp x2, _kuro_collection_len_2@PAGE
    add x2, x2, _kuro_collection_len_2@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3264]
    mov x0, #0
    str x0, [sp, #3280]
    mov x0, #0
    str x0, [sp, #3288]
    mov x0, #0
    str x0, [sp, #3296]
    mov x0, #0
    str x0, [sp, #3304]
    mov x0, #0
    str x0, [sp, #3312]
    mov x0, #0
    str x0, [sp, #3320]
    mov x0, #0
    str x0, [sp, #3328]
    mov x0, #0
    str x0, [sp, #3336]
    mov x0, #0
    str x0, [sp, #3344]
    mov x0, #0
    str x0, [sp, #3352]
    mov x0, #0
    str x0, [sp, #3368]
    mov x0, #0
    str x0, [sp, #3376]
    mov x0, #0
    str x0, [sp, #3384]
    mov x0, #0
    str x0, [sp, #3392]
    mov x0, #0
    str x0, [sp, #3400]
    ldr x0, [sp, #3264]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3280]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3288]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3296]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3304]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3312]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3320]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3328]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3336]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3344]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #72]
    ldr x0, [sp, #3352]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #80]
    ldr x0, [sp, #3368]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #88]
    ldr x0, [sp, #3376]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #96]
    ldr x0, [sp, #3384]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #104]
    ldr x0, [sp, #3392]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #112]
    ldr x0, [sp, #3400]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #120]
    mov x0, #16
    adrp x2, _kuro_collection_len_1@PAGE
    add x2, x2, _kuro_collection_len_1@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3408]
    mov x0, #0
    str x0, [sp, #3416]
    mov x0, #0
    str x0, [sp, #3424]
    mov x0, #0
    str x0, [sp, #3432]
    mov x0, #0
    str x0, [sp, #3440]
    mov x0, #0
    str x0, [sp, #3456]
    mov x0, #0
    str x0, [sp, #3464]
    mov x0, #0
    str x0, [sp, #3472]
    mov x0, #0
    str x0, [sp, #3480]
    mov x0, #0
    str x0, [sp, #3488]
    mov x0, #0
    str x0, [sp, #3496]
    mov x0, #0
    str x0, [sp, #3504]
    mov x0, #0
    str x0, [sp, #3512]
    mov x0, #0
    str x0, [sp, #3520]
    mov x0, #0
    str x0, [sp, #3528]
    mov x0, #0
    str x0, [sp, #3552]
    ldr x0, [sp, #3408]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3416]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3424]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3432]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3440]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3456]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3464]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3472]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3480]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3488]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #72]
    ldr x0, [sp, #3496]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #80]
    ldr x0, [sp, #3504]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #88]
    ldr x0, [sp, #3512]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #96]
    ldr x0, [sp, #3520]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #104]
    ldr x0, [sp, #3528]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #112]
    ldr x0, [sp, #3552]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #120]
    mov x0, #16
    adrp x2, _kuro_collection_len_3@PAGE
    add x2, x2, _kuro_collection_len_3@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3560]
    mov x0, #0
    str x0, [sp, #3568]
    mov x0, #0
    str x0, [sp, #3576]
    mov x0, #0
    str x0, [sp, #3584]
    mov x0, #0
    str x0, [sp, #3592]
    mov x0, #0
    str x0, [sp, #3600]
    mov x0, #0
    str x0, [sp, #3608]
    mov x0, #0
    str x0, [sp, #3616]
    mov x0, #0
    str x0, [sp, #3624]
    mov x0, #0
    str x0, [sp, #3640]
    mov x0, #0
    str x0, [sp, #3648]
    mov x0, #0
    str x0, [sp, #3656]
    mov x0, #0
    str x0, [sp, #3664]
    mov x0, #0
    str x0, [sp, #3672]
    mov x0, #0
    str x0, [sp, #3680]
    mov x0, #0
    str x0, [sp, #3688]
    ldr x0, [sp, #3560]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3568]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3576]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3584]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3592]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3600]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3608]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3616]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3624]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3640]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #72]
    ldr x0, [sp, #3648]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #80]
    ldr x0, [sp, #3656]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #88]
    ldr x0, [sp, #3664]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #96]
    ldr x0, [sp, #3672]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #104]
    ldr x0, [sp, #3680]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #112]
    ldr x0, [sp, #3688]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #120]
    mov x0, #16
    adrp x2, _kuro_collection_len_4@PAGE
    add x2, x2, _kuro_collection_len_4@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3696]
    mov x0, #0
    str x0, [sp, #3704]
    mov x0, #0
    str x0, [sp, #3712]
    mov x0, #0
    str x0, [sp, #3728]
    mov x0, #0
    str x0, [sp, #3736]
    mov x0, #0
    str x0, [sp, #3744]
    mov x0, #0
    str x0, [sp, #3752]
    mov x0, #0
    str x0, [sp, #3760]
    mov x0, #0
    str x0, [sp, #3768]
    mov x0, #0
    str x0, [sp, #3776]
    mov x0, #0
    str x0, [sp, #3784]
    mov x0, #0
    str x0, [sp, #3792]
    mov x0, #0
    str x0, [sp, #3800]
    mov x0, #0
    str x0, [sp, #3816]
    mov x0, #0
    str x0, [sp, #3824]
    mov x0, #0
    str x0, [sp, #3832]
    ldr x0, [sp, #3696]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3704]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3712]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3728]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3736]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3744]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3752]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3760]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3768]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3776]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #72]
    ldr x0, [sp, #3784]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #80]
    ldr x0, [sp, #3792]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #88]
    ldr x0, [sp, #3800]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #96]
    ldr x0, [sp, #3816]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #104]
    ldr x0, [sp, #3824]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #112]
    ldr x0, [sp, #3832]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #120]
    mov x0, #16
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3840]
    mov x0, #0
    str x0, [sp, #3848]
    mov x0, #0
    str x0, [sp, #3856]
    mov x0, #0
    str x0, [sp, #3864]
    mov x0, #0
    str x0, [sp, #3872]
    mov x0, #0
    str x0, [sp, #3880]
    mov x0, #0
    str x0, [sp, #3888]
    mov x0, #0
    str x0, [sp, #3904]
    mov x0, #0
    str x0, [sp, #3912]
    mov x0, #0
    str x0, [sp, #3920]
    mov x0, #0
    str x0, [sp, #3928]
    mov x0, #0
    str x0, [sp, #3936]
    mov x0, #0
    str x0, [sp, #3944]
    mov x0, #0
    str x0, [sp, #3952]
    mov x0, #0
    str x0, [sp, #3960]
    mov x0, #0
    str x0, [sp, #3968]
    ldr x0, [sp, #3840]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3848]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3856]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3864]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3872]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3880]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3888]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3904]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3912]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3920]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #72]
    ldr x0, [sp, #3928]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #80]
    ldr x0, [sp, #3936]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #88]
    ldr x0, [sp, #3944]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #96]
    ldr x0, [sp, #3952]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #104]
    ldr x0, [sp, #3960]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #112]
    ldr x0, [sp, #3968]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #120]
    mov x0, #16
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3976]
    mov x0, #0
    str x0, [sp, #3992]
    mov x0, #0
    str x0, [sp, #4000]
    mov x0, #0
    str x0, [sp, #4008]
    mov x0, #0
    str x0, [sp, #4016]
    mov x0, #0
    str x0, [sp, #4024]
    mov x0, #0
    str x0, [sp, #4032]
    mov x0, #0
    str x0, [sp, #4040]
    mov x0, #0
    str x0, [sp, #4048]
    mov x0, #0
    str x0, [sp, #4056]
    mov x0, #0
    str x0, [sp, #4064]
    mov x0, #0
    str x0, [sp, #4080]
    mov x0, #0
    str x0, [sp, #4088]
    mov x0, #0
    str x0, [sp, #4096]
    mov x0, #0
    str x0, [sp, #4104]
    mov x0, #0
    str x0, [sp, #4112]
    ldr x0, [sp, #3976]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3992]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #4000]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #4008]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #4016]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #4024]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #4032]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #4040]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #4048]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #4056]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #72]
    ldr x0, [sp, #4064]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #80]
    ldr x0, [sp, #4080]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #88]
    ldr x0, [sp, #4088]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #96]
    ldr x0, [sp, #4096]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #104]
    ldr x0, [sp, #4104]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #112]
    ldr x0, [sp, #4112]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #120]
    mov x0, #16
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_collection_len_0@PAGE
    add x0, x0, _kuro_collection_len_0@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4120]
    ldr x0, [sp, #4120]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4128]
    ldr x0, [sp, #4128]
    adrp x2, _kuro_global_61@PAGE
    add x2, x2, _kuro_global_61@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_61@PAGE
    add x0, x0, _kuro_global_61@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4136]
    mov x0, #3
    str x0, [sp, #4144]
    ldr x0, [sp, #4136]
    ldr x1, [sp, #4144]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4152]
    ldr x0, [sp, #4152]
    cbz w0, L_kuro_else72
    mov x0, #1
    str x0, [sp, #4168]
    ldr x1, [sp, #4168]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #4176]
    ldr x0, [sp, #4176]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4184]
    ldr x0, [sp, #4184]
    bl _kuro_fn_NativeValidateUnsignedInteger
    str x0, [sp, #4192]
    ldr x0, [sp, #4192]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4200]
    mov x0, #1
    str x0, [sp, #4208]
    ldr x0, [sp, #4200]
    ldr x1, [sp, #4208]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4216]
    ldr x0, [sp, #4216]
    cbz w0, L_kuro_else74
    bl _kuro_fn_EmitStraightIntegerProgram
    str x0, [sp, #4224]
    ldr x0, [sp, #4224]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    b L_kuro_endif75
L_kuro_else74:
    bl _kuro_fn_EmitLiteralPrint
    str x0, [sp, #4232]
    ldr x0, [sp, #4232]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
L_kuro_endif75:
    b L_kuro_endif73
L_kuro_else72:
    bl _kuro_fn_EmitStraightIntegerProgram
    str x0, [sp, #4240]
    ldr x0, [sp, #4240]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
L_kuro_endif73:
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4256]
    ldr x0, [sp, #4256]
    adrp x2, _kuro_global_93@PAGE
    add x2, x2, _kuro_global_93@PAGEOFF
    str x0, [x2]
    mov x15, #4752
    add sp, sp, x15
    adrp x0, _kuro_global_93@PAGE
    add x0, x0, _kuro_global_93@PAGEOFF
    ldr x0, [x0]
    ldp x19, x20, [sp], #16
    ldp x29, x30, [sp], #16
    ret
L_kuro_runtime_error:
    mov w0, #1
    mov x15, #4752
    add sp, sp, x15
    ldp x19, x20, [sp], #16
    ldp x29, x30, [sp], #16
    ret
.section __TEXT,__cstring
.section __TEXT,__text
_kuro_fn_ArtifactDecodeLine:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #784
    sub sp, sp, x15
    str x0, [sp, #72]
    adrp x0, L_kuro_data_57@PAGE
    add x0, x0, L_kuro_data_57@PAGEOFF
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    adrp x0, L_kuro_data_58@PAGE
    add x0, x0, L_kuro_data_58@PAGEOFF
    str x0, [sp, #320]
    ldr x0, [sp, #232]
    ldr x1, [sp, #320]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    ldr x1, [sp, #232]
    bl _strcpy
    ldr x0, [sp, #408]
    ldr x1, [sp, #320]
    bl _strcat
    ldr x0, [sp, #408]
    adrp x2, _kuro_global_7@PAGE
    add x2, x2, _kuro_global_7@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #72]
    str x0, [sp, #496]
    adrp x0, _kuro_global_7@PAGE
    add x0, x0, _kuro_global_7@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #584]
    ldr x0, [sp, #496]
    ldr x1, [sp, #584]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #672]
    ldr x0, [sp, #672]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else0
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #744]
    ldr x0, [sp, #744]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_ArtifactDecodeLine_endif1
L_kuro_fn_ArtifactDecodeLine_else0:
L_kuro_fn_ArtifactDecodeLine_endif1:
    ldr x0, [sp, #72]
    cbz x0, L_kuro_fn_ArtifactDecodeLine_length_zero_t8
    bl _strlen
    b L_kuro_fn_ArtifactDecodeLine_length_done_t8
L_kuro_fn_ArtifactDecodeLine_length_zero_t8:
    mov x0, #0
L_kuro_fn_ArtifactDecodeLine_length_done_t8:
    str x0, [sp, #752]
    ldr x0, [sp, #752]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #760]
    ldr x0, [sp, #760]
    adrp x2, _kuro_global_8@PAGE
    add x2, x2, _kuro_global_8@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    adrp x2, _kuro_global_4@PAGE
    add x2, x2, _kuro_global_4@PAGEOFF
    str x0, [x2]
L_kuro_fn_ArtifactDecodeLine_while_start2:
    adrp x0, _kuro_global_4@PAGE
    add x0, x0, _kuro_global_4@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #256]
    ldr x0, [sp, #248]
    ldr x1, [sp, #256]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #264]
    adrp x0, _kuro_global_11@PAGE
    add x0, x0, _kuro_global_11@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #272]
    mov x0, #0
    str x0, [sp, #280]
    ldr x0, [sp, #272]
    ldr x1, [sp, #280]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #288]
    ldr x0, [sp, #264]
    ldr x1, [sp, #288]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_while_end3
    adrp x0, _kuro_global_4@PAGE
    add x0, x0, _kuro_global_4@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #304]
    ldr x2, [sp, #72]
    ldr x1, [sp, #304]
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
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    adrp x2, _kuro_global_3@PAGE
    add x2, x2, _kuro_global_3@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_3@PAGE
    add x0, x0, _kuro_global_3@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #336]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #344]
    ldr x0, [sp, #336]
    ldr x1, [sp, #344]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else5
    mov x0, #1
    str x0, [sp, #360]
    adrp x0, _kuro_global_4@PAGE
    add x0, x0, _kuro_global_4@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #360]
    add x0, x0, x1
    adrp x2, _kuro_global_4@PAGE
    add x2, x2, _kuro_global_4@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_4@PAGE
    add x0, x0, _kuro_global_4@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #368]
    adrp x0, _kuro_global_8@PAGE
    add x0, x0, _kuro_global_8@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else7
    adrp x0, _kuro_global_4@PAGE
    add x0, x0, _kuro_global_4@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #392]
    ldr x2, [sp, #72]
    ldr x1, [sp, #392]
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
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    adrp x2, _kuro_global_10@PAGE
    add x2, x2, _kuro_global_10@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_10@PAGE
    add x0, x0, _kuro_global_10@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #424]
    adrp x0, L_kuro_data_59@PAGE
    add x0, x0, L_kuro_data_59@PAGEOFF
    str x0, [sp, #432]
    ldr x0, [sp, #424]
    ldr x1, [sp, #432]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else9
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #448]
    adrp x0, L_kuro_data_60@PAGE
    add x0, x0, L_kuro_data_60@PAGEOFF
    str x0, [sp, #456]
    ldr x0, [sp, #448]
    ldr x1, [sp, #456]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    ldr x1, [sp, #448]
    bl _strcpy
    ldr x0, [sp, #464]
    ldr x1, [sp, #456]
    bl _strcat
    ldr x0, [sp, #464]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactDecodeLine_endif10
L_kuro_fn_ArtifactDecodeLine_else9:
    adrp x0, _kuro_global_10@PAGE
    add x0, x0, _kuro_global_10@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #472]
    adrp x0, L_kuro_data_61@PAGE
    add x0, x0, L_kuro_data_61@PAGEOFF
    str x0, [sp, #480]
    ldr x0, [sp, #472]
    ldr x1, [sp, #480]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else11
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #504]
    adrp x0, _kuro_global_15@PAGE
    add x0, x0, _kuro_global_15@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #512]
    ldr x0, [sp, #504]
    ldr x1, [sp, #512]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #520]
    ldr x0, [sp, #520]
    ldr x1, [sp, #504]
    bl _strcpy
    ldr x0, [sp, #520]
    ldr x1, [sp, #512]
    bl _strcat
    ldr x0, [sp, #520]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactDecodeLine_endif12
L_kuro_fn_ArtifactDecodeLine_else11:
    adrp x0, _kuro_global_10@PAGE
    add x0, x0, _kuro_global_10@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #528]
    adrp x0, L_kuro_data_62@PAGE
    add x0, x0, L_kuro_data_62@PAGEOFF
    str x0, [sp, #536]
    ldr x0, [sp, #528]
    ldr x1, [sp, #536]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #544]
    ldr x0, [sp, #544]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else13
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #552]
    adrp x0, L_kuro_data_63@PAGE
    add x0, x0, L_kuro_data_63@PAGEOFF
    str x0, [sp, #560]
    ldr x0, [sp, #552]
    ldr x1, [sp, #560]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #568]
    ldr x0, [sp, #568]
    ldr x1, [sp, #552]
    bl _strcpy
    ldr x0, [sp, #568]
    ldr x1, [sp, #560]
    bl _strcat
    ldr x0, [sp, #568]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactDecodeLine_endif14
L_kuro_fn_ArtifactDecodeLine_else13:
    adrp x0, _kuro_global_10@PAGE
    add x0, x0, _kuro_global_10@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #576]
    adrp x0, L_kuro_data_64@PAGE
    add x0, x0, L_kuro_data_64@PAGEOFF
    str x0, [sp, #592]
    ldr x0, [sp, #576]
    ldr x1, [sp, #592]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #600]
    ldr x0, [sp, #600]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else15
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #608]
    adrp x0, L_kuro_data_65@PAGE
    add x0, x0, L_kuro_data_65@PAGEOFF
    str x0, [sp, #616]
    ldr x0, [sp, #608]
    ldr x1, [sp, #616]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #624]
    ldr x0, [sp, #624]
    ldr x1, [sp, #608]
    bl _strcpy
    ldr x0, [sp, #624]
    ldr x1, [sp, #616]
    bl _strcat
    ldr x0, [sp, #624]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactDecodeLine_endif16
L_kuro_fn_ArtifactDecodeLine_else15:
    adrp x0, _kuro_global_10@PAGE
    add x0, x0, _kuro_global_10@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #632]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #640]
    ldr x0, [sp, #632]
    ldr x1, [sp, #640]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #648]
    ldr x0, [sp, #648]
    cbz w0, L_kuro_fn_ArtifactDecodeLine_else17
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #656]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #664]
    ldr x0, [sp, #656]
    ldr x1, [sp, #664]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #680]
    ldr x0, [sp, #680]
    ldr x1, [sp, #656]
    bl _strcpy
    ldr x0, [sp, #680]
    ldr x1, [sp, #664]
    bl _strcat
    ldr x0, [sp, #680]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactDecodeLine_endif18
L_kuro_fn_ArtifactDecodeLine_else17:
    mov x0, #1
    str x0, [sp, #688]
    ldr x0, [sp, #688]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
L_kuro_fn_ArtifactDecodeLine_endif18:
L_kuro_fn_ArtifactDecodeLine_endif16:
L_kuro_fn_ArtifactDecodeLine_endif14:
L_kuro_fn_ArtifactDecodeLine_endif12:
L_kuro_fn_ArtifactDecodeLine_endif10:
    b L_kuro_fn_ArtifactDecodeLine_endif8
L_kuro_fn_ArtifactDecodeLine_else7:
    mov x0, #1
    str x0, [sp, #696]
    ldr x0, [sp, #696]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
L_kuro_fn_ArtifactDecodeLine_endif8:
    b L_kuro_fn_ArtifactDecodeLine_endif6
L_kuro_fn_ArtifactDecodeLine_else5:
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #704]
    adrp x0, _kuro_global_3@PAGE
    add x0, x0, _kuro_global_3@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #712]
    ldr x0, [sp, #704]
    ldr x1, [sp, #712]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #720]
    ldr x0, [sp, #720]
    ldr x1, [sp, #704]
    bl _strcpy
    ldr x0, [sp, #720]
    ldr x1, [sp, #712]
    bl _strcat
    ldr x0, [sp, #720]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
L_kuro_fn_ArtifactDecodeLine_endif6:
    mov x0, #1
    str x0, [sp, #728]
    adrp x0, _kuro_global_4@PAGE
    add x0, x0, _kuro_global_4@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #728]
    add x0, x0, x1
    adrp x2, _kuro_global_4@PAGE
    add x2, x2, _kuro_global_4@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactDecodeLine_while_start2
L_kuro_fn_ArtifactDecodeLine_while_end3:
    adrp x0, _kuro_global_5@PAGE
    add x0, x0, _kuro_global_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #736]
    ldr x0, [sp, #736]
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #784
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_ArtifactCommitLine:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #480
    sub sp, sp, x15
    adrp x0, _kuro_global_19@PAGE
    add x0, x0, _kuro_global_19@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    mov x0, #0
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    cbz w0, L_kuro_fn_ArtifactCommitLine_else0
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #384]
    adrp x0, _kuro_global_20@PAGE
    add x0, x0, _kuro_global_20@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #424]
    ldr x0, [sp, #384]
    ldr x1, [sp, #424]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    cbz w0, L_kuro_fn_ArtifactCommitLine_else2
    mov x0, #1
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactCommitLine_endif3
L_kuro_fn_ArtifactCommitLine_else2:
L_kuro_fn_ArtifactCommitLine_endif3:
    b L_kuro_fn_ArtifactCommitLine_endif1
L_kuro_fn_ArtifactCommitLine_else0:
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #448]
    adrp x0, _kuro_global_15@PAGE
    add x0, x0, _kuro_global_15@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #456]
    ldr x0, [sp, #448]
    ldr x1, [sp, #456]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    cbz w0, L_kuro_fn_ArtifactCommitLine_else4
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    mov x0, #0
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    cbz w0, L_kuro_fn_ArtifactCommitLine_else6
    mov x0, #1
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    adrp x2, _kuro_global_22@PAGE
    add x2, x2, _kuro_global_22@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactCommitLine_endif7
L_kuro_fn_ArtifactCommitLine_else6:
    mov x0, #1
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
L_kuro_fn_ArtifactCommitLine_endif7:
    b L_kuro_fn_ArtifactCommitLine_endif5
L_kuro_fn_ArtifactCommitLine_else4:
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #256]
    adrp x0, L_kuro_data_66@PAGE
    add x0, x0, L_kuro_data_66@PAGEOFF
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    cbz w0, L_kuro_fn_ArtifactCommitLine_else8
    mov x0, #1
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactCommitLine_endif9
L_kuro_fn_ArtifactCommitLine_else8:
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    bl _kuro_fn_ArtifactDecodeLine
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    adrp x2, _kuro_global_6@PAGE
    add x2, x2, _kuro_global_6@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_11@PAGE
    add x0, x0, _kuro_global_11@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #320]
    mov x0, #0
    str x0, [sp, #328]
    ldr x0, [sp, #320]
    ldr x1, [sp, #328]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    cbz w0, L_kuro_fn_ArtifactCommitLine_else10
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #344]
    mov x0, #65536
    str x0, [sp, #352]
    ldr x0, [sp, #344]
    ldr x1, [sp, #352]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    cbz w0, L_kuro_fn_ArtifactCommitLine_else12
    adrp x0, _kuro_global_6@PAGE
    add x0, x0, _kuro_global_6@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #368]
    adrp x1, _kuro_collection_len_0@PAGE
    add x1, x1, _kuro_collection_len_0@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #368]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_0@PAGE
    add x2, x2, _kuro_collection_len_0@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #376]
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #376]
    add x0, x0, x1
    adrp x2, _kuro_global_26@PAGE
    add x2, x2, _kuro_global_26@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_ArtifactCommitLine_endif13
L_kuro_fn_ArtifactCommitLine_else12:
    mov x0, #1
    str x0, [sp, #392]
    ldr x0, [sp, #392]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
L_kuro_fn_ArtifactCommitLine_endif13:
    b L_kuro_fn_ArtifactCommitLine_endif11
L_kuro_fn_ArtifactCommitLine_else10:
    mov x0, #1
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
L_kuro_fn_ArtifactCommitLine_endif11:
L_kuro_fn_ArtifactCommitLine_endif9:
L_kuro_fn_ArtifactCommitLine_endif5:
L_kuro_fn_ArtifactCommitLine_endif1:
    mov x0, #1
    str x0, [sp, #408]
    adrp x0, _kuro_global_19@PAGE
    add x0, x0, _kuro_global_19@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #408]
    add x0, x0, x1
    adrp x2, _kuro_global_19@PAGE
    add x2, x2, _kuro_global_19@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_67@PAGE
    add x0, x0, L_kuro_data_67@PAGEOFF
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    adrp x2, _kuro_global_18@PAGE
    add x2, x2, _kuro_global_18@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #480
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_NativeDigitText:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #448
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #152]
    mov x0, #0
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    cbz w0, L_kuro_fn_NativeDigitText_else0
    adrp x0, L_kuro_data_68@PAGE
    add x0, x0, L_kuro_data_68@PAGEOFF
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif1
L_kuro_fn_NativeDigitText_else0:
L_kuro_fn_NativeDigitText_endif1:
    ldr x0, [sp, #0]
    str x0, [sp, #400]
    mov x0, #1
    str x0, [sp, #408]
    ldr x0, [sp, #400]
    ldr x1, [sp, #408]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    cbz w0, L_kuro_fn_NativeDigitText_else2
    adrp x0, L_kuro_data_69@PAGE
    add x0, x0, L_kuro_data_69@PAGEOFF
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif3
L_kuro_fn_NativeDigitText_else2:
L_kuro_fn_NativeDigitText_endif3:
    ldr x0, [sp, #0]
    str x0, [sp, #432]
    mov x0, #2
    str x0, [sp, #440]
    ldr x0, [sp, #432]
    ldr x1, [sp, #440]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_NativeDigitText_else4
    adrp x0, L_kuro_data_70@PAGE
    add x0, x0, L_kuro_data_70@PAGEOFF
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif5
L_kuro_fn_NativeDigitText_else4:
L_kuro_fn_NativeDigitText_endif5:
    ldr x0, [sp, #0]
    str x0, [sp, #184]
    mov x0, #3
    str x0, [sp, #192]
    ldr x0, [sp, #184]
    ldr x1, [sp, #192]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    cbz w0, L_kuro_fn_NativeDigitText_else6
    adrp x0, L_kuro_data_71@PAGE
    add x0, x0, L_kuro_data_71@PAGEOFF
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif7
L_kuro_fn_NativeDigitText_else6:
L_kuro_fn_NativeDigitText_endif7:
    ldr x0, [sp, #0]
    str x0, [sp, #216]
    mov x0, #4
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    cbz w0, L_kuro_fn_NativeDigitText_else8
    adrp x0, L_kuro_data_72@PAGE
    add x0, x0, L_kuro_data_72@PAGEOFF
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif9
L_kuro_fn_NativeDigitText_else8:
L_kuro_fn_NativeDigitText_endif9:
    ldr x0, [sp, #0]
    str x0, [sp, #256]
    mov x0, #5
    str x0, [sp, #264]
    ldr x0, [sp, #256]
    ldr x1, [sp, #264]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    cbz w0, L_kuro_fn_NativeDigitText_else10
    adrp x0, L_kuro_data_73@PAGE
    add x0, x0, L_kuro_data_73@PAGEOFF
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif11
L_kuro_fn_NativeDigitText_else10:
L_kuro_fn_NativeDigitText_endif11:
    ldr x0, [sp, #0]
    str x0, [sp, #288]
    mov x0, #6
    str x0, [sp, #296]
    ldr x0, [sp, #288]
    ldr x1, [sp, #296]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    cbz w0, L_kuro_fn_NativeDigitText_else12
    adrp x0, L_kuro_data_74@PAGE
    add x0, x0, L_kuro_data_74@PAGEOFF
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif13
L_kuro_fn_NativeDigitText_else12:
L_kuro_fn_NativeDigitText_endif13:
    ldr x0, [sp, #0]
    str x0, [sp, #320]
    mov x0, #7
    str x0, [sp, #328]
    ldr x0, [sp, #320]
    ldr x1, [sp, #328]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    cbz w0, L_kuro_fn_NativeDigitText_else14
    adrp x0, L_kuro_data_75@PAGE
    add x0, x0, L_kuro_data_75@PAGEOFF
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif15
L_kuro_fn_NativeDigitText_else14:
L_kuro_fn_NativeDigitText_endif15:
    ldr x0, [sp, #0]
    str x0, [sp, #360]
    mov x0, #8
    str x0, [sp, #368]
    ldr x0, [sp, #360]
    ldr x1, [sp, #368]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    cbz w0, L_kuro_fn_NativeDigitText_else16
    adrp x0, L_kuro_data_76@PAGE
    add x0, x0, L_kuro_data_76@PAGEOFF
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeDigitText_endif17
L_kuro_fn_NativeDigitText_else16:
L_kuro_fn_NativeDigitText_endif17:
    adrp x0, L_kuro_data_77@PAGE
    add x0, x0, L_kuro_data_77@PAGEOFF
    str x0, [sp, #392]
    ldr x0, [sp, #392]
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_NativeLengthToText:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #720
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_55@PAGE
    add x2, x2, _kuro_global_55@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_54@PAGE
    add x2, x2, _kuro_global_54@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    adrp x2, _kuro_global_49@PAGE
    add x2, x2, _kuro_global_49@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    adrp x2, _kuro_global_52@PAGE
    add x2, x2, _kuro_global_52@PAGEOFF
    str x0, [x2]
L_kuro_fn_NativeLengthToText_while_start0:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #392]
    mov x0, #1000
    str x0, [sp, #480]
    ldr x0, [sp, #392]
    ldr x1, [sp, #480]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #568]
    ldr x0, [sp, #568]
    cbz w0, L_kuro_fn_NativeLengthToText_while_end1
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #648]
    mov x0, #1000
    str x0, [sp, #656]
    ldr x0, [sp, #648]
    ldr x1, [sp, #656]
    sub x0, x0, x1
    str x0, [sp, #664]
    ldr x0, [sp, #664]
    adrp x2, _kuro_global_55@PAGE
    add x2, x2, _kuro_global_55@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_54@PAGE
    add x0, x0, _kuro_global_54@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_54@PAGE
    add x2, x2, _kuro_global_54@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeLengthToText_while_start0
L_kuro_fn_NativeLengthToText_while_end1:
L_kuro_fn_NativeLengthToText_while_start3:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    mov x0, #100
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_NativeLengthToText_while_end4
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    mov x0, #100
    str x0, [sp, #176]
    ldr x0, [sp, #168]
    ldr x1, [sp, #176]
    sub x0, x0, x1
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_55@PAGE
    add x2, x2, _kuro_global_55@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #192]
    adrp x0, _kuro_global_49@PAGE
    add x0, x0, _kuro_global_49@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #192]
    add x0, x0, x1
    adrp x2, _kuro_global_49@PAGE
    add x2, x2, _kuro_global_49@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeLengthToText_while_start3
L_kuro_fn_NativeLengthToText_while_end4:
L_kuro_fn_NativeLengthToText_while_start6:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    mov x0, #10
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_NativeLengthToText_while_end7
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    mov x0, #10
    str x0, [sp, #240]
    ldr x0, [sp, #232]
    ldr x1, [sp, #240]
    sub x0, x0, x1
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    adrp x2, _kuro_global_55@PAGE
    add x2, x2, _kuro_global_55@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #256]
    adrp x0, _kuro_global_52@PAGE
    add x0, x0, _kuro_global_52@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #256]
    add x0, x0, x1
    adrp x2, _kuro_global_52@PAGE
    add x2, x2, _kuro_global_52@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeLengthToText_while_start6
L_kuro_fn_NativeLengthToText_while_end7:
    adrp x0, L_kuro_data_78@PAGE
    add x0, x0, L_kuro_data_78@PAGEOFF
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    adrp x2, _kuro_global_51@PAGE
    add x2, x2, _kuro_global_51@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_54@PAGE
    add x0, x0, _kuro_global_54@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #272]
    mov x0, #0
    str x0, [sp, #280]
    ldr x0, [sp, #272]
    ldr x1, [sp, #280]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    cbz w0, L_kuro_fn_NativeLengthToText_else9
    adrp x0, _kuro_global_54@PAGE
    add x0, x0, _kuro_global_54@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    bl _kuro_fn_NativeDigitText
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_51@PAGE
    add x0, x0, _kuro_global_51@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #320]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #328]
    ldr x0, [sp, #320]
    ldr x1, [sp, #328]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    ldr x1, [sp, #320]
    bl _strcpy
    ldr x0, [sp, #336]
    ldr x1, [sp, #328]
    bl _strcat
    ldr x0, [sp, #336]
    adrp x2, _kuro_global_51@PAGE
    add x2, x2, _kuro_global_51@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeLengthToText_endif10
L_kuro_fn_NativeLengthToText_else9:
L_kuro_fn_NativeLengthToText_endif10:
    adrp x0, _kuro_global_54@PAGE
    add x0, x0, _kuro_global_54@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #344]
    mov x0, #0
    str x0, [sp, #352]
    ldr x0, [sp, #344]
    ldr x1, [sp, #352]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #360]
    adrp x0, _kuro_global_49@PAGE
    add x0, x0, _kuro_global_49@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #368]
    mov x0, #0
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #384]
    ldr x0, [sp, #360]
    ldr x1, [sp, #384]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    cbz w0, L_kuro_fn_NativeLengthToText_else11
    adrp x0, _kuro_global_49@PAGE
    add x0, x0, _kuro_global_49@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    bl _kuro_fn_NativeDigitText
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_51@PAGE
    add x0, x0, _kuro_global_51@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #424]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #432]
    ldr x0, [sp, #424]
    ldr x1, [sp, #432]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    ldr x1, [sp, #424]
    bl _strcpy
    ldr x0, [sp, #440]
    ldr x1, [sp, #432]
    bl _strcat
    ldr x0, [sp, #440]
    adrp x2, _kuro_global_51@PAGE
    add x2, x2, _kuro_global_51@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeLengthToText_endif12
L_kuro_fn_NativeLengthToText_else11:
L_kuro_fn_NativeLengthToText_endif12:
    adrp x0, _kuro_global_54@PAGE
    add x0, x0, _kuro_global_54@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #448]
    mov x0, #0
    str x0, [sp, #456]
    ldr x0, [sp, #448]
    ldr x1, [sp, #456]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #464]
    adrp x0, _kuro_global_49@PAGE
    add x0, x0, _kuro_global_49@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #472]
    mov x0, #0
    str x0, [sp, #488]
    ldr x0, [sp, #472]
    ldr x1, [sp, #488]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #496]
    ldr x0, [sp, #464]
    ldr x1, [sp, #496]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #504]
    adrp x0, _kuro_global_52@PAGE
    add x0, x0, _kuro_global_52@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #512]
    mov x0, #0
    str x0, [sp, #520]
    ldr x0, [sp, #512]
    ldr x1, [sp, #520]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #528]
    ldr x0, [sp, #504]
    ldr x1, [sp, #528]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    cbz w0, L_kuro_fn_NativeLengthToText_else13
    adrp x0, _kuro_global_52@PAGE
    add x0, x0, _kuro_global_52@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #544]
    ldr x0, [sp, #544]
    bl _kuro_fn_NativeDigitText
    str x0, [sp, #552]
    ldr x0, [sp, #552]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_51@PAGE
    add x0, x0, _kuro_global_51@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #560]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #576]
    ldr x0, [sp, #560]
    ldr x1, [sp, #576]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #584]
    ldr x0, [sp, #584]
    ldr x1, [sp, #560]
    bl _strcpy
    ldr x0, [sp, #584]
    ldr x1, [sp, #576]
    bl _strcat
    ldr x0, [sp, #584]
    adrp x2, _kuro_global_51@PAGE
    add x2, x2, _kuro_global_51@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeLengthToText_endif14
L_kuro_fn_NativeLengthToText_else13:
L_kuro_fn_NativeLengthToText_endif14:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #592]
    ldr x0, [sp, #592]
    bl _kuro_fn_NativeDigitText
    str x0, [sp, #600]
    ldr x0, [sp, #600]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #608]
    ldr x0, [sp, #608]
    adrp x2, _kuro_global_50@PAGE
    add x2, x2, _kuro_global_50@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_51@PAGE
    add x0, x0, _kuro_global_51@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #616]
    adrp x0, _kuro_global_50@PAGE
    add x0, x0, _kuro_global_50@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #624]
    ldr x0, [sp, #616]
    ldr x1, [sp, #624]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #632]
    ldr x0, [sp, #632]
    ldr x1, [sp, #616]
    bl _strcpy
    ldr x0, [sp, #632]
    ldr x1, [sp, #624]
    bl _strcat
    ldr x0, [sp, #632]
    adrp x2, _kuro_global_51@PAGE
    add x2, x2, _kuro_global_51@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_51@PAGE
    add x0, x0, _kuro_global_51@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #640]
    ldr x0, [sp, #640]
    mov x15, #720
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #720
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_EmitLiteralPrint:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #1152
    sub sp, sp, x15
    adrp x0, _kuro_collection_len_0@PAGE
    add x0, x0, _kuro_collection_len_0@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    adrp x2, _kuro_global_30@PAGE
    add x2, x2, _kuro_global_30@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_30@PAGE
    add x0, x0, _kuro_global_30@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #432]
    mov x0, #3
    str x0, [sp, #520]
    ldr x0, [sp, #432]
    ldr x1, [sp, #520]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #608]
    ldr x0, [sp, #608]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else0
    mov x0, #0
    str x0, [sp, #696]
    ldr x1, [sp, #696]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #784]
    ldr x0, [sp, #784]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #872]
    adrp x0, L_kuro_data_79@PAGE
    add x0, x0, L_kuro_data_79@PAGEOFF
    str x0, [sp, #960]
    ldr x0, [sp, #872]
    ldr x1, [sp, #960]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1048]
    ldr x0, [sp, #1048]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else2
    mov x0, #2
    str x0, [sp, #288]
    ldr x1, [sp, #288]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #368]
    adrp x0, L_kuro_data_80@PAGE
    add x0, x0, L_kuro_data_80@PAGEOFF
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else4
    mov x0, #1
    str x0, [sp, #392]
    ldr x1, [sp, #392]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    adrp x2, _kuro_global_56@PAGE
    add x2, x2, _kuro_global_56@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    cbz x0, L_kuro_fn_EmitLiteralPrint_length_zero_t18
    bl _strlen
    b L_kuro_fn_EmitLiteralPrint_length_done_t18
L_kuro_fn_EmitLiteralPrint_length_zero_t18:
    mov x0, #0
L_kuro_fn_EmitLiteralPrint_length_done_t18:
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    adrp x2, _kuro_global_57@PAGE
    add x2, x2, _kuro_global_57@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_57@PAGE
    add x0, x0, _kuro_global_57@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #440]
    mov x0, #1000
    str x0, [sp, #448]
    ldr x0, [sp, #440]
    ldr x1, [sp, #448]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #456]
    ldr x0, [sp, #456]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else6
    adrp x0, _kuro_global_57@PAGE
    add x0, x0, _kuro_global_57@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #472]
    ldr x0, [sp, #472]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #480]
    ldr x0, [sp, #480]
    adrp x2, _kuro_global_53@PAGE
    add x2, x2, _kuro_global_53@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_81@PAGE
    add x0, x0, L_kuro_data_81@PAGEOFF
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_34@PAGE
    add x2, x2, _kuro_global_34@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitLiteralPrint_while_start8:
    adrp x0, _kuro_global_34@PAGE
    add x0, x0, _kuro_global_34@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #504]
    adrp x0, _kuro_global_57@PAGE
    add x0, x0, _kuro_global_57@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #512]
    ldr x0, [sp, #504]
    ldr x1, [sp, #512]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #528]
    ldr x0, [sp, #528]
    cbz w0, L_kuro_fn_EmitLiteralPrint_while_end9
    adrp x0, _kuro_global_34@PAGE
    add x0, x0, _kuro_global_34@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #536]
    adrp x2, _kuro_global_56@PAGE
    add x2, x2, _kuro_global_56@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #536]
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
    str x0, [sp, #544]
    ldr x0, [sp, #544]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #552]
    ldr x0, [sp, #552]
    adrp x2, _kuro_global_33@PAGE
    add x2, x2, _kuro_global_33@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #560]
    adrp x0, _kuro_global_29@PAGE
    add x0, x0, _kuro_global_29@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #568]
    ldr x0, [sp, #560]
    ldr x1, [sp, #568]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #576]
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #584]
    adrp x0, _kuro_global_62@PAGE
    add x0, x0, _kuro_global_62@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #592]
    ldr x0, [sp, #584]
    ldr x1, [sp, #592]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #600]
    ldr x0, [sp, #576]
    ldr x1, [sp, #600]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #616]
    ldr x0, [sp, #616]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else11
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #624]
    adrp x0, _kuro_global_29@PAGE
    add x0, x0, _kuro_global_29@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #632]
    ldr x0, [sp, #624]
    ldr x1, [sp, #632]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #640]
    ldr x0, [sp, #640]
    ldr x1, [sp, #624]
    bl _strcpy
    ldr x0, [sp, #640]
    ldr x1, [sp, #632]
    bl _strcat
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #648]
    ldr x0, [sp, #640]
    ldr x1, [sp, #648]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #656]
    ldr x0, [sp, #656]
    ldr x1, [sp, #640]
    bl _strcpy
    ldr x0, [sp, #656]
    ldr x1, [sp, #648]
    bl _strcat
    ldr x0, [sp, #656]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitLiteralPrint_endif12
L_kuro_fn_EmitLiteralPrint_else11:
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #664]
    adrp x0, L_kuro_data_82@PAGE
    add x0, x0, L_kuro_data_82@PAGEOFF
    str x0, [sp, #672]
    ldr x0, [sp, #664]
    ldr x1, [sp, #672]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #680]
    ldr x0, [sp, #680]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else13
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #688]
    adrp x0, _kuro_global_29@PAGE
    add x0, x0, _kuro_global_29@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #704]
    ldr x0, [sp, #688]
    ldr x1, [sp, #704]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #712]
    ldr x0, [sp, #712]
    ldr x1, [sp, #688]
    bl _strcpy
    ldr x0, [sp, #712]
    ldr x1, [sp, #704]
    bl _strcat
    adrp x0, L_kuro_data_83@PAGE
    add x0, x0, L_kuro_data_83@PAGEOFF
    str x0, [sp, #720]
    ldr x0, [sp, #712]
    ldr x1, [sp, #720]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #728]
    ldr x0, [sp, #728]
    ldr x1, [sp, #712]
    bl _strcpy
    ldr x0, [sp, #728]
    ldr x1, [sp, #720]
    bl _strcat
    ldr x0, [sp, #728]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitLiteralPrint_endif14
L_kuro_fn_EmitLiteralPrint_else13:
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #736]
    adrp x0, L_kuro_data_84@PAGE
    add x0, x0, L_kuro_data_84@PAGEOFF
    str x0, [sp, #744]
    ldr x0, [sp, #736]
    ldr x1, [sp, #744]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #752]
    ldr x0, [sp, #752]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else15
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #760]
    adrp x0, _kuro_global_29@PAGE
    add x0, x0, _kuro_global_29@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #768]
    ldr x0, [sp, #760]
    ldr x1, [sp, #768]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #776]
    ldr x0, [sp, #776]
    ldr x1, [sp, #760]
    bl _strcpy
    ldr x0, [sp, #776]
    ldr x1, [sp, #768]
    bl _strcat
    adrp x0, L_kuro_data_85@PAGE
    add x0, x0, L_kuro_data_85@PAGEOFF
    str x0, [sp, #792]
    ldr x0, [sp, #776]
    ldr x1, [sp, #792]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #800]
    ldr x0, [sp, #800]
    ldr x1, [sp, #776]
    bl _strcpy
    ldr x0, [sp, #800]
    ldr x1, [sp, #792]
    bl _strcat
    ldr x0, [sp, #800]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitLiteralPrint_endif16
L_kuro_fn_EmitLiteralPrint_else15:
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #808]
    adrp x0, L_kuro_data_86@PAGE
    add x0, x0, L_kuro_data_86@PAGEOFF
    str x0, [sp, #816]
    ldr x0, [sp, #808]
    ldr x1, [sp, #816]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #824]
    ldr x0, [sp, #824]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else17
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #832]
    adrp x0, _kuro_global_29@PAGE
    add x0, x0, _kuro_global_29@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #840]
    ldr x0, [sp, #832]
    ldr x1, [sp, #840]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #848]
    ldr x0, [sp, #848]
    ldr x1, [sp, #832]
    bl _strcpy
    ldr x0, [sp, #848]
    ldr x1, [sp, #840]
    bl _strcat
    adrp x0, L_kuro_data_87@PAGE
    add x0, x0, L_kuro_data_87@PAGEOFF
    str x0, [sp, #856]
    ldr x0, [sp, #848]
    ldr x1, [sp, #856]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #864]
    ldr x0, [sp, #864]
    ldr x1, [sp, #848]
    bl _strcpy
    ldr x0, [sp, #864]
    ldr x1, [sp, #856]
    bl _strcat
    ldr x0, [sp, #864]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitLiteralPrint_endif18
L_kuro_fn_EmitLiteralPrint_else17:
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #880]
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #888]
    ldr x0, [sp, #880]
    ldr x1, [sp, #888]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #896]
    ldr x0, [sp, #896]
    ldr x1, [sp, #880]
    bl _strcpy
    ldr x0, [sp, #896]
    ldr x1, [sp, #888]
    bl _strcat
    ldr x0, [sp, #896]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitLiteralPrint_endif18:
L_kuro_fn_EmitLiteralPrint_endif16:
L_kuro_fn_EmitLiteralPrint_endif14:
L_kuro_fn_EmitLiteralPrint_endif12:
    mov x0, #1
    str x0, [sp, #904]
    adrp x0, _kuro_global_34@PAGE
    add x0, x0, _kuro_global_34@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #904]
    add x0, x0, x1
    adrp x2, _kuro_global_34@PAGE
    add x2, x2, _kuro_global_34@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitLiteralPrint_while_start8
L_kuro_fn_EmitLiteralPrint_while_end9:
    b L_kuro_fn_EmitLiteralPrint_endif7
L_kuro_fn_EmitLiteralPrint_else6:
L_kuro_fn_EmitLiteralPrint_endif7:
    adrp x0, _kuro_global_53@PAGE
    add x0, x0, _kuro_global_53@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #912]
    adrp x0, L_kuro_data_88@PAGE
    add x0, x0, L_kuro_data_88@PAGEOFF
    str x0, [sp, #920]
    ldr x0, [sp, #912]
    ldr x1, [sp, #920]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #928]
    ldr x0, [sp, #928]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else19
    adrp x0, L_kuro_data_89@PAGE
    add x0, x0, L_kuro_data_89@PAGEOFF
    str x0, [sp, #936]
    ldr x0, [sp, #936]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #944]
    adrp x0, L_kuro_data_90@PAGE
    add x0, x0, L_kuro_data_90@PAGEOFF
    str x0, [sp, #952]
    ldr x0, [sp, #944]
    ldr x1, [sp, #952]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #968]
    ldr x0, [sp, #968]
    ldr x1, [sp, #944]
    bl _strcpy
    ldr x0, [sp, #968]
    ldr x1, [sp, #952]
    bl _strcat
    ldr x0, [sp, #968]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #976]
    adrp x0, L_kuro_data_91@PAGE
    add x0, x0, L_kuro_data_91@PAGEOFF
    str x0, [sp, #984]
    ldr x0, [sp, #976]
    ldr x1, [sp, #984]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #992]
    ldr x0, [sp, #992]
    ldr x1, [sp, #976]
    bl _strcpy
    ldr x0, [sp, #992]
    ldr x1, [sp, #984]
    bl _strcat
    ldr x0, [sp, #992]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1000]
    adrp x0, L_kuro_data_92@PAGE
    add x0, x0, L_kuro_data_92@PAGEOFF
    str x0, [sp, #1008]
    ldr x0, [sp, #1000]
    ldr x1, [sp, #1008]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1016]
    ldr x0, [sp, #1016]
    ldr x1, [sp, #1000]
    bl _strcpy
    ldr x0, [sp, #1016]
    ldr x1, [sp, #1008]
    bl _strcat
    ldr x0, [sp, #1016]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1024]
    adrp x0, _kuro_global_53@PAGE
    add x0, x0, _kuro_global_53@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1032]
    ldr x0, [sp, #1024]
    ldr x1, [sp, #1032]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1040]
    ldr x0, [sp, #1040]
    ldr x1, [sp, #1024]
    bl _strcpy
    ldr x0, [sp, #1040]
    ldr x1, [sp, #1032]
    bl _strcat
    adrp x0, L_kuro_data_93@PAGE
    add x0, x0, L_kuro_data_93@PAGEOFF
    str x0, [sp, #1056]
    ldr x0, [sp, #1040]
    ldr x1, [sp, #1056]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1064]
    ldr x0, [sp, #1064]
    ldr x1, [sp, #1040]
    bl _strcpy
    ldr x0, [sp, #1064]
    ldr x1, [sp, #1056]
    bl _strcat
    ldr x0, [sp, #1064]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1072]
    adrp x0, L_kuro_data_94@PAGE
    add x0, x0, L_kuro_data_94@PAGEOFF
    str x0, [sp, #1080]
    ldr x0, [sp, #1072]
    ldr x1, [sp, #1080]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1088]
    ldr x0, [sp, #1088]
    ldr x1, [sp, #1072]
    bl _strcpy
    ldr x0, [sp, #1088]
    ldr x1, [sp, #1080]
    bl _strcat
    ldr x0, [sp, #1088]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1096]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1104]
    ldr x0, [sp, #1096]
    ldr x1, [sp, #1104]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1112]
    ldr x0, [sp, #1112]
    ldr x1, [sp, #1096]
    bl _strcpy
    ldr x0, [sp, #1112]
    ldr x1, [sp, #1104]
    bl _strcat
    adrp x0, L_kuro_data_95@PAGE
    add x0, x0, L_kuro_data_95@PAGEOFF
    str x0, [sp, #1120]
    ldr x0, [sp, #1112]
    ldr x1, [sp, #1120]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1128]
    ldr x0, [sp, #1128]
    ldr x1, [sp, #1112]
    bl _strcpy
    ldr x0, [sp, #1128]
    ldr x1, [sp, #1120]
    bl _strcat
    ldr x0, [sp, #1128]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    cmp x0, #4096
    b.lo L_kuro_print_dynamic_number_EmitLiteralPrint_t100
    mov x1, #0x100000000000
    cmp x0, x1
    b.lo L_kuro_print_dynamic_text_EmitLiteralPrint_t100
L_kuro_print_dynamic_float_EmitLiteralPrint_t100:
    sub sp, sp, #16
    str x0, [sp]
    adrp x0, L_kuro_float_format@PAGE
    add x0, x0, L_kuro_float_format@PAGEOFF
    bl _printf
    add sp, sp, #16
    b L_kuro_print_dynamic_done_EmitLiteralPrint_t100
L_kuro_print_dynamic_text_EmitLiteralPrint_t100:
    bl _puts
    b L_kuro_print_dynamic_done_EmitLiteralPrint_t100
L_kuro_print_dynamic_number_EmitLiteralPrint_t100:
    bl _kuro_print_int
L_kuro_print_dynamic_done_EmitLiteralPrint_t100:
    b L_kuro_fn_EmitLiteralPrint_endif20
L_kuro_fn_EmitLiteralPrint_else19:
L_kuro_fn_EmitLiteralPrint_endif20:
    adrp x0, _kuro_global_53@PAGE
    add x0, x0, _kuro_global_53@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #304]
    adrp x0, L_kuro_data_96@PAGE
    add x0, x0, L_kuro_data_96@PAGEOFF
    str x0, [sp, #312]
    ldr x0, [sp, #304]
    ldr x1, [sp, #312]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    cbz w0, L_kuro_fn_EmitLiteralPrint_else21
    mov x0, #1
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitLiteralPrint_endif22
L_kuro_fn_EmitLiteralPrint_else21:
L_kuro_fn_EmitLiteralPrint_endif22:
    b L_kuro_fn_EmitLiteralPrint_endif5
L_kuro_fn_EmitLiteralPrint_else4:
    mov x0, #1
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitLiteralPrint_endif5:
    b L_kuro_fn_EmitLiteralPrint_endif3
L_kuro_fn_EmitLiteralPrint_else2:
    mov x0, #1
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitLiteralPrint_endif3:
    b L_kuro_fn_EmitLiteralPrint_endif1
L_kuro_fn_EmitLiteralPrint_else0:
    mov x0, #1
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitLiteralPrint_endif1:
    mov x0, #0
    mov x15, #1152
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_NativeValidateUnsignedInteger:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #272
    sub sp, sp, x15
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    cbz x0, L_kuro_fn_NativeValidateUnsignedInteger_length_zero_t0
    bl _strlen
    b L_kuro_fn_NativeValidateUnsignedInteger_length_done_t0
L_kuro_fn_NativeValidateUnsignedInteger_length_zero_t0:
    mov x0, #0
L_kuro_fn_NativeValidateUnsignedInteger_length_done_t0:
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_44@PAGE
    add x2, x2, _kuro_global_44@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    adrp x2, _kuro_global_45@PAGE
    add x2, x2, _kuro_global_45@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_44@PAGE
    add x0, x0, _kuro_global_44@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    mov x0, #0
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #208]
    adrp x0, _kuro_global_44@PAGE
    add x0, x0, _kuro_global_44@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    mov x0, #4
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #232]
    ldr x0, [sp, #208]
    ldr x1, [sp, #232]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_NativeValidateUnsignedInteger_else0
    mov x0, #0
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_45@PAGE
    add x2, x2, _kuro_global_45@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeValidateUnsignedInteger_endif1
L_kuro_fn_NativeValidateUnsignedInteger_else0:
L_kuro_fn_NativeValidateUnsignedInteger_endif1:
    mov x0, #0
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    adrp x2, _kuro_global_43@PAGE
    add x2, x2, _kuro_global_43@PAGEOFF
    str x0, [x2]
L_kuro_fn_NativeValidateUnsignedInteger_while_start2:
    adrp x0, _kuro_global_43@PAGE
    add x0, x0, _kuro_global_43@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    adrp x0, _kuro_global_44@PAGE
    add x0, x0, _kuro_global_44@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #112]
    ldr x0, [sp, #104]
    ldr x1, [sp, #112]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    cbz w0, L_kuro_fn_NativeValidateUnsignedInteger_while_end3
    adrp x0, _kuro_global_43@PAGE
    add x0, x0, _kuro_global_43@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x2, [sp, #24]
    ldr x1, [sp, #128]
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
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    cmp x0, #0
    b.le L_kuro_fn_NativeValidateUnsignedInteger_isclass_invalid_t18
    cmp x0, #0x1000
    b.lo L_kuro_fn_NativeValidateUnsignedInteger_isclass_invalid_t18
    ldrb w0, [x0]
    sub w0, w0, #48
    cmp w0, #9
    cset w0, ls
    b L_kuro_fn_NativeValidateUnsignedInteger_isclass_done_t18
L_kuro_fn_NativeValidateUnsignedInteger_isclass_invalid_t18:
    mov x0, #0
L_kuro_fn_NativeValidateUnsignedInteger_isclass_done_t18:
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_NativeValidateUnsignedInteger_else5
    b L_kuro_fn_NativeValidateUnsignedInteger_endif6
L_kuro_fn_NativeValidateUnsignedInteger_else5:
    mov x0, #0
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_45@PAGE
    add x2, x2, _kuro_global_45@PAGEOFF
    str x0, [x2]
L_kuro_fn_NativeValidateUnsignedInteger_endif6:
    mov x0, #1
    str x0, [sp, #176]
    adrp x0, _kuro_global_43@PAGE
    add x0, x0, _kuro_global_43@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #176]
    add x0, x0, x1
    adrp x2, _kuro_global_43@PAGE
    add x2, x2, _kuro_global_43@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_NativeValidateUnsignedInteger_while_start2
L_kuro_fn_NativeValidateUnsignedInteger_while_end3:
    adrp x0, _kuro_global_45@PAGE
    add x0, x0, _kuro_global_45@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    mov x15, #272
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #272
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_EmitIntegerBinaryPrint:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #1040
    sub sp, sp, x15
    mov x0, #1
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #288]
    ldr x1, [sp, #288]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #464]
    adrp x0, L_kuro_data_97@PAGE
    add x0, x0, L_kuro_data_97@PAGEOFF
    str x0, [sp, #552]
    ldr x0, [sp, #464]
    ldr x1, [sp, #552]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #640]
    ldr x0, [sp, #640]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else0
    mov x0, #0
    str x0, [sp, #728]
    ldr x0, [sp, #728]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif1
L_kuro_fn_EmitIntegerBinaryPrint_else0:
L_kuro_fn_EmitIntegerBinaryPrint_endif1:
    mov x0, #2
    str x0, [sp, #816]
    ldr x1, [sp, #816]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #904]
    ldr x0, [sp, #904]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #992]
    adrp x0, L_kuro_data_98@PAGE
    add x0, x0, L_kuro_data_98@PAGEOFF
    str x0, [sp, #296]
    ldr x0, [sp, #992]
    ldr x1, [sp, #296]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else2
    mov x0, #0
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif3
L_kuro_fn_EmitIntegerBinaryPrint_else2:
L_kuro_fn_EmitIntegerBinaryPrint_endif3:
    mov x0, #4
    str x0, [sp, #320]
    ldr x1, [sp, #320]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #336]
    adrp x0, L_kuro_data_99@PAGE
    add x0, x0, L_kuro_data_99@PAGEOFF
    str x0, [sp, #344]
    ldr x0, [sp, #336]
    ldr x1, [sp, #344]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else4
    mov x0, #0
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif5
L_kuro_fn_EmitIntegerBinaryPrint_else4:
L_kuro_fn_EmitIntegerBinaryPrint_endif5:
    mov x0, #6
    str x0, [sp, #368]
    ldr x1, [sp, #368]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #392]
    adrp x0, L_kuro_data_100@PAGE
    add x0, x0, L_kuro_data_100@PAGEOFF
    str x0, [sp, #400]
    ldr x0, [sp, #392]
    ldr x1, [sp, #400]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else6
    mov x0, #0
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif7
L_kuro_fn_EmitIntegerBinaryPrint_else6:
L_kuro_fn_EmitIntegerBinaryPrint_endif7:
    mov x0, #1
    str x0, [sp, #424]
    ldr x1, [sp, #424]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    adrp x2, _kuro_global_46@PAGE
    add x2, x2, _kuro_global_46@PAGEOFF
    str x0, [x2]
    mov x0, #3
    str x0, [sp, #448]
    ldr x1, [sp, #448]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #456]
    ldr x0, [sp, #456]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #472]
    ldr x0, [sp, #472]
    adrp x2, _kuro_global_69@PAGE
    add x2, x2, _kuro_global_69@PAGEOFF
    str x0, [x2]
    mov x0, #5
    str x0, [sp, #480]
    ldr x1, [sp, #480]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_58@PAGE
    add x2, x2, _kuro_global_58@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_46@PAGE
    add x0, x0, _kuro_global_46@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #504]
    ldr x0, [sp, #504]
    bl _kuro_fn_NativeValidateUnsignedInteger
    str x0, [sp, #512]
    ldr x0, [sp, #512]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #520]
    mov x0, #0
    str x0, [sp, #528]
    ldr x0, [sp, #520]
    ldr x1, [sp, #528]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else8
    mov x0, #0
    str x0, [sp, #544]
    ldr x0, [sp, #544]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif9
L_kuro_fn_EmitIntegerBinaryPrint_else8:
L_kuro_fn_EmitIntegerBinaryPrint_endif9:
    adrp x0, _kuro_global_69@PAGE
    add x0, x0, _kuro_global_69@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #560]
    ldr x0, [sp, #560]
    bl _kuro_fn_NativeValidateUnsignedInteger
    str x0, [sp, #568]
    ldr x0, [sp, #568]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #576]
    mov x0, #0
    str x0, [sp, #584]
    ldr x0, [sp, #576]
    ldr x1, [sp, #584]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #592]
    ldr x0, [sp, #592]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else10
    mov x0, #0
    str x0, [sp, #600]
    ldr x0, [sp, #600]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif11
L_kuro_fn_EmitIntegerBinaryPrint_else10:
L_kuro_fn_EmitIntegerBinaryPrint_endif11:
    adrp x0, L_kuro_data_101@PAGE
    add x0, x0, L_kuro_data_101@PAGEOFF
    str x0, [sp, #608]
    ldr x0, [sp, #608]
    adrp x2, _kuro_global_42@PAGE
    add x2, x2, _kuro_global_42@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_58@PAGE
    add x0, x0, _kuro_global_58@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #616]
    adrp x0, L_kuro_data_102@PAGE
    add x0, x0, L_kuro_data_102@PAGEOFF
    str x0, [sp, #624]
    ldr x0, [sp, #616]
    ldr x1, [sp, #624]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #632]
    ldr x0, [sp, #632]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else12
    adrp x0, L_kuro_data_103@PAGE
    add x0, x0, L_kuro_data_103@PAGEOFF
    str x0, [sp, #648]
    ldr x0, [sp, #648]
    adrp x2, _kuro_global_42@PAGE
    add x2, x2, _kuro_global_42@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif13
L_kuro_fn_EmitIntegerBinaryPrint_else12:
L_kuro_fn_EmitIntegerBinaryPrint_endif13:
    adrp x0, _kuro_global_58@PAGE
    add x0, x0, _kuro_global_58@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #656]
    adrp x0, L_kuro_data_104@PAGE
    add x0, x0, L_kuro_data_104@PAGEOFF
    str x0, [sp, #664]
    ldr x0, [sp, #656]
    ldr x1, [sp, #664]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #672]
    ldr x0, [sp, #672]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else14
    adrp x0, L_kuro_data_105@PAGE
    add x0, x0, L_kuro_data_105@PAGEOFF
    str x0, [sp, #680]
    ldr x0, [sp, #680]
    adrp x2, _kuro_global_42@PAGE
    add x2, x2, _kuro_global_42@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif15
L_kuro_fn_EmitIntegerBinaryPrint_else14:
L_kuro_fn_EmitIntegerBinaryPrint_endif15:
    adrp x0, _kuro_global_58@PAGE
    add x0, x0, _kuro_global_58@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #688]
    adrp x0, L_kuro_data_106@PAGE
    add x0, x0, L_kuro_data_106@PAGEOFF
    str x0, [sp, #696]
    ldr x0, [sp, #688]
    ldr x1, [sp, #696]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #704]
    ldr x0, [sp, #704]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else16
    adrp x0, L_kuro_data_107@PAGE
    add x0, x0, L_kuro_data_107@PAGEOFF
    str x0, [sp, #712]
    ldr x0, [sp, #712]
    adrp x2, _kuro_global_42@PAGE
    add x2, x2, _kuro_global_42@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif17
L_kuro_fn_EmitIntegerBinaryPrint_else16:
L_kuro_fn_EmitIntegerBinaryPrint_endif17:
    adrp x0, _kuro_global_58@PAGE
    add x0, x0, _kuro_global_58@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #720]
    adrp x0, L_kuro_data_108@PAGE
    add x0, x0, L_kuro_data_108@PAGEOFF
    str x0, [sp, #736]
    ldr x0, [sp, #720]
    ldr x1, [sp, #736]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #744]
    ldr x0, [sp, #744]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else18
    adrp x0, L_kuro_data_109@PAGE
    add x0, x0, L_kuro_data_109@PAGEOFF
    str x0, [sp, #752]
    ldr x0, [sp, #752]
    adrp x2, _kuro_global_42@PAGE
    add x2, x2, _kuro_global_42@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_69@PAGE
    add x0, x0, _kuro_global_69@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #760]
    adrp x0, L_kuro_data_110@PAGE
    add x0, x0, L_kuro_data_110@PAGEOFF
    str x0, [sp, #768]
    ldr x0, [sp, #760]
    ldr x1, [sp, #768]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #776]
    ldr x0, [sp, #776]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else20
    mov x0, #0
    str x0, [sp, #784]
    ldr x0, [sp, #784]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif21
L_kuro_fn_EmitIntegerBinaryPrint_else20:
L_kuro_fn_EmitIntegerBinaryPrint_endif21:
    b L_kuro_fn_EmitIntegerBinaryPrint_endif19
L_kuro_fn_EmitIntegerBinaryPrint_else18:
L_kuro_fn_EmitIntegerBinaryPrint_endif19:
    adrp x0, _kuro_global_42@PAGE
    add x0, x0, _kuro_global_42@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #792]
    adrp x0, L_kuro_data_111@PAGE
    add x0, x0, L_kuro_data_111@PAGEOFF
    str x0, [sp, #800]
    ldr x0, [sp, #792]
    ldr x1, [sp, #800]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #808]
    ldr x0, [sp, #808]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else22
    mov x0, #0
    str x0, [sp, #824]
    ldr x0, [sp, #824]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitIntegerBinaryPrint_endif23
L_kuro_fn_EmitIntegerBinaryPrint_else22:
L_kuro_fn_EmitIntegerBinaryPrint_endif23:
    adrp x0, _kuro_global_28@PAGE
    add x0, x0, _kuro_global_28@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #832]
    mov x0, #1
    str x0, [sp, #840]
    ldr x0, [sp, #832]
    ldr x1, [sp, #840]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #848]
    ldr x0, [sp, #848]
    cbz w0, L_kuro_fn_EmitIntegerBinaryPrint_else24
    adrp x0, L_kuro_data_112@PAGE
    add x0, x0, L_kuro_data_112@PAGEOFF
    str x0, [sp, #856]
    ldr x0, [sp, #856]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #864]
    adrp x0, _kuro_global_46@PAGE
    add x0, x0, _kuro_global_46@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #872]
    ldr x0, [sp, #864]
    ldr x1, [sp, #872]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #880]
    ldr x0, [sp, #880]
    ldr x1, [sp, #864]
    bl _strcpy
    ldr x0, [sp, #880]
    ldr x1, [sp, #872]
    bl _strcat
    adrp x0, L_kuro_data_113@PAGE
    add x0, x0, L_kuro_data_113@PAGEOFF
    str x0, [sp, #888]
    ldr x0, [sp, #880]
    ldr x1, [sp, #888]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #896]
    ldr x0, [sp, #896]
    ldr x1, [sp, #880]
    bl _strcpy
    ldr x0, [sp, #896]
    ldr x1, [sp, #888]
    bl _strcat
    adrp x0, _kuro_global_69@PAGE
    add x0, x0, _kuro_global_69@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #912]
    ldr x0, [sp, #896]
    ldr x1, [sp, #912]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #920]
    ldr x0, [sp, #920]
    ldr x1, [sp, #896]
    bl _strcpy
    ldr x0, [sp, #920]
    ldr x1, [sp, #912]
    bl _strcat
    adrp x0, L_kuro_data_114@PAGE
    add x0, x0, L_kuro_data_114@PAGEOFF
    str x0, [sp, #928]
    ldr x0, [sp, #920]
    ldr x1, [sp, #928]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #936]
    ldr x0, [sp, #936]
    ldr x1, [sp, #920]
    bl _strcpy
    ldr x0, [sp, #936]
    ldr x1, [sp, #928]
    bl _strcat
    ldr x0, [sp, #936]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #944]
    adrp x0, _kuro_global_42@PAGE
    add x0, x0, _kuro_global_42@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #952]
    ldr x0, [sp, #944]
    ldr x1, [sp, #952]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #960]
    ldr x0, [sp, #960]
    ldr x1, [sp, #944]
    bl _strcpy
    ldr x0, [sp, #960]
    ldr x1, [sp, #952]
    bl _strcat
    ldr x0, [sp, #960]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #968]
    adrp x0, L_kuro_data_115@PAGE
    add x0, x0, L_kuro_data_115@PAGEOFF
    str x0, [sp, #976]
    ldr x0, [sp, #968]
    ldr x1, [sp, #976]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #984]
    ldr x0, [sp, #984]
    ldr x1, [sp, #968]
    bl _strcpy
    ldr x0, [sp, #984]
    ldr x1, [sp, #976]
    bl _strcat
    ldr x0, [sp, #984]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1000]
    adrp x0, L_kuro_data_116@PAGE
    add x0, x0, L_kuro_data_116@PAGEOFF
    str x0, [sp, #1008]
    ldr x0, [sp, #1000]
    ldr x1, [sp, #1008]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1016]
    ldr x0, [sp, #1016]
    ldr x1, [sp, #1000]
    bl _strcpy
    ldr x0, [sp, #1016]
    ldr x1, [sp, #1008]
    bl _strcat
    ldr x0, [sp, #1016]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1024]
    ldr x0, [sp, #1024]
    cmp x0, #4096
    b.lo L_kuro_print_dynamic_number_EmitIntegerBinaryPrint_t93
    mov x1, #0x100000000000
    cmp x0, x1
    b.lo L_kuro_print_dynamic_text_EmitIntegerBinaryPrint_t93
L_kuro_print_dynamic_float_EmitIntegerBinaryPrint_t93:
    sub sp, sp, #16
    str x0, [sp]
    adrp x0, L_kuro_float_format@PAGE
    add x0, x0, L_kuro_float_format@PAGEOFF
    bl _printf
    add sp, sp, #16
    b L_kuro_print_dynamic_done_EmitIntegerBinaryPrint_t93
L_kuro_print_dynamic_text_EmitIntegerBinaryPrint_t93:
    bl _puts
    b L_kuro_print_dynamic_done_EmitIntegerBinaryPrint_t93
L_kuro_print_dynamic_number_EmitIntegerBinaryPrint_t93:
    bl _kuro_print_int
L_kuro_print_dynamic_done_EmitIntegerBinaryPrint_t93:
    b L_kuro_fn_EmitIntegerBinaryPrint_endif25
L_kuro_fn_EmitIntegerBinaryPrint_else24:
    mov x0, #1
    str x0, [sp, #1032]
    ldr x0, [sp, #1032]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitIntegerBinaryPrint_endif25:
    mov x0, #0
    mov x15, #1040
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_NativeFindVariable:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #240
    sub sp, sp, x15
    str x0, [sp, #8]
    str x1, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #80]
    adrp x0, _kuro_global_82@PAGE
    add x0, x0, _kuro_global_82@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    ldr x0, [sp, #80]
    ldr x1, [sp, #88]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_NativeFindVariable_else0
    ldr x0, [sp, #0]
    str x0, [sp, #176]
    ldr x1, [sp, #176]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    ldr x0, [sp, #8]
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    cbz w0, L_kuro_fn_NativeFindVariable_else2
    ldr x0, [sp, #0]
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_NativeFindVariable_endif3
L_kuro_fn_NativeFindVariable_else2:
    ldr x0, [sp, #0]
    str x0, [sp, #224]
    mov x0, #1
    str x0, [sp, #96]
    ldr x0, [sp, #224]
    ldr x1, [sp, #96]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_37@PAGE
    add x2, x2, _kuro_global_37@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #8]
    str x0, [sp, #112]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    bl _kuro_fn_NativeFindVariable
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_NativeFindVariable_endif3:
    b L_kuro_fn_NativeFindVariable_endif1
L_kuro_fn_NativeFindVariable_else0:
    mov x0, #0
    str x0, [sp, #144]
    mov x0, #1
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    sub x0, x0, x1
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_NativeFindVariable_endif1:
    mov x0, #0
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_EmitStraightIntegerProgram:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #7952
    sub sp, sp, x15
    adrp x0, _kuro_collection_len_0@PAGE
    add x0, x0, _kuro_collection_len_0@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1264]
    ldr x0, [sp, #1264]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1272]
    ldr x0, [sp, #1272]
    adrp x2, _kuro_global_77@PAGE
    add x2, x2, _kuro_global_77@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2160]
    ldr x0, [sp, #2160]
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3048]
    ldr x0, [sp, #3048]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3936]
    ldr x0, [sp, #3936]
    adrp x2, _kuro_global_82@PAGE
    add x2, x2, _kuro_global_82@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4824]
    ldr x0, [sp, #4824]
    adrp x2, _kuro_global_39@PAGE
    add x2, x2, _kuro_global_39@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #5712]
    ldr x0, [sp, #5712]
    adrp x2, _kuro_global_38@PAGE
    add x2, x2, _kuro_global_38@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #6600]
    ldr x0, [sp, #6600]
    adrp x2, _kuro_global_64@PAGE
    add x2, x2, _kuro_global_64@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #7488]
    ldr x0, [sp, #7488]
    adrp x2, _kuro_global_63@PAGE
    add x2, x2, _kuro_global_63@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #7840]
    ldr x0, [sp, #7840]
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #1280]
    ldr x0, [sp, #1280]
    adrp x2, _kuro_global_87@PAGE
    add x2, x2, _kuro_global_87@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_117@PAGE
    add x0, x0, L_kuro_data_117@PAGEOFF
    str x0, [sp, #1368]
    ldr x0, [sp, #1368]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1456]
    mov x0, #64
    str x0, [sp, #1544]
    ldr x0, [sp, #1456]
    ldr x1, [sp, #1544]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #1632]
    ldr x0, [sp, #1632]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else0
    mov x0, #1
    str x0, [sp, #1720]
    ldr x0, [sp, #1720]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif1
L_kuro_fn_EmitStraightIntegerProgram_else0:
L_kuro_fn_EmitStraightIntegerProgram_endif1:
L_kuro_fn_EmitStraightIntegerProgram_while_start2:
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1808]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1896]
    ldr x0, [sp, #1808]
    ldr x1, [sp, #1896]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #1984]
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2072]
    mov x0, #0
    str x0, [sp, #2168]
    ldr x0, [sp, #2072]
    ldr x1, [sp, #2168]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2256]
    ldr x0, [sp, #1984]
    ldr x1, [sp, #2256]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #2344]
    ldr x0, [sp, #2344]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_while_end3
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2432]
    ldr x1, [sp, #2432]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #2520]
    ldr x0, [sp, #2520]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2608]
    ldr x0, [sp, #2608]
    adrp x2, _kuro_global_78@PAGE
    add x2, x2, _kuro_global_78@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2696]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2696]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2784]
    ldr x0, [sp, #2784]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2872]
    adrp x0, L_kuro_data_118@PAGE
    add x0, x0, L_kuro_data_118@PAGEOFF
    str x0, [sp, #2960]
    ldr x0, [sp, #2872]
    ldr x1, [sp, #2960]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3056]
    ldr x0, [sp, #3056]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else5
    mov x0, #1
    str x0, [sp, #3144]
    ldr x0, [sp, #3144]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3232]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3320]
    ldr x0, [sp, #3232]
    ldr x1, [sp, #3320]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #3408]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3496]
    mov x0, #128
    str x0, [sp, #3584]
    ldr x0, [sp, #3496]
    ldr x1, [sp, #3584]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #3672]
    ldr x0, [sp, #3408]
    ldr x1, [sp, #3672]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #3760]
    ldr x0, [sp, #3760]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else7
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3848]
    ldr x1, [sp, #3848]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #3944]
    ldr x0, [sp, #3944]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4032]
    ldr x0, [sp, #4032]
    adrp x2, _kuro_global_81@PAGE
    add x2, x2, _kuro_global_81@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #4120]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4120]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_81@PAGE
    add x0, x0, _kuro_global_81@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4208]
    ldr x0, [sp, #4208]
    bl _kuro_fn_NativeValidateUnsignedInteger
    str x0, [sp, #4296]
    ldr x0, [sp, #4296]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4384]
    mov x0, #1
    str x0, [sp, #4472]
    ldr x0, [sp, #4384]
    ldr x1, [sp, #4472]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4560]
    ldr x0, [sp, #4560]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else9
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4648]
    mov x0, #8
    str x0, [sp, #4736]
    ldr x0, [sp, #4648]
    ldr x1, [sp, #4736]
    mul x0, x0, x1
    str x0, [sp, #4832]
    ldr x0, [sp, #4832]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4920]
    ldr x0, [sp, #4920]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #5008]
    ldr x0, [sp, #5008]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5096]
    ldr x0, [sp, #5096]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5184]
    adrp x0, L_kuro_data_119@PAGE
    add x0, x0, L_kuro_data_119@PAGEOFF
    str x0, [sp, #5272]
    ldr x0, [sp, #5184]
    ldr x1, [sp, #5272]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5360]
    ldr x0, [sp, #5360]
    ldr x1, [sp, #5184]
    bl _strcpy
    ldr x0, [sp, #5360]
    ldr x1, [sp, #5272]
    bl _strcat
    adrp x0, _kuro_global_81@PAGE
    add x0, x0, _kuro_global_81@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5448]
    ldr x0, [sp, #5360]
    ldr x1, [sp, #5448]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5536]
    ldr x0, [sp, #5536]
    ldr x1, [sp, #5360]
    bl _strcpy
    ldr x0, [sp, #5536]
    ldr x1, [sp, #5448]
    bl _strcat
    adrp x0, L_kuro_data_120@PAGE
    add x0, x0, L_kuro_data_120@PAGEOFF
    str x0, [sp, #5624]
    ldr x0, [sp, #5536]
    ldr x1, [sp, #5624]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5720]
    ldr x0, [sp, #5720]
    ldr x1, [sp, #5536]
    bl _strcpy
    ldr x0, [sp, #5720]
    ldr x1, [sp, #5624]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5808]
    ldr x0, [sp, #5720]
    ldr x1, [sp, #5808]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5896]
    ldr x0, [sp, #5896]
    ldr x1, [sp, #5720]
    bl _strcpy
    ldr x0, [sp, #5896]
    ldr x1, [sp, #5808]
    bl _strcat
    adrp x0, L_kuro_data_121@PAGE
    add x0, x0, L_kuro_data_121@PAGEOFF
    str x0, [sp, #5984]
    ldr x0, [sp, #5896]
    ldr x1, [sp, #5984]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6072]
    ldr x0, [sp, #6072]
    ldr x1, [sp, #5896]
    bl _strcpy
    ldr x0, [sp, #6072]
    ldr x1, [sp, #5984]
    bl _strcat
    ldr x0, [sp, #6072]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #6160]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #6160]
    add x0, x0, x1
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif10
L_kuro_fn_EmitStraightIntegerProgram_else9:
    mov x0, #1
    str x0, [sp, #6248]
    ldr x0, [sp, #6248]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif10:
    b L_kuro_fn_EmitStraightIntegerProgram_endif8
L_kuro_fn_EmitStraightIntegerProgram_else7:
    mov x0, #1
    str x0, [sp, #6336]
    ldr x0, [sp, #6336]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif8:
    b L_kuro_fn_EmitStraightIntegerProgram_endif6
L_kuro_fn_EmitStraightIntegerProgram_else5:
L_kuro_fn_EmitStraightIntegerProgram_endif6:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6424]
    adrp x0, L_kuro_data_122@PAGE
    add x0, x0, L_kuro_data_122@PAGEOFF
    str x0, [sp, #6512]
    ldr x0, [sp, #6424]
    ldr x1, [sp, #6512]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #6608]
    ldr x0, [sp, #6608]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else11
    mov x0, #1
    str x0, [sp, #6696]
    ldr x0, [sp, #6696]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6784]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6872]
    ldr x0, [sp, #6784]
    ldr x1, [sp, #6872]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #6960]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7048]
    mov x0, #1
    str x0, [sp, #7136]
    ldr x0, [sp, #7048]
    ldr x1, [sp, #7136]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #7224]
    ldr x0, [sp, #6960]
    ldr x1, [sp, #7224]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #7312]
    ldr x0, [sp, #7312]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else13
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7400]
    ldr x1, [sp, #7400]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #7496]
    ldr x0, [sp, #7496]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7584]
    ldr x0, [sp, #7584]
    adrp x2, _kuro_global_79@PAGE
    add x2, x2, _kuro_global_79@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #7672]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #7672]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7760]
    mov x0, #8
    str x0, [sp, #7792]
    ldr x0, [sp, #7760]
    ldr x1, [sp, #7792]
    mul x0, x0, x1
    str x0, [sp, #7800]
    mov x0, #8
    str x0, [sp, #7808]
    ldr x0, [sp, #7800]
    ldr x1, [sp, #7808]
    sub x0, x0, x1
    str x0, [sp, #7816]
    ldr x0, [sp, #7816]
    adrp x2, _kuro_global_70@PAGE
    add x2, x2, _kuro_global_70@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7824]
    mov x0, #8
    str x0, [sp, #7832]
    ldr x0, [sp, #7824]
    ldr x1, [sp, #7832]
    mul x0, x0, x1
    str x0, [sp, #7848]
    mov x0, #16
    str x0, [sp, #7856]
    ldr x0, [sp, #7848]
    ldr x1, [sp, #7856]
    sub x0, x0, x1
    str x0, [sp, #7864]
    ldr x0, [sp, #7864]
    adrp x2, _kuro_global_47@PAGE
    add x2, x2, _kuro_global_47@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_70@PAGE
    add x0, x0, _kuro_global_70@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7872]
    ldr x0, [sp, #7872]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #7880]
    ldr x0, [sp, #7880]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7888]
    ldr x0, [sp, #7888]
    adrp x2, _kuro_global_71@PAGE
    add x2, x2, _kuro_global_71@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_47@PAGE
    add x0, x0, _kuro_global_47@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7896]
    ldr x0, [sp, #7896]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #7904]
    ldr x0, [sp, #7904]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7912]
    ldr x0, [sp, #7912]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_123@PAGE
    add x0, x0, L_kuro_data_123@PAGEOFF
    str x0, [sp, #7920]
    ldr x0, [sp, #7920]
    adrp x2, _kuro_global_75@PAGE
    add x2, x2, _kuro_global_75@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_79@PAGE
    add x0, x0, _kuro_global_79@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1288]
    adrp x0, L_kuro_data_124@PAGE
    add x0, x0, L_kuro_data_124@PAGEOFF
    str x0, [sp, #1296]
    ldr x0, [sp, #1288]
    ldr x1, [sp, #1296]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1304]
    ldr x0, [sp, #1304]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else15
    adrp x0, L_kuro_data_125@PAGE
    add x0, x0, L_kuro_data_125@PAGEOFF
    str x0, [sp, #1312]
    ldr x0, [sp, #1312]
    adrp x2, _kuro_global_75@PAGE
    add x2, x2, _kuro_global_75@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif16
L_kuro_fn_EmitStraightIntegerProgram_else15:
L_kuro_fn_EmitStraightIntegerProgram_endif16:
    adrp x0, _kuro_global_79@PAGE
    add x0, x0, _kuro_global_79@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1320]
    adrp x0, L_kuro_data_126@PAGE
    add x0, x0, L_kuro_data_126@PAGEOFF
    str x0, [sp, #1328]
    ldr x0, [sp, #1320]
    ldr x1, [sp, #1328]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1336]
    ldr x0, [sp, #1336]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else17
    adrp x0, L_kuro_data_127@PAGE
    add x0, x0, L_kuro_data_127@PAGEOFF
    str x0, [sp, #1344]
    ldr x0, [sp, #1344]
    adrp x2, _kuro_global_75@PAGE
    add x2, x2, _kuro_global_75@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif18
L_kuro_fn_EmitStraightIntegerProgram_else17:
L_kuro_fn_EmitStraightIntegerProgram_endif18:
    adrp x0, _kuro_global_79@PAGE
    add x0, x0, _kuro_global_79@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1352]
    adrp x0, L_kuro_data_128@PAGE
    add x0, x0, L_kuro_data_128@PAGEOFF
    str x0, [sp, #1360]
    ldr x0, [sp, #1352]
    ldr x1, [sp, #1360]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1376]
    ldr x0, [sp, #1376]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else19
    adrp x0, L_kuro_data_129@PAGE
    add x0, x0, L_kuro_data_129@PAGEOFF
    str x0, [sp, #1384]
    ldr x0, [sp, #1384]
    adrp x2, _kuro_global_75@PAGE
    add x2, x2, _kuro_global_75@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif20
L_kuro_fn_EmitStraightIntegerProgram_else19:
L_kuro_fn_EmitStraightIntegerProgram_endif20:
    adrp x0, _kuro_global_79@PAGE
    add x0, x0, _kuro_global_79@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1392]
    adrp x0, L_kuro_data_130@PAGE
    add x0, x0, L_kuro_data_130@PAGEOFF
    str x0, [sp, #1400]
    ldr x0, [sp, #1392]
    ldr x1, [sp, #1400]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1408]
    ldr x0, [sp, #1408]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else21
    adrp x0, L_kuro_data_131@PAGE
    add x0, x0, L_kuro_data_131@PAGEOFF
    str x0, [sp, #1416]
    ldr x0, [sp, #1416]
    adrp x2, _kuro_global_75@PAGE
    add x2, x2, _kuro_global_75@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif22
L_kuro_fn_EmitStraightIntegerProgram_else21:
L_kuro_fn_EmitStraightIntegerProgram_endif22:
    adrp x0, _kuro_global_75@PAGE
    add x0, x0, _kuro_global_75@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1424]
    adrp x0, L_kuro_data_132@PAGE
    add x0, x0, L_kuro_data_132@PAGEOFF
    str x0, [sp, #1432]
    ldr x0, [sp, #1424]
    ldr x1, [sp, #1432]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1440]
    ldr x0, [sp, #1440]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else23
    mov x0, #1
    str x0, [sp, #1448]
    ldr x0, [sp, #1448]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif24
L_kuro_fn_EmitStraightIntegerProgram_else23:
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1464]
    adrp x0, L_kuro_data_133@PAGE
    add x0, x0, L_kuro_data_133@PAGEOFF
    str x0, [sp, #1472]
    ldr x0, [sp, #1464]
    ldr x1, [sp, #1472]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1480]
    ldr x0, [sp, #1480]
    ldr x1, [sp, #1464]
    bl _strcpy
    ldr x0, [sp, #1480]
    ldr x1, [sp, #1472]
    bl _strcat
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1488]
    ldr x0, [sp, #1480]
    ldr x1, [sp, #1488]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1496]
    ldr x0, [sp, #1496]
    ldr x1, [sp, #1480]
    bl _strcpy
    ldr x0, [sp, #1496]
    ldr x1, [sp, #1488]
    bl _strcat
    adrp x0, L_kuro_data_134@PAGE
    add x0, x0, L_kuro_data_134@PAGEOFF
    str x0, [sp, #1504]
    ldr x0, [sp, #1496]
    ldr x1, [sp, #1504]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1512]
    ldr x0, [sp, #1512]
    ldr x1, [sp, #1496]
    bl _strcpy
    ldr x0, [sp, #1512]
    ldr x1, [sp, #1504]
    bl _strcat
    adrp x0, _kuro_global_71@PAGE
    add x0, x0, _kuro_global_71@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1520]
    ldr x0, [sp, #1512]
    ldr x1, [sp, #1520]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1528]
    ldr x0, [sp, #1528]
    ldr x1, [sp, #1512]
    bl _strcpy
    ldr x0, [sp, #1528]
    ldr x1, [sp, #1520]
    bl _strcat
    adrp x0, L_kuro_data_135@PAGE
    add x0, x0, L_kuro_data_135@PAGEOFF
    str x0, [sp, #1536]
    ldr x0, [sp, #1528]
    ldr x1, [sp, #1536]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1552]
    ldr x0, [sp, #1552]
    ldr x1, [sp, #1528]
    bl _strcpy
    ldr x0, [sp, #1552]
    ldr x1, [sp, #1536]
    bl _strcat
    ldr x0, [sp, #1552]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1560]
    adrp x0, _kuro_global_75@PAGE
    add x0, x0, _kuro_global_75@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1568]
    ldr x0, [sp, #1560]
    ldr x1, [sp, #1568]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1576]
    ldr x0, [sp, #1576]
    ldr x1, [sp, #1560]
    bl _strcpy
    ldr x0, [sp, #1576]
    ldr x1, [sp, #1568]
    bl _strcat
    adrp x0, L_kuro_data_136@PAGE
    add x0, x0, L_kuro_data_136@PAGEOFF
    str x0, [sp, #1584]
    ldr x0, [sp, #1576]
    ldr x1, [sp, #1584]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1592]
    ldr x0, [sp, #1592]
    ldr x1, [sp, #1576]
    bl _strcpy
    ldr x0, [sp, #1592]
    ldr x1, [sp, #1584]
    bl _strcat
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1600]
    ldr x0, [sp, #1592]
    ldr x1, [sp, #1600]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1608]
    ldr x0, [sp, #1608]
    ldr x1, [sp, #1592]
    bl _strcpy
    ldr x0, [sp, #1608]
    ldr x1, [sp, #1600]
    bl _strcat
    adrp x0, L_kuro_data_137@PAGE
    add x0, x0, L_kuro_data_137@PAGEOFF
    str x0, [sp, #1616]
    ldr x0, [sp, #1608]
    ldr x1, [sp, #1616]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #1624]
    ldr x0, [sp, #1624]
    ldr x1, [sp, #1608]
    bl _strcpy
    ldr x0, [sp, #1624]
    ldr x1, [sp, #1616]
    bl _strcat
    ldr x0, [sp, #1624]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1640]
    mov x0, #1
    str x0, [sp, #1648]
    ldr x0, [sp, #1640]
    ldr x1, [sp, #1648]
    sub x0, x0, x1
    str x0, [sp, #1656]
    ldr x0, [sp, #1656]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif24:
    b L_kuro_fn_EmitStraightIntegerProgram_endif14
L_kuro_fn_EmitStraightIntegerProgram_else13:
    mov x0, #1
    str x0, [sp, #1664]
    ldr x0, [sp, #1664]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif14:
    b L_kuro_fn_EmitStraightIntegerProgram_endif12
L_kuro_fn_EmitStraightIntegerProgram_else11:
L_kuro_fn_EmitStraightIntegerProgram_endif12:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1672]
    adrp x0, L_kuro_data_138@PAGE
    add x0, x0, L_kuro_data_138@PAGEOFF
    str x0, [sp, #1680]
    ldr x0, [sp, #1672]
    ldr x1, [sp, #1680]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1688]
    ldr x0, [sp, #1688]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else25
    mov x0, #1
    str x0, [sp, #1696]
    ldr x0, [sp, #1696]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1704]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1712]
    ldr x0, [sp, #1704]
    ldr x1, [sp, #1712]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #1728]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1736]
    mov x0, #1
    str x0, [sp, #1744]
    ldr x0, [sp, #1736]
    ldr x1, [sp, #1744]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #1752]
    ldr x0, [sp, #1728]
    ldr x1, [sp, #1752]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #1760]
    ldr x0, [sp, #1760]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else27
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1768]
    ldr x1, [sp, #1768]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #1776]
    ldr x0, [sp, #1776]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1784]
    ldr x0, [sp, #1784]
    adrp x2, _kuro_global_32@PAGE
    add x2, x2, _kuro_global_32@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1792]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1792]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1800]
    mov x0, #8
    str x0, [sp, #1816]
    ldr x0, [sp, #1800]
    ldr x1, [sp, #1816]
    mul x0, x0, x1
    str x0, [sp, #1824]
    mov x0, #8
    str x0, [sp, #1832]
    ldr x0, [sp, #1824]
    ldr x1, [sp, #1832]
    sub x0, x0, x1
    str x0, [sp, #1840]
    ldr x0, [sp, #1840]
    adrp x2, _kuro_global_70@PAGE
    add x2, x2, _kuro_global_70@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1848]
    mov x0, #8
    str x0, [sp, #1856]
    ldr x0, [sp, #1848]
    ldr x1, [sp, #1856]
    mul x0, x0, x1
    str x0, [sp, #1864]
    mov x0, #16
    str x0, [sp, #1872]
    ldr x0, [sp, #1864]
    ldr x1, [sp, #1872]
    sub x0, x0, x1
    str x0, [sp, #1880]
    ldr x0, [sp, #1880]
    adrp x2, _kuro_global_47@PAGE
    add x2, x2, _kuro_global_47@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_70@PAGE
    add x0, x0, _kuro_global_70@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1888]
    ldr x0, [sp, #1888]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #1904]
    ldr x0, [sp, #1904]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1912]
    ldr x0, [sp, #1912]
    adrp x2, _kuro_global_71@PAGE
    add x2, x2, _kuro_global_71@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_47@PAGE
    add x0, x0, _kuro_global_47@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1920]
    ldr x0, [sp, #1920]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #1928]
    ldr x0, [sp, #1928]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1936]
    ldr x0, [sp, #1936]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_139@PAGE
    add x0, x0, L_kuro_data_139@PAGEOFF
    str x0, [sp, #1944]
    ldr x0, [sp, #1944]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1952]
    adrp x0, L_kuro_data_140@PAGE
    add x0, x0, L_kuro_data_140@PAGEOFF
    str x0, [sp, #1960]
    ldr x0, [sp, #1952]
    ldr x1, [sp, #1960]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1968]
    ldr x0, [sp, #1968]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else29
    adrp x0, L_kuro_data_141@PAGE
    add x0, x0, L_kuro_data_141@PAGEOFF
    str x0, [sp, #1976]
    ldr x0, [sp, #1976]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif30
L_kuro_fn_EmitStraightIntegerProgram_else29:
L_kuro_fn_EmitStraightIntegerProgram_endif30:
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1992]
    adrp x0, L_kuro_data_142@PAGE
    add x0, x0, L_kuro_data_142@PAGEOFF
    str x0, [sp, #2000]
    ldr x0, [sp, #1992]
    ldr x1, [sp, #2000]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2008]
    ldr x0, [sp, #2008]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else31
    adrp x0, L_kuro_data_143@PAGE
    add x0, x0, L_kuro_data_143@PAGEOFF
    str x0, [sp, #2016]
    ldr x0, [sp, #2016]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif32
L_kuro_fn_EmitStraightIntegerProgram_else31:
L_kuro_fn_EmitStraightIntegerProgram_endif32:
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2024]
    adrp x0, L_kuro_data_144@PAGE
    add x0, x0, L_kuro_data_144@PAGEOFF
    str x0, [sp, #2032]
    ldr x0, [sp, #2024]
    ldr x1, [sp, #2032]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2040]
    ldr x0, [sp, #2040]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else33
    adrp x0, L_kuro_data_145@PAGE
    add x0, x0, L_kuro_data_145@PAGEOFF
    str x0, [sp, #2048]
    ldr x0, [sp, #2048]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif34
L_kuro_fn_EmitStraightIntegerProgram_else33:
L_kuro_fn_EmitStraightIntegerProgram_endif34:
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2056]
    adrp x0, L_kuro_data_146@PAGE
    add x0, x0, L_kuro_data_146@PAGEOFF
    str x0, [sp, #2064]
    ldr x0, [sp, #2056]
    ldr x1, [sp, #2064]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2080]
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2088]
    adrp x0, L_kuro_data_147@PAGE
    add x0, x0, L_kuro_data_147@PAGEOFF
    str x0, [sp, #2096]
    ldr x0, [sp, #2088]
    ldr x1, [sp, #2096]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2104]
    ldr x0, [sp, #2080]
    ldr x1, [sp, #2104]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2112]
    ldr x0, [sp, #2112]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else35
    adrp x0, L_kuro_data_148@PAGE
    add x0, x0, L_kuro_data_148@PAGEOFF
    str x0, [sp, #2120]
    ldr x0, [sp, #2120]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif36
L_kuro_fn_EmitStraightIntegerProgram_else35:
L_kuro_fn_EmitStraightIntegerProgram_endif36:
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2128]
    adrp x0, L_kuro_data_149@PAGE
    add x0, x0, L_kuro_data_149@PAGEOFF
    str x0, [sp, #2136]
    ldr x0, [sp, #2128]
    ldr x1, [sp, #2136]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2144]
    ldr x0, [sp, #2144]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else37
    adrp x0, L_kuro_data_150@PAGE
    add x0, x0, L_kuro_data_150@PAGEOFF
    str x0, [sp, #2152]
    ldr x0, [sp, #2152]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif38
L_kuro_fn_EmitStraightIntegerProgram_else37:
L_kuro_fn_EmitStraightIntegerProgram_endif38:
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2176]
    adrp x0, L_kuro_data_151@PAGE
    add x0, x0, L_kuro_data_151@PAGEOFF
    str x0, [sp, #2184]
    ldr x0, [sp, #2176]
    ldr x1, [sp, #2184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2192]
    adrp x0, _kuro_global_32@PAGE
    add x0, x0, _kuro_global_32@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2200]
    adrp x0, L_kuro_data_152@PAGE
    add x0, x0, L_kuro_data_152@PAGEOFF
    str x0, [sp, #2208]
    ldr x0, [sp, #2200]
    ldr x1, [sp, #2208]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2216]
    ldr x0, [sp, #2192]
    ldr x1, [sp, #2216]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2224]
    ldr x0, [sp, #2224]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else39
    adrp x0, L_kuro_data_153@PAGE
    add x0, x0, L_kuro_data_153@PAGEOFF
    str x0, [sp, #2232]
    ldr x0, [sp, #2232]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif40
L_kuro_fn_EmitStraightIntegerProgram_else39:
L_kuro_fn_EmitStraightIntegerProgram_endif40:
    adrp x0, _kuro_global_31@PAGE
    add x0, x0, _kuro_global_31@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2240]
    adrp x0, L_kuro_data_154@PAGE
    add x0, x0, L_kuro_data_154@PAGEOFF
    str x0, [sp, #2248]
    ldr x0, [sp, #2240]
    ldr x1, [sp, #2248]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2264]
    ldr x0, [sp, #2264]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else41
    mov x0, #1
    str x0, [sp, #2272]
    ldr x0, [sp, #2272]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif42
L_kuro_fn_EmitStraightIntegerProgram_else41:
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2280]
    adrp x0, L_kuro_data_155@PAGE
    add x0, x0, L_kuro_data_155@PAGEOFF
    str x0, [sp, #2288]
    ldr x0, [sp, #2280]
    ldr x1, [sp, #2288]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2296]
    ldr x0, [sp, #2296]
    ldr x1, [sp, #2280]
    bl _strcpy
    ldr x0, [sp, #2296]
    ldr x1, [sp, #2288]
    bl _strcat
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2304]
    ldr x0, [sp, #2296]
    ldr x1, [sp, #2304]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2312]
    ldr x0, [sp, #2312]
    ldr x1, [sp, #2296]
    bl _strcpy
    ldr x0, [sp, #2312]
    ldr x1, [sp, #2304]
    bl _strcat
    adrp x0, L_kuro_data_156@PAGE
    add x0, x0, L_kuro_data_156@PAGEOFF
    str x0, [sp, #2320]
    ldr x0, [sp, #2312]
    ldr x1, [sp, #2320]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2328]
    ldr x0, [sp, #2328]
    ldr x1, [sp, #2312]
    bl _strcpy
    ldr x0, [sp, #2328]
    ldr x1, [sp, #2320]
    bl _strcat
    adrp x0, _kuro_global_71@PAGE
    add x0, x0, _kuro_global_71@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2336]
    ldr x0, [sp, #2328]
    ldr x1, [sp, #2336]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2352]
    ldr x0, [sp, #2352]
    ldr x1, [sp, #2328]
    bl _strcpy
    ldr x0, [sp, #2352]
    ldr x1, [sp, #2336]
    bl _strcat
    adrp x0, L_kuro_data_157@PAGE
    add x0, x0, L_kuro_data_157@PAGEOFF
    str x0, [sp, #2360]
    ldr x0, [sp, #2352]
    ldr x1, [sp, #2360]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2368]
    ldr x0, [sp, #2368]
    ldr x1, [sp, #2352]
    bl _strcpy
    ldr x0, [sp, #2368]
    ldr x1, [sp, #2360]
    bl _strcat
    ldr x0, [sp, #2368]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2376]
    adrp x0, _kuro_global_31@PAGE
    add x0, x0, _kuro_global_31@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2384]
    ldr x0, [sp, #2376]
    ldr x1, [sp, #2384]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2392]
    ldr x0, [sp, #2392]
    ldr x1, [sp, #2376]
    bl _strcpy
    ldr x0, [sp, #2392]
    ldr x1, [sp, #2384]
    bl _strcat
    adrp x0, L_kuro_data_158@PAGE
    add x0, x0, L_kuro_data_158@PAGEOFF
    str x0, [sp, #2400]
    ldr x0, [sp, #2392]
    ldr x1, [sp, #2400]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2408]
    ldr x0, [sp, #2408]
    ldr x1, [sp, #2392]
    bl _strcpy
    ldr x0, [sp, #2408]
    ldr x1, [sp, #2400]
    bl _strcat
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2416]
    ldr x0, [sp, #2408]
    ldr x1, [sp, #2416]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2424]
    ldr x0, [sp, #2424]
    ldr x1, [sp, #2408]
    bl _strcpy
    ldr x0, [sp, #2424]
    ldr x1, [sp, #2416]
    bl _strcat
    adrp x0, L_kuro_data_159@PAGE
    add x0, x0, L_kuro_data_159@PAGEOFF
    str x0, [sp, #2440]
    ldr x0, [sp, #2424]
    ldr x1, [sp, #2440]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2448]
    ldr x0, [sp, #2448]
    ldr x1, [sp, #2424]
    bl _strcpy
    ldr x0, [sp, #2448]
    ldr x1, [sp, #2440]
    bl _strcat
    ldr x0, [sp, #2448]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2456]
    mov x0, #1
    str x0, [sp, #2464]
    ldr x0, [sp, #2456]
    ldr x1, [sp, #2464]
    sub x0, x0, x1
    str x0, [sp, #2472]
    ldr x0, [sp, #2472]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif42:
    b L_kuro_fn_EmitStraightIntegerProgram_endif28
L_kuro_fn_EmitStraightIntegerProgram_else27:
    mov x0, #1
    str x0, [sp, #2480]
    ldr x0, [sp, #2480]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif28:
    b L_kuro_fn_EmitStraightIntegerProgram_endif26
L_kuro_fn_EmitStraightIntegerProgram_else25:
L_kuro_fn_EmitStraightIntegerProgram_endif26:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2488]
    adrp x0, L_kuro_data_160@PAGE
    add x0, x0, L_kuro_data_160@PAGEOFF
    str x0, [sp, #2496]
    ldr x0, [sp, #2488]
    ldr x1, [sp, #2496]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2504]
    ldr x0, [sp, #2504]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else43
    mov x0, #1
    str x0, [sp, #2512]
    ldr x0, [sp, #2512]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2528]
    mov x0, #0
    str x0, [sp, #2536]
    ldr x0, [sp, #2528]
    ldr x1, [sp, #2536]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #2544]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2552]
    mov x0, #16
    str x0, [sp, #2560]
    ldr x0, [sp, #2552]
    ldr x1, [sp, #2560]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #2568]
    ldr x0, [sp, #2544]
    ldr x1, [sp, #2568]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #2576]
    ldr x0, [sp, #2576]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else45
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2584]
    mov x0, #8
    str x0, [sp, #2592]
    ldr x0, [sp, #2584]
    ldr x1, [sp, #2592]
    mul x0, x0, x1
    str x0, [sp, #2600]
    mov x0, #8
    str x0, [sp, #2616]
    ldr x0, [sp, #2600]
    ldr x1, [sp, #2616]
    sub x0, x0, x1
    str x0, [sp, #2624]
    ldr x0, [sp, #2624]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2632]
    ldr x0, [sp, #2632]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #2640]
    ldr x0, [sp, #2640]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2648]
    ldr x0, [sp, #2648]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_38@PAGE
    add x0, x0, _kuro_global_38@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2656]
    ldr x0, [sp, #2656]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #2664]
    ldr x0, [sp, #2664]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2672]
    ldr x0, [sp, #2672]
    adrp x2, _kuro_global_41@PAGE
    add x2, x2, _kuro_global_41@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2680]
    adrp x0, _kuro_global_38@PAGE
    add x0, x0, _kuro_global_38@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2688]
    ldr x1, [sp, #2680]
    ldr x0, [sp, #2688]
    adrp x2, _kuro_collection_2@PAGE
    add x2, x2, _kuro_collection_2@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2704]
    mov x0, #0
    str x0, [sp, #2712]
    ldr x1, [sp, #2704]
    ldr x0, [sp, #2712]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2720]
    adrp x0, L_kuro_data_161@PAGE
    add x0, x0, L_kuro_data_161@PAGEOFF
    str x0, [sp, #2728]
    ldr x0, [sp, #2720]
    ldr x1, [sp, #2728]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2736]
    ldr x0, [sp, #2736]
    ldr x1, [sp, #2720]
    bl _strcpy
    ldr x0, [sp, #2736]
    ldr x1, [sp, #2728]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2744]
    ldr x0, [sp, #2736]
    ldr x1, [sp, #2744]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2752]
    ldr x0, [sp, #2752]
    ldr x1, [sp, #2736]
    bl _strcpy
    ldr x0, [sp, #2752]
    ldr x1, [sp, #2744]
    bl _strcat
    adrp x0, L_kuro_data_162@PAGE
    add x0, x0, L_kuro_data_162@PAGEOFF
    str x0, [sp, #2760]
    ldr x0, [sp, #2752]
    ldr x1, [sp, #2760]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2768]
    ldr x0, [sp, #2768]
    ldr x1, [sp, #2752]
    bl _strcpy
    ldr x0, [sp, #2768]
    ldr x1, [sp, #2760]
    bl _strcat
    adrp x0, _kuro_global_41@PAGE
    add x0, x0, _kuro_global_41@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2776]
    ldr x0, [sp, #2768]
    ldr x1, [sp, #2776]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2792]
    ldr x0, [sp, #2792]
    ldr x1, [sp, #2768]
    bl _strcpy
    ldr x0, [sp, #2792]
    ldr x1, [sp, #2776]
    bl _strcat
    adrp x0, L_kuro_data_163@PAGE
    add x0, x0, L_kuro_data_163@PAGEOFF
    str x0, [sp, #2800]
    ldr x0, [sp, #2792]
    ldr x1, [sp, #2800]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2808]
    ldr x0, [sp, #2808]
    ldr x1, [sp, #2792]
    bl _strcpy
    ldr x0, [sp, #2808]
    ldr x1, [sp, #2800]
    bl _strcat
    ldr x0, [sp, #2808]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2816]
    mov x0, #1
    str x0, [sp, #2824]
    ldr x0, [sp, #2816]
    ldr x1, [sp, #2824]
    sub x0, x0, x1
    str x0, [sp, #2832]
    ldr x0, [sp, #2832]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2840]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2840]
    add x0, x0, x1
    adrp x2, _kuro_global_39@PAGE
    add x2, x2, _kuro_global_39@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #2848]
    adrp x0, _kuro_global_38@PAGE
    add x0, x0, _kuro_global_38@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2848]
    add x0, x0, x1
    adrp x2, _kuro_global_38@PAGE
    add x2, x2, _kuro_global_38@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif46
L_kuro_fn_EmitStraightIntegerProgram_else45:
    mov x0, #1
    str x0, [sp, #2856]
    ldr x0, [sp, #2856]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif46:
    b L_kuro_fn_EmitStraightIntegerProgram_endif44
L_kuro_fn_EmitStraightIntegerProgram_else43:
L_kuro_fn_EmitStraightIntegerProgram_endif44:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2864]
    adrp x0, L_kuro_data_164@PAGE
    add x0, x0, L_kuro_data_164@PAGEOFF
    str x0, [sp, #2880]
    ldr x0, [sp, #2864]
    ldr x1, [sp, #2880]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2888]
    ldr x0, [sp, #2888]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else47
    mov x0, #1
    str x0, [sp, #2896]
    ldr x0, [sp, #2896]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2904]
    mov x0, #0
    str x0, [sp, #2912]
    ldr x0, [sp, #2904]
    ldr x1, [sp, #2912]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #2920]
    ldr x0, [sp, #2920]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else49
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2928]
    mov x0, #1
    str x0, [sp, #2936]
    ldr x0, [sp, #2928]
    ldr x1, [sp, #2936]
    sub x0, x0, x1
    str x0, [sp, #2944]
    ldr x0, [sp, #2944]
    adrp x2, _kuro_global_40@PAGE
    add x2, x2, _kuro_global_40@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_40@PAGE
    add x0, x0, _kuro_global_40@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2952]
    ldr x1, [sp, #2952]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #2968]
    ldr x0, [sp, #2968]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2976]
    mov x0, #0
    str x0, [sp, #2984]
    ldr x0, [sp, #2976]
    ldr x1, [sp, #2984]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2992]
    ldr x0, [sp, #2992]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else51
    adrp x0, _kuro_global_40@PAGE
    add x0, x0, _kuro_global_40@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3000]
    mov x0, #1
    str x0, [sp, #3008]
    ldr x1, [sp, #3000]
    ldr x0, [sp, #3008]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_40@PAGE
    add x0, x0, _kuro_global_40@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3016]
    ldr x1, [sp, #3016]
    adrp x2, _kuro_collection_2@PAGE
    add x2, x2, _kuro_collection_2@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #3024]
    ldr x0, [sp, #3024]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3032]
    ldr x0, [sp, #3032]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #3040]
    ldr x0, [sp, #3040]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3064]
    ldr x0, [sp, #3064]
    adrp x2, _kuro_global_41@PAGE
    add x2, x2, _kuro_global_41@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3072]
    adrp x0, L_kuro_data_165@PAGE
    add x0, x0, L_kuro_data_165@PAGEOFF
    str x0, [sp, #3080]
    ldr x0, [sp, #3072]
    ldr x1, [sp, #3080]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3088]
    ldr x0, [sp, #3088]
    ldr x1, [sp, #3072]
    bl _strcpy
    ldr x0, [sp, #3088]
    ldr x1, [sp, #3080]
    bl _strcat
    adrp x0, _kuro_global_41@PAGE
    add x0, x0, _kuro_global_41@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3096]
    ldr x0, [sp, #3088]
    ldr x1, [sp, #3096]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3104]
    ldr x0, [sp, #3104]
    ldr x1, [sp, #3088]
    bl _strcpy
    ldr x0, [sp, #3104]
    ldr x1, [sp, #3096]
    bl _strcat
    adrp x0, L_kuro_data_166@PAGE
    add x0, x0, L_kuro_data_166@PAGEOFF
    str x0, [sp, #3112]
    ldr x0, [sp, #3104]
    ldr x1, [sp, #3112]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3120]
    ldr x0, [sp, #3120]
    ldr x1, [sp, #3104]
    bl _strcpy
    ldr x0, [sp, #3120]
    ldr x1, [sp, #3112]
    bl _strcat
    adrp x0, _kuro_global_41@PAGE
    add x0, x0, _kuro_global_41@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3128]
    ldr x0, [sp, #3120]
    ldr x1, [sp, #3128]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3136]
    ldr x0, [sp, #3136]
    ldr x1, [sp, #3120]
    bl _strcpy
    ldr x0, [sp, #3136]
    ldr x1, [sp, #3128]
    bl _strcat
    adrp x0, L_kuro_data_167@PAGE
    add x0, x0, L_kuro_data_167@PAGEOFF
    str x0, [sp, #3152]
    ldr x0, [sp, #3136]
    ldr x1, [sp, #3152]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3160]
    ldr x0, [sp, #3160]
    ldr x1, [sp, #3136]
    bl _strcpy
    ldr x0, [sp, #3160]
    ldr x1, [sp, #3152]
    bl _strcat
    ldr x0, [sp, #3160]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif52
L_kuro_fn_EmitStraightIntegerProgram_else51:
    mov x0, #1
    str x0, [sp, #3168]
    ldr x0, [sp, #3168]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif52:
    b L_kuro_fn_EmitStraightIntegerProgram_endif50
L_kuro_fn_EmitStraightIntegerProgram_else49:
    mov x0, #1
    str x0, [sp, #3176]
    ldr x0, [sp, #3176]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif50:
    b L_kuro_fn_EmitStraightIntegerProgram_endif48
L_kuro_fn_EmitStraightIntegerProgram_else47:
L_kuro_fn_EmitStraightIntegerProgram_endif48:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3184]
    adrp x0, L_kuro_data_168@PAGE
    add x0, x0, L_kuro_data_168@PAGEOFF
    str x0, [sp, #3192]
    ldr x0, [sp, #3184]
    ldr x1, [sp, #3192]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3200]
    ldr x0, [sp, #3200]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else53
    mov x0, #1
    str x0, [sp, #3208]
    ldr x0, [sp, #3208]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3216]
    mov x0, #0
    str x0, [sp, #3224]
    ldr x0, [sp, #3216]
    ldr x1, [sp, #3224]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #3240]
    ldr x0, [sp, #3240]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else55
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3248]
    mov x0, #1
    str x0, [sp, #3256]
    ldr x0, [sp, #3248]
    ldr x1, [sp, #3256]
    sub x0, x0, x1
    str x0, [sp, #3264]
    ldr x0, [sp, #3264]
    adrp x2, _kuro_global_40@PAGE
    add x2, x2, _kuro_global_40@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_40@PAGE
    add x0, x0, _kuro_global_40@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3272]
    ldr x1, [sp, #3272]
    adrp x2, _kuro_collection_2@PAGE
    add x2, x2, _kuro_collection_2@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #3280]
    ldr x0, [sp, #3280]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3288]
    ldr x0, [sp, #3288]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #3296]
    ldr x0, [sp, #3296]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3304]
    ldr x0, [sp, #3304]
    adrp x2, _kuro_global_41@PAGE
    add x2, x2, _kuro_global_41@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_40@PAGE
    add x0, x0, _kuro_global_40@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3312]
    ldr x1, [sp, #3312]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #3328]
    ldr x0, [sp, #3328]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3336]
    mov x0, #1
    str x0, [sp, #3344]
    ldr x0, [sp, #3336]
    ldr x1, [sp, #3344]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3352]
    ldr x0, [sp, #3352]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else57
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3360]
    adrp x0, L_kuro_data_169@PAGE
    add x0, x0, L_kuro_data_169@PAGEOFF
    str x0, [sp, #3368]
    ldr x0, [sp, #3360]
    ldr x1, [sp, #3368]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3376]
    ldr x0, [sp, #3376]
    ldr x1, [sp, #3360]
    bl _strcpy
    ldr x0, [sp, #3376]
    ldr x1, [sp, #3368]
    bl _strcat
    adrp x0, _kuro_global_41@PAGE
    add x0, x0, _kuro_global_41@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3384]
    ldr x0, [sp, #3376]
    ldr x1, [sp, #3384]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3392]
    ldr x0, [sp, #3392]
    ldr x1, [sp, #3376]
    bl _strcpy
    ldr x0, [sp, #3392]
    ldr x1, [sp, #3384]
    bl _strcat
    adrp x0, L_kuro_data_170@PAGE
    add x0, x0, L_kuro_data_170@PAGEOFF
    str x0, [sp, #3400]
    ldr x0, [sp, #3392]
    ldr x1, [sp, #3400]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3416]
    ldr x0, [sp, #3416]
    ldr x1, [sp, #3392]
    bl _strcpy
    ldr x0, [sp, #3416]
    ldr x1, [sp, #3400]
    bl _strcat
    ldr x0, [sp, #3416]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif58
L_kuro_fn_EmitStraightIntegerProgram_else57:
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3424]
    adrp x0, L_kuro_data_171@PAGE
    add x0, x0, L_kuro_data_171@PAGEOFF
    str x0, [sp, #3432]
    ldr x0, [sp, #3424]
    ldr x1, [sp, #3432]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3440]
    ldr x0, [sp, #3440]
    ldr x1, [sp, #3424]
    bl _strcpy
    ldr x0, [sp, #3440]
    ldr x1, [sp, #3432]
    bl _strcat
    adrp x0, _kuro_global_41@PAGE
    add x0, x0, _kuro_global_41@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3448]
    ldr x0, [sp, #3440]
    ldr x1, [sp, #3448]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3456]
    ldr x0, [sp, #3456]
    ldr x1, [sp, #3440]
    bl _strcpy
    ldr x0, [sp, #3456]
    ldr x1, [sp, #3448]
    bl _strcat
    adrp x0, L_kuro_data_172@PAGE
    add x0, x0, L_kuro_data_172@PAGEOFF
    str x0, [sp, #3464]
    ldr x0, [sp, #3456]
    ldr x1, [sp, #3464]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3472]
    ldr x0, [sp, #3472]
    ldr x1, [sp, #3456]
    bl _strcpy
    ldr x0, [sp, #3472]
    ldr x1, [sp, #3464]
    bl _strcat
    ldr x0, [sp, #3472]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif58:
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3480]
    mov x0, #1
    str x0, [sp, #3488]
    ldr x0, [sp, #3480]
    ldr x1, [sp, #3488]
    sub x0, x0, x1
    str x0, [sp, #3504]
    ldr x0, [sp, #3504]
    adrp x2, _kuro_global_39@PAGE
    add x2, x2, _kuro_global_39@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif56
L_kuro_fn_EmitStraightIntegerProgram_else55:
    mov x0, #1
    str x0, [sp, #3512]
    ldr x0, [sp, #3512]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif56:
    b L_kuro_fn_EmitStraightIntegerProgram_endif54
L_kuro_fn_EmitStraightIntegerProgram_else53:
L_kuro_fn_EmitStraightIntegerProgram_endif54:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3520]
    adrp x0, L_kuro_data_173@PAGE
    add x0, x0, L_kuro_data_173@PAGEOFF
    str x0, [sp, #3528]
    ldr x0, [sp, #3520]
    ldr x1, [sp, #3528]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #3536]
    ldr x0, [sp, #3536]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else59
    mov x0, #1
    str x0, [sp, #3544]
    ldr x0, [sp, #3544]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3552]
    mov x0, #0
    str x0, [sp, #3560]
    ldr x0, [sp, #3552]
    ldr x1, [sp, #3560]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #3568]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3576]
    mov x0, #16
    str x0, [sp, #3592]
    ldr x0, [sp, #3576]
    ldr x1, [sp, #3592]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #3600]
    ldr x0, [sp, #3568]
    ldr x1, [sp, #3600]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #3608]
    ldr x0, [sp, #3608]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else61
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3616]
    mov x0, #8
    str x0, [sp, #3624]
    ldr x0, [sp, #3616]
    ldr x1, [sp, #3624]
    mul x0, x0, x1
    str x0, [sp, #3632]
    mov x0, #8
    str x0, [sp, #3640]
    ldr x0, [sp, #3632]
    ldr x1, [sp, #3640]
    sub x0, x0, x1
    str x0, [sp, #3648]
    ldr x0, [sp, #3648]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    mov x0, #1536
    str x0, [sp, #3656]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3664]
    mov x0, #8
    str x0, [sp, #3680]
    ldr x0, [sp, #3664]
    ldr x1, [sp, #3680]
    mul x0, x0, x1
    str x0, [sp, #3688]
    ldr x0, [sp, #3656]
    ldr x1, [sp, #3688]
    add x0, x0, x1
    str x0, [sp, #3696]
    ldr x0, [sp, #3696]
    adrp x2, _kuro_global_67@PAGE
    add x2, x2, _kuro_global_67@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3704]
    ldr x0, [sp, #3704]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #3712]
    ldr x0, [sp, #3712]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3720]
    ldr x0, [sp, #3720]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_67@PAGE
    add x0, x0, _kuro_global_67@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3728]
    ldr x0, [sp, #3728]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #3736]
    ldr x0, [sp, #3736]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3744]
    ldr x0, [sp, #3744]
    adrp x2, _kuro_global_68@PAGE
    add x2, x2, _kuro_global_68@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_63@PAGE
    add x0, x0, _kuro_global_63@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3752]
    ldr x0, [sp, #3752]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #3768]
    ldr x0, [sp, #3768]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3776]
    ldr x0, [sp, #3776]
    adrp x2, _kuro_global_66@PAGE
    add x2, x2, _kuro_global_66@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3784]
    mov x0, #1
    str x0, [sp, #3792]
    ldr x0, [sp, #3784]
    ldr x1, [sp, #3792]
    sub x0, x0, x1
    str x0, [sp, #3800]
    ldr x0, [sp, #3800]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3808]
    adrp x0, _kuro_global_63@PAGE
    add x0, x0, _kuro_global_63@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3816]
    ldr x1, [sp, #3808]
    ldr x0, [sp, #3816]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3824]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3832]
    ldr x1, [sp, #3824]
    ldr x0, [sp, #3832]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3840]
    adrp x0, L_kuro_data_174@PAGE
    add x0, x0, L_kuro_data_174@PAGEOFF
    str x0, [sp, #3856]
    ldr x0, [sp, #3840]
    ldr x1, [sp, #3856]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3864]
    ldr x0, [sp, #3864]
    ldr x1, [sp, #3840]
    bl _strcpy
    ldr x0, [sp, #3864]
    ldr x1, [sp, #3856]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3872]
    ldr x0, [sp, #3864]
    ldr x1, [sp, #3872]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3880]
    ldr x0, [sp, #3880]
    ldr x1, [sp, #3864]
    bl _strcpy
    ldr x0, [sp, #3880]
    ldr x1, [sp, #3872]
    bl _strcat
    adrp x0, L_kuro_data_175@PAGE
    add x0, x0, L_kuro_data_175@PAGEOFF
    str x0, [sp, #3888]
    ldr x0, [sp, #3880]
    ldr x1, [sp, #3888]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3896]
    ldr x0, [sp, #3896]
    ldr x1, [sp, #3880]
    bl _strcpy
    ldr x0, [sp, #3896]
    ldr x1, [sp, #3888]
    bl _strcat
    adrp x0, _kuro_global_68@PAGE
    add x0, x0, _kuro_global_68@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3904]
    ldr x0, [sp, #3896]
    ldr x1, [sp, #3904]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3912]
    ldr x0, [sp, #3912]
    ldr x1, [sp, #3896]
    bl _strcpy
    ldr x0, [sp, #3912]
    ldr x1, [sp, #3904]
    bl _strcat
    adrp x0, L_kuro_data_176@PAGE
    add x0, x0, L_kuro_data_176@PAGEOFF
    str x0, [sp, #3920]
    ldr x0, [sp, #3912]
    ldr x1, [sp, #3920]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3928]
    ldr x0, [sp, #3928]
    ldr x1, [sp, #3912]
    bl _strcpy
    ldr x0, [sp, #3928]
    ldr x1, [sp, #3920]
    bl _strcat
    ldr x0, [sp, #3928]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3952]
    adrp x0, L_kuro_data_177@PAGE
    add x0, x0, L_kuro_data_177@PAGEOFF
    str x0, [sp, #3960]
    ldr x0, [sp, #3952]
    ldr x1, [sp, #3960]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3968]
    ldr x0, [sp, #3968]
    ldr x1, [sp, #3952]
    bl _strcpy
    ldr x0, [sp, #3968]
    ldr x1, [sp, #3960]
    bl _strcat
    adrp x0, _kuro_global_66@PAGE
    add x0, x0, _kuro_global_66@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3976]
    ldr x0, [sp, #3968]
    ldr x1, [sp, #3976]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3984]
    ldr x0, [sp, #3984]
    ldr x1, [sp, #3968]
    bl _strcpy
    ldr x0, [sp, #3984]
    ldr x1, [sp, #3976]
    bl _strcat
    adrp x0, L_kuro_data_178@PAGE
    add x0, x0, L_kuro_data_178@PAGEOFF
    str x0, [sp, #3992]
    ldr x0, [sp, #3984]
    ldr x1, [sp, #3992]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4000]
    ldr x0, [sp, #4000]
    ldr x1, [sp, #3984]
    bl _strcpy
    ldr x0, [sp, #4000]
    ldr x1, [sp, #3992]
    bl _strcat
    adrp x0, _kuro_global_68@PAGE
    add x0, x0, _kuro_global_68@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4008]
    ldr x0, [sp, #4000]
    ldr x1, [sp, #4008]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4016]
    ldr x0, [sp, #4016]
    ldr x1, [sp, #4000]
    bl _strcpy
    ldr x0, [sp, #4016]
    ldr x1, [sp, #4008]
    bl _strcat
    adrp x0, L_kuro_data_179@PAGE
    add x0, x0, L_kuro_data_179@PAGEOFF
    str x0, [sp, #4024]
    ldr x0, [sp, #4016]
    ldr x1, [sp, #4024]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4040]
    ldr x0, [sp, #4040]
    ldr x1, [sp, #4016]
    bl _strcpy
    ldr x0, [sp, #4040]
    ldr x1, [sp, #4024]
    bl _strcat
    adrp x0, _kuro_global_66@PAGE
    add x0, x0, _kuro_global_66@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4048]
    ldr x0, [sp, #4040]
    ldr x1, [sp, #4048]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4056]
    ldr x0, [sp, #4056]
    ldr x1, [sp, #4040]
    bl _strcpy
    ldr x0, [sp, #4056]
    ldr x1, [sp, #4048]
    bl _strcat
    adrp x0, L_kuro_data_180@PAGE
    add x0, x0, L_kuro_data_180@PAGEOFF
    str x0, [sp, #4064]
    ldr x0, [sp, #4056]
    ldr x1, [sp, #4064]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4072]
    ldr x0, [sp, #4072]
    ldr x1, [sp, #4056]
    bl _strcpy
    ldr x0, [sp, #4072]
    ldr x1, [sp, #4064]
    bl _strcat
    ldr x0, [sp, #4072]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #4080]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4080]
    add x0, x0, x1
    adrp x2, _kuro_global_64@PAGE
    add x2, x2, _kuro_global_64@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #4088]
    adrp x0, _kuro_global_63@PAGE
    add x0, x0, _kuro_global_63@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4088]
    add x0, x0, x1
    adrp x2, _kuro_global_63@PAGE
    add x2, x2, _kuro_global_63@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif62
L_kuro_fn_EmitStraightIntegerProgram_else61:
    mov x0, #1
    str x0, [sp, #4096]
    ldr x0, [sp, #4096]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif62:
    b L_kuro_fn_EmitStraightIntegerProgram_endif60
L_kuro_fn_EmitStraightIntegerProgram_else59:
L_kuro_fn_EmitStraightIntegerProgram_endif60:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4104]
    adrp x0, L_kuro_data_181@PAGE
    add x0, x0, L_kuro_data_181@PAGEOFF
    str x0, [sp, #4112]
    ldr x0, [sp, #4104]
    ldr x1, [sp, #4112]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4128]
    ldr x0, [sp, #4128]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else63
    mov x0, #1
    str x0, [sp, #4136]
    ldr x0, [sp, #4136]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4144]
    mov x0, #0
    str x0, [sp, #4152]
    ldr x0, [sp, #4144]
    ldr x1, [sp, #4152]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #4160]
    ldr x0, [sp, #4160]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else65
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4168]
    mov x0, #1
    str x0, [sp, #4176]
    ldr x0, [sp, #4168]
    ldr x1, [sp, #4176]
    sub x0, x0, x1
    str x0, [sp, #4184]
    ldr x0, [sp, #4184]
    adrp x2, _kuro_global_65@PAGE
    add x2, x2, _kuro_global_65@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_65@PAGE
    add x0, x0, _kuro_global_65@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4192]
    ldr x1, [sp, #4192]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #4200]
    ldr x0, [sp, #4200]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4216]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4224]
    ldr x0, [sp, #4216]
    ldr x1, [sp, #4224]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4232]
    ldr x0, [sp, #4232]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else67
    adrp x0, _kuro_global_65@PAGE
    add x0, x0, _kuro_global_65@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4240]
    ldr x1, [sp, #4240]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #4248]
    ldr x0, [sp, #4248]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4256]
    ldr x0, [sp, #4256]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #4264]
    ldr x0, [sp, #4264]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4272]
    ldr x0, [sp, #4272]
    adrp x2, _kuro_global_66@PAGE
    add x2, x2, _kuro_global_66@PAGEOFF
    str x0, [x2]
    mov x0, #1536
    str x0, [sp, #4280]
    adrp x0, _kuro_global_65@PAGE
    add x0, x0, _kuro_global_65@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4288]
    mov x0, #8
    str x0, [sp, #4304]
    ldr x0, [sp, #4288]
    ldr x1, [sp, #4304]
    mul x0, x0, x1
    str x0, [sp, #4312]
    ldr x0, [sp, #4280]
    ldr x1, [sp, #4312]
    add x0, x0, x1
    str x0, [sp, #4320]
    ldr x0, [sp, #4320]
    adrp x2, _kuro_global_67@PAGE
    add x2, x2, _kuro_global_67@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_67@PAGE
    add x0, x0, _kuro_global_67@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4328]
    ldr x0, [sp, #4328]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #4336]
    ldr x0, [sp, #4336]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4344]
    ldr x0, [sp, #4344]
    adrp x2, _kuro_global_68@PAGE
    add x2, x2, _kuro_global_68@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4352]
    adrp x0, L_kuro_data_182@PAGE
    add x0, x0, L_kuro_data_182@PAGEOFF
    str x0, [sp, #4360]
    ldr x0, [sp, #4352]
    ldr x1, [sp, #4360]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4368]
    ldr x0, [sp, #4368]
    ldr x1, [sp, #4352]
    bl _strcpy
    ldr x0, [sp, #4368]
    ldr x1, [sp, #4360]
    bl _strcat
    adrp x0, _kuro_global_68@PAGE
    add x0, x0, _kuro_global_68@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4376]
    ldr x0, [sp, #4368]
    ldr x1, [sp, #4376]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4392]
    ldr x0, [sp, #4392]
    ldr x1, [sp, #4368]
    bl _strcpy
    ldr x0, [sp, #4392]
    ldr x1, [sp, #4376]
    bl _strcat
    adrp x0, L_kuro_data_183@PAGE
    add x0, x0, L_kuro_data_183@PAGEOFF
    str x0, [sp, #4400]
    ldr x0, [sp, #4392]
    ldr x1, [sp, #4400]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4408]
    ldr x0, [sp, #4408]
    ldr x1, [sp, #4392]
    bl _strcpy
    ldr x0, [sp, #4408]
    ldr x1, [sp, #4400]
    bl _strcat
    adrp x0, _kuro_global_68@PAGE
    add x0, x0, _kuro_global_68@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4416]
    ldr x0, [sp, #4408]
    ldr x1, [sp, #4416]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4424]
    ldr x0, [sp, #4424]
    ldr x1, [sp, #4408]
    bl _strcpy
    ldr x0, [sp, #4424]
    ldr x1, [sp, #4416]
    bl _strcat
    adrp x0, L_kuro_data_184@PAGE
    add x0, x0, L_kuro_data_184@PAGEOFF
    str x0, [sp, #4432]
    ldr x0, [sp, #4424]
    ldr x1, [sp, #4432]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4440]
    ldr x0, [sp, #4440]
    ldr x1, [sp, #4424]
    bl _strcpy
    ldr x0, [sp, #4440]
    ldr x1, [sp, #4432]
    bl _strcat
    adrp x0, _kuro_global_66@PAGE
    add x0, x0, _kuro_global_66@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4448]
    ldr x0, [sp, #4440]
    ldr x1, [sp, #4448]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4456]
    ldr x0, [sp, #4456]
    ldr x1, [sp, #4440]
    bl _strcpy
    ldr x0, [sp, #4456]
    ldr x1, [sp, #4448]
    bl _strcat
    adrp x0, L_kuro_data_185@PAGE
    add x0, x0, L_kuro_data_185@PAGEOFF
    str x0, [sp, #4464]
    ldr x0, [sp, #4456]
    ldr x1, [sp, #4464]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4480]
    ldr x0, [sp, #4480]
    ldr x1, [sp, #4456]
    bl _strcpy
    ldr x0, [sp, #4480]
    ldr x1, [sp, #4464]
    bl _strcat
    adrp x0, _kuro_global_66@PAGE
    add x0, x0, _kuro_global_66@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4488]
    ldr x0, [sp, #4480]
    ldr x1, [sp, #4488]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4496]
    ldr x0, [sp, #4496]
    ldr x1, [sp, #4480]
    bl _strcpy
    ldr x0, [sp, #4496]
    ldr x1, [sp, #4488]
    bl _strcat
    adrp x0, L_kuro_data_186@PAGE
    add x0, x0, L_kuro_data_186@PAGEOFF
    str x0, [sp, #4504]
    ldr x0, [sp, #4496]
    ldr x1, [sp, #4504]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4512]
    ldr x0, [sp, #4512]
    ldr x1, [sp, #4496]
    bl _strcpy
    ldr x0, [sp, #4512]
    ldr x1, [sp, #4504]
    bl _strcat
    ldr x0, [sp, #4512]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4520]
    mov x0, #1
    str x0, [sp, #4528]
    ldr x0, [sp, #4520]
    ldr x1, [sp, #4528]
    sub x0, x0, x1
    str x0, [sp, #4536]
    ldr x0, [sp, #4536]
    adrp x2, _kuro_global_64@PAGE
    add x2, x2, _kuro_global_64@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif68
L_kuro_fn_EmitStraightIntegerProgram_else67:
    mov x0, #1
    str x0, [sp, #4544]
    ldr x0, [sp, #4544]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif68:
    b L_kuro_fn_EmitStraightIntegerProgram_endif66
L_kuro_fn_EmitStraightIntegerProgram_else65:
    mov x0, #1
    str x0, [sp, #4552]
    ldr x0, [sp, #4552]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif66:
    b L_kuro_fn_EmitStraightIntegerProgram_endif64
L_kuro_fn_EmitStraightIntegerProgram_else63:
L_kuro_fn_EmitStraightIntegerProgram_endif64:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4568]
    adrp x0, L_kuro_data_187@PAGE
    add x0, x0, L_kuro_data_187@PAGEOFF
    str x0, [sp, #4576]
    ldr x0, [sp, #4568]
    ldr x1, [sp, #4576]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4584]
    ldr x0, [sp, #4584]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else69
    mov x0, #1
    str x0, [sp, #4592]
    ldr x0, [sp, #4592]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4600]
    mov x0, #16
    str x0, [sp, #4608]
    ldr x0, [sp, #4600]
    ldr x1, [sp, #4608]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4616]
    ldr x0, [sp, #4616]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else71
    adrp x0, _kuro_global_87@PAGE
    add x0, x0, _kuro_global_87@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4624]
    ldr x0, [sp, #4624]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #4632]
    ldr x0, [sp, #4632]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4640]
    ldr x0, [sp, #4640]
    adrp x2, _kuro_global_91@PAGE
    add x2, x2, _kuro_global_91@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4656]
    adrp x0, _kuro_global_87@PAGE
    add x0, x0, _kuro_global_87@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4664]
    ldr x1, [sp, #4656]
    ldr x0, [sp, #4664]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4672]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4680]
    ldr x1, [sp, #4672]
    ldr x0, [sp, #4680]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4688]
    mov x0, #0
    str x0, [sp, #4696]
    ldr x1, [sp, #4688]
    ldr x0, [sp, #4696]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4704]
    adrp x0, L_kuro_data_188@PAGE
    add x0, x0, L_kuro_data_188@PAGEOFF
    str x0, [sp, #4712]
    ldr x0, [sp, #4704]
    ldr x1, [sp, #4712]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4720]
    ldr x0, [sp, #4720]
    ldr x1, [sp, #4704]
    bl _strcpy
    ldr x0, [sp, #4720]
    ldr x1, [sp, #4712]
    bl _strcat
    adrp x0, _kuro_global_91@PAGE
    add x0, x0, _kuro_global_91@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4728]
    ldr x0, [sp, #4720]
    ldr x1, [sp, #4728]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4744]
    ldr x0, [sp, #4744]
    ldr x1, [sp, #4720]
    bl _strcpy
    ldr x0, [sp, #4744]
    ldr x1, [sp, #4728]
    bl _strcat
    adrp x0, L_kuro_data_189@PAGE
    add x0, x0, L_kuro_data_189@PAGEOFF
    str x0, [sp, #4752]
    ldr x0, [sp, #4744]
    ldr x1, [sp, #4752]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4760]
    ldr x0, [sp, #4760]
    ldr x1, [sp, #4744]
    bl _strcpy
    ldr x0, [sp, #4760]
    ldr x1, [sp, #4752]
    bl _strcat
    ldr x0, [sp, #4760]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #4768]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4768]
    add x0, x0, x1
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #4776]
    adrp x0, _kuro_global_87@PAGE
    add x0, x0, _kuro_global_87@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4776]
    add x0, x0, x1
    adrp x2, _kuro_global_87@PAGE
    add x2, x2, _kuro_global_87@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif72
L_kuro_fn_EmitStraightIntegerProgram_else71:
    mov x0, #1
    str x0, [sp, #4784]
    ldr x0, [sp, #4784]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif72:
    b L_kuro_fn_EmitStraightIntegerProgram_endif70
L_kuro_fn_EmitStraightIntegerProgram_else69:
L_kuro_fn_EmitStraightIntegerProgram_endif70:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4792]
    adrp x0, L_kuro_data_190@PAGE
    add x0, x0, L_kuro_data_190@PAGEOFF
    str x0, [sp, #4800]
    ldr x0, [sp, #4792]
    ldr x1, [sp, #4800]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4808]
    ldr x0, [sp, #4808]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else73
    mov x0, #1
    str x0, [sp, #4816]
    ldr x0, [sp, #4816]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4840]
    mov x0, #0
    str x0, [sp, #4848]
    ldr x0, [sp, #4840]
    ldr x1, [sp, #4848]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #4856]
    ldr x0, [sp, #4856]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else75
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4864]
    mov x0, #1
    str x0, [sp, #4872]
    ldr x0, [sp, #4864]
    ldr x1, [sp, #4872]
    sub x0, x0, x1
    str x0, [sp, #4880]
    ldr x0, [sp, #4880]
    adrp x2, _kuro_global_90@PAGE
    add x2, x2, _kuro_global_90@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4888]
    ldr x1, [sp, #4888]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #4896]
    ldr x0, [sp, #4896]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4904]
    ldr x0, [sp, #4904]
    adrp x2, _kuro_global_92@PAGE
    add x2, x2, _kuro_global_92@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4912]
    ldr x1, [sp, #4912]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #4928]
    ldr x0, [sp, #4928]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4936]
    ldr x0, [sp, #4936]
    adrp x2, _kuro_global_89@PAGE
    add x2, x2, _kuro_global_89@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_92@PAGE
    add x0, x0, _kuro_global_92@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4944]
    mov x0, #0
    str x0, [sp, #4952]
    ldr x0, [sp, #4944]
    ldr x1, [sp, #4952]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4960]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4968]
    adrp x0, _kuro_global_89@PAGE
    add x0, x0, _kuro_global_89@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4976]
    mov x0, #1
    str x0, [sp, #4984]
    ldr x0, [sp, #4976]
    ldr x1, [sp, #4984]
    add x0, x0, x1
    str x0, [sp, #4992]
    ldr x0, [sp, #4968]
    ldr x1, [sp, #4992]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #5000]
    ldr x0, [sp, #4960]
    ldr x1, [sp, #5000]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #5016]
    ldr x0, [sp, #5016]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else77
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5024]
    mov x0, #1
    str x0, [sp, #5032]
    ldr x1, [sp, #5024]
    ldr x0, [sp, #5032]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5040]
    ldr x1, [sp, #5040]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #5048]
    ldr x0, [sp, #5048]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5056]
    ldr x0, [sp, #5056]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #5064]
    ldr x0, [sp, #5064]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5072]
    ldr x0, [sp, #5072]
    adrp x2, _kuro_global_91@PAGE
    add x2, x2, _kuro_global_91@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5080]
    mov x0, #8
    str x0, [sp, #5088]
    ldr x0, [sp, #5080]
    ldr x1, [sp, #5088]
    mul x0, x0, x1
    str x0, [sp, #5104]
    mov x0, #8
    str x0, [sp, #5112]
    ldr x0, [sp, #5104]
    ldr x1, [sp, #5112]
    sub x0, x0, x1
    str x0, [sp, #5120]
    ldr x0, [sp, #5120]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5128]
    ldr x0, [sp, #5128]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #5136]
    ldr x0, [sp, #5136]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5144]
    ldr x0, [sp, #5144]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5152]
    adrp x0, L_kuro_data_191@PAGE
    add x0, x0, L_kuro_data_191@PAGEOFF
    str x0, [sp, #5160]
    ldr x0, [sp, #5152]
    ldr x1, [sp, #5160]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5168]
    ldr x0, [sp, #5168]
    ldr x1, [sp, #5152]
    bl _strcpy
    ldr x0, [sp, #5168]
    ldr x1, [sp, #5160]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5176]
    ldr x0, [sp, #5168]
    ldr x1, [sp, #5176]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5192]
    ldr x0, [sp, #5192]
    ldr x1, [sp, #5168]
    bl _strcpy
    ldr x0, [sp, #5192]
    ldr x1, [sp, #5176]
    bl _strcat
    adrp x0, L_kuro_data_192@PAGE
    add x0, x0, L_kuro_data_192@PAGEOFF
    str x0, [sp, #5200]
    ldr x0, [sp, #5192]
    ldr x1, [sp, #5200]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5208]
    ldr x0, [sp, #5208]
    ldr x1, [sp, #5192]
    bl _strcpy
    ldr x0, [sp, #5208]
    ldr x1, [sp, #5200]
    bl _strcat
    adrp x0, _kuro_global_91@PAGE
    add x0, x0, _kuro_global_91@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5216]
    ldr x0, [sp, #5208]
    ldr x1, [sp, #5216]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5224]
    ldr x0, [sp, #5224]
    ldr x1, [sp, #5208]
    bl _strcpy
    ldr x0, [sp, #5224]
    ldr x1, [sp, #5216]
    bl _strcat
    adrp x0, L_kuro_data_193@PAGE
    add x0, x0, L_kuro_data_193@PAGEOFF
    str x0, [sp, #5232]
    ldr x0, [sp, #5224]
    ldr x1, [sp, #5232]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5240]
    ldr x0, [sp, #5240]
    ldr x1, [sp, #5224]
    bl _strcpy
    ldr x0, [sp, #5240]
    ldr x1, [sp, #5232]
    bl _strcat
    ldr x0, [sp, #5240]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5248]
    mov x0, #1
    str x0, [sp, #5256]
    ldr x0, [sp, #5248]
    ldr x1, [sp, #5256]
    sub x0, x0, x1
    str x0, [sp, #5264]
    ldr x0, [sp, #5264]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif78
L_kuro_fn_EmitStraightIntegerProgram_else77:
    mov x0, #1
    str x0, [sp, #5280]
    ldr x0, [sp, #5280]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif78:
    b L_kuro_fn_EmitStraightIntegerProgram_endif76
L_kuro_fn_EmitStraightIntegerProgram_else75:
    mov x0, #1
    str x0, [sp, #5288]
    ldr x0, [sp, #5288]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif76:
    b L_kuro_fn_EmitStraightIntegerProgram_endif74
L_kuro_fn_EmitStraightIntegerProgram_else73:
L_kuro_fn_EmitStraightIntegerProgram_endif74:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5296]
    adrp x0, L_kuro_data_194@PAGE
    add x0, x0, L_kuro_data_194@PAGEOFF
    str x0, [sp, #5304]
    ldr x0, [sp, #5296]
    ldr x1, [sp, #5304]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #5312]
    ldr x0, [sp, #5312]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else79
    mov x0, #1
    str x0, [sp, #5320]
    ldr x0, [sp, #5320]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5328]
    mov x0, #0
    str x0, [sp, #5336]
    ldr x0, [sp, #5328]
    ldr x1, [sp, #5336]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #5344]
    ldr x0, [sp, #5344]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else81
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5352]
    mov x0, #1
    str x0, [sp, #5368]
    ldr x0, [sp, #5352]
    ldr x1, [sp, #5368]
    sub x0, x0, x1
    str x0, [sp, #5376]
    ldr x0, [sp, #5376]
    adrp x2, _kuro_global_90@PAGE
    add x2, x2, _kuro_global_90@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5384]
    ldr x1, [sp, #5384]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #5392]
    ldr x0, [sp, #5392]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5400]
    ldr x0, [sp, #5400]
    adrp x2, _kuro_global_92@PAGE
    add x2, x2, _kuro_global_92@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5408]
    ldr x1, [sp, #5408]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #5416]
    ldr x0, [sp, #5416]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5424]
    ldr x0, [sp, #5424]
    adrp x2, _kuro_global_89@PAGE
    add x2, x2, _kuro_global_89@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_92@PAGE
    add x0, x0, _kuro_global_92@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5432]
    mov x0, #1
    str x0, [sp, #5440]
    ldr x0, [sp, #5432]
    ldr x1, [sp, #5440]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #5456]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5464]
    adrp x0, _kuro_global_89@PAGE
    add x0, x0, _kuro_global_89@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5472]
    ldr x0, [sp, #5464]
    ldr x1, [sp, #5472]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #5480]
    ldr x0, [sp, #5456]
    ldr x1, [sp, #5480]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #5488]
    ldr x0, [sp, #5488]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else83
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5496]
    ldr x1, [sp, #5496]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #5504]
    ldr x0, [sp, #5504]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5512]
    ldr x0, [sp, #5512]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #5520]
    ldr x0, [sp, #5520]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5528]
    ldr x0, [sp, #5528]
    adrp x2, _kuro_global_91@PAGE
    add x2, x2, _kuro_global_91@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5544]
    adrp x0, L_kuro_data_195@PAGE
    add x0, x0, L_kuro_data_195@PAGEOFF
    str x0, [sp, #5552]
    ldr x0, [sp, #5544]
    ldr x1, [sp, #5552]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5560]
    ldr x0, [sp, #5560]
    ldr x1, [sp, #5544]
    bl _strcpy
    ldr x0, [sp, #5560]
    ldr x1, [sp, #5552]
    bl _strcat
    adrp x0, _kuro_global_91@PAGE
    add x0, x0, _kuro_global_91@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5568]
    ldr x0, [sp, #5560]
    ldr x1, [sp, #5568]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5576]
    ldr x0, [sp, #5576]
    ldr x1, [sp, #5560]
    bl _strcpy
    ldr x0, [sp, #5576]
    ldr x1, [sp, #5568]
    bl _strcat
    adrp x0, L_kuro_data_196@PAGE
    add x0, x0, L_kuro_data_196@PAGEOFF
    str x0, [sp, #5584]
    ldr x0, [sp, #5576]
    ldr x1, [sp, #5584]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5592]
    ldr x0, [sp, #5592]
    ldr x1, [sp, #5576]
    bl _strcpy
    ldr x0, [sp, #5592]
    ldr x1, [sp, #5584]
    bl _strcat
    adrp x0, _kuro_global_91@PAGE
    add x0, x0, _kuro_global_91@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5600]
    ldr x0, [sp, #5592]
    ldr x1, [sp, #5600]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5608]
    ldr x0, [sp, #5608]
    ldr x1, [sp, #5592]
    bl _strcpy
    ldr x0, [sp, #5608]
    ldr x1, [sp, #5600]
    bl _strcat
    adrp x0, L_kuro_data_197@PAGE
    add x0, x0, L_kuro_data_197@PAGEOFF
    str x0, [sp, #5616]
    ldr x0, [sp, #5608]
    ldr x1, [sp, #5616]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5632]
    ldr x0, [sp, #5632]
    ldr x1, [sp, #5608]
    bl _strcpy
    ldr x0, [sp, #5632]
    ldr x1, [sp, #5616]
    bl _strcat
    ldr x0, [sp, #5632]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5640]
    mov x0, #1
    str x0, [sp, #5648]
    ldr x0, [sp, #5640]
    ldr x1, [sp, #5648]
    sub x0, x0, x1
    str x0, [sp, #5656]
    ldr x0, [sp, #5656]
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif84
L_kuro_fn_EmitStraightIntegerProgram_else83:
    mov x0, #1
    str x0, [sp, #5664]
    ldr x0, [sp, #5664]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif84:
    b L_kuro_fn_EmitStraightIntegerProgram_endif82
L_kuro_fn_EmitStraightIntegerProgram_else81:
    mov x0, #1
    str x0, [sp, #5672]
    ldr x0, [sp, #5672]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif82:
    b L_kuro_fn_EmitStraightIntegerProgram_endif80
L_kuro_fn_EmitStraightIntegerProgram_else79:
L_kuro_fn_EmitStraightIntegerProgram_endif80:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5680]
    adrp x0, L_kuro_data_198@PAGE
    add x0, x0, L_kuro_data_198@PAGEOFF
    str x0, [sp, #5688]
    ldr x0, [sp, #5680]
    ldr x1, [sp, #5688]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #5696]
    ldr x0, [sp, #5696]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else85
    mov x0, #1
    str x0, [sp, #5704]
    ldr x0, [sp, #5704]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5728]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5736]
    ldr x0, [sp, #5728]
    ldr x1, [sp, #5736]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #5744]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5752]
    mov x0, #0
    str x0, [sp, #5760]
    ldr x0, [sp, #5752]
    ldr x1, [sp, #5760]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #5768]
    ldr x0, [sp, #5744]
    ldr x1, [sp, #5768]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #5776]
    ldr x0, [sp, #5776]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else87
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5784]
    ldr x1, [sp, #5784]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #5792]
    ldr x0, [sp, #5792]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5800]
    ldr x0, [sp, #5800]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #5816]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #5816]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5824]
    mov x0, #0
    str x0, [sp, #5832]
    ldr x0, [sp, #5824]
    ldr x1, [sp, #5832]
    bl _kuro_fn_NativeFindVariable
    str x0, [sp, #5840]
    ldr x0, [sp, #5840]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5848]
    ldr x0, [sp, #5848]
    adrp x2, _kuro_global_86@PAGE
    add x2, x2, _kuro_global_86@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_86@PAGE
    add x0, x0, _kuro_global_86@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5856]
    mov x0, #0
    str x0, [sp, #5864]
    ldr x0, [sp, #5856]
    ldr x1, [sp, #5864]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #5872]
    ldr x0, [sp, #5872]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else89
    adrp x0, _kuro_global_82@PAGE
    add x0, x0, _kuro_global_82@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5880]
    mov x0, #32
    str x0, [sp, #5888]
    ldr x0, [sp, #5880]
    ldr x1, [sp, #5888]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #5904]
    ldr x0, [sp, #5904]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else91
    adrp x0, _kuro_global_82@PAGE
    add x0, x0, _kuro_global_82@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5912]
    ldr x0, [sp, #5912]
    adrp x2, _kuro_global_86@PAGE
    add x2, x2, _kuro_global_86@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5920]
    adrp x1, _kuro_collection_len_5@PAGE
    add x1, x1, _kuro_collection_len_5@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #5920]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_5@PAGE
    add x2, x2, _kuro_collection_len_5@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #5928]
    adrp x0, _kuro_global_82@PAGE
    add x0, x0, _kuro_global_82@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #5928]
    add x0, x0, x1
    adrp x2, _kuro_global_82@PAGE
    add x2, x2, _kuro_global_82@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif92
L_kuro_fn_EmitStraightIntegerProgram_else91:
    mov x0, #1
    str x0, [sp, #5936]
    ldr x0, [sp, #5936]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif92:
    b L_kuro_fn_EmitStraightIntegerProgram_endif90
L_kuro_fn_EmitStraightIntegerProgram_else89:
L_kuro_fn_EmitStraightIntegerProgram_endif90:
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5944]
    mov x0, #8
    str x0, [sp, #5952]
    ldr x0, [sp, #5944]
    ldr x1, [sp, #5952]
    mul x0, x0, x1
    str x0, [sp, #5960]
    mov x0, #8
    str x0, [sp, #5968]
    ldr x0, [sp, #5960]
    ldr x1, [sp, #5968]
    sub x0, x0, x1
    str x0, [sp, #5976]
    ldr x0, [sp, #5976]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    mov x0, #1024
    str x0, [sp, #5992]
    adrp x0, _kuro_global_86@PAGE
    add x0, x0, _kuro_global_86@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6000]
    mov x0, #8
    str x0, [sp, #6008]
    ldr x0, [sp, #6000]
    ldr x1, [sp, #6008]
    mul x0, x0, x1
    str x0, [sp, #6016]
    ldr x0, [sp, #5992]
    ldr x1, [sp, #6016]
    add x0, x0, x1
    str x0, [sp, #6024]
    ldr x0, [sp, #6024]
    adrp x2, _kuro_global_84@PAGE
    add x2, x2, _kuro_global_84@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6032]
    ldr x0, [sp, #6032]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #6040]
    ldr x0, [sp, #6040]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6048]
    ldr x0, [sp, #6048]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_84@PAGE
    add x0, x0, _kuro_global_84@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6056]
    ldr x0, [sp, #6056]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #6064]
    ldr x0, [sp, #6064]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6080]
    ldr x0, [sp, #6080]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6088]
    adrp x0, L_kuro_data_199@PAGE
    add x0, x0, L_kuro_data_199@PAGEOFF
    str x0, [sp, #6096]
    ldr x0, [sp, #6088]
    ldr x1, [sp, #6096]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6104]
    ldr x0, [sp, #6104]
    ldr x1, [sp, #6088]
    bl _strcpy
    ldr x0, [sp, #6104]
    ldr x1, [sp, #6096]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6112]
    ldr x0, [sp, #6104]
    ldr x1, [sp, #6112]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6120]
    ldr x0, [sp, #6120]
    ldr x1, [sp, #6104]
    bl _strcpy
    ldr x0, [sp, #6120]
    ldr x1, [sp, #6112]
    bl _strcat
    adrp x0, L_kuro_data_200@PAGE
    add x0, x0, L_kuro_data_200@PAGEOFF
    str x0, [sp, #6128]
    ldr x0, [sp, #6120]
    ldr x1, [sp, #6128]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6136]
    ldr x0, [sp, #6136]
    ldr x1, [sp, #6120]
    bl _strcpy
    ldr x0, [sp, #6136]
    ldr x1, [sp, #6128]
    bl _strcat
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6144]
    ldr x0, [sp, #6136]
    ldr x1, [sp, #6144]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6152]
    ldr x0, [sp, #6152]
    ldr x1, [sp, #6136]
    bl _strcpy
    ldr x0, [sp, #6152]
    ldr x1, [sp, #6144]
    bl _strcat
    adrp x0, L_kuro_data_201@PAGE
    add x0, x0, L_kuro_data_201@PAGEOFF
    str x0, [sp, #6168]
    ldr x0, [sp, #6152]
    ldr x1, [sp, #6168]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6176]
    ldr x0, [sp, #6176]
    ldr x1, [sp, #6152]
    bl _strcpy
    ldr x0, [sp, #6176]
    ldr x1, [sp, #6168]
    bl _strcat
    ldr x0, [sp, #6176]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6184]
    mov x0, #1
    str x0, [sp, #6192]
    ldr x0, [sp, #6184]
    ldr x1, [sp, #6192]
    sub x0, x0, x1
    str x0, [sp, #6200]
    ldr x0, [sp, #6200]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif88
L_kuro_fn_EmitStraightIntegerProgram_else87:
    mov x0, #1
    str x0, [sp, #6208]
    ldr x0, [sp, #6208]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif88:
    b L_kuro_fn_EmitStraightIntegerProgram_endif86
L_kuro_fn_EmitStraightIntegerProgram_else85:
L_kuro_fn_EmitStraightIntegerProgram_endif86:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6216]
    adrp x0, L_kuro_data_202@PAGE
    add x0, x0, L_kuro_data_202@PAGEOFF
    str x0, [sp, #6224]
    ldr x0, [sp, #6216]
    ldr x1, [sp, #6224]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #6232]
    ldr x0, [sp, #6232]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else93
    mov x0, #1
    str x0, [sp, #6240]
    ldr x0, [sp, #6240]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6256]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6264]
    ldr x0, [sp, #6256]
    ldr x1, [sp, #6264]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #6272]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6280]
    mov x0, #128
    str x0, [sp, #6288]
    ldr x0, [sp, #6280]
    ldr x1, [sp, #6288]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #6296]
    ldr x0, [sp, #6272]
    ldr x1, [sp, #6296]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #6304]
    ldr x0, [sp, #6304]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else95
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6312]
    ldr x1, [sp, #6312]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #6320]
    ldr x0, [sp, #6320]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6328]
    ldr x0, [sp, #6328]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #6344]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #6344]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6352]
    mov x0, #0
    str x0, [sp, #6360]
    ldr x0, [sp, #6352]
    ldr x1, [sp, #6360]
    bl _kuro_fn_NativeFindVariable
    str x0, [sp, #6368]
    ldr x0, [sp, #6368]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6376]
    ldr x0, [sp, #6376]
    adrp x2, _kuro_global_86@PAGE
    add x2, x2, _kuro_global_86@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_86@PAGE
    add x0, x0, _kuro_global_86@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6384]
    mov x0, #0
    str x0, [sp, #6392]
    ldr x0, [sp, #6384]
    ldr x1, [sp, #6392]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #6400]
    ldr x0, [sp, #6400]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else97
    mov x0, #1
    str x0, [sp, #6408]
    ldr x0, [sp, #6408]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif98
L_kuro_fn_EmitStraightIntegerProgram_else97:
    mov x0, #1024
    str x0, [sp, #6416]
    adrp x0, _kuro_global_86@PAGE
    add x0, x0, _kuro_global_86@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6432]
    mov x0, #8
    str x0, [sp, #6440]
    ldr x0, [sp, #6432]
    ldr x1, [sp, #6440]
    mul x0, x0, x1
    str x0, [sp, #6448]
    ldr x0, [sp, #6416]
    ldr x1, [sp, #6448]
    add x0, x0, x1
    str x0, [sp, #6456]
    ldr x0, [sp, #6456]
    adrp x2, _kuro_global_84@PAGE
    add x2, x2, _kuro_global_84@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6464]
    mov x0, #8
    str x0, [sp, #6472]
    ldr x0, [sp, #6464]
    ldr x1, [sp, #6472]
    mul x0, x0, x1
    str x0, [sp, #6480]
    ldr x0, [sp, #6480]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_84@PAGE
    add x0, x0, _kuro_global_84@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6488]
    ldr x0, [sp, #6488]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #6496]
    ldr x0, [sp, #6496]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6504]
    ldr x0, [sp, #6504]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6520]
    ldr x0, [sp, #6520]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #6528]
    ldr x0, [sp, #6528]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6536]
    ldr x0, [sp, #6536]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6544]
    adrp x0, L_kuro_data_203@PAGE
    add x0, x0, L_kuro_data_203@PAGEOFF
    str x0, [sp, #6552]
    ldr x0, [sp, #6544]
    ldr x1, [sp, #6552]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6560]
    ldr x0, [sp, #6560]
    ldr x1, [sp, #6544]
    bl _strcpy
    ldr x0, [sp, #6560]
    ldr x1, [sp, #6552]
    bl _strcat
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6568]
    ldr x0, [sp, #6560]
    ldr x1, [sp, #6568]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6576]
    ldr x0, [sp, #6576]
    ldr x1, [sp, #6560]
    bl _strcpy
    ldr x0, [sp, #6576]
    ldr x1, [sp, #6568]
    bl _strcat
    adrp x0, L_kuro_data_204@PAGE
    add x0, x0, L_kuro_data_204@PAGEOFF
    str x0, [sp, #6584]
    ldr x0, [sp, #6576]
    ldr x1, [sp, #6584]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6592]
    ldr x0, [sp, #6592]
    ldr x1, [sp, #6576]
    bl _strcpy
    ldr x0, [sp, #6592]
    ldr x1, [sp, #6584]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6616]
    ldr x0, [sp, #6592]
    ldr x1, [sp, #6616]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6624]
    ldr x0, [sp, #6624]
    ldr x1, [sp, #6592]
    bl _strcpy
    ldr x0, [sp, #6624]
    ldr x1, [sp, #6616]
    bl _strcat
    adrp x0, L_kuro_data_205@PAGE
    add x0, x0, L_kuro_data_205@PAGEOFF
    str x0, [sp, #6632]
    ldr x0, [sp, #6624]
    ldr x1, [sp, #6632]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #6640]
    ldr x0, [sp, #6640]
    ldr x1, [sp, #6624]
    bl _strcpy
    ldr x0, [sp, #6640]
    ldr x1, [sp, #6632]
    bl _strcat
    ldr x0, [sp, #6640]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #6648]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #6648]
    add x0, x0, x1
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif98:
    b L_kuro_fn_EmitStraightIntegerProgram_endif96
L_kuro_fn_EmitStraightIntegerProgram_else95:
    mov x0, #1
    str x0, [sp, #6656]
    ldr x0, [sp, #6656]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif96:
    b L_kuro_fn_EmitStraightIntegerProgram_endif94
L_kuro_fn_EmitStraightIntegerProgram_else93:
L_kuro_fn_EmitStraightIntegerProgram_endif94:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6664]
    adrp x0, L_kuro_data_206@PAGE
    add x0, x0, L_kuro_data_206@PAGEOFF
    str x0, [sp, #6672]
    ldr x0, [sp, #6664]
    ldr x1, [sp, #6672]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #6680]
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6688]
    adrp x0, L_kuro_data_207@PAGE
    add x0, x0, L_kuro_data_207@PAGEOFF
    str x0, [sp, #6704]
    ldr x0, [sp, #6688]
    ldr x1, [sp, #6704]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #6712]
    ldr x0, [sp, #6680]
    ldr x1, [sp, #6712]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #6720]
    ldr x0, [sp, #6720]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else99
    mov x0, #1
    str x0, [sp, #6728]
    ldr x0, [sp, #6728]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6736]
    adrp x0, _kuro_global_77@PAGE
    add x0, x0, _kuro_global_77@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6744]
    ldr x0, [sp, #6736]
    ldr x1, [sp, #6744]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #6752]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6760]
    mov x0, #0
    str x0, [sp, #6768]
    ldr x0, [sp, #6760]
    ldr x1, [sp, #6768]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #6776]
    ldr x0, [sp, #6752]
    ldr x1, [sp, #6776]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #6792]
    ldr x0, [sp, #6792]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else101
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6800]
    ldr x1, [sp, #6800]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #6808]
    ldr x0, [sp, #6808]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6816]
    ldr x0, [sp, #6816]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #6824]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #6824]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6832]
    mov x0, #0
    str x0, [sp, #6840]
    ldr x0, [sp, #6832]
    ldr x1, [sp, #6840]
    bl _kuro_fn_NativeFindVariable
    str x0, [sp, #6848]
    ldr x0, [sp, #6848]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6856]
    ldr x0, [sp, #6856]
    adrp x2, _kuro_global_86@PAGE
    add x2, x2, _kuro_global_86@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_86@PAGE
    add x0, x0, _kuro_global_86@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6864]
    mov x0, #0
    str x0, [sp, #6880]
    ldr x0, [sp, #6864]
    ldr x1, [sp, #6880]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #6888]
    ldr x0, [sp, #6888]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else103
    mov x0, #1
    str x0, [sp, #6896]
    ldr x0, [sp, #6896]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif104
L_kuro_fn_EmitStraightIntegerProgram_else103:
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6904]
    mov x0, #8
    str x0, [sp, #6912]
    ldr x0, [sp, #6904]
    ldr x1, [sp, #6912]
    mul x0, x0, x1
    str x0, [sp, #6920]
    mov x0, #8
    str x0, [sp, #6928]
    ldr x0, [sp, #6920]
    ldr x1, [sp, #6928]
    sub x0, x0, x1
    str x0, [sp, #6936]
    ldr x0, [sp, #6936]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    mov x0, #1024
    str x0, [sp, #6944]
    adrp x0, _kuro_global_86@PAGE
    add x0, x0, _kuro_global_86@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6952]
    mov x0, #8
    str x0, [sp, #6968]
    ldr x0, [sp, #6952]
    ldr x1, [sp, #6968]
    mul x0, x0, x1
    str x0, [sp, #6976]
    ldr x0, [sp, #6944]
    ldr x1, [sp, #6976]
    add x0, x0, x1
    str x0, [sp, #6984]
    ldr x0, [sp, #6984]
    adrp x2, _kuro_global_84@PAGE
    add x2, x2, _kuro_global_84@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #6992]
    ldr x0, [sp, #6992]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #7000]
    ldr x0, [sp, #7000]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7008]
    ldr x0, [sp, #7008]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_84@PAGE
    add x0, x0, _kuro_global_84@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7016]
    ldr x0, [sp, #7016]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #7024]
    ldr x0, [sp, #7024]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7032]
    ldr x0, [sp, #7032]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7040]
    adrp x0, L_kuro_data_208@PAGE
    add x0, x0, L_kuro_data_208@PAGEOFF
    str x0, [sp, #7056]
    ldr x0, [sp, #7040]
    ldr x1, [sp, #7056]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7064]
    ldr x0, [sp, #7064]
    ldr x1, [sp, #7040]
    bl _strcpy
    ldr x0, [sp, #7064]
    ldr x1, [sp, #7056]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7072]
    ldr x0, [sp, #7064]
    ldr x1, [sp, #7072]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7080]
    ldr x0, [sp, #7080]
    ldr x1, [sp, #7064]
    bl _strcpy
    ldr x0, [sp, #7080]
    ldr x1, [sp, #7072]
    bl _strcat
    adrp x0, L_kuro_data_209@PAGE
    add x0, x0, L_kuro_data_209@PAGEOFF
    str x0, [sp, #7088]
    ldr x0, [sp, #7080]
    ldr x1, [sp, #7088]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7096]
    ldr x0, [sp, #7096]
    ldr x1, [sp, #7080]
    bl _strcpy
    ldr x0, [sp, #7096]
    ldr x1, [sp, #7088]
    bl _strcat
    ldr x0, [sp, #7096]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7104]
    adrp x0, L_kuro_data_210@PAGE
    add x0, x0, L_kuro_data_210@PAGEOFF
    str x0, [sp, #7112]
    ldr x0, [sp, #7104]
    ldr x1, [sp, #7112]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #7120]
    ldr x0, [sp, #7120]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else105
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7128]
    adrp x0, L_kuro_data_211@PAGE
    add x0, x0, L_kuro_data_211@PAGEOFF
    str x0, [sp, #7144]
    ldr x0, [sp, #7128]
    ldr x1, [sp, #7144]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7152]
    ldr x0, [sp, #7152]
    ldr x1, [sp, #7128]
    bl _strcpy
    ldr x0, [sp, #7152]
    ldr x1, [sp, #7144]
    bl _strcat
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7160]
    ldr x0, [sp, #7152]
    ldr x1, [sp, #7160]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7168]
    ldr x0, [sp, #7168]
    ldr x1, [sp, #7152]
    bl _strcpy
    ldr x0, [sp, #7168]
    ldr x1, [sp, #7160]
    bl _strcat
    adrp x0, L_kuro_data_212@PAGE
    add x0, x0, L_kuro_data_212@PAGEOFF
    str x0, [sp, #7176]
    ldr x0, [sp, #7168]
    ldr x1, [sp, #7176]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7184]
    ldr x0, [sp, #7184]
    ldr x1, [sp, #7168]
    bl _strcpy
    ldr x0, [sp, #7184]
    ldr x1, [sp, #7176]
    bl _strcat
    ldr x0, [sp, #7184]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif106
L_kuro_fn_EmitStraightIntegerProgram_else105:
L_kuro_fn_EmitStraightIntegerProgram_endif106:
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7192]
    adrp x0, L_kuro_data_213@PAGE
    add x0, x0, L_kuro_data_213@PAGEOFF
    str x0, [sp, #7200]
    ldr x0, [sp, #7192]
    ldr x1, [sp, #7200]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7208]
    ldr x0, [sp, #7208]
    ldr x1, [sp, #7192]
    bl _strcpy
    ldr x0, [sp, #7208]
    ldr x1, [sp, #7200]
    bl _strcat
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7216]
    ldr x0, [sp, #7208]
    ldr x1, [sp, #7216]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7232]
    ldr x0, [sp, #7232]
    ldr x1, [sp, #7208]
    bl _strcpy
    ldr x0, [sp, #7232]
    ldr x1, [sp, #7216]
    bl _strcat
    adrp x0, L_kuro_data_214@PAGE
    add x0, x0, L_kuro_data_214@PAGEOFF
    str x0, [sp, #7240]
    ldr x0, [sp, #7232]
    ldr x1, [sp, #7240]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7248]
    ldr x0, [sp, #7248]
    ldr x1, [sp, #7232]
    bl _strcpy
    ldr x0, [sp, #7248]
    ldr x1, [sp, #7240]
    bl _strcat
    ldr x0, [sp, #7248]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7256]
    mov x0, #1
    str x0, [sp, #7264]
    ldr x0, [sp, #7256]
    ldr x1, [sp, #7264]
    sub x0, x0, x1
    str x0, [sp, #7272]
    ldr x0, [sp, #7272]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif104:
    b L_kuro_fn_EmitStraightIntegerProgram_endif102
L_kuro_fn_EmitStraightIntegerProgram_else101:
    mov x0, #1
    str x0, [sp, #7280]
    ldr x0, [sp, #7280]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif102:
    b L_kuro_fn_EmitStraightIntegerProgram_endif100
L_kuro_fn_EmitStraightIntegerProgram_else99:
L_kuro_fn_EmitStraightIntegerProgram_endif100:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7288]
    adrp x0, L_kuro_data_215@PAGE
    add x0, x0, L_kuro_data_215@PAGEOFF
    str x0, [sp, #7296]
    ldr x0, [sp, #7288]
    ldr x1, [sp, #7296]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #7304]
    ldr x0, [sp, #7304]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else107
    mov x0, #1
    str x0, [sp, #7320]
    ldr x0, [sp, #7320]
    adrp x2, _kuro_global_76@PAGE
    add x2, x2, _kuro_global_76@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7328]
    mov x0, #0
    str x0, [sp, #7336]
    ldr x0, [sp, #7328]
    ldr x1, [sp, #7336]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #7344]
    ldr x0, [sp, #7344]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else109
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7352]
    mov x0, #8
    str x0, [sp, #7360]
    ldr x0, [sp, #7352]
    ldr x1, [sp, #7360]
    mul x0, x0, x1
    str x0, [sp, #7368]
    mov x0, #8
    str x0, [sp, #7376]
    ldr x0, [sp, #7368]
    ldr x1, [sp, #7376]
    sub x0, x0, x1
    str x0, [sp, #7384]
    ldr x0, [sp, #7384]
    adrp x2, _kuro_global_73@PAGE
    add x2, x2, _kuro_global_73@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_73@PAGE
    add x0, x0, _kuro_global_73@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7392]
    ldr x0, [sp, #7392]
    bl _kuro_fn_NativeLengthToText
    str x0, [sp, #7408]
    ldr x0, [sp, #7408]
    adrp x2, _kuro_global_95@PAGE
    add x2, x2, _kuro_global_95@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_95@PAGE
    add x0, x0, _kuro_global_95@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7416]
    ldr x0, [sp, #7416]
    adrp x2, _kuro_global_74@PAGE
    add x2, x2, _kuro_global_74@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7424]
    adrp x0, L_kuro_data_216@PAGE
    add x0, x0, L_kuro_data_216@PAGEOFF
    str x0, [sp, #7432]
    ldr x0, [sp, #7424]
    ldr x1, [sp, #7432]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7440]
    ldr x0, [sp, #7440]
    ldr x1, [sp, #7424]
    bl _strcpy
    ldr x0, [sp, #7440]
    ldr x1, [sp, #7432]
    bl _strcat
    adrp x0, _kuro_global_74@PAGE
    add x0, x0, _kuro_global_74@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7448]
    ldr x0, [sp, #7440]
    ldr x1, [sp, #7448]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7456]
    ldr x0, [sp, #7456]
    ldr x1, [sp, #7440]
    bl _strcpy
    ldr x0, [sp, #7456]
    ldr x1, [sp, #7448]
    bl _strcat
    adrp x0, L_kuro_data_217@PAGE
    add x0, x0, L_kuro_data_217@PAGEOFF
    str x0, [sp, #7464]
    ldr x0, [sp, #7456]
    ldr x1, [sp, #7464]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7472]
    ldr x0, [sp, #7472]
    ldr x1, [sp, #7456]
    bl _strcpy
    ldr x0, [sp, #7472]
    ldr x1, [sp, #7464]
    bl _strcat
    ldr x0, [sp, #7472]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7480]
    mov x0, #1
    str x0, [sp, #7504]
    ldr x0, [sp, #7480]
    ldr x1, [sp, #7504]
    sub x0, x0, x1
    str x0, [sp, #7512]
    ldr x0, [sp, #7512]
    adrp x2, _kuro_global_72@PAGE
    add x2, x2, _kuro_global_72@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif110
L_kuro_fn_EmitStraightIntegerProgram_else109:
    mov x0, #1
    str x0, [sp, #7520]
    ldr x0, [sp, #7520]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
L_kuro_fn_EmitStraightIntegerProgram_endif110:
    b L_kuro_fn_EmitStraightIntegerProgram_endif108
L_kuro_fn_EmitStraightIntegerProgram_else107:
L_kuro_fn_EmitStraightIntegerProgram_endif108:
    adrp x0, _kuro_global_76@PAGE
    add x0, x0, _kuro_global_76@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7528]
    mov x0, #0
    str x0, [sp, #7536]
    ldr x0, [sp, #7528]
    ldr x1, [sp, #7536]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #7544]
    ldr x0, [sp, #7544]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else111
    mov x0, #1
    str x0, [sp, #7552]
    ldr x0, [sp, #7552]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif112
L_kuro_fn_EmitStraightIntegerProgram_else111:
L_kuro_fn_EmitStraightIntegerProgram_endif112:
    b L_kuro_fn_EmitStraightIntegerProgram_while_start2
L_kuro_fn_EmitStraightIntegerProgram_while_end3:
    adrp x0, _kuro_global_72@PAGE
    add x0, x0, _kuro_global_72@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7560]
    mov x0, #0
    str x0, [sp, #7568]
    ldr x0, [sp, #7560]
    ldr x1, [sp, #7568]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #7576]
    adrp x0, _kuro_global_39@PAGE
    add x0, x0, _kuro_global_39@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7592]
    mov x0, #0
    str x0, [sp, #7600]
    ldr x0, [sp, #7592]
    ldr x1, [sp, #7600]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #7608]
    ldr x0, [sp, #7576]
    ldr x1, [sp, #7608]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #7616]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7624]
    mov x0, #0
    str x0, [sp, #7632]
    ldr x0, [sp, #7624]
    ldr x1, [sp, #7632]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #7640]
    ldr x0, [sp, #7616]
    ldr x1, [sp, #7640]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #7648]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7656]
    mov x0, #0
    str x0, [sp, #7664]
    ldr x0, [sp, #7656]
    ldr x1, [sp, #7664]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #7680]
    ldr x0, [sp, #7648]
    ldr x1, [sp, #7680]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #7688]
    ldr x0, [sp, #7688]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else113
    mov x0, #1
    str x0, [sp, #7696]
    ldr x0, [sp, #7696]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_EmitStraightIntegerProgram_endif114
L_kuro_fn_EmitStraightIntegerProgram_else113:
L_kuro_fn_EmitStraightIntegerProgram_endif114:
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7704]
    mov x0, #0
    str x0, [sp, #7712]
    ldr x0, [sp, #7704]
    ldr x1, [sp, #7712]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #7720]
    ldr x0, [sp, #7720]
    cbz w0, L_kuro_fn_EmitStraightIntegerProgram_else115
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7728]
    adrp x0, L_kuro_data_218@PAGE
    add x0, x0, L_kuro_data_218@PAGEOFF
    str x0, [sp, #7736]
    ldr x0, [sp, #7728]
    ldr x1, [sp, #7736]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7744]
    ldr x0, [sp, #7744]
    ldr x1, [sp, #7728]
    bl _strcpy
    ldr x0, [sp, #7744]
    ldr x1, [sp, #7736]
    bl _strcat
    ldr x0, [sp, #7744]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7752]
    adrp x0, L_kuro_data_219@PAGE
    add x0, x0, L_kuro_data_219@PAGEOFF
    str x0, [sp, #7768]
    ldr x0, [sp, #7752]
    ldr x1, [sp, #7768]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #7776]
    ldr x0, [sp, #7776]
    ldr x1, [sp, #7752]
    bl _strcpy
    ldr x0, [sp, #7776]
    ldr x1, [sp, #7768]
    bl _strcat
    ldr x0, [sp, #7776]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #7784]
    ldr x0, [sp, #7784]
    cmp x0, #4096
    b.lo L_kuro_print_dynamic_number_EmitStraightIntegerProgram_t832
    mov x1, #0x100000000000
    cmp x0, x1
    b.lo L_kuro_print_dynamic_text_EmitStraightIntegerProgram_t832
L_kuro_print_dynamic_float_EmitStraightIntegerProgram_t832:
    sub sp, sp, #16
    str x0, [sp]
    adrp x0, L_kuro_float_format@PAGE
    add x0, x0, L_kuro_float_format@PAGEOFF
    bl _printf
    add sp, sp, #16
    b L_kuro_print_dynamic_done_EmitStraightIntegerProgram_t832
L_kuro_print_dynamic_text_EmitStraightIntegerProgram_t832:
    bl _puts
    b L_kuro_print_dynamic_done_EmitStraightIntegerProgram_t832
L_kuro_print_dynamic_number_EmitStraightIntegerProgram_t832:
    bl _kuro_print_int
L_kuro_print_dynamic_done_EmitStraightIntegerProgram_t832:
    b L_kuro_fn_EmitStraightIntegerProgram_endif116
L_kuro_fn_EmitStraightIntegerProgram_else115:
L_kuro_fn_EmitStraightIntegerProgram_endif116:
    mov x0, #0
    mov x15, #7952
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
.section __TEXT,__cstring
L_kuro_data_0: .asciz "kuro.bytecode/1"
L_kuro_data_1: .asciz ""
L_kuro_data_2: .asciz "\\"
L_kuro_data_3: .asciz "kuro.input/1"
L_kuro_data_4: .asciz ""
L_kuro_data_5: .asciz "\n"
L_kuro_data_6: .asciz "\r"
L_kuro_data_7: .asciz ""
L_kuro_data_8: .asciz "BC_CONST"
L_kuro_data_9: .asciz "BC_LOADVAR"
L_kuro_data_10: .asciz "BC_STORE_LIST"
L_kuro_data_11: .asciz "BC_BINOP"
L_kuro_data_12: .asciz "BC_CMP"
L_kuro_data_13: .asciz "BC_BOOL"
L_kuro_data_14: .asciz "BC_ISCLASS"
L_kuro_data_15: .asciz "BC_UPDATE"
L_kuro_data_16: .asciz "BC_ADD"
L_kuro_data_17: .asciz "BC_APPEND"
L_kuro_data_18: .asciz "BC_LENGTH"
L_kuro_data_19: .asciz "BC_SET"
L_kuro_data_20: .asciz "BC_INPUT"
L_kuro_data_21: .asciz "BC_FUNC_BEGIN"
L_kuro_data_22: .asciz "BC_CALL_BEGIN"
L_kuro_data_23: .asciz "BC_GET"
L_kuro_data_24: .asciz "BC_DECLTYPE"
L_kuro_data_25: .asciz "BC_PARAM"
L_kuro_data_26: .asciz "BC_PRINT"
L_kuro_data_27: .asciz "BC_IF_BEGIN"
L_kuro_data_28: .asciz "BC_ELSE_BEGIN"
L_kuro_data_29: .asciz "BC_IF_END"
L_kuro_data_30: .asciz "BC_REPEAT_BEGIN"
L_kuro_data_31: .asciz "BC_REPEAT_END"
L_kuro_data_32: .asciz "BC_WHILE_BEGIN"
L_kuro_data_33: .asciz "BC_WHILE_TEST"
L_kuro_data_34: .asciz "BC_WHILE_END"
L_kuro_data_35: .asciz "BC_FUNC_END"
L_kuro_data_36: .asciz "BC_RETURN"
L_kuro_data_37: .asciz "BC_CALL_END"
L_kuro_data_38: .asciz "BC_IF_BEGIN"
L_kuro_data_39: .asciz "BC_ELSE_BEGIN"
L_kuro_data_40: .asciz "BC_IF_END"
L_kuro_data_41: .asciz "BC_REPEAT_BEGIN"
L_kuro_data_42: .asciz "BC_REPEAT_END"
L_kuro_data_43: .asciz "BC_WHILE_BEGIN"
L_kuro_data_44: .asciz "BC_WHILE_TEST"
L_kuro_data_45: .asciz "BC_WHILE_END"
L_kuro_data_46: .asciz "BC_FUNC_BEGIN"
L_kuro_data_47: .asciz "BC_PARAM"
L_kuro_data_48: .asciz "BC_RETURN"
L_kuro_data_49: .asciz "BC_FUNC_END"
L_kuro_data_50: .asciz "BC_CALL_BEGIN"
L_kuro_data_51: .asciz "BC_CALL_END"
L_kuro_data_52: .asciz "BC_INVALID_ARTIFACT"
L_kuro_data_53: .asciz "BC_INVALID_ARTIFACT"
L_kuro_data_54: .asciz ""
L_kuro_data_55: .asciz "\\"
L_kuro_data_56: .asciz "\""
L_kuro_data_57: .asciz ""
L_kuro_data_58: .asciz "e"
L_kuro_data_59: .asciz "n"
L_kuro_data_60: .asciz "\n"
L_kuro_data_61: .asciz "i"
L_kuro_data_62: .asciz "r"
L_kuro_data_63: .asciz "\r"
L_kuro_data_64: .asciz "t"
L_kuro_data_65: .asciz "\t"
L_kuro_data_66: .asciz ""
L_kuro_data_67: .asciz ""
L_kuro_data_68: .asciz "0"
L_kuro_data_69: .asciz "1"
L_kuro_data_70: .asciz "2"
L_kuro_data_71: .asciz "3"
L_kuro_data_72: .asciz "4"
L_kuro_data_73: .asciz "5"
L_kuro_data_74: .asciz "6"
L_kuro_data_75: .asciz "7"
L_kuro_data_76: .asciz "8"
L_kuro_data_77: .asciz "9"
L_kuro_data_78: .asciz ""
L_kuro_data_79: .asciz "BC_CONST"
L_kuro_data_80: .asciz "BC_PRINT"
L_kuro_data_81: .asciz ""
L_kuro_data_82: .asciz "\n"
L_kuro_data_83: .asciz "n"
L_kuro_data_84: .asciz "\r"
L_kuro_data_85: .asciz "r"
L_kuro_data_86: .asciz "\t"
L_kuro_data_87: .asciz "t"
L_kuro_data_88: .asciz ""
L_kuro_data_89: .asciz ".section __TEXT,__text\n.globl _main\n_main:\n"
L_kuro_data_90: .asciz "    adrp x1, L_kuro_literal@PAGE\n"
L_kuro_data_91: .asciz "    add x1, x1, L_kuro_literal@PAGEOFF\n"
L_kuro_data_92: .asciz "    mov x0, #1\n    mov x2, #"
L_kuro_data_93: .asciz "\n    mov x16, #4\n    svc #0x80\n    mov x0, #0\n    mov x16, #1\n    svc #0x80\n"
L_kuro_data_94: .asciz ".section __TEXT,__cstring\nL_kuro_literal:\n.asciz \""
L_kuro_data_95: .asciz "\"\n"
L_kuro_data_96: .asciz ""
L_kuro_data_97: .asciz "BC_CONST"
L_kuro_data_98: .asciz "BC_CONST"
L_kuro_data_99: .asciz "BC_BINOP"
L_kuro_data_100: .asciz "BC_PRINT"
L_kuro_data_101: .asciz ""
L_kuro_data_102: .asciz "+"
L_kuro_data_103: .asciz "    add x0, x0, x1\n"
L_kuro_data_104: .asciz "-"
L_kuro_data_105: .asciz "    sub x0, x0, x1\n"
L_kuro_data_106: .asciz "*"
L_kuro_data_107: .asciz "    mul x0, x0, x1\n"
L_kuro_data_108: .asciz "/"
L_kuro_data_109: .asciz "    sdiv x0, x0, x1\n"
L_kuro_data_110: .asciz "0"
L_kuro_data_111: .asciz ""
L_kuro_data_112: .asciz ".section __TEXT,__text\n.globl _main\n_main:\n    mov x0, #"
L_kuro_data_113: .asciz "\n    mov x1, #"
L_kuro_data_114: .asciz "\n"
L_kuro_data_115: .asciz "    bl _kuro_print_int\n    mov x0, #0\n    mov x16, #1\n    svc #0x80\n"
L_kuro_data_116: .asciz "_kuro_print_int:\n    sub sp, sp, #32\n    add x3, sp, #31\n    mov w4, #10\n    strb w4, [x3]\n    mov x2, #1\n    mov x5, #10\n    mov x6, #0\n    cmp x0, #0\n    b.ge L_kuro_digits\n    neg x0, x0\n    mov x6, #1\nL_kuro_digits:\n    udiv x7, x0, x5\n    msub x8, x7, x5, x0\n    add x8, x8, #48\n    sub x3, x3, #1\n    strb w8, [x3]\n    add x2, x2, #1\n    mov x0, x7\n    cbnz x0, L_kuro_digits\n    cbz x6, L_kuro_write\n    sub x3, x3, #1\n    mov w8, #45\n    strb w8, [x3]\n    add x2, x2, #1\nL_kuro_write:\n    mov x0, #1\n    mov x1, x3\n    mov x16, #4\n    svc #0x80\n    add sp, sp, #32\n    ret\n"
L_kuro_data_117: .asciz ".section __TEXT,__text\n.globl _main\n_main:\n    sub sp, sp, #2048\n"
L_kuro_data_118: .asciz "BC_CONST"
L_kuro_data_119: .asciz "    mov x0, #"
L_kuro_data_120: .asciz "\n    str x0, [sp, #"
L_kuro_data_121: .asciz "]\n"
L_kuro_data_122: .asciz "BC_BINOP"
L_kuro_data_123: .asciz ""
L_kuro_data_124: .asciz "+"
L_kuro_data_125: .asciz "    add x0, x0, x1\n"
L_kuro_data_126: .asciz "-"
L_kuro_data_127: .asciz "    sub x0, x0, x1\n"
L_kuro_data_128: .asciz "*"
L_kuro_data_129: .asciz "    mul x0, x0, x1\n"
L_kuro_data_130: .asciz "/"
L_kuro_data_131: .asciz "    cbz x1, L_kuro_division_error\n    sdiv x0, x0, x1\n"
L_kuro_data_132: .asciz ""
L_kuro_data_133: .asciz "    ldr x0, [sp, #"
L_kuro_data_134: .asciz "]\n    ldr x1, [sp, #"
L_kuro_data_135: .asciz "]\n"
L_kuro_data_136: .asciz "    str x0, [sp, #"
L_kuro_data_137: .asciz "]\n"
L_kuro_data_138: .asciz "BC_CMP"
L_kuro_data_139: .asciz ""
L_kuro_data_140: .asciz "eq"
L_kuro_data_141: .asciz "    cset w0, eq\n"
L_kuro_data_142: .asciz "neq"
L_kuro_data_143: .asciz "    cset w0, ne\n"
L_kuro_data_144: .asciz "lt"
L_kuro_data_145: .asciz "    cset w0, lt\n"
L_kuro_data_146: .asciz "lte"
L_kuro_data_147: .asciz "le"
L_kuro_data_148: .asciz "    cset w0, le\n"
L_kuro_data_149: .asciz "gt"
L_kuro_data_150: .asciz "    cset w0, gt\n"
L_kuro_data_151: .asciz "gte"
L_kuro_data_152: .asciz "ge"
L_kuro_data_153: .asciz "    cset w0, ge\n"
L_kuro_data_154: .asciz ""
L_kuro_data_155: .asciz "    ldr x0, [sp, #"
L_kuro_data_156: .asciz "]\n    ldr x1, [sp, #"
L_kuro_data_157: .asciz "]\n    cmp x0, x1\n"
L_kuro_data_158: .asciz "    str x0, [sp, #"
L_kuro_data_159: .asciz "]\n"
L_kuro_data_160: .asciz "BC_IF_BEGIN"
L_kuro_data_161: .asciz "    ldr x0, [sp, #"
L_kuro_data_162: .asciz "]\n    cbz x0, L_kuro_else_"
L_kuro_data_163: .asciz "\n"
L_kuro_data_164: .asciz "BC_ELSE_BEGIN"
L_kuro_data_165: .asciz "    b L_kuro_endif_"
L_kuro_data_166: .asciz "\nL_kuro_else_"
L_kuro_data_167: .asciz ":\n"
L_kuro_data_168: .asciz "BC_IF_END"
L_kuro_data_169: .asciz "L_kuro_endif_"
L_kuro_data_170: .asciz ":\n"
L_kuro_data_171: .asciz "L_kuro_else_"
L_kuro_data_172: .asciz ":\n"
L_kuro_data_173: .asciz "BC_REPEAT_BEGIN"
L_kuro_data_174: .asciz "    ldr x0, [sp, #"
L_kuro_data_175: .asciz "]\n    str x0, [sp, #"
L_kuro_data_176: .asciz "]\n"
L_kuro_data_177: .asciz "L_kuro_repeat_"
L_kuro_data_178: .asciz ":\n    ldr x0, [sp, #"
L_kuro_data_179: .asciz "]\n    cmp x0, #0\n    b.le L_kuro_endrepeat_"
L_kuro_data_180: .asciz "\n"
L_kuro_data_181: .asciz "BC_REPEAT_END"
L_kuro_data_182: .asciz "    ldr x0, [sp, #"
L_kuro_data_183: .asciz "]\n    sub x0, x0, #1\n    str x0, [sp, #"
L_kuro_data_184: .asciz "]\n    b L_kuro_repeat_"
L_kuro_data_185: .asciz "\nL_kuro_endrepeat_"
L_kuro_data_186: .asciz ":\n"
L_kuro_data_187: .asciz "BC_WHILE_BEGIN"
L_kuro_data_188: .asciz "L_kuro_while_"
L_kuro_data_189: .asciz ":\n"
L_kuro_data_190: .asciz "BC_WHILE_TEST"
L_kuro_data_191: .asciz "    ldr x0, [sp, #"
L_kuro_data_192: .asciz "]\n    cbz x0, L_kuro_endwhile_"
L_kuro_data_193: .asciz "\n"
L_kuro_data_194: .asciz "BC_WHILE_END"
L_kuro_data_195: .asciz "    b L_kuro_while_"
L_kuro_data_196: .asciz "\nL_kuro_endwhile_"
L_kuro_data_197: .asciz ":\n"
L_kuro_data_198: .asciz "BC_STORE_LIST"
L_kuro_data_199: .asciz "    ldr x0, [sp, #"
L_kuro_data_200: .asciz "]\n    str x0, [sp, #"
L_kuro_data_201: .asciz "]\n"
L_kuro_data_202: .asciz "BC_LOADVAR"
L_kuro_data_203: .asciz "    ldr x0, [sp, #"
L_kuro_data_204: .asciz "]\n    str x0, [sp, #"
L_kuro_data_205: .asciz "]\n"
L_kuro_data_206: .asciz "BC_UPDATE"
L_kuro_data_207: .asciz "BC_ADD"
L_kuro_data_208: .asciz "    ldr x0, [sp, #"
L_kuro_data_209: .asciz "]\n"
L_kuro_data_210: .asciz "BC_ADD"
L_kuro_data_211: .asciz "    ldr x1, [sp, #"
L_kuro_data_212: .asciz "]\n    add x0, x1, x0\n"
L_kuro_data_213: .asciz "    str x0, [sp, #"
L_kuro_data_214: .asciz "]\n"
L_kuro_data_215: .asciz "BC_PRINT"
L_kuro_data_216: .asciz "    ldr x0, [sp, #"
L_kuro_data_217: .asciz "]\n    bl _kuro_print_int\n"
L_kuro_data_218: .asciz "    add sp, sp, #2048\n    mov x0, #0\n    mov x16, #1\n    svc #0x80\nL_kuro_division_error:\n    add sp, sp, #2048\n    mov x0, #1\n    mov x16, #1\n    svc #0x80\n"
L_kuro_data_219: .asciz "_kuro_print_int:\n    sub sp, sp, #32\n    add x3, sp, #31\n    mov w4, #10\n    strb w4, [x3]\n    mov x2, #1\n    mov x5, #10\n    mov x6, #0\n    cmp x0, #0\n    b.ge L_kuro_digits_straight\n    neg x0, x0\n    mov x6, #1\nL_kuro_digits_straight:\n    udiv x7, x0, x5\n    msub x8, x7, x5, x0\n    add x8, x8, #48\n    sub x3, x3, #1\n    strb w8, [x3]\n    add x2, x2, #1\n    mov x0, x7\n    cbnz x0, L_kuro_digits_straight\n    cbz x6, L_kuro_write_straight\n    sub x3, x3, #1\n    mov w8, #45\n    strb w8, [x3]\n    add x2, x2, #1\nL_kuro_write_straight:\n    mov x0, #1\n    mov x1, x3\n    mov x16, #4\n    svc #0x80\n    add sp, sp, #32\n    ret\n"
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
.zerofill __DATA,__bss,_kuro_collection_len_0,8,3
.zerofill __DATA,__bss,_kuro_collection_len_1,8,3
.zerofill __DATA,__bss,_kuro_collection_len_2,8,3
.zerofill __DATA,__bss,_kuro_collection_len_3,8,3
.zerofill __DATA,__bss,_kuro_collection_len_4,8,3
.zerofill __DATA,__bss,_kuro_collection_len_5,8,3
.zerofill __DATA,__bss,_kuro_collection_len_6,8,3
.zerofill __DATA,__bss,_kuro_collection_len_7,8,3
.zerofill __DATA,__bss,_kuro_collection_len_8,8,3
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
.zerofill __DATA,__bss,_kuro_char_34,2,1
.zerofill __DATA,__bss,_kuro_char_1,2,1
.zerofill __DATA,__bss,_kuro_char_2,2,1
.zerofill __DATA,__bss,_kuro_char_3,2,1
.zerofill __DATA,__bss,_kuro_char_4,2,1
.zerofill __DATA,__bss,_kuro_char_heap,2097152,4
.zerofill __DATA,__bss,_kuro_char_heap_cursor,8,3
.zerofill __DATA,__bss,_kuro_int_buffer,32,3
.zerofill __DATA,__bss,_kuro_input_buffer,1048576,4
