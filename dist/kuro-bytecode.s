.section __TEXT,__text
.globl _main
.p2align 2
_main:
    stp x29, x30, [sp, #-16]!
    stp x19, x20, [sp, #-16]!
    mov x29, sp
    mov x15, #4624
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
    str x0, [sp, #1064]
    ldr x0, [sp, #1064]
    adrp x2, _kuro_global_20@PAGE
    add x2, x2, _kuro_global_20@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_1@PAGE
    add x0, x0, L_kuro_data_1@PAGEOFF
    str x0, [sp, #1072]
    ldr x0, [sp, #1072]
    adrp x2, _kuro_global_18@PAGE
    add x2, x2, _kuro_global_18@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #1960]
    ldr x0, [sp, #1960]
    adrp x2, _kuro_global_19@PAGE
    add x2, x2, _kuro_global_19@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2848]
    ldr x0, [sp, #2848]
    adrp x2, _kuro_global_14@PAGE
    add x2, x2, _kuro_global_14@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3736]
    ldr x0, [sp, #3736]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4144]
    ldr x0, [sp, #4144]
    adrp x2, _kuro_global_26@PAGE
    add x2, x2, _kuro_global_26@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_2@PAGE
    add x0, x0, L_kuro_data_2@PAGEOFF
    str x0, [sp, #4232]
    ldr x0, [sp, #4232]
    adrp x2, _kuro_global_9@PAGE
    add x2, x2, _kuro_global_9@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_3@PAGE
    add x0, x0, L_kuro_data_3@PAGEOFF
    str x0, [sp, #4320]
    ldr x0, [sp, #4320]
    adrp x2, _kuro_global_15@PAGE
    add x2, x2, _kuro_global_15@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4408]
    ldr x0, [sp, #4408]
    adrp x2, _kuro_global_22@PAGE
    add x2, x2, _kuro_global_22@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_4@PAGE
    add x0, x0, L_kuro_data_4@PAGEOFF
    str x0, [sp, #4496]
    ldr x0, [sp, #4496]
    adrp x2, _kuro_global_64@PAGE
    add x2, x2, _kuro_global_64@PAGEOFF
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
    str x0, [sp, #1080]
    ldr x0, [sp, #1080]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1168]
    ldr x0, [sp, #1168]
    adrp x2, _kuro_global_17@PAGE
    add x2, x2, _kuro_global_17@PAGEOFF
    str x0, [x2]
L_kuro_while_start0:
    adrp x0, _kuro_global_14@PAGE
    add x0, x0, _kuro_global_14@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1256]
    adrp x0, _kuro_global_17@PAGE
    add x0, x0, _kuro_global_17@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1344]
    ldr x0, [sp, #1256]
    ldr x1, [sp, #1344]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #1432]
    ldr x0, [sp, #1432]
    cbz w0, L_kuro_while_end1
    adrp x0, _kuro_global_14@PAGE
    add x0, x0, _kuro_global_14@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1520]
    adrp x2, _kuro_global_25@PAGE
    add x2, x2, _kuro_global_25@PAGEOFF
    ldr x2, [x2]
    ldr x1, [sp, #1520]
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
    str x0, [sp, #1608]
    ldr x0, [sp, #1608]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1696]
    ldr x0, [sp, #1696]
    adrp x2, _kuro_global_2@PAGE
    add x2, x2, _kuro_global_2@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_22@PAGE
    add x0, x0, _kuro_global_22@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1784]
    mov x0, #1
    str x0, [sp, #1872]
    ldr x0, [sp, #1784]
    ldr x1, [sp, #1872]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1968]
    ldr x0, [sp, #1968]
    cbz w0, L_kuro_else3
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2056]
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2144]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2232]
    ldr x0, [sp, #2232]
    ldr x1, [sp, #2056]
    bl _strcpy
    ldr x0, [sp, #2232]
    ldr x1, [sp, #2144]
    bl _strcat
    ldr x0, [sp, #2232]
    adrp x2, _kuro_global_64@PAGE
    add x2, x2, _kuro_global_64@PAGEOFF
    str x0, [x2]
    b L_kuro_endif4
L_kuro_else3:
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2320]
    adrp x0, L_kuro_data_5@PAGE
    add x0, x0, L_kuro_data_5@PAGEOFF
    str x0, [sp, #2408]
    ldr x0, [sp, #2320]
    ldr x1, [sp, #2408]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2496]
    ldr x0, [sp, #2496]
    cbz w0, L_kuro_else5
    bl _kuro_fn_ArtifactCommitLine
    str x0, [sp, #2584]
    ldr x0, [sp, #2584]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_endif6
L_kuro_else5:
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2672]
    adrp x0, L_kuro_data_6@PAGE
    add x0, x0, L_kuro_data_6@PAGEOFF
    str x0, [sp, #2760]
    ldr x0, [sp, #2672]
    ldr x1, [sp, #2760]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2856]
    ldr x0, [sp, #2856]
    cbz w0, L_kuro_else7
    mov x0, #1
    str x0, [sp, #2944]
    ldr x0, [sp, #2944]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif8
L_kuro_else7:
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3032]
    adrp x0, _kuro_global_2@PAGE
    add x0, x0, _kuro_global_2@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3120]
    mov x0, #4096
    bl _malloc
    str x0, [sp, #3208]
    ldr x0, [sp, #3208]
    ldr x1, [sp, #3032]
    bl _strcpy
    ldr x0, [sp, #3208]
    ldr x1, [sp, #3120]
    bl _strcat
    ldr x0, [sp, #3208]
    adrp x2, _kuro_global_18@PAGE
    add x2, x2, _kuro_global_18@PAGEOFF
    str x0, [x2]
L_kuro_endif8:
L_kuro_endif6:
L_kuro_endif4:
    mov x0, #1
    str x0, [sp, #3296]
    adrp x0, _kuro_global_14@PAGE
    add x0, x0, _kuro_global_14@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #3296]
    add x0, x0, x1
    adrp x2, _kuro_global_14@PAGE
    add x2, x2, _kuro_global_14@PAGEOFF
    str x0, [x2]
    b L_kuro_while_start0
L_kuro_while_end1:
    adrp x0, _kuro_global_22@PAGE
    add x0, x0, _kuro_global_22@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3384]
    mov x0, #0
    str x0, [sp, #3472]
    ldr x0, [sp, #3384]
    ldr x1, [sp, #3472]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3560]
    adrp x0, _kuro_global_18@PAGE
    add x0, x0, _kuro_global_18@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3648]
    adrp x0, L_kuro_data_7@PAGE
    add x0, x0, L_kuro_data_7@PAGEOFF
    str x0, [sp, #3744]
    ldr x0, [sp, #3648]
    ldr x1, [sp, #3744]
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    str x0, [sp, #3832]
    ldr x0, [sp, #3560]
    ldr x1, [sp, #3832]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #3920]
    ldr x0, [sp, #3920]
    cbz w0, L_kuro_else9
    bl _kuro_fn_ArtifactCommitLine
    str x0, [sp, #4008]
    ldr x0, [sp, #4008]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_endif10
L_kuro_else9:
L_kuro_endif10:
    adrp x0, _kuro_global_19@PAGE
    add x0, x0, _kuro_global_19@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4096]
    mov x0, #2
    str x0, [sp, #4104]
    ldr x0, [sp, #4096]
    ldr x1, [sp, #4104]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4112]
    ldr x0, [sp, #4112]
    cbz w0, L_kuro_else11
    mov x0, #1
    str x0, [sp, #4120]
    ldr x0, [sp, #4120]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif12
L_kuro_else11:
L_kuro_endif12:
    mov x0, #0
    str x0, [sp, #4128]
    ldr x0, [sp, #4128]
    adrp x2, _kuro_global_24@PAGE
    add x2, x2, _kuro_global_24@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4136]
    ldr x0, [sp, #4136]
    adrp x2, _kuro_global_13@PAGE
    add x2, x2, _kuro_global_13@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4152]
    ldr x0, [sp, #4152]
    adrp x2, _kuro_global_23@PAGE
    add x2, x2, _kuro_global_23@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4160]
    ldr x0, [sp, #4160]
    adrp x2, _kuro_global_27@PAGE
    add x2, x2, _kuro_global_27@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4168]
    ldr x0, [sp, #4168]
    adrp x2, _kuro_global_12@PAGE
    add x2, x2, _kuro_global_12@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4176]
    ldr x0, [sp, #4176]
    adrp x2, _kuro_global_1@PAGE
    add x2, x2, _kuro_global_1@PAGEOFF
    str x0, [x2]
L_kuro_while_start13:
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4184]
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4192]
    ldr x0, [sp, #4184]
    ldr x1, [sp, #4192]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4200]
    adrp x0, _kuro_global_11@PAGE
    add x0, x0, _kuro_global_11@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4208]
    mov x0, #0
    str x0, [sp, #4216]
    ldr x0, [sp, #4208]
    ldr x1, [sp, #4216]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #4224]
    ldr x0, [sp, #4200]
    ldr x1, [sp, #4224]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #4240]
    ldr x0, [sp, #4240]
    cbz w0, L_kuro_while_end14
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4248]
    ldr x1, [sp, #4248]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #4256]
    ldr x0, [sp, #4256]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4264]
    ldr x0, [sp, #4264]
    adrp x2, _kuro_global_21@PAGE
    add x2, x2, _kuro_global_21@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4272]
    ldr x0, [sp, #4272]
    adrp x2, _kuro_global_0@PAGE
    add x2, x2, _kuro_global_0@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4280]
    ldr x0, [sp, #4280]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4288]
    adrp x0, L_kuro_data_8@PAGE
    add x0, x0, L_kuro_data_8@PAGEOFF
    str x0, [sp, #4296]
    ldr x0, [sp, #4288]
    ldr x1, [sp, #4296]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4304]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4312]
    adrp x0, L_kuro_data_9@PAGE
    add x0, x0, L_kuro_data_9@PAGEOFF
    str x0, [sp, #4328]
    ldr x0, [sp, #4312]
    ldr x1, [sp, #4328]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4336]
    ldr x0, [sp, #4304]
    ldr x1, [sp, #4336]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4344]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4352]
    adrp x0, L_kuro_data_10@PAGE
    add x0, x0, L_kuro_data_10@PAGEOFF
    str x0, [sp, #4360]
    ldr x0, [sp, #4352]
    ldr x1, [sp, #4360]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4368]
    ldr x0, [sp, #4344]
    ldr x1, [sp, #4368]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4376]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4384]
    adrp x0, L_kuro_data_11@PAGE
    add x0, x0, L_kuro_data_11@PAGEOFF
    str x0, [sp, #4392]
    ldr x0, [sp, #4384]
    ldr x1, [sp, #4392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4400]
    ldr x0, [sp, #4376]
    ldr x1, [sp, #4400]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4416]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4424]
    adrp x0, L_kuro_data_12@PAGE
    add x0, x0, L_kuro_data_12@PAGEOFF
    str x0, [sp, #4432]
    ldr x0, [sp, #4424]
    ldr x1, [sp, #4432]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4440]
    ldr x0, [sp, #4416]
    ldr x1, [sp, #4440]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4448]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4456]
    adrp x0, L_kuro_data_13@PAGE
    add x0, x0, L_kuro_data_13@PAGEOFF
    str x0, [sp, #4464]
    ldr x0, [sp, #4456]
    ldr x1, [sp, #4464]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4472]
    ldr x0, [sp, #4448]
    ldr x1, [sp, #4472]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4480]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4488]
    adrp x0, L_kuro_data_14@PAGE
    add x0, x0, L_kuro_data_14@PAGEOFF
    str x0, [sp, #4504]
    ldr x0, [sp, #4488]
    ldr x1, [sp, #4504]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4512]
    ldr x0, [sp, #4480]
    ldr x1, [sp, #4512]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4520]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4528]
    adrp x0, L_kuro_data_15@PAGE
    add x0, x0, L_kuro_data_15@PAGEOFF
    str x0, [sp, #4536]
    ldr x0, [sp, #4528]
    ldr x1, [sp, #4536]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4544]
    ldr x0, [sp, #4520]
    ldr x1, [sp, #4544]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #4552]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4560]
    adrp x0, L_kuro_data_16@PAGE
    add x0, x0, L_kuro_data_16@PAGEOFF
    str x0, [sp, #4568]
    ldr x0, [sp, #4560]
    ldr x1, [sp, #4568]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #4576]
    ldr x0, [sp, #4552]
    ldr x1, [sp, #4576]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1088]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1096]
    adrp x0, L_kuro_data_17@PAGE
    add x0, x0, L_kuro_data_17@PAGEOFF
    str x0, [sp, #1104]
    ldr x0, [sp, #1096]
    ldr x1, [sp, #1104]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1112]
    ldr x0, [sp, #1088]
    ldr x1, [sp, #1112]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1120]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1128]
    adrp x0, L_kuro_data_18@PAGE
    add x0, x0, L_kuro_data_18@PAGEOFF
    str x0, [sp, #1136]
    ldr x0, [sp, #1128]
    ldr x1, [sp, #1136]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1144]
    ldr x0, [sp, #1120]
    ldr x1, [sp, #1144]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1152]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1160]
    adrp x0, L_kuro_data_19@PAGE
    add x0, x0, L_kuro_data_19@PAGEOFF
    str x0, [sp, #1176]
    ldr x0, [sp, #1160]
    ldr x1, [sp, #1176]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1184]
    ldr x0, [sp, #1152]
    ldr x1, [sp, #1184]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1192]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1200]
    adrp x0, L_kuro_data_20@PAGE
    add x0, x0, L_kuro_data_20@PAGEOFF
    str x0, [sp, #1208]
    ldr x0, [sp, #1200]
    ldr x1, [sp, #1208]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1216]
    ldr x0, [sp, #1192]
    ldr x1, [sp, #1216]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1224]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1232]
    adrp x0, L_kuro_data_21@PAGE
    add x0, x0, L_kuro_data_21@PAGEOFF
    str x0, [sp, #1240]
    ldr x0, [sp, #1232]
    ldr x1, [sp, #1240]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1248]
    ldr x0, [sp, #1224]
    ldr x1, [sp, #1248]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1264]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1272]
    adrp x0, L_kuro_data_22@PAGE
    add x0, x0, L_kuro_data_22@PAGEOFF
    str x0, [sp, #1280]
    ldr x0, [sp, #1272]
    ldr x1, [sp, #1280]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1288]
    ldr x0, [sp, #1264]
    ldr x1, [sp, #1288]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1296]
    ldr x0, [sp, #1296]
    cbz w0, L_kuro_else16
    mov x0, #1
    str x0, [sp, #1304]
    ldr x0, [sp, #1304]
    adrp x2, _kuro_global_0@PAGE
    add x2, x2, _kuro_global_0@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1312]
    ldr x0, [sp, #1312]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    b L_kuro_endif17
L_kuro_else16:
L_kuro_endif17:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1320]
    adrp x0, L_kuro_data_23@PAGE
    add x0, x0, L_kuro_data_23@PAGEOFF
    str x0, [sp, #1328]
    ldr x0, [sp, #1320]
    ldr x1, [sp, #1328]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1336]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1352]
    adrp x0, L_kuro_data_24@PAGE
    add x0, x0, L_kuro_data_24@PAGEOFF
    str x0, [sp, #1360]
    ldr x0, [sp, #1352]
    ldr x1, [sp, #1360]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1368]
    ldr x0, [sp, #1336]
    ldr x1, [sp, #1368]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1376]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1384]
    adrp x0, L_kuro_data_25@PAGE
    add x0, x0, L_kuro_data_25@PAGEOFF
    str x0, [sp, #1392]
    ldr x0, [sp, #1384]
    ldr x1, [sp, #1392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1400]
    ldr x0, [sp, #1376]
    ldr x1, [sp, #1400]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1408]
    ldr x0, [sp, #1408]
    cbz w0, L_kuro_else18
    mov x0, #2
    str x0, [sp, #1416]
    ldr x0, [sp, #1416]
    adrp x2, _kuro_global_0@PAGE
    add x2, x2, _kuro_global_0@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #1424]
    ldr x0, [sp, #1424]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    b L_kuro_endif19
L_kuro_else18:
L_kuro_endif19:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1440]
    adrp x0, L_kuro_data_26@PAGE
    add x0, x0, L_kuro_data_26@PAGEOFF
    str x0, [sp, #1448]
    ldr x0, [sp, #1440]
    ldr x1, [sp, #1448]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1456]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1464]
    adrp x0, L_kuro_data_27@PAGE
    add x0, x0, L_kuro_data_27@PAGEOFF
    str x0, [sp, #1472]
    ldr x0, [sp, #1464]
    ldr x1, [sp, #1472]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1480]
    ldr x0, [sp, #1456]
    ldr x1, [sp, #1480]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1488]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1496]
    adrp x0, L_kuro_data_28@PAGE
    add x0, x0, L_kuro_data_28@PAGEOFF
    str x0, [sp, #1504]
    ldr x0, [sp, #1496]
    ldr x1, [sp, #1504]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1512]
    ldr x0, [sp, #1488]
    ldr x1, [sp, #1512]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1528]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1536]
    adrp x0, L_kuro_data_29@PAGE
    add x0, x0, L_kuro_data_29@PAGEOFF
    str x0, [sp, #1544]
    ldr x0, [sp, #1536]
    ldr x1, [sp, #1544]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1552]
    ldr x0, [sp, #1528]
    ldr x1, [sp, #1552]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1560]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1568]
    adrp x0, L_kuro_data_30@PAGE
    add x0, x0, L_kuro_data_30@PAGEOFF
    str x0, [sp, #1576]
    ldr x0, [sp, #1568]
    ldr x1, [sp, #1576]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1584]
    ldr x0, [sp, #1560]
    ldr x1, [sp, #1584]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1592]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1600]
    adrp x0, L_kuro_data_31@PAGE
    add x0, x0, L_kuro_data_31@PAGEOFF
    str x0, [sp, #1616]
    ldr x0, [sp, #1600]
    ldr x1, [sp, #1616]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1624]
    ldr x0, [sp, #1592]
    ldr x1, [sp, #1624]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1632]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1640]
    adrp x0, L_kuro_data_32@PAGE
    add x0, x0, L_kuro_data_32@PAGEOFF
    str x0, [sp, #1648]
    ldr x0, [sp, #1640]
    ldr x1, [sp, #1648]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1656]
    ldr x0, [sp, #1632]
    ldr x1, [sp, #1656]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1664]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1672]
    adrp x0, L_kuro_data_33@PAGE
    add x0, x0, L_kuro_data_33@PAGEOFF
    str x0, [sp, #1680]
    ldr x0, [sp, #1672]
    ldr x1, [sp, #1680]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1688]
    ldr x0, [sp, #1664]
    ldr x1, [sp, #1688]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1704]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1712]
    adrp x0, L_kuro_data_34@PAGE
    add x0, x0, L_kuro_data_34@PAGEOFF
    str x0, [sp, #1720]
    ldr x0, [sp, #1712]
    ldr x1, [sp, #1720]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1728]
    ldr x0, [sp, #1704]
    ldr x1, [sp, #1728]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1736]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1744]
    adrp x0, L_kuro_data_35@PAGE
    add x0, x0, L_kuro_data_35@PAGEOFF
    str x0, [sp, #1752]
    ldr x0, [sp, #1744]
    ldr x1, [sp, #1752]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1760]
    ldr x0, [sp, #1736]
    ldr x1, [sp, #1760]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1768]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1776]
    adrp x0, L_kuro_data_36@PAGE
    add x0, x0, L_kuro_data_36@PAGEOFF
    str x0, [sp, #1792]
    ldr x0, [sp, #1776]
    ldr x1, [sp, #1792]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1800]
    ldr x0, [sp, #1768]
    ldr x1, [sp, #1800]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1808]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1816]
    adrp x0, L_kuro_data_37@PAGE
    add x0, x0, L_kuro_data_37@PAGEOFF
    str x0, [sp, #1824]
    ldr x0, [sp, #1816]
    ldr x1, [sp, #1824]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1832]
    ldr x0, [sp, #1808]
    ldr x1, [sp, #1832]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #1840]
    ldr x0, [sp, #1840]
    cbz w0, L_kuro_else20
    mov x0, #1
    str x0, [sp, #1848]
    ldr x0, [sp, #1848]
    adrp x2, _kuro_global_16@PAGE
    add x2, x2, _kuro_global_16@PAGEOFF
    str x0, [x2]
    b L_kuro_endif21
L_kuro_else20:
L_kuro_endif21:
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1856]
    adrp x0, L_kuro_data_38@PAGE
    add x0, x0, L_kuro_data_38@PAGEOFF
    str x0, [sp, #1864]
    ldr x0, [sp, #1856]
    ldr x1, [sp, #1864]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1880]
    ldr x0, [sp, #1880]
    cbz w0, L_kuro_else22
    mov x0, #1
    str x0, [sp, #1888]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #1888]
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
    str x0, [sp, #1896]
    adrp x0, L_kuro_data_39@PAGE
    add x0, x0, L_kuro_data_39@PAGEOFF
    str x0, [sp, #1904]
    ldr x0, [sp, #1896]
    ldr x1, [sp, #1904]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1912]
    ldr x0, [sp, #1912]
    cbz w0, L_kuro_else24
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1920]
    mov x0, #0
    str x0, [sp, #1928]
    ldr x0, [sp, #1920]
    ldr x1, [sp, #1928]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #1936]
    ldr x0, [sp, #1936]
    cbz w0, L_kuro_else26
    mov x0, #1
    str x0, [sp, #1944]
    ldr x0, [sp, #1944]
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
    str x0, [sp, #1952]
    adrp x0, L_kuro_data_40@PAGE
    add x0, x0, L_kuro_data_40@PAGEOFF
    str x0, [sp, #1976]
    ldr x0, [sp, #1952]
    ldr x1, [sp, #1976]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #1984]
    ldr x0, [sp, #1984]
    cbz w0, L_kuro_else28
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1992]
    mov x0, #0
    str x0, [sp, #2000]
    ldr x0, [sp, #1992]
    ldr x1, [sp, #2000]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2008]
    ldr x0, [sp, #2008]
    cbz w0, L_kuro_else30
    mov x0, #1
    str x0, [sp, #2016]
    ldr x0, [sp, #2016]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif31
L_kuro_else30:
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2024]
    mov x0, #1
    str x0, [sp, #2032]
    ldr x0, [sp, #2024]
    ldr x1, [sp, #2032]
    sub x0, x0, x1
    str x0, [sp, #2040]
    ldr x0, [sp, #2040]
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
    str x0, [sp, #2048]
    adrp x0, L_kuro_data_41@PAGE
    add x0, x0, L_kuro_data_41@PAGEOFF
    str x0, [sp, #2064]
    ldr x0, [sp, #2048]
    ldr x1, [sp, #2064]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2072]
    ldr x0, [sp, #2072]
    cbz w0, L_kuro_else32
    mov x0, #1
    str x0, [sp, #2080]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2080]
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
    str x0, [sp, #2088]
    adrp x0, L_kuro_data_42@PAGE
    add x0, x0, L_kuro_data_42@PAGEOFF
    str x0, [sp, #2096]
    ldr x0, [sp, #2088]
    ldr x1, [sp, #2096]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2104]
    ldr x0, [sp, #2104]
    cbz w0, L_kuro_else34
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2112]
    mov x0, #0
    str x0, [sp, #2120]
    ldr x0, [sp, #2112]
    ldr x1, [sp, #2120]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2128]
    ldr x0, [sp, #2128]
    cbz w0, L_kuro_else36
    mov x0, #1
    str x0, [sp, #2136]
    ldr x0, [sp, #2136]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif37
L_kuro_else36:
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2152]
    mov x0, #1
    str x0, [sp, #2160]
    ldr x0, [sp, #2152]
    ldr x1, [sp, #2160]
    sub x0, x0, x1
    str x0, [sp, #2168]
    ldr x0, [sp, #2168]
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
    str x0, [sp, #2176]
    adrp x0, L_kuro_data_43@PAGE
    add x0, x0, L_kuro_data_43@PAGEOFF
    str x0, [sp, #2184]
    ldr x0, [sp, #2176]
    ldr x1, [sp, #2184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2192]
    ldr x0, [sp, #2192]
    cbz w0, L_kuro_else38
    mov x0, #1
    str x0, [sp, #2200]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2200]
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
    str x0, [sp, #2208]
    adrp x0, L_kuro_data_44@PAGE
    add x0, x0, L_kuro_data_44@PAGEOFF
    str x0, [sp, #2216]
    ldr x0, [sp, #2208]
    ldr x1, [sp, #2216]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2224]
    ldr x0, [sp, #2224]
    cbz w0, L_kuro_else40
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2240]
    mov x0, #0
    str x0, [sp, #2248]
    ldr x0, [sp, #2240]
    ldr x1, [sp, #2248]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2256]
    ldr x0, [sp, #2256]
    cbz w0, L_kuro_else42
    mov x0, #1
    str x0, [sp, #2264]
    ldr x0, [sp, #2264]
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
    str x0, [sp, #2272]
    adrp x0, L_kuro_data_45@PAGE
    add x0, x0, L_kuro_data_45@PAGEOFF
    str x0, [sp, #2280]
    ldr x0, [sp, #2272]
    ldr x1, [sp, #2280]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2288]
    ldr x0, [sp, #2288]
    cbz w0, L_kuro_else44
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2296]
    mov x0, #0
    str x0, [sp, #2304]
    ldr x0, [sp, #2296]
    ldr x1, [sp, #2304]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2312]
    ldr x0, [sp, #2312]
    cbz w0, L_kuro_else46
    mov x0, #1
    str x0, [sp, #2328]
    ldr x0, [sp, #2328]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif47
L_kuro_else46:
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2336]
    mov x0, #1
    str x0, [sp, #2344]
    ldr x0, [sp, #2336]
    ldr x1, [sp, #2344]
    sub x0, x0, x1
    str x0, [sp, #2352]
    ldr x0, [sp, #2352]
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
    str x0, [sp, #2360]
    adrp x0, L_kuro_data_46@PAGE
    add x0, x0, L_kuro_data_46@PAGEOFF
    str x0, [sp, #2368]
    ldr x0, [sp, #2360]
    ldr x1, [sp, #2368]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2376]
    ldr x0, [sp, #2376]
    cbz w0, L_kuro_else48
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2384]
    mov x0, #0
    str x0, [sp, #2392]
    ldr x0, [sp, #2384]
    ldr x1, [sp, #2392]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2400]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2416]
    mov x0, #0
    str x0, [sp, #2424]
    ldr x0, [sp, #2416]
    ldr x1, [sp, #2424]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2432]
    ldr x0, [sp, #2400]
    ldr x1, [sp, #2432]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2440]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2448]
    mov x0, #0
    str x0, [sp, #2456]
    ldr x0, [sp, #2448]
    ldr x1, [sp, #2456]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2464]
    ldr x0, [sp, #2440]
    ldr x1, [sp, #2464]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2472]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2480]
    mov x0, #0
    str x0, [sp, #2488]
    ldr x0, [sp, #2480]
    ldr x1, [sp, #2488]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2504]
    ldr x0, [sp, #2472]
    ldr x1, [sp, #2504]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2512]
    ldr x0, [sp, #2512]
    cbz w0, L_kuro_else50
    mov x0, #1
    str x0, [sp, #2520]
    ldr x0, [sp, #2520]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif51
L_kuro_else50:
    mov x0, #1
    str x0, [sp, #2528]
    ldr x0, [sp, #2528]
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
    str x0, [sp, #2536]
    adrp x0, L_kuro_data_47@PAGE
    add x0, x0, L_kuro_data_47@PAGEOFF
    str x0, [sp, #2544]
    ldr x0, [sp, #2536]
    ldr x1, [sp, #2544]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2552]
    adrp x0, _kuro_global_21@PAGE
    add x0, x0, _kuro_global_21@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2560]
    adrp x0, L_kuro_data_48@PAGE
    add x0, x0, L_kuro_data_48@PAGEOFF
    str x0, [sp, #2568]
    ldr x0, [sp, #2560]
    ldr x1, [sp, #2568]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2576]
    ldr x0, [sp, #2552]
    ldr x1, [sp, #2576]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2592]
    ldr x0, [sp, #2592]
    cbz w0, L_kuro_else52
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2600]
    mov x0, #0
    str x0, [sp, #2608]
    ldr x0, [sp, #2600]
    ldr x1, [sp, #2608]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2616]
    ldr x0, [sp, #2616]
    cbz w0, L_kuro_else54
    mov x0, #1
    str x0, [sp, #2624]
    ldr x0, [sp, #2624]
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
    str x0, [sp, #2632]
    adrp x0, L_kuro_data_49@PAGE
    add x0, x0, L_kuro_data_49@PAGEOFF
    str x0, [sp, #2640]
    ldr x0, [sp, #2632]
    ldr x1, [sp, #2640]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2648]
    ldr x0, [sp, #2648]
    cbz w0, L_kuro_else56
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2656]
    mov x0, #1
    str x0, [sp, #2664]
    ldr x0, [sp, #2656]
    ldr x1, [sp, #2664]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2680]
    adrp x0, _kuro_global_13@PAGE
    add x0, x0, _kuro_global_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2688]
    mov x0, #0
    str x0, [sp, #2696]
    ldr x0, [sp, #2688]
    ldr x1, [sp, #2696]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2704]
    ldr x0, [sp, #2680]
    ldr x1, [sp, #2704]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2712]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2720]
    mov x0, #0
    str x0, [sp, #2728]
    ldr x0, [sp, #2720]
    ldr x1, [sp, #2728]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2736]
    ldr x0, [sp, #2712]
    ldr x1, [sp, #2736]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2744]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2752]
    mov x0, #0
    str x0, [sp, #2768]
    ldr x0, [sp, #2752]
    ldr x1, [sp, #2768]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #2776]
    ldr x0, [sp, #2744]
    ldr x1, [sp, #2776]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2784]
    ldr x0, [sp, #2784]
    cbz w0, L_kuro_else58
    mov x0, #1
    str x0, [sp, #2792]
    ldr x0, [sp, #2792]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif59
L_kuro_else58:
    mov x0, #0
    str x0, [sp, #2800]
    ldr x0, [sp, #2800]
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
    str x0, [sp, #2808]
    adrp x0, L_kuro_data_50@PAGE
    add x0, x0, L_kuro_data_50@PAGEOFF
    str x0, [sp, #2816]
    ldr x0, [sp, #2808]
    ldr x1, [sp, #2816]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2824]
    ldr x0, [sp, #2824]
    cbz w0, L_kuro_else60
    mov x0, #1
    str x0, [sp, #2832]
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #2832]
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
    str x0, [sp, #2840]
    adrp x0, L_kuro_data_51@PAGE
    add x0, x0, L_kuro_data_51@PAGEOFF
    str x0, [sp, #2864]
    ldr x0, [sp, #2840]
    ldr x1, [sp, #2864]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #2872]
    ldr x0, [sp, #2872]
    cbz w0, L_kuro_else62
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2880]
    mov x0, #0
    str x0, [sp, #2888]
    ldr x0, [sp, #2880]
    ldr x1, [sp, #2888]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #2896]
    ldr x0, [sp, #2896]
    cbz w0, L_kuro_else64
    mov x0, #1
    str x0, [sp, #2904]
    ldr x0, [sp, #2904]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif65
L_kuro_else64:
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2912]
    mov x0, #1
    str x0, [sp, #2920]
    ldr x0, [sp, #2912]
    ldr x1, [sp, #2920]
    sub x0, x0, x1
    str x0, [sp, #2928]
    ldr x0, [sp, #2928]
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
    str x0, [sp, #2936]
    mov x0, #1
    str x0, [sp, #2952]
    ldr x0, [sp, #2936]
    ldr x1, [sp, #2952]
    add x0, x0, x1
    str x0, [sp, #2960]
    adrp x0, _kuro_global_0@PAGE
    add x0, x0, _kuro_global_0@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2968]
    ldr x0, [sp, #2960]
    ldr x1, [sp, #2968]
    add x0, x0, x1
    str x0, [sp, #2976]
    ldr x0, [sp, #2976]
    adrp x2, _kuro_global_24@PAGE
    add x2, x2, _kuro_global_24@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_16@PAGE
    add x0, x0, _kuro_global_16@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2984]
    mov x0, #0
    str x0, [sp, #2992]
    ldr x0, [sp, #2984]
    ldr x1, [sp, #2992]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3000]
    adrp x0, _kuro_global_24@PAGE
    add x0, x0, _kuro_global_24@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3008]
    adrp x0, _kuro_global_26@PAGE
    add x0, x0, _kuro_global_26@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3016]
    ldr x0, [sp, #3008]
    ldr x1, [sp, #3016]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #3024]
    ldr x0, [sp, #3000]
    ldr x1, [sp, #3024]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3040]
    ldr x0, [sp, #3040]
    cbz w0, L_kuro_else66
    mov x0, #1
    str x0, [sp, #3048]
    ldr x0, [sp, #3048]
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
    str x0, [sp, #3056]
    mov x0, #0
    str x0, [sp, #3064]
    ldr x0, [sp, #3056]
    ldr x1, [sp, #3064]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #3072]
    adrp x0, _kuro_global_23@PAGE
    add x0, x0, _kuro_global_23@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3080]
    mov x0, #0
    str x0, [sp, #3088]
    ldr x0, [sp, #3080]
    ldr x1, [sp, #3088]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #3096]
    ldr x0, [sp, #3072]
    ldr x1, [sp, #3096]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3104]
    adrp x0, _kuro_global_27@PAGE
    add x0, x0, _kuro_global_27@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3112]
    mov x0, #0
    str x0, [sp, #3128]
    ldr x0, [sp, #3112]
    ldr x1, [sp, #3128]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #3136]
    ldr x0, [sp, #3104]
    ldr x1, [sp, #3136]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3144]
    adrp x0, _kuro_global_12@PAGE
    add x0, x0, _kuro_global_12@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3152]
    mov x0, #0
    str x0, [sp, #3160]
    ldr x0, [sp, #3152]
    ldr x1, [sp, #3160]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #3168]
    ldr x0, [sp, #3144]
    ldr x1, [sp, #3168]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3176]
    adrp x0, _kuro_global_1@PAGE
    add x0, x0, _kuro_global_1@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3184]
    mov x0, #0
    str x0, [sp, #3192]
    ldr x0, [sp, #3184]
    ldr x1, [sp, #3192]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #3200]
    ldr x0, [sp, #3176]
    ldr x1, [sp, #3200]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3216]
    ldr x0, [sp, #3216]
    cbz w0, L_kuro_else68
    mov x0, #1
    str x0, [sp, #3224]
    ldr x0, [sp, #3224]
    adrp x2, _kuro_global_11@PAGE
    add x2, x2, _kuro_global_11@PAGEOFF
    str x0, [x2]
    b L_kuro_endif69
L_kuro_else68:
L_kuro_endif69:
    adrp x0, _kuro_global_11@PAGE
    add x0, x0, _kuro_global_11@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3232]
    mov x0, #1
    str x0, [sp, #3240]
    ldr x0, [sp, #3232]
    ldr x1, [sp, #3240]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #3248]
    ldr x0, [sp, #3248]
    cbz w0, L_kuro_else70
    adrp x0, L_kuro_data_52@PAGE
    add x0, x0, L_kuro_data_52@PAGEOFF
    str x0, [sp, #3256]
    adrp x0, L_kuro_data_53@PAGE
    add x0, x0, L_kuro_data_53@PAGEOFF
    str x0, [sp, #3264]
    ldr x0, [sp, #3256]
    adrp x1, _kuro_collection_0@PAGE
    add x1, x1, _kuro_collection_0@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3264]
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
    adrp x0, L_kuro_data_54@PAGE
    add x0, x0, L_kuro_data_54@PAGEOFF
    str x0, [sp, #3272]
    adrp x0, L_kuro_data_55@PAGE
    add x0, x0, L_kuro_data_55@PAGEOFF
    str x0, [sp, #3280]
    ldr x0, [sp, #3272]
    adrp x1, _kuro_collection_9@PAGE
    add x1, x1, _kuro_collection_9@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3280]
    adrp x1, _kuro_collection_9@PAGE
    add x1, x1, _kuro_collection_9@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_56@PAGE
    add x0, x0, L_kuro_data_56@PAGEOFF
    str x0, [sp, #3288]
    adrp x0, L_kuro_data_57@PAGE
    add x0, x0, L_kuro_data_57@PAGEOFF
    str x0, [sp, #3304]
    ldr x0, [sp, #3288]
    adrp x1, _kuro_collection_15@PAGE
    add x1, x1, _kuro_collection_15@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3304]
    adrp x1, _kuro_collection_15@PAGE
    add x1, x1, _kuro_collection_15@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_15@PAGE
    add x2, x2, _kuro_collection_len_15@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3312]
    ldr x0, [sp, #3312]
    adrp x2, _kuro_global_78@PAGE
    add x2, x2, _kuro_global_78@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_58@PAGE
    add x0, x0, L_kuro_data_58@PAGEOFF
    str x0, [sp, #3320]
    adrp x0, L_kuro_data_59@PAGE
    add x0, x0, L_kuro_data_59@PAGEOFF
    str x0, [sp, #3328]
    ldr x0, [sp, #3320]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3328]
    adrp x1, _kuro_collection_2@PAGE
    add x1, x1, _kuro_collection_2@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_2@PAGE
    add x2, x2, _kuro_collection_len_2@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3336]
    ldr x0, [sp, #3336]
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_60@PAGE
    add x0, x0, L_kuro_data_60@PAGEOFF
    str x0, [sp, #3344]
    adrp x0, L_kuro_data_61@PAGE
    add x0, x0, L_kuro_data_61@PAGEOFF
    str x0, [sp, #3352]
    ldr x0, [sp, #3344]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3352]
    adrp x1, _kuro_collection_3@PAGE
    add x1, x1, _kuro_collection_3@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_3@PAGE
    add x2, x2, _kuro_collection_len_3@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_62@PAGE
    add x0, x0, L_kuro_data_62@PAGEOFF
    str x0, [sp, #3360]
    adrp x0, L_kuro_data_63@PAGE
    add x0, x0, L_kuro_data_63@PAGEOFF
    str x0, [sp, #3368]
    ldr x0, [sp, #3360]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3368]
    adrp x1, _kuro_collection_1@PAGE
    add x1, x1, _kuro_collection_1@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_1@PAGE
    add x2, x2, _kuro_collection_len_1@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3376]
    ldr x0, [sp, #3376]
    adrp x2, _kuro_global_37@PAGE
    add x2, x2, _kuro_global_37@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3392]
    ldr x0, [sp, #3392]
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3400]
    ldr x0, [sp, #3400]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3408]
    ldr x0, [sp, #3408]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3416]
    ldr x0, [sp, #3416]
    adrp x2, _kuro_global_139@PAGE
    add x2, x2, _kuro_global_139@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3424]
    ldr x0, [sp, #3424]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3432]
    ldr x0, [sp, #3432]
    adrp x2, _kuro_global_34@PAGE
    add x2, x2, _kuro_global_34@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_64@PAGE
    add x0, x0, L_kuro_data_64@PAGEOFF
    str x0, [sp, #3440]
    ldr x0, [sp, #3440]
    adrp x2, _kuro_global_33@PAGE
    add x2, x2, _kuro_global_33@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3448]
    ldr x0, [sp, #3448]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3456]
    ldr x0, [sp, #3456]
    adrp x2, _kuro_global_90@PAGE
    add x2, x2, _kuro_global_90@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3464]
    ldr x0, [sp, #3464]
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3480]
    ldr x0, [sp, #3480]
    adrp x2, _kuro_global_71@PAGE
    add x2, x2, _kuro_global_71@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #3488]
    ldr x0, [sp, #3488]
    adrp x2, _kuro_global_65@PAGE
    add x2, x2, _kuro_global_65@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_65@PAGE
    add x0, x0, L_kuro_data_65@PAGEOFF
    str x0, [sp, #3496]
    adrp x0, L_kuro_data_66@PAGE
    add x0, x0, L_kuro_data_66@PAGEOFF
    str x0, [sp, #3504]
    ldr x0, [sp, #3496]
    adrp x1, _kuro_collection_11@PAGE
    add x1, x1, _kuro_collection_11@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3504]
    adrp x1, _kuro_collection_11@PAGE
    add x1, x1, _kuro_collection_11@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_11@PAGE
    add x2, x2, _kuro_collection_len_11@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3512]
    ldr x0, [sp, #3512]
    adrp x2, _kuro_global_81@PAGE
    add x2, x2, _kuro_global_81@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3520]
    ldr x0, [sp, #3520]
    adrp x2, _kuro_global_55@PAGE
    add x2, x2, _kuro_global_55@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3528]
    ldr x0, [sp, #3528]
    adrp x2, _kuro_global_56@PAGE
    add x2, x2, _kuro_global_56@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_67@PAGE
    add x0, x0, L_kuro_data_67@PAGEOFF
    str x0, [sp, #3536]
    adrp x0, L_kuro_data_68@PAGE
    add x0, x0, L_kuro_data_68@PAGEOFF
    str x0, [sp, #3544]
    ldr x0, [sp, #3536]
    adrp x1, _kuro_collection_5@PAGE
    add x1, x1, _kuro_collection_5@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3544]
    adrp x1, _kuro_collection_5@PAGE
    add x1, x1, _kuro_collection_5@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_5@PAGE
    add x2, x2, _kuro_collection_len_5@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_69@PAGE
    add x0, x0, L_kuro_data_69@PAGEOFF
    str x0, [sp, #3552]
    adrp x0, L_kuro_data_70@PAGE
    add x0, x0, L_kuro_data_70@PAGEOFF
    str x0, [sp, #3568]
    ldr x0, [sp, #3552]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3568]
    adrp x1, _kuro_collection_8@PAGE
    add x1, x1, _kuro_collection_8@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3576]
    mov x0, #0
    str x0, [sp, #3584]
    ldr x0, [sp, #3576]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3584]
    adrp x1, _kuro_collection_7@PAGE
    add x1, x1, _kuro_collection_7@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3592]
    mov x0, #0
    str x0, [sp, #3600]
    ldr x0, [sp, #3592]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3600]
    adrp x1, _kuro_collection_4@PAGE
    add x1, x1, _kuro_collection_4@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_4@PAGE
    add x2, x2, _kuro_collection_len_4@PAGEOFF
    str x0, [x2]
    mov x0, #2
    str x0, [sp, #3608]
    ldr x0, [sp, #3608]
    adrp x2, _kuro_global_58@PAGE
    add x2, x2, _kuro_global_58@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3616]
    mov x0, #0
    str x0, [sp, #3624]
    mov x0, #0
    str x0, [sp, #3632]
    mov x0, #0
    str x0, [sp, #3640]
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
    mov x0, #0
    str x0, [sp, #3696]
    ldr x0, [sp, #3616]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3624]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3632]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3640]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3656]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3664]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3672]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3680]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3688]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3696]
    adrp x1, _kuro_collection_6@PAGE
    add x1, x1, _kuro_collection_6@PAGEOFF
    str x0, [x1, #72]
    mov x0, #10
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x0, [x2]
    mov x0, #10
    str x0, [sp, #3704]
    ldr x0, [sp, #3704]
    adrp x2, _kuro_global_57@PAGE
    add x2, x2, _kuro_global_57@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3712]
    mov x0, #0
    str x0, [sp, #3720]
    mov x0, #0
    str x0, [sp, #3728]
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
    ldr x0, [sp, #3712]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3720]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3728]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3752]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3760]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3768]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3776]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3784]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3792]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3800]
    adrp x1, _kuro_collection_12@PAGE
    add x1, x1, _kuro_collection_12@PAGEOFF
    str x0, [x1, #72]
    mov x0, #10
    adrp x2, _kuro_collection_len_12@PAGE
    add x2, x2, _kuro_collection_len_12@PAGEOFF
    str x0, [x2]
    mov x0, #10
    str x0, [sp, #3808]
    ldr x0, [sp, #3808]
    adrp x2, _kuro_global_89@PAGE
    add x2, x2, _kuro_global_89@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3816]
    ldr x0, [sp, #3816]
    adrp x2, _kuro_global_141@PAGE
    add x2, x2, _kuro_global_141@PAGEOFF
    str x0, [x2]
    mov x0, #10
    str x0, [sp, #3824]
    ldr x0, [sp, #3824]
    adrp x2, _kuro_global_140@PAGE
    add x2, x2, _kuro_global_140@PAGEOFF
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
    str x0, [sp, #3896]
    mov x0, #0
    str x0, [sp, #3904]
    mov x0, #0
    str x0, [sp, #3912]
    ldr x0, [sp, #3840]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3848]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3856]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3864]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3872]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3880]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3888]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3896]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3904]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #3912]
    adrp x1, _kuro_collection_17@PAGE
    add x1, x1, _kuro_collection_17@PAGEOFF
    str x0, [x1, #72]
    mov x0, #10
    adrp x2, _kuro_collection_len_17@PAGE
    add x2, x2, _kuro_collection_len_17@PAGEOFF
    str x0, [x2]
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
    mov x0, #0
    str x0, [sp, #3976]
    mov x0, #0
    str x0, [sp, #3984]
    mov x0, #0
    str x0, [sp, #3992]
    mov x0, #0
    str x0, [sp, #4000]
    ldr x0, [sp, #3928]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #3936]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #8]
    ldr x0, [sp, #3944]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #16]
    ldr x0, [sp, #3952]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #24]
    ldr x0, [sp, #3960]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #32]
    ldr x0, [sp, #3968]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #40]
    ldr x0, [sp, #3976]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #48]
    ldr x0, [sp, #3984]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #56]
    ldr x0, [sp, #3992]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #64]
    ldr x0, [sp, #4000]
    adrp x1, _kuro_collection_16@PAGE
    add x1, x1, _kuro_collection_16@PAGEOFF
    str x0, [x1, #72]
    mov x0, #10
    adrp x2, _kuro_collection_len_16@PAGE
    add x2, x2, _kuro_collection_len_16@PAGEOFF
    str x0, [x2]
    adrp x0, L_kuro_data_71@PAGE
    add x0, x0, L_kuro_data_71@PAGEOFF
    str x0, [sp, #4016]
    adrp x0, L_kuro_data_72@PAGE
    add x0, x0, L_kuro_data_72@PAGEOFF
    str x0, [sp, #4024]
    ldr x0, [sp, #4016]
    adrp x1, _kuro_collection_13@PAGE
    add x1, x1, _kuro_collection_13@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #4024]
    adrp x1, _kuro_collection_13@PAGE
    add x1, x1, _kuro_collection_13@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_13@PAGE
    add x2, x2, _kuro_collection_len_13@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4032]
    mov x0, #0
    str x0, [sp, #4040]
    ldr x0, [sp, #4032]
    adrp x1, _kuro_collection_14@PAGE
    add x1, x1, _kuro_collection_14@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #4040]
    adrp x1, _kuro_collection_14@PAGE
    add x1, x1, _kuro_collection_14@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_14@PAGE
    add x2, x2, _kuro_collection_len_14@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4048]
    ldr x0, [sp, #4048]
    adrp x2, _kuro_global_70@PAGE
    add x2, x2, _kuro_global_70@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #4056]
    ldr x0, [sp, #4056]
    adrp x2, _kuro_global_79@PAGE
    add x2, x2, _kuro_global_79@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_VMRun
    str x0, [sp, #4064]
    ldr x0, [sp, #4064]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4072]
    ldr x0, [sp, #4072]
    adrp x2, _kuro_global_29@PAGE
    add x2, x2, _kuro_global_29@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4080]
    ldr x0, [sp, #4080]
    adrp x2, _kuro_global_30@PAGE
    add x2, x2, _kuro_global_30@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_RuntimeRun
    str x0, [sp, #4088]
    ldr x0, [sp, #4088]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x15, #4624
    add sp, sp, x15
    adrp x0, _kuro_global_29@PAGE
    add x0, x0, _kuro_global_29@PAGEOFF
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
_kuro_fn_ArtifactDecodeLine:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #784
    sub sp, sp, x15
    str x0, [sp, #72]
    adrp x0, L_kuro_data_73@PAGE
    add x0, x0, L_kuro_data_73@PAGEOFF
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    adrp x2, _kuro_global_5@PAGE
    add x2, x2, _kuro_global_5@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_9@PAGE
    add x0, x0, _kuro_global_9@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    adrp x0, L_kuro_data_74@PAGE
    add x0, x0, L_kuro_data_74@PAGEOFF
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
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
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
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
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
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
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
    adrp x0, L_kuro_data_75@PAGE
    add x0, x0, L_kuro_data_75@PAGEOFF
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
    adrp x0, L_kuro_data_76@PAGE
    add x0, x0, L_kuro_data_76@PAGEOFF
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
    adrp x0, L_kuro_data_77@PAGE
    add x0, x0, L_kuro_data_77@PAGEOFF
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
    adrp x0, L_kuro_data_78@PAGE
    add x0, x0, L_kuro_data_78@PAGEOFF
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
    adrp x0, L_kuro_data_79@PAGE
    add x0, x0, L_kuro_data_79@PAGEOFF
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
    adrp x0, L_kuro_data_80@PAGE
    add x0, x0, L_kuro_data_80@PAGEOFF
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
    adrp x0, L_kuro_data_81@PAGE
    add x0, x0, L_kuro_data_81@PAGEOFF
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
    adrp x0, L_kuro_data_82@PAGE
    add x0, x0, L_kuro_data_82@PAGEOFF
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
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
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
    adrp x0, L_kuro_data_83@PAGE
    add x0, x0, L_kuro_data_83@PAGEOFF
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
_kuro_fn_VMFindName:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #256
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #8]
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    str x0, [sp, #24]
    ldr x0, [sp, #8]
    str x0, [sp, #96]
    ldr x0, [sp, #24]
    str x0, [sp, #184]
    ldr x0, [sp, #96]
    ldr x1, [sp, #184]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMFindName_else0
    ldr x0, [sp, #8]
    str x0, [sp, #200]
    ldr x1, [sp, #200]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    ldr x0, [sp, #0]
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    cbz w0, L_kuro_fn_VMFindName_else2
    ldr x0, [sp, #8]
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    mov x15, #256
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMFindName_endif3
L_kuro_fn_VMFindName_else2:
    ldr x0, [sp, #8]
    str x0, [sp, #104]
    mov x0, #1
    str x0, [sp, #112]
    ldr x0, [sp, #104]
    ldr x1, [sp, #112]
    add x0, x0, x1
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #32]
    ldr x0, [sp, #0]
    str x0, [sp, #128]
    ldr x0, [sp, #32]
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    bl _kuro_fn_VMFindName
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    mov x15, #256
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMFindName_endif3:
    b L_kuro_fn_VMFindName_endif1
L_kuro_fn_VMFindName_else0:
    mov x0, #0
    str x0, [sp, #160]
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    sub x0, x0, x1
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    mov x15, #256
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMFindName_endif1:
    mov x0, #0
    mov x15, #256
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMFindFrameName:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #240
    sub sp, sp, x15
    str x0, [sp, #8]
    str x1, [sp, #16]
    str x2, [sp, #0]
    ldr x0, [sp, #16]
    str x0, [sp, #80]
    ldr x0, [sp, #0]
    str x0, [sp, #88]
    ldr x0, [sp, #80]
    ldr x1, [sp, #88]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    cbz w0, L_kuro_fn_VMFindFrameName_else0
    ldr x0, [sp, #16]
    str x0, [sp, #184]
    ldr x1, [sp, #184]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    ldr x0, [sp, #8]
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    cbz w0, L_kuro_fn_VMFindFrameName_else2
    ldr x0, [sp, #16]
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMFindFrameName_endif3
L_kuro_fn_VMFindFrameName_else2:
    ldr x0, [sp, #16]
    str x0, [sp, #232]
    mov x0, #1
    str x0, [sp, #96]
    ldr x0, [sp, #232]
    ldr x1, [sp, #96]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #32]
    ldr x0, [sp, #8]
    str x0, [sp, #112]
    ldr x0, [sp, #32]
    str x0, [sp, #120]
    ldr x0, [sp, #0]
    str x0, [sp, #128]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    ldr x2, [sp, #128]
    bl _kuro_fn_VMFindFrameName
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMFindFrameName_endif3:
    b L_kuro_fn_VMFindFrameName_endif1
L_kuro_fn_VMFindFrameName_else0:
    mov x0, #0
    str x0, [sp, #152]
    mov x0, #1
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    sub x0, x0, x1
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMFindFrameName_endif1:
    mov x0, #0
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMFindCollection:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #224
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #8]
    ldr x0, [sp, #8]
    str x0, [sp, #72]
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x0, [sp, #72]
    ldr x1, [sp, #80]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_VMFindCollection_else0
    ldr x0, [sp, #8]
    str x0, [sp, #160]
    ldr x1, [sp, #160]
    adrp x2, _kuro_collection_2@PAGE
    add x2, x2, _kuro_collection_2@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #176]
    ldr x0, [sp, #0]
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMFindCollection_else2
    ldr x0, [sp, #8]
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    mov x15, #224
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMFindCollection_endif3
L_kuro_fn_VMFindCollection_else2:
    ldr x0, [sp, #0]
    str x0, [sp, #208]
    ldr x0, [sp, #8]
    str x0, [sp, #88]
    mov x0, #1
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #208]
    ldr x1, [sp, #104]
    bl _kuro_fn_VMFindCollection
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    mov x15, #224
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMFindCollection_endif3:
    b L_kuro_fn_VMFindCollection_endif1
L_kuro_fn_VMFindCollection_else0:
    mov x0, #0
    str x0, [sp, #128]
    mov x0, #1
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    sub x0, x0, x1
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    mov x15, #224
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMFindCollection_endif1:
    mov x0, #0
    mov x15, #224
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMMarkCollection:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #72]
    mov x0, #0
    str x0, [sp, #80]
    ldr x0, [sp, #72]
    ldr x1, [sp, #80]
    bl _kuro_fn_VMFindCollection
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    mov x0, #0
    str x0, [sp, #128]
    ldr x0, [sp, #120]
    ldr x1, [sp, #128]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    cbz w0, L_kuro_fn_VMMarkCollection_else0
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    mov x0, #2
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_VMMarkCollection_else2
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    ldr x0, [sp, #0]
    str x0, [sp, #88]
    ldr x1, [sp, #168]
    ldr x0, [sp, #88]
    adrp x2, _kuro_collection_2@PAGE
    add x2, x2, _kuro_collection_2@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMMarkCollection_endif3
L_kuro_fn_VMMarkCollection_else2:
    ldr x0, [sp, #0]
    str x0, [sp, #96]
    adrp x1, _kuro_collection_len_2@PAGE
    add x1, x1, _kuro_collection_len_2@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_2@PAGE
    add x2, x2, _kuro_collection_2@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #96]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_2@PAGE
    add x2, x2, _kuro_collection_len_2@PAGEOFF
    str x1, [x2]
L_kuro_fn_VMMarkCollection_endif3:
    mov x0, #1
    str x0, [sp, #104]
    adrp x0, _kuro_global_36@PAGE
    add x0, x0, _kuro_global_36@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #104]
    add x0, x0, x1
    adrp x2, _kuro_global_36@PAGE
    add x2, x2, _kuro_global_36@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMMarkCollection_endif1
L_kuro_fn_VMMarkCollection_else0:
L_kuro_fn_VMMarkCollection_endif1:
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMAppendCollectionItem:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #144
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #32]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    mov x0, #2
    str x0, [sp, #64]
    ldr x0, [sp, #56]
    ldr x1, [sp, #64]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    cbz w0, L_kuro_fn_VMAppendCollectionItem_else0
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x0, [sp, #0]
    str x0, [sp, #88]
    ldr x1, [sp, #80]
    ldr x0, [sp, #88]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    ldr x0, [sp, #32]
    str x0, [sp, #104]
    ldr x1, [sp, #96]
    ldr x0, [sp, #104]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMAppendCollectionItem_endif1
L_kuro_fn_VMAppendCollectionItem_else0:
    ldr x0, [sp, #0]
    str x0, [sp, #112]
    adrp x1, _kuro_collection_len_3@PAGE
    add x1, x1, _kuro_collection_len_3@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #112]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_3@PAGE
    add x2, x2, _kuro_collection_len_3@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #32]
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
L_kuro_fn_VMAppendCollectionItem_endif1:
    mov x0, #1
    str x0, [sp, #128]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #128]
    add x0, x0, x1
    adrp x2, _kuro_global_37@PAGE
    add x2, x2, _kuro_global_37@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #144
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMGetCollectionItem:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #384
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #56]
    mov x0, #0
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #32]
    mov x0, #0
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #40]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    str x0, [sp, #24]
    mov x0, #0
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    str x0, [sp, #48]
L_kuro_fn_VMGetCollectionItem_while_start0:
    ldr x0, [sp, #32]
    str x0, [sp, #312]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #320]
    ldr x0, [sp, #312]
    ldr x1, [sp, #320]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #328]
    ldr x0, [sp, #24]
    str x0, [sp, #336]
    mov x0, #0
    str x0, [sp, #344]
    ldr x0, [sp, #336]
    ldr x1, [sp, #344]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #352]
    ldr x0, [sp, #328]
    ldr x1, [sp, #352]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    cbz w0, L_kuro_fn_VMGetCollectionItem_while_end1
    ldr x0, [sp, #32]
    str x0, [sp, #144]
    ldr x1, [sp, #144]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #160]
    ldr x0, [sp, #0]
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    cbz w0, L_kuro_fn_VMGetCollectionItem_else3
    ldr x0, [sp, #40]
    str x0, [sp, #184]
    ldr x0, [sp, #56]
    str x0, [sp, #192]
    ldr x0, [sp, #184]
    ldr x1, [sp, #192]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    cbz w0, L_kuro_fn_VMGetCollectionItem_else5
    ldr x0, [sp, #32]
    str x0, [sp, #208]
    ldr x1, [sp, #208]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    str x0, [sp, #48]
    mov x0, #1
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    str x0, [sp, #24]
    b L_kuro_fn_VMGetCollectionItem_endif6
L_kuro_fn_VMGetCollectionItem_else5:
    mov x0, #1
    str x0, [sp, #248]
    ldr x0, [sp, #40]
    ldr x1, [sp, #248]
    add x0, x0, x1
    str x0, [sp, #40]
L_kuro_fn_VMGetCollectionItem_endif6:
    b L_kuro_fn_VMGetCollectionItem_endif4
L_kuro_fn_VMGetCollectionItem_else3:
L_kuro_fn_VMGetCollectionItem_endif4:
    mov x0, #1
    str x0, [sp, #256]
    ldr x0, [sp, #32]
    ldr x1, [sp, #256]
    add x0, x0, x1
    str x0, [sp, #32]
    b L_kuro_fn_VMGetCollectionItem_while_start0
L_kuro_fn_VMGetCollectionItem_while_end1:
    ldr x0, [sp, #24]
    str x0, [sp, #264]
    mov x0, #0
    str x0, [sp, #272]
    ldr x0, [sp, #264]
    ldr x1, [sp, #272]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    cbz w0, L_kuro_fn_VMGetCollectionItem_else7
    mov x0, #1
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMGetCollectionItem_endif8
L_kuro_fn_VMGetCollectionItem_else7:
L_kuro_fn_VMGetCollectionItem_endif8:
    ldr x0, [sp, #48]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    mov x15, #384
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #384
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMLengthCollection:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #176
    sub sp, sp, x15
    str x0, [sp, #0]
    mov x0, #0
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    str x0, [sp, #24]
    mov x0, #0
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    str x0, [sp, #16]
L_kuro_fn_VMLengthCollection_while_start0:
    ldr x0, [sp, #24]
    str x0, [sp, #96]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    cbz w0, L_kuro_fn_VMLengthCollection_while_end1
    ldr x0, [sp, #24]
    str x0, [sp, #120]
    ldr x1, [sp, #120]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #0]
    str x0, [sp, #144]
    ldr x0, [sp, #136]
    ldr x1, [sp, #144]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    cbz w0, L_kuro_fn_VMLengthCollection_else3
    mov x0, #1
    str x0, [sp, #72]
    ldr x0, [sp, #16]
    ldr x1, [sp, #72]
    add x0, x0, x1
    str x0, [sp, #16]
    b L_kuro_fn_VMLengthCollection_endif4
L_kuro_fn_VMLengthCollection_else3:
L_kuro_fn_VMLengthCollection_endif4:
    mov x0, #1
    str x0, [sp, #80]
    ldr x0, [sp, #24]
    ldr x1, [sp, #80]
    add x0, x0, x1
    str x0, [sp, #24]
    b L_kuro_fn_VMLengthCollection_while_start0
L_kuro_fn_VMLengthCollection_while_end1:
    ldr x0, [sp, #16]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #176
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMSetCollectionItem:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #352
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #56]
    str x2, [sp, #48]
    mov x0, #0
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #32]
    mov x0, #0
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #40]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    str x0, [sp, #24]
L_kuro_fn_VMSetCollectionItem_while_start0:
    ldr x0, [sp, #32]
    str x0, [sp, #280]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #296]
    ldr x0, [sp, #24]
    str x0, [sp, #304]
    mov x0, #0
    str x0, [sp, #312]
    ldr x0, [sp, #304]
    ldr x1, [sp, #312]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #320]
    ldr x0, [sp, #296]
    ldr x1, [sp, #320]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    cbz w0, L_kuro_fn_VMSetCollectionItem_while_end1
    ldr x0, [sp, #32]
    str x0, [sp, #136]
    ldr x1, [sp, #136]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x0, [sp, #0]
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_VMSetCollectionItem_else3
    ldr x0, [sp, #40]
    str x0, [sp, #176]
    ldr x0, [sp, #56]
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMSetCollectionItem_else5
    ldr x0, [sp, #32]
    str x0, [sp, #200]
    ldr x0, [sp, #48]
    str x0, [sp, #208]
    ldr x1, [sp, #200]
    ldr x0, [sp, #208]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #1
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    str x0, [sp, #24]
    b L_kuro_fn_VMSetCollectionItem_endif6
L_kuro_fn_VMSetCollectionItem_else5:
    mov x0, #1
    str x0, [sp, #232]
    ldr x0, [sp, #40]
    ldr x1, [sp, #232]
    add x0, x0, x1
    str x0, [sp, #40]
L_kuro_fn_VMSetCollectionItem_endif6:
    b L_kuro_fn_VMSetCollectionItem_endif4
L_kuro_fn_VMSetCollectionItem_else3:
L_kuro_fn_VMSetCollectionItem_endif4:
    mov x0, #1
    str x0, [sp, #240]
    ldr x0, [sp, #32]
    ldr x1, [sp, #240]
    add x0, x0, x1
    str x0, [sp, #32]
    b L_kuro_fn_VMSetCollectionItem_while_start0
L_kuro_fn_VMSetCollectionItem_while_end1:
    ldr x0, [sp, #24]
    str x0, [sp, #248]
    mov x0, #0
    str x0, [sp, #256]
    ldr x0, [sp, #248]
    ldr x1, [sp, #256]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    cbz w0, L_kuro_fn_VMSetCollectionItem_else7
    mov x0, #1
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMSetCollectionItem_endif8
L_kuro_fn_VMSetCollectionItem_else7:
L_kuro_fn_VMSetCollectionItem_endif8:
    mov x0, #0
    mov x15, #352
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMCopyCollection:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #224
    sub sp, sp, x15
    str x0, [sp, #8]
    str x1, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    bl _kuro_fn_VMMarkCollection
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #32]
L_kuro_fn_VMCopyCollection_while_start0:
    ldr x0, [sp, #32]
    str x0, [sp, #152]
    adrp x0, _kuro_global_37@PAGE
    add x0, x0, _kuro_global_37@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cbz w0, L_kuro_fn_VMCopyCollection_while_end1
    ldr x0, [sp, #32]
    str x0, [sp, #176]
    ldr x1, [sp, #176]
    adrp x2, _kuro_collection_3@PAGE
    add x2, x2, _kuro_collection_3@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    ldr x0, [sp, #8]
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    cbz w0, L_kuro_fn_VMCopyCollection_else3
    ldr x0, [sp, #32]
    str x0, [sp, #96]
    ldr x1, [sp, #96]
    adrp x2, _kuro_collection_1@PAGE
    add x2, x2, _kuro_collection_1@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #0]
    str x0, [sp, #112]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    bl _kuro_fn_VMAppendCollectionItem
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMCopyCollection_endif4
L_kuro_fn_VMCopyCollection_else3:
L_kuro_fn_VMCopyCollection_endif4:
    mov x0, #1
    str x0, [sp, #136]
    ldr x0, [sp, #32]
    ldr x1, [sp, #136]
    add x0, x0, x1
    str x0, [sp, #32]
    b L_kuro_fn_VMCopyCollection_while_start0
L_kuro_fn_VMCopyCollection_while_end1:
    mov x0, #0
    mov x15, #224
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMSetResult:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #96
    sub sp, sp, x15
    str x0, [sp, #16]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #40]
    mov x0, #0
    str x0, [sp, #48]
    ldr x0, [sp, #40]
    ldr x1, [sp, #48]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    cbz w0, L_kuro_fn_VMSetResult_else0
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    ldr x0, [sp, #16]
    str x0, [sp, #72]
    ldr x1, [sp, #64]
    ldr x0, [sp, #72]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMSetResult_endif1
L_kuro_fn_VMSetResult_else0:
    ldr x0, [sp, #16]
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_71@PAGE
    add x2, x2, _kuro_global_71@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMSetResult_endif1:
    mov x0, #0
    mov x15, #96
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMPush:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    str x0, [sp, #32]
    adrp x0, _kuro_collection_len_13@PAGE
    add x0, x0, _kuro_collection_len_13@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    str x0, [sp, #0]
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    ldr x0, [sp, #0]
    str x0, [sp, #104]
    ldr x0, [sp, #96]
    ldr x1, [sp, #104]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    cbz w0, L_kuro_fn_VMPush_else0
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    ldr x0, [sp, #32]
    str x0, [sp, #128]
    ldr x1, [sp, #120]
    ldr x0, [sp, #128]
    adrp x2, _kuro_collection_13@PAGE
    add x2, x2, _kuro_collection_13@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    mov x0, #0
    str x0, [sp, #144]
    ldr x1, [sp, #136]
    ldr x0, [sp, #144]
    adrp x2, _kuro_collection_14@PAGE
    add x2, x2, _kuro_collection_14@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMPush_endif1
L_kuro_fn_VMPush_else0:
    ldr x0, [sp, #32]
    str x0, [sp, #152]
    adrp x1, _kuro_collection_len_13@PAGE
    add x1, x1, _kuro_collection_len_13@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_13@PAGE
    add x2, x2, _kuro_collection_13@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #152]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_13@PAGE
    add x2, x2, _kuro_collection_len_13@PAGEOFF
    str x1, [x2]
    mov x0, #0
    str x0, [sp, #80]
    adrp x1, _kuro_collection_len_14@PAGE
    add x1, x1, _kuro_collection_len_14@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_14@PAGE
    add x2, x2, _kuro_collection_14@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #80]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_14@PAGE
    add x2, x2, _kuro_collection_len_14@PAGEOFF
    str x1, [x2]
L_kuro_fn_VMPush_endif1:
    mov x0, #1
    str x0, [sp, #88]
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #88]
    add x0, x0, x1
    adrp x2, _kuro_global_139@PAGE
    add x2, x2, _kuro_global_139@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMPushCollection:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #96
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    bl _kuro_fn_VMPush
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    mov x0, #1
    str x0, [sp, #64]
    ldr x0, [sp, #56]
    ldr x1, [sp, #64]
    sub x0, x0, x1
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    str x0, [sp, #16]
    ldr x0, [sp, #16]
    str x0, [sp, #80]
    mov x0, #1
    str x0, [sp, #88]
    ldr x1, [sp, #80]
    ldr x0, [sp, #88]
    adrp x2, _kuro_collection_14@PAGE
    add x2, x2, _kuro_collection_14@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #0
    mov x15, #96
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMPop:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #48]
    mov x0, #0
    str x0, [sp, #56]
    ldr x0, [sp, #48]
    ldr x1, [sp, #56]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    cbz w0, L_kuro_fn_VMPop_else0
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    mov x0, #1
    str x0, [sp, #112]
    ldr x0, [sp, #104]
    ldr x1, [sp, #112]
    sub x0, x0, x1
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_139@PAGE
    add x2, x2, _kuro_global_139@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x1, [sp, #128]
    adrp x2, _kuro_collection_14@PAGE
    add x2, x2, _kuro_collection_14@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_70@PAGE
    add x2, x2, _kuro_global_70@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_139@PAGE
    add x0, x0, _kuro_global_139@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x1, [sp, #152]
    adrp x2, _kuro_collection_13@PAGE
    add x2, x2, _kuro_collection_13@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #72]
    ldr x0, [sp, #72]
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMPop_endif1
L_kuro_fn_VMPop_else0:
    mov x0, #1
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMPop_endif1:
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMLoad:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #560
    sub sp, sp, x15
    str x0, [sp, #0]
    mov x0, #0
    str x0, [sp, #168]
    mov x0, #1
    str x0, [sp, #176]
    ldr x0, [sp, #168]
    ldr x1, [sp, #176]
    sub x0, x0, x1
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #64]
    ldr x0, [sp, #0]
    str x0, [sp, #352]
    adrp x0, L_kuro_data_84@PAGE
    add x0, x0, L_kuro_data_84@PAGEOFF
    str x0, [sp, #440]
    ldr x0, [sp, #352]
    ldr x1, [sp, #440]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #512]
    ldr x0, [sp, #512]
    cbz w0, L_kuro_fn_VMLoad_else0
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #520]
    mov x0, #0
    str x0, [sp, #528]
    ldr x0, [sp, #520]
    ldr x1, [sp, #528]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    cbz w0, L_kuro_fn_VMLoad_else2
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #544]
    ldr x1, [sp, #544]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMLoad_endif3
L_kuro_fn_VMLoad_else2:
    adrp x0, _kuro_global_71@PAGE
    add x0, x0, _kuro_global_71@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMLoad_endif3:
    b L_kuro_fn_VMLoad_endif1
L_kuro_fn_VMLoad_else0:
L_kuro_fn_VMLoad_endif1:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #208]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #208]
    ldr x1, [sp, #216]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_VMLoad_else4
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    ldr x1, [sp, #232]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    str x0, [sp, #72]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #256]
    ldr x1, [sp, #256]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    str x0, [sp, #48]
    ldr x0, [sp, #72]
    str x0, [sp, #288]
    ldr x0, [sp, #48]
    str x0, [sp, #296]
    ldr x0, [sp, #288]
    ldr x1, [sp, #296]
    add x0, x0, x1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    str x0, [sp, #56]
    ldr x0, [sp, #0]
    str x0, [sp, #312]
    ldr x0, [sp, #72]
    str x0, [sp, #320]
    ldr x0, [sp, #56]
    str x0, [sp, #328]
    ldr x0, [sp, #312]
    ldr x1, [sp, #320]
    ldr x2, [sp, #328]
    bl _kuro_fn_VMFindFrameName
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    str x0, [sp, #360]
    mov x0, #0
    str x0, [sp, #368]
    ldr x0, [sp, #360]
    ldr x1, [sp, #368]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    cbz w0, L_kuro_fn_VMLoad_else6
    ldr x0, [sp, #64]
    str x0, [sp, #384]
    ldr x1, [sp, #384]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #392]
    ldr x0, [sp, #392]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMLoad_endif7
L_kuro_fn_VMLoad_else6:
L_kuro_fn_VMLoad_endif7:
    b L_kuro_fn_VMLoad_endif5
L_kuro_fn_VMLoad_else4:
L_kuro_fn_VMLoad_endif5:
    ldr x0, [sp, #0]
    str x0, [sp, #408]
    mov x0, #0
    str x0, [sp, #416]
    ldr x0, [sp, #408]
    ldr x1, [sp, #416]
    bl _kuro_fn_VMFindName
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    str x0, [sp, #448]
    mov x0, #0
    str x0, [sp, #456]
    ldr x0, [sp, #448]
    ldr x1, [sp, #456]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    cbz w0, L_kuro_fn_VMLoad_else8
    ldr x0, [sp, #64]
    str x0, [sp, #472]
    ldr x1, [sp, #472]
    adrp x2, _kuro_collection_15@PAGE
    add x2, x2, _kuro_collection_15@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #480]
    ldr x0, [sp, #480]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMLoad_endif9
L_kuro_fn_VMLoad_else8:
    mov x0, #1
    str x0, [sp, #496]
    ldr x0, [sp, #496]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #504]
    ldr x0, [sp, #504]
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMLoad_endif9:
    mov x0, #0
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMStore:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #560
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #96]
    mov x0, #0
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    str x0, [sp, #80]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    mov x0, #0
    str x0, [sp, #288]
    ldr x0, [sp, #200]
    ldr x1, [sp, #288]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    cbz w0, L_kuro_fn_VMStore_else0
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #464]
    ldr x1, [sp, #464]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #520]
    ldr x0, [sp, #520]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #528]
    ldr x0, [sp, #528]
    str x0, [sp, #72]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #536]
    ldr x1, [sp, #536]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #544]
    ldr x0, [sp, #544]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #552]
    ldr x0, [sp, #552]
    str x0, [sp, #48]
    ldr x0, [sp, #72]
    str x0, [sp, #208]
    ldr x0, [sp, #48]
    str x0, [sp, #216]
    ldr x0, [sp, #208]
    ldr x1, [sp, #216]
    add x0, x0, x1
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    str x0, [sp, #56]
    ldr x0, [sp, #0]
    str x0, [sp, #232]
    ldr x0, [sp, #72]
    str x0, [sp, #240]
    ldr x0, [sp, #56]
    str x0, [sp, #248]
    ldr x0, [sp, #232]
    ldr x1, [sp, #240]
    ldr x2, [sp, #248]
    bl _kuro_fn_VMFindFrameName
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    str x0, [sp, #272]
    mov x0, #0
    str x0, [sp, #280]
    ldr x0, [sp, #272]
    ldr x1, [sp, #280]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    cbz w0, L_kuro_fn_VMStore_else2
    ldr x0, [sp, #64]
    str x0, [sp, #304]
    ldr x0, [sp, #96]
    str x0, [sp, #312]
    ldr x1, [sp, #304]
    ldr x0, [sp, #312]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #1
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    str x0, [sp, #80]
    b L_kuro_fn_VMStore_endif3
L_kuro_fn_VMStore_else2:
L_kuro_fn_VMStore_endif3:
    b L_kuro_fn_VMStore_endif1
L_kuro_fn_VMStore_else0:
L_kuro_fn_VMStore_endif1:
    ldr x0, [sp, #80]
    str x0, [sp, #328]
    mov x0, #0
    str x0, [sp, #336]
    ldr x0, [sp, #328]
    ldr x1, [sp, #336]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    cbz w0, L_kuro_fn_VMStore_else4
    ldr x0, [sp, #0]
    str x0, [sp, #352]
    mov x0, #0
    str x0, [sp, #360]
    ldr x0, [sp, #352]
    ldr x1, [sp, #360]
    bl _kuro_fn_VMFindName
    str x0, [sp, #368]
    ldr x0, [sp, #368]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    str x0, [sp, #392]
    mov x0, #0
    str x0, [sp, #400]
    ldr x0, [sp, #392]
    ldr x1, [sp, #400]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    cbz w0, L_kuro_fn_VMStore_else6
    ldr x0, [sp, #64]
    str x0, [sp, #416]
    ldr x0, [sp, #96]
    str x0, [sp, #424]
    ldr x1, [sp, #416]
    ldr x0, [sp, #424]
    adrp x2, _kuro_collection_15@PAGE
    add x2, x2, _kuro_collection_15@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMStore_endif7
L_kuro_fn_VMStore_else6:
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #432]
    mov x0, #2
    str x0, [sp, #440]
    ldr x0, [sp, #432]
    ldr x1, [sp, #440]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #448]
    ldr x0, [sp, #448]
    cbz w0, L_kuro_fn_VMStore_else8
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #456]
    ldr x0, [sp, #0]
    str x0, [sp, #472]
    ldr x1, [sp, #456]
    ldr x0, [sp, #472]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #480]
    ldr x0, [sp, #96]
    str x0, [sp, #488]
    ldr x1, [sp, #480]
    ldr x0, [sp, #488]
    adrp x2, _kuro_collection_15@PAGE
    add x2, x2, _kuro_collection_15@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMStore_endif9
L_kuro_fn_VMStore_else8:
    ldr x0, [sp, #0]
    str x0, [sp, #496]
    adrp x1, _kuro_collection_len_9@PAGE
    add x1, x1, _kuro_collection_len_9@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_9@PAGE
    add x2, x2, _kuro_collection_9@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #496]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_9@PAGE
    add x2, x2, _kuro_collection_len_9@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #96]
    str x0, [sp, #504]
    adrp x1, _kuro_collection_len_15@PAGE
    add x1, x1, _kuro_collection_len_15@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_15@PAGE
    add x2, x2, _kuro_collection_15@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #504]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_15@PAGE
    add x2, x2, _kuro_collection_len_15@PAGEOFF
    str x1, [x2]
L_kuro_fn_VMStore_endif9:
    mov x0, #1
    str x0, [sp, #512]
    adrp x0, _kuro_global_78@PAGE
    add x0, x0, _kuro_global_78@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #512]
    add x0, x0, x1
    adrp x2, _kuro_global_78@PAGE
    add x2, x2, _kuro_global_78@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStore_endif7:
    b L_kuro_fn_VMStore_endif5
L_kuro_fn_VMStore_else4:
L_kuro_fn_VMStore_endif5:
    mov x0, #0
    mov x15, #560
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMStoreFrame:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #400
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #64]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x1, [sp, #128]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    str x0, [sp, #48]
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    mov x0, #0
    str x0, [sp, #352]
    ldr x0, [sp, #312]
    ldr x1, [sp, #352]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    cbz w0, L_kuro_fn_VMStoreFrame_else0
    mov x0, #0
    str x0, [sp, #368]
    ldr x0, [sp, #0]
    str x0, [sp, #376]
    ldr x1, [sp, #368]
    ldr x0, [sp, #376]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #0
    str x0, [sp, #384]
    ldr x0, [sp, #64]
    str x0, [sp, #392]
    ldr x1, [sp, #384]
    ldr x0, [sp, #392]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMStoreFrame_endif1
L_kuro_fn_VMStoreFrame_else0:
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    mov x0, #1
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_VMStoreFrame_else2
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #0]
    str x0, [sp, #176]
    ldr x1, [sp, #168]
    ldr x0, [sp, #176]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #1
    str x0, [sp, #184]
    ldr x0, [sp, #64]
    str x0, [sp, #192]
    ldr x1, [sp, #184]
    ldr x0, [sp, #192]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMStoreFrame_endif3
L_kuro_fn_VMStoreFrame_else2:
    adrp x0, _kuro_collection_len_5@PAGE
    add x0, x0, _kuro_collection_len_5@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    str x0, [sp, #40]
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    ldr x0, [sp, #40]
    str x0, [sp, #232]
    ldr x0, [sp, #216]
    ldr x1, [sp, #232]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_VMStoreFrame_else4
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    ldr x0, [sp, #0]
    str x0, [sp, #256]
    ldr x1, [sp, #248]
    ldr x0, [sp, #256]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    ldr x0, [sp, #64]
    str x0, [sp, #272]
    ldr x1, [sp, #264]
    ldr x0, [sp, #272]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMStoreFrame_endif5
L_kuro_fn_VMStoreFrame_else4:
    ldr x0, [sp, #0]
    str x0, [sp, #280]
    adrp x1, _kuro_collection_len_5@PAGE
    add x1, x1, _kuro_collection_len_5@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_5@PAGE
    add x2, x2, _kuro_collection_5@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #280]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_5@PAGE
    add x2, x2, _kuro_collection_len_5@PAGEOFF
    str x1, [x2]
    ldr x0, [sp, #64]
    str x0, [sp, #288]
    adrp x1, _kuro_collection_len_8@PAGE
    add x1, x1, _kuro_collection_len_8@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_8@PAGE
    add x2, x2, _kuro_collection_8@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #288]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_8@PAGE
    add x2, x2, _kuro_collection_len_8@PAGEOFF
    str x1, [x2]
L_kuro_fn_VMStoreFrame_endif5:
L_kuro_fn_VMStoreFrame_endif3:
L_kuro_fn_VMStoreFrame_endif1:
    mov x0, #1
    str x0, [sp, #296]
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #296]
    add x0, x0, x1
    adrp x2, _kuro_global_56@PAGE
    add x2, x2, _kuro_global_56@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #48]
    str x0, [sp, #304]
    mov x0, #1
    str x0, [sp, #320]
    ldr x0, [sp, #304]
    ldr x1, [sp, #320]
    add x0, x0, x1
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    str x0, [sp, #56]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #336]
    ldr x0, [sp, #56]
    str x0, [sp, #344]
    ldr x1, [sp, #336]
    ldr x0, [sp, #344]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #0
    mov x15, #400
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMReadOperand:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #64
    sub sp, sp, x15
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #16]
    ldr x1, [sp, #16]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #24]
    ldr x0, [sp, #24]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #32]
    mov x0, #1
    str x0, [sp, #40]
    ldr x0, [sp, #32]
    ldr x1, [sp, #40]
    add x0, x0, x1
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    mov x15, #64
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    mov x0, #0
    mov x15, #64
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMSkipFalse:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #416
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #24]
    mov x0, #0
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #32]
L_kuro_fn_VMSkipFalse_while_start0:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #304]
    ldr x0, [sp, #216]
    ldr x1, [sp, #304]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #352]
    ldr x0, [sp, #32]
    str x0, [sp, #360]
    mov x0, #0
    str x0, [sp, #368]
    ldr x0, [sp, #360]
    ldr x1, [sp, #368]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #376]
    ldr x0, [sp, #352]
    ldr x1, [sp, #376]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    cbz w0, L_kuro_fn_VMSkipFalse_while_end1
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #392]
    ldr x1, [sp, #392]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #40]
    mov x0, #1
    str x0, [sp, #152]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #152]
    add x0, x0, x1
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #40]
    str x0, [sp, #160]
    adrp x0, L_kuro_data_85@PAGE
    add x0, x0, L_kuro_data_85@PAGEOFF
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #176]
    cbz w0, L_kuro_fn_VMSkipFalse_else3
    mov x0, #1
    str x0, [sp, #184]
    ldr x0, [sp, #24]
    ldr x1, [sp, #184]
    add x0, x0, x1
    str x0, [sp, #24]
    b L_kuro_fn_VMSkipFalse_endif4
L_kuro_fn_VMSkipFalse_else3:
    ldr x0, [sp, #40]
    str x0, [sp, #192]
    adrp x0, L_kuro_data_86@PAGE
    add x0, x0, L_kuro_data_86@PAGEOFF
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #208]
    ldr x0, [sp, #24]
    str x0, [sp, #224]
    mov x0, #0
    str x0, [sp, #232]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #240]
    ldr x0, [sp, #208]
    ldr x1, [sp, #240]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    cbz w0, L_kuro_fn_VMSkipFalse_else5
    mov x0, #1
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #32]
    b L_kuro_fn_VMSkipFalse_endif6
L_kuro_fn_VMSkipFalse_else5:
    ldr x0, [sp, #40]
    str x0, [sp, #264]
    adrp x0, L_kuro_data_87@PAGE
    add x0, x0, L_kuro_data_87@PAGEOFF
    str x0, [sp, #272]
    ldr x0, [sp, #264]
    ldr x1, [sp, #272]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    cbz w0, L_kuro_fn_VMSkipFalse_else7
    ldr x0, [sp, #24]
    str x0, [sp, #288]
    mov x0, #0
    str x0, [sp, #296]
    ldr x0, [sp, #288]
    ldr x1, [sp, #296]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    cbz w0, L_kuro_fn_VMSkipFalse_else9
    mov x0, #1
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    str x0, [sp, #32]
    b L_kuro_fn_VMSkipFalse_endif10
L_kuro_fn_VMSkipFalse_else9:
    ldr x0, [sp, #24]
    str x0, [sp, #328]
    mov x0, #1
    str x0, [sp, #336]
    ldr x0, [sp, #328]
    ldr x1, [sp, #336]
    sub x0, x0, x1
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    str x0, [sp, #24]
L_kuro_fn_VMSkipFalse_endif10:
    b L_kuro_fn_VMSkipFalse_endif8
L_kuro_fn_VMSkipFalse_else7:
L_kuro_fn_VMSkipFalse_endif8:
L_kuro_fn_VMSkipFalse_endif6:
L_kuro_fn_VMSkipFalse_endif4:
    b L_kuro_fn_VMSkipFalse_while_start0
L_kuro_fn_VMSkipFalse_while_end1:
    mov x0, #0
    mov x15, #416
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMSkipElse:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #336
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #24]
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #32]
L_kuro_fn_VMSkipElse_while_start0:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    ldr x0, [sp, #200]
    ldr x1, [sp, #264]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #272]
    ldr x0, [sp, #32]
    str x0, [sp, #280]
    mov x0, #0
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #296]
    ldr x0, [sp, #272]
    ldr x1, [sp, #296]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    cbz w0, L_kuro_fn_VMSkipElse_while_end1
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x1, [sp, #312]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #40]
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #40]
    str x0, [sp, #144]
    adrp x0, L_kuro_data_88@PAGE
    add x0, x0, L_kuro_data_88@PAGEOFF
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_VMSkipElse_else3
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #24]
    ldr x1, [sp, #168]
    add x0, x0, x1
    str x0, [sp, #24]
    b L_kuro_fn_VMSkipElse_endif4
L_kuro_fn_VMSkipElse_else3:
    ldr x0, [sp, #40]
    str x0, [sp, #176]
    adrp x0, L_kuro_data_89@PAGE
    add x0, x0, L_kuro_data_89@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMSkipElse_else5
    ldr x0, [sp, #24]
    str x0, [sp, #208]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #208]
    ldr x1, [sp, #216]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_VMSkipElse_else7
    mov x0, #1
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    str x0, [sp, #32]
    b L_kuro_fn_VMSkipElse_endif8
L_kuro_fn_VMSkipElse_else7:
    ldr x0, [sp, #24]
    str x0, [sp, #240]
    mov x0, #1
    str x0, [sp, #248]
    ldr x0, [sp, #240]
    ldr x1, [sp, #248]
    sub x0, x0, x1
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #24]
L_kuro_fn_VMSkipElse_endif8:
    b L_kuro_fn_VMSkipElse_endif6
L_kuro_fn_VMSkipElse_else5:
L_kuro_fn_VMSkipElse_endif6:
L_kuro_fn_VMSkipElse_endif4:
    b L_kuro_fn_VMSkipElse_while_start0
L_kuro_fn_VMSkipElse_while_end1:
    mov x0, #0
    mov x15, #336
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMSkipRepeat:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #336
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #24]
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #32]
L_kuro_fn_VMSkipRepeat_while_start0:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    ldr x0, [sp, #200]
    ldr x1, [sp, #264]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #272]
    ldr x0, [sp, #32]
    str x0, [sp, #280]
    mov x0, #0
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #296]
    ldr x0, [sp, #272]
    ldr x1, [sp, #296]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    cbz w0, L_kuro_fn_VMSkipRepeat_while_end1
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x1, [sp, #312]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #40]
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #40]
    str x0, [sp, #144]
    adrp x0, L_kuro_data_90@PAGE
    add x0, x0, L_kuro_data_90@PAGEOFF
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_VMSkipRepeat_else3
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #24]
    ldr x1, [sp, #168]
    add x0, x0, x1
    str x0, [sp, #24]
    b L_kuro_fn_VMSkipRepeat_endif4
L_kuro_fn_VMSkipRepeat_else3:
    ldr x0, [sp, #40]
    str x0, [sp, #176]
    adrp x0, L_kuro_data_91@PAGE
    add x0, x0, L_kuro_data_91@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMSkipRepeat_else5
    ldr x0, [sp, #24]
    str x0, [sp, #208]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #208]
    ldr x1, [sp, #216]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_VMSkipRepeat_else7
    mov x0, #1
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    str x0, [sp, #32]
    b L_kuro_fn_VMSkipRepeat_endif8
L_kuro_fn_VMSkipRepeat_else7:
    ldr x0, [sp, #24]
    str x0, [sp, #240]
    mov x0, #1
    str x0, [sp, #248]
    ldr x0, [sp, #240]
    ldr x1, [sp, #248]
    sub x0, x0, x1
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #24]
L_kuro_fn_VMSkipRepeat_endif8:
    b L_kuro_fn_VMSkipRepeat_endif6
L_kuro_fn_VMSkipRepeat_else5:
L_kuro_fn_VMSkipRepeat_endif6:
L_kuro_fn_VMSkipRepeat_endif4:
    b L_kuro_fn_VMSkipRepeat_while_start0
L_kuro_fn_VMSkipRepeat_while_end1:
    mov x0, #0
    mov x15, #336
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMRunRepeat:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #448
    sub sp, sp, x15
    str x0, [sp, #0]
    str x1, [sp, #8]
    ldr x0, [sp, #0]
    str x0, [sp, #112]
    mov x0, #0
    str x0, [sp, #120]
    ldr x0, [sp, #112]
    ldr x1, [sp, #120]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    cbz w0, L_kuro_fn_VMRunRepeat_else0
    ldr x0, [sp, #0]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    str x0, [sp, #48]
L_kuro_fn_VMRunRepeat_while_start2:
    ldr x0, [sp, #48]
    str x0, [sp, #360]
    mov x0, #0
    str x0, [sp, #368]
    ldr x0, [sp, #360]
    ldr x1, [sp, #368]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #376]
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #384]
    mov x0, #0
    str x0, [sp, #392]
    ldr x0, [sp, #384]
    ldr x1, [sp, #392]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #400]
    ldr x0, [sp, #376]
    ldr x1, [sp, #400]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    cbz w0, L_kuro_fn_VMRunRepeat_while_end3
    ldr x0, [sp, #8]
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #40]
L_kuro_fn_VMRunRepeat_while_start5:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #160]
    ldr x0, [sp, #152]
    ldr x1, [sp, #160]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #168]
    ldr x0, [sp, #40]
    str x0, [sp, #176]
    mov x0, #0
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #168]
    ldr x1, [sp, #192]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #200]
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    mov x0, #0
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #232]
    ldr x0, [sp, #200]
    ldr x1, [sp, #232]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #240]
    ldr x0, [sp, #240]
    cbz w0, L_kuro_fn_VMRunRepeat_while_end6
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    ldr x1, [sp, #248]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    adrp x0, L_kuro_data_92@PAGE
    add x0, x0, L_kuro_data_92@PAGEOFF
    str x0, [sp, #272]
    ldr x0, [sp, #264]
    ldr x1, [sp, #272]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    cbz w0, L_kuro_fn_VMRunRepeat_else8
    mov x0, #1
    str x0, [sp, #288]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #288]
    add x0, x0, x1
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    str x0, [sp, #40]
    b L_kuro_fn_VMRunRepeat_endif9
L_kuro_fn_VMRunRepeat_else8:
    bl _kuro_fn_VMStep
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMRunRepeat_endif9:
    b L_kuro_fn_VMRunRepeat_while_start5
L_kuro_fn_VMRunRepeat_while_end6:
    ldr x0, [sp, #48]
    str x0, [sp, #320]
    mov x0, #1
    str x0, [sp, #328]
    ldr x0, [sp, #320]
    ldr x1, [sp, #328]
    sub x0, x0, x1
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    str x0, [sp, #48]
    b L_kuro_fn_VMRunRepeat_while_start2
L_kuro_fn_VMRunRepeat_while_end3:
    b L_kuro_fn_VMRunRepeat_endif1
L_kuro_fn_VMRunRepeat_else0:
    mov x0, #0
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    bl _kuro_fn_VMSkipRepeat
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMRunRepeat_endif1:
    mov x0, #0
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMSkipWhile:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #336
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    str x0, [sp, #24]
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #32]
L_kuro_fn_VMSkipWhile_while_start0:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    ldr x0, [sp, #200]
    ldr x1, [sp, #264]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #272]
    ldr x0, [sp, #32]
    str x0, [sp, #280]
    mov x0, #0
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #296]
    ldr x0, [sp, #272]
    ldr x1, [sp, #296]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    cbz w0, L_kuro_fn_VMSkipWhile_while_end1
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x1, [sp, #312]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #40]
    mov x0, #1
    str x0, [sp, #136]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #136]
    add x0, x0, x1
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #40]
    str x0, [sp, #144]
    adrp x0, L_kuro_data_93@PAGE
    add x0, x0, L_kuro_data_93@PAGEOFF
    str x0, [sp, #152]
    ldr x0, [sp, #144]
    ldr x1, [sp, #152]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    cbz w0, L_kuro_fn_VMSkipWhile_else3
    mov x0, #1
    str x0, [sp, #168]
    ldr x0, [sp, #24]
    ldr x1, [sp, #168]
    add x0, x0, x1
    str x0, [sp, #24]
    b L_kuro_fn_VMSkipWhile_endif4
L_kuro_fn_VMSkipWhile_else3:
    ldr x0, [sp, #40]
    str x0, [sp, #176]
    adrp x0, L_kuro_data_94@PAGE
    add x0, x0, L_kuro_data_94@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMSkipWhile_else5
    ldr x0, [sp, #24]
    str x0, [sp, #208]
    mov x0, #0
    str x0, [sp, #216]
    ldr x0, [sp, #208]
    ldr x1, [sp, #216]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_VMSkipWhile_else7
    mov x0, #1
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    str x0, [sp, #32]
    b L_kuro_fn_VMSkipWhile_endif8
L_kuro_fn_VMSkipWhile_else7:
    ldr x0, [sp, #24]
    str x0, [sp, #240]
    mov x0, #1
    str x0, [sp, #248]
    ldr x0, [sp, #240]
    ldr x1, [sp, #248]
    sub x0, x0, x1
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    str x0, [sp, #24]
L_kuro_fn_VMSkipWhile_endif8:
    b L_kuro_fn_VMSkipWhile_endif6
L_kuro_fn_VMSkipWhile_else5:
L_kuro_fn_VMSkipWhile_endif6:
L_kuro_fn_VMSkipWhile_endif4:
    b L_kuro_fn_VMSkipWhile_while_start0
L_kuro_fn_VMSkipWhile_while_end1:
    mov x0, #0
    mov x15, #336
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMRunWhile:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #816
    sub sp, sp, x15
    str x0, [sp, #0]
    mov x0, #1
    str x0, [sp, #176]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #176]
    add x0, x0, x1
    adrp x2, _kuro_global_141@PAGE
    add x2, x2, _kuro_global_141@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #184]
    adrp x0, _kuro_global_140@PAGE
    add x0, x0, _kuro_global_140@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #272]
    ldr x0, [sp, #184]
    ldr x1, [sp, #272]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    cbz w0, L_kuro_fn_VMRunWhile_else0
    mov x0, #0
    str x0, [sp, #448]
    adrp x1, _kuro_collection_len_17@PAGE
    add x1, x1, _kuro_collection_len_17@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_17@PAGE
    add x2, x2, _kuro_collection_17@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #448]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_17@PAGE
    add x2, x2, _kuro_collection_len_17@PAGEOFF
    str x1, [x2]
    mov x0, #0
    str x0, [sp, #536]
    adrp x1, _kuro_collection_len_16@PAGE
    add x1, x1, _kuro_collection_len_16@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_16@PAGE
    add x2, x2, _kuro_collection_16@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #536]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_16@PAGE
    add x2, x2, _kuro_collection_len_16@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #624]
    adrp x0, _kuro_global_140@PAGE
    add x0, x0, _kuro_global_140@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #624]
    add x0, x0, x1
    adrp x2, _kuro_global_140@PAGE
    add x2, x2, _kuro_global_140@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMRunWhile_endif1
L_kuro_fn_VMRunWhile_else0:
L_kuro_fn_VMRunWhile_endif1:
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #712]
    mov x0, #0
    str x0, [sp, #760]
    ldr x1, [sp, #712]
    ldr x0, [sp, #760]
    adrp x2, _kuro_collection_17@PAGE
    add x2, x2, _kuro_collection_17@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #0
    str x0, [sp, #768]
    ldr x0, [sp, #768]
    str x0, [sp, #48]
L_kuro_fn_VMRunWhile_while_start2:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #208]
    ldr x0, [sp, #48]
    str x0, [sp, #216]
    mov x0, #0
    str x0, [sp, #224]
    ldr x0, [sp, #216]
    ldr x1, [sp, #224]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #232]
    ldr x0, [sp, #208]
    ldr x1, [sp, #232]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #240]
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    mov x0, #0
    str x0, [sp, #256]
    ldr x0, [sp, #248]
    ldr x1, [sp, #256]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #264]
    ldr x0, [sp, #240]
    ldr x1, [sp, #264]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    cbz w0, L_kuro_fn_VMRunWhile_while_end3
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #288]
    ldr x1, [sp, #288]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #304]
    adrp x0, L_kuro_data_95@PAGE
    add x0, x0, L_kuro_data_95@PAGEOFF
    str x0, [sp, #312]
    ldr x0, [sp, #304]
    ldr x1, [sp, #312]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    cbz w0, L_kuro_fn_VMRunWhile_else5
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #328]
    mov x0, #1
    str x0, [sp, #336]
    ldr x0, [sp, #328]
    ldr x1, [sp, #336]
    add x0, x0, x1
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_VMPop
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #368]
    mov x0, #0
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    cbz w0, L_kuro_fn_VMRunWhile_else7
    mov x0, #0
    str x0, [sp, #392]
    ldr x0, [sp, #392]
    bl _kuro_fn_VMSkipWhile
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #408]
    mov x0, #1
    str x0, [sp, #416]
    ldr x1, [sp, #408]
    ldr x0, [sp, #416]
    adrp x2, _kuro_collection_17@PAGE
    add x2, x2, _kuro_collection_17@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #1
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    str x0, [sp, #48]
    b L_kuro_fn_VMRunWhile_endif8
L_kuro_fn_VMRunWhile_else7:
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #432]
    mov x0, #0
    str x0, [sp, #440]
    ldr x1, [sp, #432]
    ldr x0, [sp, #440]
    adrp x2, _kuro_collection_16@PAGE
    add x2, x2, _kuro_collection_16@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #0
    str x0, [sp, #456]
    ldr x0, [sp, #456]
    str x0, [sp, #40]
L_kuro_fn_VMRunWhile_while_start9:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #464]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #472]
    ldr x0, [sp, #464]
    ldr x1, [sp, #472]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #480]
    ldr x0, [sp, #40]
    str x0, [sp, #488]
    mov x0, #0
    str x0, [sp, #496]
    ldr x0, [sp, #488]
    ldr x1, [sp, #496]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #504]
    ldr x0, [sp, #480]
    ldr x1, [sp, #504]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #512]
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #520]
    mov x0, #0
    str x0, [sp, #528]
    ldr x0, [sp, #520]
    ldr x1, [sp, #528]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #544]
    ldr x0, [sp, #512]
    ldr x1, [sp, #544]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #552]
    ldr x0, [sp, #552]
    cbz w0, L_kuro_fn_VMRunWhile_while_end10
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #560]
    ldr x1, [sp, #560]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #568]
    ldr x0, [sp, #568]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #576]
    adrp x0, L_kuro_data_96@PAGE
    add x0, x0, L_kuro_data_96@PAGEOFF
    str x0, [sp, #584]
    ldr x0, [sp, #576]
    ldr x1, [sp, #584]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #592]
    ldr x0, [sp, #592]
    cbz w0, L_kuro_fn_VMRunWhile_else12
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #600]
    mov x0, #1
    str x0, [sp, #608]
    ldr x0, [sp, #600]
    ldr x1, [sp, #608]
    add x0, x0, x1
    str x0, [sp, #616]
    ldr x0, [sp, #616]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #632]
    mov x0, #1
    str x0, [sp, #640]
    ldr x1, [sp, #632]
    ldr x0, [sp, #640]
    adrp x2, _kuro_collection_16@PAGE
    add x2, x2, _kuro_collection_16@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    mov x0, #1
    str x0, [sp, #648]
    ldr x0, [sp, #648]
    str x0, [sp, #40]
    b L_kuro_fn_VMRunWhile_endif13
L_kuro_fn_VMRunWhile_else12:
    bl _kuro_fn_VMStep
    str x0, [sp, #656]
    ldr x0, [sp, #656]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #664]
    ldr x1, [sp, #664]
    adrp x2, _kuro_collection_16@PAGE
    add x2, x2, _kuro_collection_16@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #672]
    ldr x0, [sp, #672]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #680]
    ldr x0, [sp, #680]
    str x0, [sp, #40]
L_kuro_fn_VMRunWhile_endif13:
    b L_kuro_fn_VMRunWhile_while_start9
L_kuro_fn_VMRunWhile_while_end10:
    ldr x0, [sp, #0]
    str x0, [sp, #688]
    ldr x0, [sp, #688]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMRunWhile_endif8:
    b L_kuro_fn_VMRunWhile_endif6
L_kuro_fn_VMRunWhile_else5:
    bl _kuro_fn_VMStep
    str x0, [sp, #696]
    ldr x0, [sp, #696]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMRunWhile_endif6:
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #704]
    ldr x1, [sp, #704]
    adrp x2, _kuro_collection_17@PAGE
    add x2, x2, _kuro_collection_17@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #720]
    ldr x0, [sp, #720]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #728]
    ldr x0, [sp, #728]
    str x0, [sp, #48]
    b L_kuro_fn_VMRunWhile_while_start2
L_kuro_fn_VMRunWhile_while_end3:
    adrp x0, _kuro_global_141@PAGE
    add x0, x0, _kuro_global_141@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #736]
    mov x0, #1
    str x0, [sp, #744]
    ldr x0, [sp, #736]
    ldr x1, [sp, #744]
    sub x0, x0, x1
    str x0, [sp, #752]
    ldr x0, [sp, #752]
    adrp x2, _kuro_global_141@PAGE
    add x2, x2, _kuro_global_141@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #816
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMSkipFunction:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #224
    sub sp, sp, x15
    mov x0, #0
    str x0, [sp, #48]
    ldr x0, [sp, #48]
    str x0, [sp, #16]
L_kuro_fn_VMSkipFunction_while_start0:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #144]
    ldr x0, [sp, #56]
    ldr x1, [sp, #144]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #152]
    ldr x0, [sp, #16]
    str x0, [sp, #160]
    mov x0, #0
    str x0, [sp, #168]
    ldr x0, [sp, #160]
    ldr x1, [sp, #168]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #176]
    ldr x0, [sp, #152]
    ldr x1, [sp, #176]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    cbz w0, L_kuro_fn_VMSkipFunction_while_end1
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    ldr x1, [sp, #192]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    adrp x0, L_kuro_data_97@PAGE
    add x0, x0, L_kuro_data_97@PAGEOFF
    str x0, [sp, #72]
    ldr x0, [sp, #64]
    ldr x1, [sp, #72]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #80]
    ldr x0, [sp, #80]
    cbz w0, L_kuro_fn_VMSkipFunction_else3
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #88]
    mov x0, #1
    str x0, [sp, #96]
    ldr x0, [sp, #88]
    ldr x1, [sp, #96]
    add x0, x0, x1
    str x0, [sp, #104]
    ldr x0, [sp, #104]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #16]
    b L_kuro_fn_VMSkipFunction_endif4
L_kuro_fn_VMSkipFunction_else3:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #120]
    mov x0, #1
    str x0, [sp, #128]
    ldr x0, [sp, #120]
    ldr x1, [sp, #128]
    add x0, x0, x1
    str x0, [sp, #136]
    ldr x0, [sp, #136]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMSkipFunction_endif4:
    b L_kuro_fn_VMSkipFunction_while_start0
L_kuro_fn_VMSkipFunction_while_end1:
    mov x0, #0
    mov x15, #224
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMCollectParams:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #240
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #80]
    ldr x1, [sp, #80]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #176]
    adrp x0, L_kuro_data_98@PAGE
    add x0, x0, L_kuro_data_98@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMCollectParams_else0
    ldr x0, [sp, #0]
    str x0, [sp, #200]
    mov x0, #1
    str x0, [sp, #208]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    add x0, x0, x1
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    adrp x2, _kuro_global_82@PAGE
    add x2, x2, _kuro_global_82@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_82@PAGE
    add x0, x0, _kuro_global_82@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #224]
    ldr x1, [sp, #224]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #96]
    adrp x1, _kuro_collection_len_11@PAGE
    add x1, x1, _kuro_collection_len_11@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_11@PAGE
    add x2, x2, _kuro_collection_11@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #96]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_11@PAGE
    add x2, x2, _kuro_collection_len_11@PAGEOFF
    str x1, [x2]
    adrp x0, _kuro_global_81@PAGE
    add x0, x0, _kuro_global_81@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    mov x0, #1
    str x0, [sp, #112]
    ldr x0, [sp, #104]
    ldr x1, [sp, #112]
    add x0, x0, x1
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_81@PAGE
    add x2, x2, _kuro_global_81@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #0]
    str x0, [sp, #128]
    mov x0, #3
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    add x0, x0, x1
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_83@PAGE
    add x2, x2, _kuro_global_83@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_83@PAGE
    add x0, x0, _kuro_global_83@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    bl _kuro_fn_VMCollectParams
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMCollectParams_endif1
L_kuro_fn_VMCollectParams_else0:
    ldr x0, [sp, #0]
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    adrp x2, _kuro_global_59@PAGE
    add x2, x2, _kuro_global_59@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMCollectParams_endif1:
    mov x0, #0
    mov x15, #240
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMFindFunction:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #448
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    str x0, [sp, #48]
    mov x0, #0
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    str x0, [sp, #40]
L_kuro_fn_VMFindFunction_while_start0:
    ldr x0, [sp, #48]
    str x0, [sp, #240]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #328]
    ldr x0, [sp, #240]
    ldr x1, [sp, #328]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #384]
    ldr x0, [sp, #40]
    str x0, [sp, #392]
    mov x0, #0
    str x0, [sp, #400]
    ldr x0, [sp, #392]
    ldr x1, [sp, #400]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #408]
    ldr x0, [sp, #384]
    ldr x1, [sp, #408]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    cbz w0, L_kuro_fn_VMFindFunction_while_end1
    ldr x0, [sp, #48]
    str x0, [sp, #424]
    ldr x1, [sp, #424]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    adrp x0, L_kuro_data_99@PAGE
    add x0, x0, L_kuro_data_99@PAGEOFF
    str x0, [sp, #176]
    ldr x0, [sp, #168]
    ldr x1, [sp, #176]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    cbz w0, L_kuro_fn_VMFindFunction_else3
    ldr x0, [sp, #48]
    str x0, [sp, #192]
    mov x0, #1
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    add x0, x0, x1
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    adrp x2, _kuro_global_52@PAGE
    add x2, x2, _kuro_global_52@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_52@PAGE
    add x0, x0, _kuro_global_52@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    ldr x1, [sp, #216]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #248]
    ldr x0, [sp, #232]
    ldr x1, [sp, #248]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    cbz w0, L_kuro_fn_VMFindFunction_else5
    adrp x0, L_kuro_data_100@PAGE
    add x0, x0, L_kuro_data_100@PAGEOFF
    str x0, [sp, #264]
    adrp x0, L_kuro_data_101@PAGE
    add x0, x0, L_kuro_data_101@PAGEOFF
    str x0, [sp, #272]
    ldr x0, [sp, #264]
    adrp x1, _kuro_collection_11@PAGE
    add x1, x1, _kuro_collection_11@PAGEOFF
    str x0, [x1, #0]
    ldr x0, [sp, #272]
    adrp x1, _kuro_collection_11@PAGE
    add x1, x1, _kuro_collection_11@PAGEOFF
    str x0, [x1, #8]
    mov x0, #2
    adrp x2, _kuro_collection_len_11@PAGE
    add x2, x2, _kuro_collection_len_11@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    adrp x2, _kuro_global_81@PAGE
    add x2, x2, _kuro_global_81@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #48]
    str x0, [sp, #288]
    mov x0, #2
    str x0, [sp, #296]
    ldr x0, [sp, #288]
    ldr x1, [sp, #296]
    add x0, x0, x1
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    adrp x2, _kuro_global_84@PAGE
    add x2, x2, _kuro_global_84@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_84@PAGE
    add x0, x0, _kuro_global_84@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    bl _kuro_fn_VMCollectParams
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    str x0, [sp, #40]
    b L_kuro_fn_VMFindFunction_endif6
L_kuro_fn_VMFindFunction_else5:
L_kuro_fn_VMFindFunction_endif6:
    b L_kuro_fn_VMFindFunction_endif4
L_kuro_fn_VMFindFunction_else3:
L_kuro_fn_VMFindFunction_endif4:
    mov x0, #1
    str x0, [sp, #344]
    ldr x0, [sp, #48]
    ldr x1, [sp, #344]
    add x0, x0, x1
    str x0, [sp, #48]
    b L_kuro_fn_VMFindFunction_while_start0
L_kuro_fn_VMFindFunction_while_end1:
    ldr x0, [sp, #40]
    str x0, [sp, #352]
    mov x0, #0
    str x0, [sp, #360]
    ldr x0, [sp, #352]
    ldr x1, [sp, #360]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #368]
    ldr x0, [sp, #368]
    cbz w0, L_kuro_fn_VMFindFunction_else7
    mov x0, #1
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMFindFunction_endif8
L_kuro_fn_VMFindFunction_else7:
L_kuro_fn_VMFindFunction_endif8:
    mov x0, #0
    mov x15, #448
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMInvoke:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #976
    sub sp, sp, x15
    str x0, [sp, #0]
    mov x0, #0
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #0]
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    adrp x2, _kuro_global_33@PAGE
    add x2, x2, _kuro_global_33@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #392]
    ldr x0, [sp, #392]
    bl _kuro_fn_VMFindFunction
    str x0, [sp, #480]
    ldr x0, [sp, #480]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #568]
    mov x0, #0
    str x0, [sp, #656]
    ldr x0, [sp, #568]
    ldr x1, [sp, #656]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #744]
    ldr x0, [sp, #744]
    cbz w0, L_kuro_fn_VMInvoke_else0
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #832]
    mov x0, #1
    str x0, [sp, #920]
    ldr x0, [sp, #832]
    ldr x1, [sp, #920]
    add x0, x0, x1
    str x0, [sp, #936]
    ldr x0, [sp, #936]
    adrp x2, _kuro_global_55@PAGE
    add x2, x2, _kuro_global_55@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    adrp x0, _kuro_global_89@PAGE
    add x0, x0, _kuro_global_89@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #320]
    ldr x0, [sp, #312]
    ldr x1, [sp, #320]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    cbz w0, L_kuro_fn_VMInvoke_else2
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #336]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #344]
    ldr x1, [sp, #336]
    ldr x0, [sp, #344]
    adrp x2, _kuro_collection_12@PAGE
    add x2, x2, _kuro_collection_12@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMInvoke_endif3
L_kuro_fn_VMInvoke_else2:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #352]
    adrp x1, _kuro_collection_len_12@PAGE
    add x1, x1, _kuro_collection_len_12@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_12@PAGE
    add x2, x2, _kuro_collection_12@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #352]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_12@PAGE
    add x2, x2, _kuro_collection_len_12@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #360]
    adrp x0, _kuro_global_89@PAGE
    add x0, x0, _kuro_global_89@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #360]
    add x0, x0, x1
    adrp x2, _kuro_global_89@PAGE
    add x2, x2, _kuro_global_89@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMInvoke_endif3:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #368]
    adrp x0, _kuro_global_57@PAGE
    add x0, x0, _kuro_global_57@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #376]
    ldr x0, [sp, #368]
    ldr x1, [sp, #376]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    cbz w0, L_kuro_fn_VMInvoke_else4
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #400]
    mov x0, #0
    str x0, [sp, #408]
    ldr x1, [sp, #400]
    ldr x0, [sp, #408]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMInvoke_endif5
L_kuro_fn_VMInvoke_else4:
    mov x0, #0
    str x0, [sp, #416]
    adrp x1, _kuro_collection_len_6@PAGE
    add x1, x1, _kuro_collection_len_6@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #416]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_6@PAGE
    add x2, x2, _kuro_collection_len_6@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #424]
    adrp x0, _kuro_global_57@PAGE
    add x0, x0, _kuro_global_57@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #424]
    add x0, x0, x1
    adrp x2, _kuro_global_57@PAGE
    add x2, x2, _kuro_global_57@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMInvoke_endif5:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #432]
    adrp x0, _kuro_global_58@PAGE
    add x0, x0, _kuro_global_58@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #440]
    ldr x0, [sp, #432]
    ldr x1, [sp, #440]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #448]
    ldr x0, [sp, #448]
    cbz w0, L_kuro_fn_VMInvoke_else6
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #456]
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #464]
    ldr x1, [sp, #456]
    ldr x0, [sp, #464]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #472]
    mov x0, #0
    str x0, [sp, #488]
    ldr x1, [sp, #472]
    ldr x0, [sp, #488]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    cmp x1, #65536
    b.hs L_kuro_collection_bounds
    lsl x1, x1, #3
    str x0, [x2, x1]
    b L_kuro_fn_VMInvoke_endif7
L_kuro_fn_VMInvoke_else6:
    adrp x0, _kuro_global_56@PAGE
    add x0, x0, _kuro_global_56@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #496]
    adrp x1, _kuro_collection_len_7@PAGE
    add x1, x1, _kuro_collection_len_7@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #496]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_7@PAGE
    add x2, x2, _kuro_collection_len_7@PAGEOFF
    str x1, [x2]
    mov x0, #0
    str x0, [sp, #504]
    adrp x1, _kuro_collection_len_4@PAGE
    add x1, x1, _kuro_collection_len_4@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_4@PAGE
    add x2, x2, _kuro_collection_4@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #504]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_4@PAGE
    add x2, x2, _kuro_collection_len_4@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #512]
    adrp x0, _kuro_global_58@PAGE
    add x0, x0, _kuro_global_58@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #512]
    add x0, x0, x1
    adrp x2, _kuro_global_58@PAGE
    add x2, x2, _kuro_global_58@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMInvoke_endif7:
    adrp x0, _kuro_global_81@PAGE
    add x0, x0, _kuro_global_81@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #520]
    mov x0, #1
    str x0, [sp, #528]
    ldr x0, [sp, #520]
    ldr x1, [sp, #528]
    sub x0, x0, x1
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    str x0, [sp, #104]
L_kuro_fn_VMInvoke_while_start8:
    ldr x0, [sp, #104]
    str x0, [sp, #544]
    mov x0, #0
    str x0, [sp, #552]
    ldr x0, [sp, #544]
    ldr x1, [sp, #552]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #560]
    ldr x0, [sp, #560]
    cbz w0, L_kuro_fn_VMInvoke_while_end9
    bl _kuro_fn_VMPop
    str x0, [sp, #576]
    ldr x0, [sp, #576]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #584]
    ldr x0, [sp, #584]
    str x0, [sp, #128]
    ldr x0, [sp, #104]
    str x0, [sp, #592]
    mov x0, #2
    str x0, [sp, #600]
    ldr x0, [sp, #592]
    ldr x1, [sp, #600]
    add x0, x0, x1
    str x0, [sp, #608]
    ldr x0, [sp, #608]
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    str x0, [sp, #616]
    ldr x1, [sp, #616]
    adrp x2, _kuro_collection_11@PAGE
    add x2, x2, _kuro_collection_11@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #624]
    ldr x0, [sp, #624]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #632]
    ldr x0, [sp, #632]
    str x0, [sp, #112]
    ldr x0, [sp, #112]
    str x0, [sp, #640]
    ldr x0, [sp, #128]
    str x0, [sp, #648]
    ldr x0, [sp, #640]
    ldr x1, [sp, #648]
    bl _kuro_fn_VMStoreFrame
    str x0, [sp, #664]
    ldr x0, [sp, #664]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #104]
    str x0, [sp, #672]
    mov x0, #1
    str x0, [sp, #680]
    ldr x0, [sp, #672]
    ldr x1, [sp, #680]
    sub x0, x0, x1
    str x0, [sp, #688]
    ldr x0, [sp, #688]
    str x0, [sp, #104]
    b L_kuro_fn_VMInvoke_while_start8
L_kuro_fn_VMInvoke_while_end9:
    mov x0, #0
    str x0, [sp, #696]
    ldr x0, [sp, #696]
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_59@PAGE
    add x0, x0, _kuro_global_59@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #704]
    ldr x0, [sp, #704]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMInvoke_while_start11:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #712]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #720]
    ldr x0, [sp, #712]
    ldr x1, [sp, #720]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #728]
    adrp x0, _kuro_global_88@PAGE
    add x0, x0, _kuro_global_88@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #736]
    mov x0, #0
    str x0, [sp, #752]
    ldr x0, [sp, #736]
    ldr x1, [sp, #752]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #760]
    ldr x0, [sp, #728]
    ldr x1, [sp, #760]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #768]
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #776]
    mov x0, #0
    str x0, [sp, #784]
    ldr x0, [sp, #776]
    ldr x1, [sp, #784]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #792]
    ldr x0, [sp, #768]
    ldr x1, [sp, #792]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #800]
    ldr x0, [sp, #800]
    cbz w0, L_kuro_fn_VMInvoke_while_end12
    bl _kuro_fn_VMStep
    str x0, [sp, #808]
    ldr x0, [sp, #808]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMInvoke_while_start11
L_kuro_fn_VMInvoke_while_end12:
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #816]
    ldr x1, [sp, #816]
    adrp x2, _kuro_collection_12@PAGE
    add x2, x2, _kuro_collection_12@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #824]
    ldr x0, [sp, #824]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #840]
    ldr x0, [sp, #840]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #848]
    ldr x1, [sp, #848]
    adrp x2, _kuro_collection_7@PAGE
    add x2, x2, _kuro_collection_7@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #856]
    ldr x0, [sp, #856]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #864]
    ldr x0, [sp, #864]
    adrp x2, _kuro_global_56@PAGE
    add x2, x2, _kuro_global_56@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #872]
    mov x0, #1
    str x0, [sp, #880]
    ldr x0, [sp, #872]
    ldr x1, [sp, #880]
    sub x0, x0, x1
    str x0, [sp, #888]
    ldr x0, [sp, #888]
    adrp x2, _kuro_global_55@PAGE
    add x2, x2, _kuro_global_55@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #896]
    ldr x0, [sp, #896]
    bl _kuro_fn_VMSetResult
    str x0, [sp, #904]
    ldr x0, [sp, #904]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_90@PAGE
    add x0, x0, _kuro_global_90@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #912]
    ldr x0, [sp, #912]
    bl _kuro_fn_VMPush
    str x0, [sp, #928]
    ldr x0, [sp, #928]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMInvoke_endif1
L_kuro_fn_VMInvoke_else0:
L_kuro_fn_VMInvoke_endif1:
    mov x0, #0
    mov x15, #976
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMDecodeDigit:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #512
    sub sp, sp, x15
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #176]
    adrp x0, L_kuro_data_102@PAGE
    add x0, x0, L_kuro_data_102@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #176]
    ldr x1, [sp, #184]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    cbz w0, L_kuro_fn_VMDecodeDigit_else0
    mov x0, #0
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif1
L_kuro_fn_VMDecodeDigit_else0:
    ldr x0, [sp, #0]
    str x0, [sp, #448]
    adrp x0, L_kuro_data_103@PAGE
    add x0, x0, L_kuro_data_103@PAGEOFF
    str x0, [sp, #472]
    ldr x0, [sp, #448]
    ldr x1, [sp, #472]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #480]
    ldr x0, [sp, #480]
    cbz w0, L_kuro_fn_VMDecodeDigit_else2
    mov x0, #1
    str x0, [sp, #488]
    ldr x0, [sp, #488]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif3
L_kuro_fn_VMDecodeDigit_else2:
    ldr x0, [sp, #0]
    str x0, [sp, #496]
    adrp x0, L_kuro_data_104@PAGE
    add x0, x0, L_kuro_data_104@PAGEOFF
    str x0, [sp, #504]
    ldr x0, [sp, #496]
    ldr x1, [sp, #504]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_VMDecodeDigit_else4
    mov x0, #2
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif5
L_kuro_fn_VMDecodeDigit_else4:
    ldr x0, [sp, #0]
    str x0, [sp, #208]
    adrp x0, L_kuro_data_105@PAGE
    add x0, x0, L_kuro_data_105@PAGEOFF
    str x0, [sp, #216]
    ldr x0, [sp, #208]
    ldr x1, [sp, #216]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    cbz w0, L_kuro_fn_VMDecodeDigit_else6
    mov x0, #3
    str x0, [sp, #232]
    ldr x0, [sp, #232]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif7
L_kuro_fn_VMDecodeDigit_else6:
    ldr x0, [sp, #0]
    str x0, [sp, #240]
    adrp x0, L_kuro_data_106@PAGE
    add x0, x0, L_kuro_data_106@PAGEOFF
    str x0, [sp, #248]
    ldr x0, [sp, #240]
    ldr x1, [sp, #248]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    cbz w0, L_kuro_fn_VMDecodeDigit_else8
    mov x0, #4
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif9
L_kuro_fn_VMDecodeDigit_else8:
    ldr x0, [sp, #0]
    str x0, [sp, #280]
    adrp x0, L_kuro_data_107@PAGE
    add x0, x0, L_kuro_data_107@PAGEOFF
    str x0, [sp, #288]
    ldr x0, [sp, #280]
    ldr x1, [sp, #288]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    cbz w0, L_kuro_fn_VMDecodeDigit_else10
    mov x0, #5
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif11
L_kuro_fn_VMDecodeDigit_else10:
    ldr x0, [sp, #0]
    str x0, [sp, #312]
    adrp x0, L_kuro_data_108@PAGE
    add x0, x0, L_kuro_data_108@PAGEOFF
    str x0, [sp, #320]
    ldr x0, [sp, #312]
    ldr x1, [sp, #320]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    cbz w0, L_kuro_fn_VMDecodeDigit_else12
    mov x0, #6
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif13
L_kuro_fn_VMDecodeDigit_else12:
    ldr x0, [sp, #0]
    str x0, [sp, #344]
    adrp x0, L_kuro_data_109@PAGE
    add x0, x0, L_kuro_data_109@PAGEOFF
    str x0, [sp, #352]
    ldr x0, [sp, #344]
    ldr x1, [sp, #352]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #368]
    ldr x0, [sp, #368]
    cbz w0, L_kuro_fn_VMDecodeDigit_else14
    mov x0, #7
    str x0, [sp, #376]
    ldr x0, [sp, #376]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif15
L_kuro_fn_VMDecodeDigit_else14:
    ldr x0, [sp, #0]
    str x0, [sp, #384]
    adrp x0, L_kuro_data_110@PAGE
    add x0, x0, L_kuro_data_110@PAGEOFF
    str x0, [sp, #392]
    ldr x0, [sp, #384]
    ldr x1, [sp, #392]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #400]
    ldr x0, [sp, #400]
    cbz w0, L_kuro_fn_VMDecodeDigit_else16
    mov x0, #8
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif17
L_kuro_fn_VMDecodeDigit_else16:
    ldr x0, [sp, #0]
    str x0, [sp, #416]
    adrp x0, L_kuro_data_111@PAGE
    add x0, x0, L_kuro_data_111@PAGEOFF
    str x0, [sp, #424]
    ldr x0, [sp, #416]
    ldr x1, [sp, #424]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #432]
    ldr x0, [sp, #432]
    cbz w0, L_kuro_fn_VMDecodeDigit_else18
    mov x0, #9
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeDigit_endif19
L_kuro_fn_VMDecodeDigit_else18:
    mov x0, #0
    str x0, [sp, #456]
    ldr x0, [sp, #456]
    adrp x2, _kuro_global_79@PAGE
    add x2, x2, _kuro_global_79@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMDecodeDigit_endif19:
L_kuro_fn_VMDecodeDigit_endif17:
L_kuro_fn_VMDecodeDigit_endif15:
L_kuro_fn_VMDecodeDigit_endif13:
L_kuro_fn_VMDecodeDigit_endif11:
L_kuro_fn_VMDecodeDigit_endif9:
L_kuro_fn_VMDecodeDigit_endif7:
L_kuro_fn_VMDecodeDigit_endif5:
L_kuro_fn_VMDecodeDigit_endif3:
L_kuro_fn_VMDecodeDigit_endif1:
    mov x0, #0
    mov x15, #512
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMDecodeNumber:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #672
    sub sp, sp, x15
    str x0, [sp, #112]
    str x1, [sp, #32]
    str x2, [sp, #8]
    str x3, [sp, #0]
    str x4, [sp, #16]
    str x5, [sp, #24]
    ldr x0, [sp, #32]
    str x0, [sp, #192]
    ldr x0, [sp, #8]
    str x0, [sp, #200]
    ldr x0, [sp, #192]
    ldr x1, [sp, #200]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    cbz w0, L_kuro_fn_VMDecodeNumber_else0
    ldr x0, [sp, #32]
    str x0, [sp, #376]
    ldr x2, [sp, #112]
    ldr x1, [sp, #376]
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
    str x0, [sp, #464]
    ldr x0, [sp, #464]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #552]
    ldr x0, [sp, #552]
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    str x0, [sp, #632]
    adrp x0, L_kuro_data_112@PAGE
    add x0, x0, L_kuro_data_112@PAGEOFF
    str x0, [sp, #640]
    ldr x0, [sp, #632]
    ldr x1, [sp, #640]
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    str x0, [sp, #648]
    ldr x0, [sp, #648]
    cbz w0, L_kuro_fn_VMDecodeNumber_else2
    ldr x0, [sp, #32]
    str x0, [sp, #656]
    mov x0, #1
    str x0, [sp, #208]
    ldr x0, [sp, #656]
    ldr x1, [sp, #208]
    add x0, x0, x1
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    str x0, [sp, #88]
    ldr x0, [sp, #112]
    str x0, [sp, #224]
    ldr x0, [sp, #88]
    str x0, [sp, #232]
    ldr x0, [sp, #8]
    str x0, [sp, #240]
    ldr x0, [sp, #0]
    str x0, [sp, #248]
    ldr x0, [sp, #16]
    str x0, [sp, #256]
    mov x0, #1
    str x0, [sp, #264]
    ldr x0, [sp, #224]
    ldr x1, [sp, #232]
    ldr x2, [sp, #240]
    ldr x3, [sp, #248]
    ldr x4, [sp, #256]
    ldr x5, [sp, #264]
    bl _kuro_fn_VMDecodeNumber
    str x0, [sp, #272]
    ldr x0, [sp, #272]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #280]
    ldr x0, [sp, #280]
    mov x15, #672
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeNumber_endif3
L_kuro_fn_VMDecodeNumber_else2:
    ldr x0, [sp, #56]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    bl _kuro_fn_VMDecodeDigit
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    str x0, [sp, #64]
    ldr x0, [sp, #0]
    str x0, [sp, #320]
    mov x0, #10
    str x0, [sp, #328]
    ldr x0, [sp, #320]
    ldr x1, [sp, #328]
    mul x0, x0, x1
    str x0, [sp, #336]
    ldr x0, [sp, #64]
    str x0, [sp, #344]
    ldr x0, [sp, #336]
    ldr x1, [sp, #344]
    add x0, x0, x1
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    str x0, [sp, #96]
    ldr x0, [sp, #24]
    str x0, [sp, #360]
    mov x0, #1
    str x0, [sp, #368]
    ldr x0, [sp, #360]
    ldr x1, [sp, #368]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #384]
    ldr x0, [sp, #384]
    cbz w0, L_kuro_fn_VMDecodeNumber_else4
    ldr x0, [sp, #16]
    str x0, [sp, #392]
    mov x0, #10
    str x0, [sp, #400]
    ldr x0, [sp, #392]
    ldr x1, [sp, #400]
    mul x0, x0, x1
    str x0, [sp, #408]
    ldr x0, [sp, #408]
    str x0, [sp, #104]
    b L_kuro_fn_VMDecodeNumber_endif5
L_kuro_fn_VMDecodeNumber_else4:
    ldr x0, [sp, #16]
    str x0, [sp, #416]
    ldr x0, [sp, #416]
    str x0, [sp, #104]
L_kuro_fn_VMDecodeNumber_endif5:
    ldr x0, [sp, #32]
    str x0, [sp, #424]
    mov x0, #1
    str x0, [sp, #432]
    ldr x0, [sp, #424]
    ldr x1, [sp, #432]
    add x0, x0, x1
    str x0, [sp, #440]
    ldr x0, [sp, #440]
    str x0, [sp, #88]
    ldr x0, [sp, #112]
    str x0, [sp, #448]
    ldr x0, [sp, #88]
    str x0, [sp, #456]
    ldr x0, [sp, #8]
    str x0, [sp, #472]
    ldr x0, [sp, #96]
    str x0, [sp, #480]
    ldr x0, [sp, #104]
    str x0, [sp, #488]
    ldr x0, [sp, #24]
    str x0, [sp, #496]
    ldr x0, [sp, #448]
    ldr x1, [sp, #456]
    ldr x2, [sp, #472]
    ldr x3, [sp, #480]
    ldr x4, [sp, #488]
    ldr x5, [sp, #496]
    bl _kuro_fn_VMDecodeNumber
    str x0, [sp, #504]
    ldr x0, [sp, #504]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #512]
    ldr x0, [sp, #512]
    mov x15, #672
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMDecodeNumber_endif3:
    b L_kuro_fn_VMDecodeNumber_endif1
L_kuro_fn_VMDecodeNumber_else0:
    ldr x0, [sp, #24]
    str x0, [sp, #520]
    mov x0, #1
    str x0, [sp, #528]
    ldr x0, [sp, #520]
    ldr x1, [sp, #528]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #536]
    ldr x0, [sp, #536]
    cbz w0, L_kuro_fn_VMDecodeNumber_else6
    ldr x0, [sp, #0]
    str x0, [sp, #544]
    adrp x0, L_kuro_float_113@PAGE
    add x0, x0, L_kuro_float_113@PAGEOFF
    ldr d0, [x0]
    fmov x0, d0
    str x0, [sp, #560]
    ldr x0, [sp, #544]
    ldr x1, [sp, #560]
    scvtf d0, x0
    fmov d1, x1
    fmul d0, d0, d1
    fmov x0, d0
    str x0, [sp, #568]
    ldr x0, [sp, #568]
    str x0, [sp, #72]
    ldr x0, [sp, #16]
    str x0, [sp, #576]
    adrp x0, L_kuro_float_114@PAGE
    add x0, x0, L_kuro_float_114@PAGEOFF
    ldr d0, [x0]
    fmov x0, d0
    str x0, [sp, #584]
    ldr x0, [sp, #576]
    ldr x1, [sp, #584]
    scvtf d0, x0
    fmov d1, x1
    fmul d0, d0, d1
    fmov x0, d0
    str x0, [sp, #592]
    ldr x0, [sp, #592]
    str x0, [sp, #80]
    ldr x0, [sp, #72]
    str x0, [sp, #600]
    ldr x0, [sp, #80]
    str x0, [sp, #608]
    ldr x0, [sp, #600]
    ldr x1, [sp, #608]
    fmov d0, x0
    fmov d1, x1
    fdiv d0, d0, d1
    fmov x0, d0
    str x0, [sp, #616]
    ldr x0, [sp, #616]
    mov x15, #672
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeNumber_endif7
L_kuro_fn_VMDecodeNumber_else6:
    ldr x0, [sp, #0]
    str x0, [sp, #624]
    ldr x0, [sp, #624]
    mov x15, #672
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMDecodeNumber_endif7:
L_kuro_fn_VMDecodeNumber_endif1:
    mov x0, #0
    mov x15, #672
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMDecodeConstant:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #368
    sub sp, sp, x15
    str x0, [sp, #40]
    ldr x0, [sp, #40]
    cbz x0, L_kuro_fn_VMDecodeConstant_length_zero_t0
    bl _strlen
    b L_kuro_fn_VMDecodeConstant_length_done_t0
L_kuro_fn_VMDecodeConstant_length_zero_t0:
    mov x0, #0
L_kuro_fn_VMDecodeConstant_length_done_t0:
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    str x0, [sp, #0]
    ldr x0, [sp, #0]
    str x0, [sp, #216]
    mov x0, #0
    str x0, [sp, #304]
    ldr x0, [sp, #216]
    ldr x1, [sp, #304]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #320]
    ldr x0, [sp, #320]
    cbz w0, L_kuro_fn_VMDecodeConstant_else0
    ldr x0, [sp, #40]
    str x0, [sp, #328]
    ldr x0, [sp, #328]
    mov x15, #368
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeConstant_endif1
L_kuro_fn_VMDecodeConstant_else0:
L_kuro_fn_VMDecodeConstant_endif1:
    mov x0, #1
    str x0, [sp, #336]
    ldr x0, [sp, #336]
    adrp x2, _kuro_global_79@PAGE
    add x2, x2, _kuro_global_79@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #0]
    str x0, [sp, #344]
    mov x0, #1
    str x0, [sp, #352]
    ldr x0, [sp, #344]
    ldr x1, [sp, #352]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #360]
    ldr x0, [sp, #360]
    cbz w0, L_kuro_fn_VMDecodeConstant_else2
    mov x0, #0
    str x0, [sp, #136]
    ldr x2, [sp, #40]
    ldr x1, [sp, #136]
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
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x0, [sp, #152]
    bl _kuro_fn_VMDecodeDigit
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_79@PAGE
    add x0, x0, _kuro_global_79@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    mov x0, #1
    str x0, [sp, #176]
    ldr x0, [sp, #168]
    ldr x1, [sp, #176]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    cbz w0, L_kuro_fn_VMDecodeConstant_else4
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    mov x15, #368
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeConstant_endif5
L_kuro_fn_VMDecodeConstant_else4:
L_kuro_fn_VMDecodeConstant_endif5:
    b L_kuro_fn_VMDecodeConstant_endif3
L_kuro_fn_VMDecodeConstant_else2:
L_kuro_fn_VMDecodeConstant_endif3:
    ldr x0, [sp, #40]
    str x0, [sp, #200]
    mov x0, #0
    str x0, [sp, #208]
    ldr x0, [sp, #0]
    str x0, [sp, #224]
    mov x0, #0
    str x0, [sp, #232]
    mov x0, #1
    str x0, [sp, #240]
    mov x0, #0
    str x0, [sp, #248]
    ldr x0, [sp, #200]
    ldr x1, [sp, #208]
    ldr x2, [sp, #224]
    ldr x3, [sp, #232]
    ldr x4, [sp, #240]
    ldr x5, [sp, #248]
    bl _kuro_fn_VMDecodeNumber
    str x0, [sp, #256]
    ldr x0, [sp, #256]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #264]
    ldr x0, [sp, #264]
    str x0, [sp, #8]
    adrp x0, _kuro_global_79@PAGE
    add x0, x0, _kuro_global_79@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #272]
    mov x0, #1
    str x0, [sp, #280]
    ldr x0, [sp, #272]
    ldr x1, [sp, #280]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    cbz w0, L_kuro_fn_VMDecodeConstant_else6
    ldr x0, [sp, #8]
    str x0, [sp, #296]
    ldr x0, [sp, #296]
    mov x15, #368
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMDecodeConstant_endif7
L_kuro_fn_VMDecodeConstant_else6:
    ldr x0, [sp, #40]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    mov x15, #368
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
L_kuro_fn_VMDecodeConstant_endif7:
    mov x0, #0
    mov x15, #368
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMStep:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #5824
    sub sp, sp, x15
    mov x0, #0
    str x0, [sp, #1616]
    ldr x0, [sp, #1616]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1624]
    ldr x1, [sp, #1624]
    adrp x2, _kuro_collection_0@PAGE
    add x2, x2, _kuro_collection_0@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #2512]
    ldr x0, [sp, #2512]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3400]
    ldr x0, [sp, #3400]
    str x0, [sp, #360]
    mov x0, #1
    str x0, [sp, #4288]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #4288]
    add x0, x0, x1
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #360]
    str x0, [sp, #5176]
    adrp x0, L_kuro_data_115@PAGE
    add x0, x0, L_kuro_data_115@PAGEOFF
    str x0, [sp, #5448]
    ldr x0, [sp, #5176]
    ldr x1, [sp, #5448]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t7
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t7
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t7
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t7
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t7
L_kuro_fn_VMStep_cmp_numeric_t7:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t7:
    str x0, [sp, #5536]
    ldr x0, [sp, #5536]
    cbz w0, L_kuro_fn_VMStep_else0
    bl _kuro_fn_VMPop
    str x0, [sp, #5624]
    ldr x0, [sp, #5624]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5712]
    mov x0, #0
    str x0, [sp, #1632]
    ldr x0, [sp, #5712]
    ldr x1, [sp, #1632]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t11
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t11
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t11
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t11
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t11
L_kuro_fn_VMStep_cmp_numeric_t11:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t11:
    str x0, [sp, #1720]
    ldr x0, [sp, #1720]
    cbz w0, L_kuro_fn_VMStep_else2
    mov x0, #0
    str x0, [sp, #1808]
    ldr x0, [sp, #1808]
    bl _kuro_fn_VMSkipFalse
    str x0, [sp, #1896]
    ldr x0, [sp, #1896]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif3
L_kuro_fn_VMStep_else2:
L_kuro_fn_VMStep_endif3:
    mov x0, #0
    str x0, [sp, #1984]
    ldr x0, [sp, #1984]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif1
L_kuro_fn_VMStep_else0:
L_kuro_fn_VMStep_endif1:
    ldr x0, [sp, #360]
    str x0, [sp, #2072]
    adrp x0, L_kuro_data_116@PAGE
    add x0, x0, L_kuro_data_116@PAGEOFF
    str x0, [sp, #2160]
    ldr x0, [sp, #2072]
    ldr x1, [sp, #2160]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t17
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t17
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t17
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t17
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t17
L_kuro_fn_VMStep_cmp_numeric_t17:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t17:
    str x0, [sp, #2248]
    ldr x0, [sp, #2248]
    cbz w0, L_kuro_fn_VMStep_else4
    mov x0, #0
    str x0, [sp, #2336]
    ldr x0, [sp, #2336]
    bl _kuro_fn_VMSkipElse
    str x0, [sp, #2424]
    ldr x0, [sp, #2424]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2520]
    ldr x0, [sp, #2520]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif5
L_kuro_fn_VMStep_else4:
L_kuro_fn_VMStep_endif5:
    ldr x0, [sp, #360]
    str x0, [sp, #2608]
    adrp x0, L_kuro_data_117@PAGE
    add x0, x0, L_kuro_data_117@PAGEOFF
    str x0, [sp, #2696]
    ldr x0, [sp, #2608]
    ldr x1, [sp, #2696]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t23
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t23
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t23
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t23
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t23
L_kuro_fn_VMStep_cmp_numeric_t23:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t23:
    str x0, [sp, #2784]
    ldr x0, [sp, #2784]
    cbz w0, L_kuro_fn_VMStep_else6
    mov x0, #0
    str x0, [sp, #2872]
    ldr x0, [sp, #2872]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif7
L_kuro_fn_VMStep_else6:
L_kuro_fn_VMStep_endif7:
    ldr x0, [sp, #360]
    str x0, [sp, #2960]
    adrp x0, L_kuro_data_118@PAGE
    add x0, x0, L_kuro_data_118@PAGEOFF
    str x0, [sp, #3048]
    ldr x0, [sp, #2960]
    ldr x1, [sp, #3048]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t27
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t27
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t27
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t27
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t27
L_kuro_fn_VMStep_cmp_numeric_t27:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t27:
    str x0, [sp, #3136]
    ldr x0, [sp, #3136]
    cbz w0, L_kuro_fn_VMStep_else8
    bl _kuro_fn_VMPop
    str x0, [sp, #3224]
    ldr x0, [sp, #3224]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3312]
    ldr x0, [sp, #3312]
    str x0, [sp, #296]
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3408]
    ldr x0, [sp, #3408]
    str x0, [sp, #408]
    ldr x0, [sp, #296]
    str x0, [sp, #3496]
    ldr x0, [sp, #408]
    str x0, [sp, #3584]
    ldr x0, [sp, #3496]
    ldr x1, [sp, #3584]
    bl _kuro_fn_VMRunRepeat
    str x0, [sp, #3672]
    ldr x0, [sp, #3672]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3760]
    ldr x0, [sp, #3760]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif9
L_kuro_fn_VMStep_else8:
L_kuro_fn_VMStep_endif9:
    ldr x0, [sp, #360]
    str x0, [sp, #3848]
    adrp x0, L_kuro_data_119@PAGE
    add x0, x0, L_kuro_data_119@PAGEOFF
    str x0, [sp, #3936]
    ldr x0, [sp, #3848]
    ldr x1, [sp, #3936]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t37
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t37
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t37
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t37
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t37
L_kuro_fn_VMStep_cmp_numeric_t37:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t37:
    str x0, [sp, #4024]
    ldr x0, [sp, #4024]
    cbz w0, L_kuro_fn_VMStep_else10
    mov x0, #0
    str x0, [sp, #4112]
    ldr x0, [sp, #4112]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif11
L_kuro_fn_VMStep_else10:
L_kuro_fn_VMStep_endif11:
    ldr x0, [sp, #360]
    str x0, [sp, #4200]
    adrp x0, L_kuro_data_120@PAGE
    add x0, x0, L_kuro_data_120@PAGEOFF
    str x0, [sp, #4296]
    ldr x0, [sp, #4200]
    ldr x1, [sp, #4296]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t41
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t41
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t41
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t41
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t41
L_kuro_fn_VMStep_cmp_numeric_t41:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t41:
    str x0, [sp, #4384]
    ldr x0, [sp, #4384]
    cbz w0, L_kuro_fn_VMStep_else12
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4472]
    ldr x0, [sp, #4472]
    str x0, [sp, #424]
    ldr x0, [sp, #424]
    str x0, [sp, #4560]
    ldr x0, [sp, #4560]
    bl _kuro_fn_VMRunWhile
    str x0, [sp, #4648]
    ldr x0, [sp, #4648]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4736]
    ldr x0, [sp, #4736]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif13
L_kuro_fn_VMStep_else12:
L_kuro_fn_VMStep_endif13:
    ldr x0, [sp, #360]
    str x0, [sp, #4824]
    adrp x0, L_kuro_data_121@PAGE
    add x0, x0, L_kuro_data_121@PAGEOFF
    str x0, [sp, #4912]
    ldr x0, [sp, #4824]
    ldr x1, [sp, #4912]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t48
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t48
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t48
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t48
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t48
L_kuro_fn_VMStep_cmp_numeric_t48:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t48:
    str x0, [sp, #5000]
    ldr x0, [sp, #360]
    str x0, [sp, #5088]
    adrp x0, L_kuro_data_122@PAGE
    add x0, x0, L_kuro_data_122@PAGEOFF
    str x0, [sp, #5184]
    ldr x0, [sp, #5088]
    ldr x1, [sp, #5184]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t51
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t51
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t51
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t51
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t51
L_kuro_fn_VMStep_cmp_numeric_t51:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t51:
    str x0, [sp, #5272]
    ldr x0, [sp, #5000]
    ldr x1, [sp, #5272]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #5360]
    ldr x0, [sp, #5360]
    cbz w0, L_kuro_fn_VMStep_else14
    mov x0, #0
    str x0, [sp, #5392]
    ldr x0, [sp, #5392]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif15
L_kuro_fn_VMStep_else14:
L_kuro_fn_VMStep_endif15:
    ldr x0, [sp, #360]
    str x0, [sp, #5400]
    adrp x0, L_kuro_data_123@PAGE
    add x0, x0, L_kuro_data_123@PAGEOFF
    str x0, [sp, #5408]
    ldr x0, [sp, #5400]
    ldr x1, [sp, #5408]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t56
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t56
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t56
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t56
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t56
L_kuro_fn_VMStep_cmp_numeric_t56:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t56:
    str x0, [sp, #5416]
    ldr x0, [sp, #5416]
    cbz w0, L_kuro_fn_VMStep_else16
    bl _kuro_fn_VMSkipFunction
    str x0, [sp, #5424]
    ldr x0, [sp, #5424]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #5432]
    ldr x0, [sp, #5432]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif17
L_kuro_fn_VMStep_else16:
L_kuro_fn_VMStep_endif17:
    ldr x0, [sp, #360]
    str x0, [sp, #5440]
    adrp x0, L_kuro_data_124@PAGE
    add x0, x0, L_kuro_data_124@PAGEOFF
    str x0, [sp, #5456]
    ldr x0, [sp, #5440]
    ldr x1, [sp, #5456]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t61
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t61
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t61
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t61
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t61
L_kuro_fn_VMStep_cmp_numeric_t61:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t61:
    str x0, [sp, #5464]
    ldr x0, [sp, #5464]
    cbz w0, L_kuro_fn_VMStep_else18
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5472]
    mov x0, #0
    str x0, [sp, #5480]
    ldr x0, [sp, #5472]
    ldr x1, [sp, #5480]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #5488]
    ldr x0, [sp, #5488]
    cbz w0, L_kuro_fn_VMStep_else20
    mov x0, #0
    str x0, [sp, #5496]
    ldr x0, [sp, #5496]
    adrp x2, _kuro_global_90@PAGE
    add x2, x2, _kuro_global_90@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #5504]
    ldr x0, [sp, #5504]
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif21
L_kuro_fn_VMStep_else20:
L_kuro_fn_VMStep_endif21:
    mov x0, #0
    str x0, [sp, #5512]
    ldr x0, [sp, #5512]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif19
L_kuro_fn_VMStep_else18:
L_kuro_fn_VMStep_endif19:
    ldr x0, [sp, #360]
    str x0, [sp, #5520]
    adrp x0, L_kuro_data_125@PAGE
    add x0, x0, L_kuro_data_125@PAGEOFF
    str x0, [sp, #5528]
    ldr x0, [sp, #5520]
    ldr x1, [sp, #5528]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t70
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t70
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t70
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t70
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t70
L_kuro_fn_VMStep_cmp_numeric_t70:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t70:
    str x0, [sp, #5544]
    ldr x0, [sp, #5544]
    cbz w0, L_kuro_fn_VMStep_else22
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #5552]
    ldr x0, [sp, #5552]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5560]
    ldr x0, [sp, #5560]
    adrp x2, _kuro_global_33@PAGE
    add x2, x2, _kuro_global_33@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #5568]
    ldr x0, [sp, #5568]
    adrp x2, _kuro_global_34@PAGE
    add x2, x2, _kuro_global_34@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #5576]
    ldr x0, [sp, #5576]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif23
L_kuro_fn_VMStep_else22:
L_kuro_fn_VMStep_endif23:
    ldr x0, [sp, #360]
    str x0, [sp, #5584]
    adrp x0, L_kuro_data_126@PAGE
    add x0, x0, L_kuro_data_126@PAGEOFF
    str x0, [sp, #5592]
    ldr x0, [sp, #5584]
    ldr x1, [sp, #5592]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t77
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t77
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t77
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t77
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t77
L_kuro_fn_VMStep_cmp_numeric_t77:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t77:
    str x0, [sp, #5600]
    ldr x0, [sp, #5600]
    cbz w0, L_kuro_fn_VMStep_else24
    adrp x0, _kuro_global_34@PAGE
    add x0, x0, _kuro_global_34@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5608]
    mov x0, #1
    str x0, [sp, #5616]
    ldr x0, [sp, #5608]
    ldr x1, [sp, #5616]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t80
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t80
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t80
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t80
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t80
L_kuro_fn_VMStep_cmp_numeric_t80:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t80:
    str x0, [sp, #5632]
    ldr x0, [sp, #5632]
    cbz w0, L_kuro_fn_VMStep_else26
    adrp x0, _kuro_global_33@PAGE
    add x0, x0, _kuro_global_33@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5640]
    ldr x0, [sp, #5640]
    bl _kuro_fn_VMInvoke
    str x0, [sp, #5648]
    ldr x0, [sp, #5648]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #5656]
    ldr x0, [sp, #5656]
    adrp x2, _kuro_global_34@PAGE
    add x2, x2, _kuro_global_34@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #5664]
    ldr x0, [sp, #5664]
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif27
L_kuro_fn_VMStep_else26:
L_kuro_fn_VMStep_endif27:
    mov x0, #0
    str x0, [sp, #5672]
    ldr x0, [sp, #5672]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif25
L_kuro_fn_VMStep_else24:
L_kuro_fn_VMStep_endif25:
    ldr x0, [sp, #360]
    str x0, [sp, #5680]
    adrp x0, L_kuro_data_127@PAGE
    add x0, x0, L_kuro_data_127@PAGEOFF
    str x0, [sp, #5688]
    ldr x0, [sp, #5680]
    ldr x1, [sp, #5688]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t88
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t88
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t88
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t88
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t88
L_kuro_fn_VMStep_cmp_numeric_t88:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t88:
    str x0, [sp, #5696]
    ldr x0, [sp, #5696]
    cbz w0, L_kuro_fn_VMStep_else28
    bl _kuro_fn_VMPop
    str x0, [sp, #5704]
    ldr x0, [sp, #5704]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5720]
    ldr x0, [sp, #5720]
    adrp x2, _kuro_global_90@PAGE
    add x2, x2, _kuro_global_90@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #5728]
    ldr x0, [sp, #5728]
    adrp x2, _kuro_global_88@PAGE
    add x2, x2, _kuro_global_88@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #5736]
    ldr x0, [sp, #5736]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif29
L_kuro_fn_VMStep_else28:
L_kuro_fn_VMStep_endif29:
    ldr x0, [sp, #360]
    str x0, [sp, #5744]
    adrp x0, L_kuro_data_128@PAGE
    add x0, x0, L_kuro_data_128@PAGEOFF
    str x0, [sp, #5752]
    ldr x0, [sp, #5744]
    ldr x1, [sp, #5752]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t95
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t95
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t95
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t95
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t95
L_kuro_fn_VMStep_cmp_numeric_t95:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t95:
    str x0, [sp, #5760]
    ldr x0, [sp, #5760]
    cbz w0, L_kuro_fn_VMStep_else30
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #5768]
    ldr x0, [sp, #5768]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5776]
    ldr x0, [sp, #5776]
    bl _kuro_fn_VMDecodeConstant
    str x0, [sp, #5784]
    ldr x0, [sp, #5784]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5792]
    ldr x0, [sp, #5792]
    bl _kuro_fn_VMPush
    str x0, [sp, #1640]
    ldr x0, [sp, #1640]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #1648]
    ldr x0, [sp, #1648]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif31
L_kuro_fn_VMStep_else30:
L_kuro_fn_VMStep_endif31:
    ldr x0, [sp, #360]
    str x0, [sp, #1656]
    adrp x0, L_kuro_data_129@PAGE
    add x0, x0, L_kuro_data_129@PAGEOFF
    str x0, [sp, #1664]
    ldr x0, [sp, #1656]
    ldr x1, [sp, #1664]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t104
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t104
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t104
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t104
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t104
L_kuro_fn_VMStep_cmp_numeric_t104:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t104:
    str x0, [sp, #1672]
    ldr x0, [sp, #1672]
    cbz w0, L_kuro_fn_VMStep_else32
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #1680]
    ldr x0, [sp, #1680]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1688]
    ldr x0, [sp, #1688]
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    str x0, [sp, #1696]
    adrp x0, L_kuro_data_130@PAGE
    add x0, x0, L_kuro_data_130@PAGEOFF
    str x0, [sp, #1704]
    ldr x0, [sp, #1696]
    ldr x1, [sp, #1704]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t109
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t109
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t109
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t109
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t109
L_kuro_fn_VMStep_cmp_numeric_t109:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t109:
    str x0, [sp, #1712]
    ldr x0, [sp, #1712]
    cbz w0, L_kuro_fn_VMStep_else34
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1728]
    mov x0, #0
    str x0, [sp, #1736]
    ldr x0, [sp, #1728]
    ldr x1, [sp, #1736]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #1744]
    ldr x0, [sp, #1744]
    cbz w0, L_kuro_fn_VMStep_else36
    adrp x0, _kuro_global_55@PAGE
    add x0, x0, _kuro_global_55@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1752]
    ldr x1, [sp, #1752]
    adrp x2, _kuro_collection_6@PAGE
    add x2, x2, _kuro_collection_6@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #1760]
    ldr x0, [sp, #1760]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1768]
    ldr x0, [sp, #1768]
    bl _kuro_fn_VMPush
    str x0, [sp, #1776]
    ldr x0, [sp, #1776]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif37
L_kuro_fn_VMStep_else36:
    adrp x0, _kuro_global_71@PAGE
    add x0, x0, _kuro_global_71@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1784]
    ldr x0, [sp, #1784]
    bl _kuro_fn_VMPush
    str x0, [sp, #1792]
    ldr x0, [sp, #1792]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif37:
    b L_kuro_fn_VMStep_endif35
L_kuro_fn_VMStep_else34:
    ldr x0, [sp, #344]
    str x0, [sp, #1800]
    mov x0, #0
    str x0, [sp, #1816]
    ldr x0, [sp, #1800]
    ldr x1, [sp, #1816]
    bl _kuro_fn_VMFindCollection
    str x0, [sp, #1824]
    ldr x0, [sp, #1824]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1832]
    mov x0, #0
    str x0, [sp, #1840]
    ldr x0, [sp, #1832]
    ldr x1, [sp, #1840]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #1848]
    ldr x0, [sp, #1848]
    cbz w0, L_kuro_fn_VMStep_else38
    ldr x0, [sp, #344]
    str x0, [sp, #1856]
    ldr x0, [sp, #1856]
    bl _kuro_fn_VMPushCollection
    str x0, [sp, #1864]
    ldr x0, [sp, #1864]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif39
L_kuro_fn_VMStep_else38:
    ldr x0, [sp, #344]
    str x0, [sp, #1872]
    ldr x0, [sp, #1872]
    bl _kuro_fn_VMLoad
    str x0, [sp, #1880]
    ldr x0, [sp, #1880]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1888]
    ldr x0, [sp, #1888]
    bl _kuro_fn_VMPush
    str x0, [sp, #1904]
    ldr x0, [sp, #1904]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif39:
L_kuro_fn_VMStep_endif35:
    mov x0, #0
    str x0, [sp, #1912]
    ldr x0, [sp, #1912]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif33
L_kuro_fn_VMStep_else32:
L_kuro_fn_VMStep_endif33:
    ldr x0, [sp, #360]
    str x0, [sp, #1920]
    adrp x0, L_kuro_data_131@PAGE
    add x0, x0, L_kuro_data_131@PAGEOFF
    str x0, [sp, #1928]
    ldr x0, [sp, #1920]
    ldr x1, [sp, #1928]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t134
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t134
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t134
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t134
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t134
L_kuro_fn_VMStep_cmp_numeric_t134:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t134:
    str x0, [sp, #1936]
    ldr x0, [sp, #1936]
    cbz w0, L_kuro_fn_VMStep_else40
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #1944]
    ldr x0, [sp, #1944]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1952]
    ldr x0, [sp, #1952]
    str x0, [sp, #344]
    bl _kuro_fn_VMPop
    str x0, [sp, #1960]
    ldr x0, [sp, #1960]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1968]
    ldr x0, [sp, #1968]
    str x0, [sp, #416]
    adrp x0, _kuro_global_70@PAGE
    add x0, x0, _kuro_global_70@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #1976]
    mov x0, #1
    str x0, [sp, #1992]
    ldr x0, [sp, #1976]
    ldr x1, [sp, #1992]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t141
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t141
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t141
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t141
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t141
L_kuro_fn_VMStep_cmp_numeric_t141:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t141:
    str x0, [sp, #2000]
    ldr x0, [sp, #2000]
    cbz w0, L_kuro_fn_VMStep_else42
    ldr x0, [sp, #416]
    str x0, [sp, #2008]
    ldr x0, [sp, #344]
    str x0, [sp, #2016]
    ldr x0, [sp, #2008]
    ldr x1, [sp, #2016]
    bl _kuro_fn_VMCopyCollection
    str x0, [sp, #2024]
    ldr x0, [sp, #2024]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif43
L_kuro_fn_VMStep_else42:
    ldr x0, [sp, #344]
    str x0, [sp, #2032]
    ldr x0, [sp, #416]
    str x0, [sp, #2040]
    ldr x0, [sp, #2032]
    ldr x1, [sp, #2040]
    bl _kuro_fn_VMStore
    str x0, [sp, #2048]
    ldr x0, [sp, #2048]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif43:
    mov x0, #0
    str x0, [sp, #2056]
    ldr x0, [sp, #2056]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif41
L_kuro_fn_VMStep_else40:
L_kuro_fn_VMStep_endif41:
    ldr x0, [sp, #360]
    str x0, [sp, #2064]
    adrp x0, L_kuro_data_132@PAGE
    add x0, x0, L_kuro_data_132@PAGEOFF
    str x0, [sp, #2080]
    ldr x0, [sp, #2064]
    ldr x1, [sp, #2080]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t151
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t151
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t151
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t151
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t151
L_kuro_fn_VMStep_cmp_numeric_t151:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t151:
    str x0, [sp, #2088]
    ldr x0, [sp, #2088]
    cbz w0, L_kuro_fn_VMStep_else44
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #2096]
    ldr x0, [sp, #2096]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #2104]
    ldr x0, [sp, #2104]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2112]
    ldr x0, [sp, #2112]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif45
L_kuro_fn_VMStep_else44:
L_kuro_fn_VMStep_endif45:
    ldr x0, [sp, #360]
    str x0, [sp, #2120]
    adrp x0, L_kuro_data_133@PAGE
    add x0, x0, L_kuro_data_133@PAGEOFF
    str x0, [sp, #2128]
    ldr x0, [sp, #2120]
    ldr x1, [sp, #2128]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t157
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t157
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t157
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t157
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t157
L_kuro_fn_VMStep_cmp_numeric_t157:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t157:
    str x0, [sp, #2136]
    ldr x0, [sp, #2136]
    cbz w0, L_kuro_fn_VMStep_else46
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #2144]
    ldr x0, [sp, #2144]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2152]
    ldr x0, [sp, #2152]
    str x0, [sp, #344]
    adrp x0, _kuro_global_65@PAGE
    add x0, x0, _kuro_global_65@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2168]
    mov x0, #1
    str x0, [sp, #2176]
    ldr x0, [sp, #2168]
    ldr x1, [sp, #2176]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t162
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t162
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t162
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t162
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t162
L_kuro_fn_VMStep_cmp_numeric_t162:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t162:
    str x0, [sp, #2184]
    ldr x0, [sp, #2184]
    cbz w0, L_kuro_fn_VMStep_else48
    ldr x0, [sp, #344]
    str x0, [sp, #2192]
    adrp x0, _kuro_global_64@PAGE
    add x0, x0, _kuro_global_64@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2200]
    ldr x0, [sp, #2192]
    ldr x1, [sp, #2200]
    bl _kuro_fn_VMStore
    str x0, [sp, #2208]
    ldr x0, [sp, #2208]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2216]
    ldr x0, [sp, #2216]
    adrp x2, _kuro_global_65@PAGE
    add x2, x2, _kuro_global_65@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif49
L_kuro_fn_VMStep_else48:
    ldr x0, [sp, #344]
    str x0, [sp, #2224]
    adrp x0, L_kuro_data_134@PAGE
    add x0, x0, L_kuro_data_134@PAGEOFF
    str x0, [sp, #2232]
    ldr x0, [sp, #2224]
    ldr x1, [sp, #2232]
    bl _kuro_fn_VMStore
    str x0, [sp, #2240]
    ldr x0, [sp, #2240]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif49:
    mov x0, #0
    str x0, [sp, #2256]
    ldr x0, [sp, #2256]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif47
L_kuro_fn_VMStep_else46:
L_kuro_fn_VMStep_endif47:
    ldr x0, [sp, #360]
    str x0, [sp, #2264]
    adrp x0, L_kuro_data_135@PAGE
    add x0, x0, L_kuro_data_135@PAGEOFF
    str x0, [sp, #2272]
    ldr x0, [sp, #2264]
    ldr x1, [sp, #2272]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t173
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t173
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t173
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t173
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t173
L_kuro_fn_VMStep_cmp_numeric_t173:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t173:
    str x0, [sp, #2280]
    ldr x0, [sp, #2280]
    cbz w0, L_kuro_fn_VMStep_else50
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #2288]
    ldr x0, [sp, #2288]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2296]
    ldr x0, [sp, #2296]
    str x0, [sp, #368]
    bl _kuro_fn_VMPop
    str x0, [sp, #2304]
    ldr x0, [sp, #2304]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2312]
    ldr x0, [sp, #2312]
    str x0, [sp, #400]
    bl _kuro_fn_VMPop
    str x0, [sp, #2320]
    ldr x0, [sp, #2320]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2328]
    ldr x0, [sp, #2328]
    str x0, [sp, #328]
    ldr x0, [sp, #368]
    str x0, [sp, #2344]
    adrp x0, L_kuro_data_136@PAGE
    add x0, x0, L_kuro_data_136@PAGEOFF
    str x0, [sp, #2352]
    ldr x0, [sp, #2344]
    ldr x1, [sp, #2352]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t182
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t182
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t182
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t182
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t182
L_kuro_fn_VMStep_cmp_numeric_t182:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t182:
    str x0, [sp, #2360]
    ldr x0, [sp, #2360]
    cbz w0, L_kuro_fn_VMStep_else52
    ldr x0, [sp, #328]
    str x0, [sp, #2368]
    ldr x0, [sp, #400]
    str x0, [sp, #2376]
    ldr x0, [sp, #2368]
    ldr x1, [sp, #2376]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_binop_numeric_t185
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_binop_numeric_t185
    cmp x1, #0
    b.le L_kuro_fn_VMStep_binop_numeric_t185
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_binop_numeric_t185
    b L_kuro_fn_VMStep_binop_text_t185
L_kuro_fn_VMStep_binop_numeric_t185:
    add x0, x0, x1
    b L_kuro_fn_VMStep_binop_done_t185
L_kuro_fn_VMStep_binop_text_t185:
    mov x0, #4096
    bl _malloc
    str x0, [sp, #2384]
    ldr x0, [sp, #2384]
    ldr x1, [sp, #2368]
    bl _strcpy
    ldr x0, [sp, #2384]
    ldr x1, [sp, #2376]
    bl _strcat
L_kuro_fn_VMStep_binop_done_t185:
    str x0, [sp, #2384]
    ldr x0, [sp, #2384]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif53
L_kuro_fn_VMStep_else52:
    ldr x0, [sp, #368]
    str x0, [sp, #2392]
    adrp x0, L_kuro_data_137@PAGE
    add x0, x0, L_kuro_data_137@PAGEOFF
    str x0, [sp, #2400]
    ldr x0, [sp, #2392]
    ldr x1, [sp, #2400]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t188
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t188
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t188
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t188
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t188
L_kuro_fn_VMStep_cmp_numeric_t188:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t188:
    str x0, [sp, #2408]
    ldr x0, [sp, #2408]
    cbz w0, L_kuro_fn_VMStep_else54
    ldr x0, [sp, #328]
    str x0, [sp, #2416]
    ldr x0, [sp, #400]
    str x0, [sp, #2432]
    ldr x0, [sp, #2416]
    ldr x1, [sp, #2432]
    sub x0, x0, x1
    str x0, [sp, #2440]
    ldr x0, [sp, #2440]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif55
L_kuro_fn_VMStep_else54:
    ldr x0, [sp, #368]
    str x0, [sp, #2448]
    adrp x0, L_kuro_data_138@PAGE
    add x0, x0, L_kuro_data_138@PAGEOFF
    str x0, [sp, #2456]
    ldr x0, [sp, #2448]
    ldr x1, [sp, #2456]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t194
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t194
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t194
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t194
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t194
L_kuro_fn_VMStep_cmp_numeric_t194:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t194:
    str x0, [sp, #2464]
    ldr x0, [sp, #2464]
    cbz w0, L_kuro_fn_VMStep_else56
    ldr x0, [sp, #328]
    str x0, [sp, #2472]
    ldr x0, [sp, #400]
    str x0, [sp, #2480]
    ldr x0, [sp, #2472]
    ldr x1, [sp, #2480]
    mul x0, x0, x1
    str x0, [sp, #2488]
    ldr x0, [sp, #2488]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif57
L_kuro_fn_VMStep_else56:
    ldr x0, [sp, #368]
    str x0, [sp, #2496]
    adrp x0, L_kuro_data_139@PAGE
    add x0, x0, L_kuro_data_139@PAGEOFF
    str x0, [sp, #2504]
    ldr x0, [sp, #2496]
    ldr x1, [sp, #2504]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t200
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t200
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t200
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t200
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t200
L_kuro_fn_VMStep_cmp_numeric_t200:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t200:
    str x0, [sp, #2528]
    ldr x0, [sp, #2528]
    cbz w0, L_kuro_fn_VMStep_else58
    ldr x0, [sp, #328]
    str x0, [sp, #2536]
    ldr x0, [sp, #400]
    str x0, [sp, #2544]
    ldr x0, [sp, #2536]
    ldr x1, [sp, #2544]
    sdiv x0, x0, x1
    str x0, [sp, #2552]
    ldr x0, [sp, #2552]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif59
L_kuro_fn_VMStep_else58:
    mov x0, #1
    str x0, [sp, #2560]
    ldr x0, [sp, #2560]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2568]
    ldr x0, [sp, #2568]
    str x0, [sp, #392]
L_kuro_fn_VMStep_endif59:
L_kuro_fn_VMStep_endif57:
L_kuro_fn_VMStep_endif55:
L_kuro_fn_VMStep_endif53:
    ldr x0, [sp, #392]
    str x0, [sp, #2576]
    ldr x0, [sp, #2576]
    bl _kuro_fn_VMPush
    str x0, [sp, #2584]
    ldr x0, [sp, #2584]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #2592]
    ldr x0, [sp, #2592]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif51
L_kuro_fn_VMStep_else50:
L_kuro_fn_VMStep_endif51:
    ldr x0, [sp, #360]
    str x0, [sp, #2600]
    adrp x0, L_kuro_data_140@PAGE
    add x0, x0, L_kuro_data_140@PAGEOFF
    str x0, [sp, #2616]
    ldr x0, [sp, #2600]
    ldr x1, [sp, #2616]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t211
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t211
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t211
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t211
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t211
L_kuro_fn_VMStep_cmp_numeric_t211:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t211:
    str x0, [sp, #2624]
    ldr x0, [sp, #2624]
    cbz w0, L_kuro_fn_VMStep_else60
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #2632]
    ldr x0, [sp, #2632]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2640]
    ldr x0, [sp, #2640]
    str x0, [sp, #368]
    bl _kuro_fn_VMPop
    str x0, [sp, #2648]
    ldr x0, [sp, #2648]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2656]
    ldr x0, [sp, #2656]
    str x0, [sp, #400]
    bl _kuro_fn_VMPop
    str x0, [sp, #2664]
    ldr x0, [sp, #2664]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #2672]
    ldr x0, [sp, #2672]
    str x0, [sp, #328]
    mov x0, #0
    str x0, [sp, #2680]
    ldr x0, [sp, #2680]
    str x0, [sp, #392]
    ldr x0, [sp, #368]
    str x0, [sp, #2688]
    adrp x0, L_kuro_data_141@PAGE
    add x0, x0, L_kuro_data_141@PAGEOFF
    str x0, [sp, #2704]
    ldr x0, [sp, #2688]
    ldr x1, [sp, #2704]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t221
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t221
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t221
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t221
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t221
L_kuro_fn_VMStep_cmp_numeric_t221:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t221:
    str x0, [sp, #2712]
    ldr x0, [sp, #2712]
    cbz w0, L_kuro_fn_VMStep_else62
    ldr x0, [sp, #328]
    str x0, [sp, #2720]
    ldr x0, [sp, #400]
    str x0, [sp, #2728]
    ldr x0, [sp, #2720]
    ldr x1, [sp, #2728]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t224
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t224
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t224
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t224
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t224
L_kuro_fn_VMStep_cmp_numeric_t224:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t224:
    str x0, [sp, #2736]
    ldr x0, [sp, #2736]
    cbz w0, L_kuro_fn_VMStep_else64
    mov x0, #1
    str x0, [sp, #2744]
    ldr x0, [sp, #2744]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif65
L_kuro_fn_VMStep_else64:
L_kuro_fn_VMStep_endif65:
    b L_kuro_fn_VMStep_endif63
L_kuro_fn_VMStep_else62:
    ldr x0, [sp, #368]
    str x0, [sp, #2752]
    adrp x0, L_kuro_data_142@PAGE
    add x0, x0, L_kuro_data_142@PAGEOFF
    str x0, [sp, #2760]
    ldr x0, [sp, #2752]
    ldr x1, [sp, #2760]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t228
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t228
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t228
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t228
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t228
L_kuro_fn_VMStep_cmp_numeric_t228:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t228:
    str x0, [sp, #2768]
    ldr x0, [sp, #2768]
    cbz w0, L_kuro_fn_VMStep_else66
    ldr x0, [sp, #328]
    str x0, [sp, #2776]
    ldr x0, [sp, #400]
    str x0, [sp, #2792]
    ldr x0, [sp, #2776]
    ldr x1, [sp, #2792]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t231
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t231
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t231
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t231
    bl _strcmp
    cmp x0, #0
    cset w0, ne
    b L_kuro_fn_VMStep_cmp_done_t231
L_kuro_fn_VMStep_cmp_numeric_t231:
    cmp x0, x1
    cset w0, ne
L_kuro_fn_VMStep_cmp_done_t231:
    str x0, [sp, #2800]
    ldr x0, [sp, #2800]
    cbz w0, L_kuro_fn_VMStep_else68
    mov x0, #1
    str x0, [sp, #2808]
    ldr x0, [sp, #2808]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif69
L_kuro_fn_VMStep_else68:
L_kuro_fn_VMStep_endif69:
    b L_kuro_fn_VMStep_endif67
L_kuro_fn_VMStep_else66:
    ldr x0, [sp, #368]
    str x0, [sp, #2816]
    adrp x0, L_kuro_data_143@PAGE
    add x0, x0, L_kuro_data_143@PAGEOFF
    str x0, [sp, #2824]
    ldr x0, [sp, #2816]
    ldr x1, [sp, #2824]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t235
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t235
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t235
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t235
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t235
L_kuro_fn_VMStep_cmp_numeric_t235:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t235:
    str x0, [sp, #2832]
    ldr x0, [sp, #2832]
    cbz w0, L_kuro_fn_VMStep_else70
    ldr x0, [sp, #328]
    str x0, [sp, #2840]
    ldr x0, [sp, #400]
    str x0, [sp, #2848]
    ldr x0, [sp, #2840]
    ldr x1, [sp, #2848]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #2856]
    ldr x0, [sp, #2856]
    cbz w0, L_kuro_fn_VMStep_else72
    mov x0, #1
    str x0, [sp, #2864]
    ldr x0, [sp, #2864]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif73
L_kuro_fn_VMStep_else72:
L_kuro_fn_VMStep_endif73:
    b L_kuro_fn_VMStep_endif71
L_kuro_fn_VMStep_else70:
    ldr x0, [sp, #368]
    str x0, [sp, #2880]
    adrp x0, L_kuro_data_144@PAGE
    add x0, x0, L_kuro_data_144@PAGEOFF
    str x0, [sp, #2888]
    ldr x0, [sp, #2880]
    ldr x1, [sp, #2888]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t242
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t242
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t242
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t242
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t242
L_kuro_fn_VMStep_cmp_numeric_t242:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t242:
    str x0, [sp, #2896]
    ldr x0, [sp, #368]
    str x0, [sp, #2904]
    adrp x0, L_kuro_data_145@PAGE
    add x0, x0, L_kuro_data_145@PAGEOFF
    str x0, [sp, #2912]
    ldr x0, [sp, #2904]
    ldr x1, [sp, #2912]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t245
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t245
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t245
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t245
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t245
L_kuro_fn_VMStep_cmp_numeric_t245:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t245:
    str x0, [sp, #2920]
    ldr x0, [sp, #2896]
    ldr x1, [sp, #2920]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #2928]
    ldr x0, [sp, #2928]
    cbz w0, L_kuro_fn_VMStep_else74
    ldr x0, [sp, #328]
    str x0, [sp, #2936]
    ldr x0, [sp, #400]
    str x0, [sp, #2944]
    ldr x0, [sp, #2936]
    ldr x1, [sp, #2944]
    cmp x0, x1
    cset w0, le
    str x0, [sp, #2952]
    ldr x0, [sp, #2952]
    cbz w0, L_kuro_fn_VMStep_else76
    mov x0, #1
    str x0, [sp, #2968]
    ldr x0, [sp, #2968]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif77
L_kuro_fn_VMStep_else76:
L_kuro_fn_VMStep_endif77:
    b L_kuro_fn_VMStep_endif75
L_kuro_fn_VMStep_else74:
    ldr x0, [sp, #368]
    str x0, [sp, #2976]
    adrp x0, L_kuro_data_146@PAGE
    add x0, x0, L_kuro_data_146@PAGEOFF
    str x0, [sp, #2984]
    ldr x0, [sp, #2976]
    ldr x1, [sp, #2984]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t253
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t253
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t253
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t253
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t253
L_kuro_fn_VMStep_cmp_numeric_t253:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t253:
    str x0, [sp, #2992]
    ldr x0, [sp, #2992]
    cbz w0, L_kuro_fn_VMStep_else78
    ldr x0, [sp, #328]
    str x0, [sp, #3000]
    ldr x0, [sp, #400]
    str x0, [sp, #3008]
    ldr x0, [sp, #3000]
    ldr x1, [sp, #3008]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #3016]
    ldr x0, [sp, #3016]
    cbz w0, L_kuro_fn_VMStep_else80
    mov x0, #1
    str x0, [sp, #3024]
    ldr x0, [sp, #3024]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif81
L_kuro_fn_VMStep_else80:
L_kuro_fn_VMStep_endif81:
    b L_kuro_fn_VMStep_endif79
L_kuro_fn_VMStep_else78:
    ldr x0, [sp, #368]
    str x0, [sp, #3032]
    adrp x0, L_kuro_data_147@PAGE
    add x0, x0, L_kuro_data_147@PAGEOFF
    str x0, [sp, #3040]
    ldr x0, [sp, #3032]
    ldr x1, [sp, #3040]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t260
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t260
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t260
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t260
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t260
L_kuro_fn_VMStep_cmp_numeric_t260:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t260:
    str x0, [sp, #3056]
    ldr x0, [sp, #368]
    str x0, [sp, #3064]
    adrp x0, L_kuro_data_148@PAGE
    add x0, x0, L_kuro_data_148@PAGEOFF
    str x0, [sp, #3072]
    ldr x0, [sp, #3064]
    ldr x1, [sp, #3072]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t263
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t263
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t263
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t263
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t263
L_kuro_fn_VMStep_cmp_numeric_t263:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t263:
    str x0, [sp, #3080]
    ldr x0, [sp, #3056]
    ldr x1, [sp, #3080]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3088]
    ldr x0, [sp, #3088]
    cbz w0, L_kuro_fn_VMStep_else82
    ldr x0, [sp, #328]
    str x0, [sp, #3096]
    ldr x0, [sp, #400]
    str x0, [sp, #3104]
    ldr x0, [sp, #3096]
    ldr x1, [sp, #3104]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #3112]
    ldr x0, [sp, #3112]
    cbz w0, L_kuro_fn_VMStep_else84
    mov x0, #1
    str x0, [sp, #3120]
    ldr x0, [sp, #3120]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif85
L_kuro_fn_VMStep_else84:
L_kuro_fn_VMStep_endif85:
    b L_kuro_fn_VMStep_endif83
L_kuro_fn_VMStep_else82:
L_kuro_fn_VMStep_endif83:
L_kuro_fn_VMStep_endif79:
L_kuro_fn_VMStep_endif75:
L_kuro_fn_VMStep_endif71:
L_kuro_fn_VMStep_endif67:
L_kuro_fn_VMStep_endif63:
    ldr x0, [sp, #392]
    str x0, [sp, #3128]
    ldr x0, [sp, #3128]
    bl _kuro_fn_VMPush
    str x0, [sp, #3144]
    ldr x0, [sp, #3144]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3152]
    ldr x0, [sp, #3152]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif61
L_kuro_fn_VMStep_else60:
L_kuro_fn_VMStep_endif61:
    ldr x0, [sp, #360]
    str x0, [sp, #3160]
    adrp x0, L_kuro_data_149@PAGE
    add x0, x0, L_kuro_data_149@PAGEOFF
    str x0, [sp, #3168]
    ldr x0, [sp, #3160]
    ldr x1, [sp, #3168]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t274
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t274
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t274
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t274
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t274
L_kuro_fn_VMStep_cmp_numeric_t274:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t274:
    str x0, [sp, #3176]
    ldr x0, [sp, #3176]
    cbz w0, L_kuro_fn_VMStep_else86
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #3184]
    ldr x0, [sp, #3184]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3192]
    ldr x0, [sp, #3192]
    str x0, [sp, #368]
    bl _kuro_fn_VMPop
    str x0, [sp, #3200]
    ldr x0, [sp, #3200]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3208]
    ldr x0, [sp, #3208]
    str x0, [sp, #400]
    bl _kuro_fn_VMPop
    str x0, [sp, #3216]
    ldr x0, [sp, #3216]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3232]
    ldr x0, [sp, #3232]
    str x0, [sp, #328]
    mov x0, #0
    str x0, [sp, #3240]
    ldr x0, [sp, #3240]
    str x0, [sp, #392]
    ldr x0, [sp, #368]
    str x0, [sp, #3248]
    adrp x0, L_kuro_data_150@PAGE
    add x0, x0, L_kuro_data_150@PAGEOFF
    str x0, [sp, #3256]
    ldr x0, [sp, #3248]
    ldr x1, [sp, #3256]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t284
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t284
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t284
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t284
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t284
L_kuro_fn_VMStep_cmp_numeric_t284:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t284:
    str x0, [sp, #3264]
    ldr x0, [sp, #3264]
    cbz w0, L_kuro_fn_VMStep_else88
    ldr x0, [sp, #328]
    str x0, [sp, #3272]
    mov x0, #1
    str x0, [sp, #3280]
    ldr x0, [sp, #3272]
    ldr x1, [sp, #3280]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t287
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t287
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t287
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t287
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t287
L_kuro_fn_VMStep_cmp_numeric_t287:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t287:
    str x0, [sp, #3288]
    ldr x0, [sp, #400]
    str x0, [sp, #3296]
    mov x0, #1
    str x0, [sp, #3304]
    ldr x0, [sp, #3296]
    ldr x1, [sp, #3304]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t290
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t290
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t290
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t290
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t290
L_kuro_fn_VMStep_cmp_numeric_t290:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t290:
    str x0, [sp, #3320]
    ldr x0, [sp, #3288]
    ldr x1, [sp, #3320]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    and w0, w0, w1
    str x0, [sp, #3328]
    ldr x0, [sp, #3328]
    cbz w0, L_kuro_fn_VMStep_else90
    mov x0, #1
    str x0, [sp, #3336]
    ldr x0, [sp, #3336]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif91
L_kuro_fn_VMStep_else90:
L_kuro_fn_VMStep_endif91:
    b L_kuro_fn_VMStep_endif89
L_kuro_fn_VMStep_else88:
    ldr x0, [sp, #368]
    str x0, [sp, #3344]
    adrp x0, L_kuro_data_151@PAGE
    add x0, x0, L_kuro_data_151@PAGEOFF
    str x0, [sp, #3352]
    ldr x0, [sp, #3344]
    ldr x1, [sp, #3352]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t295
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t295
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t295
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t295
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t295
L_kuro_fn_VMStep_cmp_numeric_t295:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t295:
    str x0, [sp, #3360]
    ldr x0, [sp, #3360]
    cbz w0, L_kuro_fn_VMStep_else92
    ldr x0, [sp, #328]
    str x0, [sp, #3368]
    mov x0, #1
    str x0, [sp, #3376]
    ldr x0, [sp, #3368]
    ldr x1, [sp, #3376]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t298
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t298
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t298
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t298
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t298
L_kuro_fn_VMStep_cmp_numeric_t298:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t298:
    str x0, [sp, #3384]
    ldr x0, [sp, #400]
    str x0, [sp, #3392]
    mov x0, #1
    str x0, [sp, #3416]
    ldr x0, [sp, #3392]
    ldr x1, [sp, #3416]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t301
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t301
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t301
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t301
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t301
L_kuro_fn_VMStep_cmp_numeric_t301:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t301:
    str x0, [sp, #3424]
    ldr x0, [sp, #3384]
    ldr x1, [sp, #3424]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3432]
    ldr x0, [sp, #3432]
    cbz w0, L_kuro_fn_VMStep_else94
    mov x0, #1
    str x0, [sp, #3440]
    ldr x0, [sp, #3440]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif95
L_kuro_fn_VMStep_else94:
L_kuro_fn_VMStep_endif95:
    b L_kuro_fn_VMStep_endif93
L_kuro_fn_VMStep_else92:
L_kuro_fn_VMStep_endif93:
L_kuro_fn_VMStep_endif89:
    ldr x0, [sp, #392]
    str x0, [sp, #3448]
    ldr x0, [sp, #3448]
    bl _kuro_fn_VMPush
    str x0, [sp, #3456]
    ldr x0, [sp, #3456]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3464]
    ldr x0, [sp, #3464]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif87
L_kuro_fn_VMStep_else86:
L_kuro_fn_VMStep_endif87:
    ldr x0, [sp, #360]
    str x0, [sp, #3472]
    adrp x0, L_kuro_data_152@PAGE
    add x0, x0, L_kuro_data_152@PAGEOFF
    str x0, [sp, #3480]
    ldr x0, [sp, #3472]
    ldr x1, [sp, #3480]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t309
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t309
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t309
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t309
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t309
L_kuro_fn_VMStep_cmp_numeric_t309:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t309:
    str x0, [sp, #3488]
    ldr x0, [sp, #3488]
    cbz w0, L_kuro_fn_VMStep_else96
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #3504]
    ldr x0, [sp, #3504]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3512]
    ldr x0, [sp, #3512]
    str x0, [sp, #272]
    bl _kuro_fn_VMPop
    str x0, [sp, #3520]
    ldr x0, [sp, #3520]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3528]
    ldr x0, [sp, #3528]
    str x0, [sp, #280]
    mov x0, #0
    str x0, [sp, #3536]
    ldr x0, [sp, #3536]
    str x0, [sp, #392]
    ldr x0, [sp, #272]
    str x0, [sp, #3544]
    adrp x0, L_kuro_data_153@PAGE
    add x0, x0, L_kuro_data_153@PAGEOFF
    str x0, [sp, #3552]
    ldr x0, [sp, #3544]
    ldr x1, [sp, #3552]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t317
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t317
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t317
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t317
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t317
L_kuro_fn_VMStep_cmp_numeric_t317:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t317:
    str x0, [sp, #3560]
    ldr x0, [sp, #3560]
    cbz w0, L_kuro_fn_VMStep_else98
    ldr x0, [sp, #280]
    str x0, [sp, #3568]
    ldr x0, [sp, #3568]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_isclass_invalid_t319
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_isclass_invalid_t319
    ldrb w0, [x0]
    sub w0, w0, #48
    cmp w0, #9
    cset w0, ls
    b L_kuro_fn_VMStep_isclass_done_t319
L_kuro_fn_VMStep_isclass_invalid_t319:
    mov x0, #0
L_kuro_fn_VMStep_isclass_done_t319:
    str x0, [sp, #3576]
    ldr x0, [sp, #3576]
    cbz w0, L_kuro_fn_VMStep_else100
    mov x0, #1
    str x0, [sp, #3592]
    ldr x0, [sp, #3592]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif101
L_kuro_fn_VMStep_else100:
L_kuro_fn_VMStep_endif101:
    b L_kuro_fn_VMStep_endif99
L_kuro_fn_VMStep_else98:
    ldr x0, [sp, #272]
    str x0, [sp, #3600]
    adrp x0, L_kuro_data_154@PAGE
    add x0, x0, L_kuro_data_154@PAGEOFF
    str x0, [sp, #3608]
    ldr x0, [sp, #3600]
    ldr x1, [sp, #3608]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t323
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t323
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t323
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t323
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t323
L_kuro_fn_VMStep_cmp_numeric_t323:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t323:
    str x0, [sp, #3616]
    ldr x0, [sp, #3616]
    cbz w0, L_kuro_fn_VMStep_else102
    ldr x0, [sp, #280]
    str x0, [sp, #3624]
    ldr x0, [sp, #3624]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_isclass_invalid_t325
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_isclass_invalid_t325
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
    b L_kuro_fn_VMStep_isclass_done_t325
L_kuro_fn_VMStep_isclass_invalid_t325:
    mov x0, #0
L_kuro_fn_VMStep_isclass_done_t325:
    str x0, [sp, #3632]
    ldr x0, [sp, #3632]
    cbz w0, L_kuro_fn_VMStep_else104
    mov x0, #1
    str x0, [sp, #3640]
    ldr x0, [sp, #3640]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif105
L_kuro_fn_VMStep_else104:
L_kuro_fn_VMStep_endif105:
    b L_kuro_fn_VMStep_endif103
L_kuro_fn_VMStep_else102:
    ldr x0, [sp, #272]
    str x0, [sp, #3648]
    adrp x0, L_kuro_data_155@PAGE
    add x0, x0, L_kuro_data_155@PAGEOFF
    str x0, [sp, #3656]
    ldr x0, [sp, #3648]
    ldr x1, [sp, #3656]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t329
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t329
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t329
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t329
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t329
L_kuro_fn_VMStep_cmp_numeric_t329:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t329:
    str x0, [sp, #3664]
    ldr x0, [sp, #3664]
    cbz w0, L_kuro_fn_VMStep_else106
    ldr x0, [sp, #280]
    str x0, [sp, #3680]
    ldr x0, [sp, #3680]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_isclass_invalid_t331
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_isclass_invalid_t331
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
    b L_kuro_fn_VMStep_isclass_done_t331
L_kuro_fn_VMStep_isclass_invalid_t331:
    mov x0, #0
L_kuro_fn_VMStep_isclass_done_t331:
    str x0, [sp, #3688]
    ldr x0, [sp, #3688]
    cbz w0, L_kuro_fn_VMStep_else108
    mov x0, #1
    str x0, [sp, #3696]
    ldr x0, [sp, #3696]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif109
L_kuro_fn_VMStep_else108:
L_kuro_fn_VMStep_endif109:
    b L_kuro_fn_VMStep_endif107
L_kuro_fn_VMStep_else106:
    ldr x0, [sp, #272]
    str x0, [sp, #3704]
    adrp x0, L_kuro_data_156@PAGE
    add x0, x0, L_kuro_data_156@PAGEOFF
    str x0, [sp, #3712]
    ldr x0, [sp, #3704]
    ldr x1, [sp, #3712]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t335
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t335
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t335
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t335
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t335
L_kuro_fn_VMStep_cmp_numeric_t335:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t335:
    str x0, [sp, #3720]
    ldr x0, [sp, #3720]
    cbz w0, L_kuro_fn_VMStep_else110
    ldr x0, [sp, #280]
    str x0, [sp, #3728]
    ldr x0, [sp, #3728]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_isclass_invalid_t337
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_isclass_invalid_t337
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
    b L_kuro_fn_VMStep_isclass_done_t337
L_kuro_fn_VMStep_isclass_invalid_t337:
    mov x0, #0
L_kuro_fn_VMStep_isclass_done_t337:
    str x0, [sp, #3736]
    ldr x0, [sp, #3736]
    cbz w0, L_kuro_fn_VMStep_else112
    mov x0, #1
    str x0, [sp, #3744]
    ldr x0, [sp, #3744]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif113
L_kuro_fn_VMStep_else112:
L_kuro_fn_VMStep_endif113:
    b L_kuro_fn_VMStep_endif111
L_kuro_fn_VMStep_else110:
    ldr x0, [sp, #272]
    str x0, [sp, #3752]
    adrp x0, L_kuro_data_157@PAGE
    add x0, x0, L_kuro_data_157@PAGEOFF
    str x0, [sp, #3768]
    ldr x0, [sp, #3752]
    ldr x1, [sp, #3768]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t341
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t341
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t341
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t341
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t341
L_kuro_fn_VMStep_cmp_numeric_t341:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t341:
    str x0, [sp, #3776]
    ldr x0, [sp, #3776]
    cbz w0, L_kuro_fn_VMStep_else114
    ldr x0, [sp, #280]
    str x0, [sp, #3784]
    ldr x0, [sp, #3784]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_isclass_invalid_t343
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_isclass_invalid_t343
    ldrb w0, [x0]
    cmp w0, #34
    cset w0, eq
    b L_kuro_fn_VMStep_isclass_done_t343
L_kuro_fn_VMStep_isclass_invalid_t343:
    mov x0, #0
L_kuro_fn_VMStep_isclass_done_t343:
    str x0, [sp, #3792]
    ldr x0, [sp, #3792]
    cbz w0, L_kuro_fn_VMStep_else116
    mov x0, #1
    str x0, [sp, #3800]
    ldr x0, [sp, #3800]
    str x0, [sp, #392]
    b L_kuro_fn_VMStep_endif117
L_kuro_fn_VMStep_else116:
L_kuro_fn_VMStep_endif117:
    b L_kuro_fn_VMStep_endif115
L_kuro_fn_VMStep_else114:
    mov x0, #1
    str x0, [sp, #3808]
    ldr x0, [sp, #3808]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif115:
L_kuro_fn_VMStep_endif111:
L_kuro_fn_VMStep_endif107:
L_kuro_fn_VMStep_endif103:
L_kuro_fn_VMStep_endif99:
    ldr x0, [sp, #392]
    str x0, [sp, #3816]
    ldr x0, [sp, #3816]
    bl _kuro_fn_VMPush
    str x0, [sp, #3824]
    ldr x0, [sp, #3824]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #3832]
    ldr x0, [sp, #3832]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif97
L_kuro_fn_VMStep_else96:
L_kuro_fn_VMStep_endif97:
    ldr x0, [sp, #360]
    str x0, [sp, #3840]
    adrp x0, L_kuro_data_158@PAGE
    add x0, x0, L_kuro_data_158@PAGEOFF
    str x0, [sp, #3856]
    ldr x0, [sp, #3840]
    ldr x1, [sp, #3856]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t351
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t351
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t351
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t351
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t351
L_kuro_fn_VMStep_cmp_numeric_t351:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t351:
    str x0, [sp, #3864]
    ldr x0, [sp, #360]
    str x0, [sp, #3872]
    adrp x0, L_kuro_data_159@PAGE
    add x0, x0, L_kuro_data_159@PAGEOFF
    str x0, [sp, #3880]
    ldr x0, [sp, #3872]
    ldr x1, [sp, #3880]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t354
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t354
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t354
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t354
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t354
L_kuro_fn_VMStep_cmp_numeric_t354:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t354:
    str x0, [sp, #3888]
    ldr x0, [sp, #3864]
    ldr x1, [sp, #3888]
    cmp x0, #0
    cset w0, ne
    cmp x1, #0
    cset w1, ne
    orr w0, w0, w1
    str x0, [sp, #3896]
    ldr x0, [sp, #3896]
    cbz w0, L_kuro_fn_VMStep_else118
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #3904]
    ldr x0, [sp, #3904]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3912]
    ldr x0, [sp, #3912]
    str x0, [sp, #344]
    bl _kuro_fn_VMPop
    str x0, [sp, #3920]
    ldr x0, [sp, #3920]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3928]
    ldr x0, [sp, #3928]
    str x0, [sp, #416]
    ldr x0, [sp, #360]
    str x0, [sp, #3944]
    adrp x0, L_kuro_data_160@PAGE
    add x0, x0, L_kuro_data_160@PAGEOFF
    str x0, [sp, #3952]
    ldr x0, [sp, #3944]
    ldr x1, [sp, #3952]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t362
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t362
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t362
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t362
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t362
L_kuro_fn_VMStep_cmp_numeric_t362:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t362:
    str x0, [sp, #3960]
    ldr x0, [sp, #3960]
    cbz w0, L_kuro_fn_VMStep_else120
    ldr x0, [sp, #344]
    str x0, [sp, #3968]
    ldr x0, [sp, #3968]
    bl _kuro_fn_VMLoad
    str x0, [sp, #3976]
    ldr x0, [sp, #3976]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #3984]
    ldr x0, [sp, #416]
    str x0, [sp, #3992]
    ldr x0, [sp, #3984]
    ldr x1, [sp, #3992]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_binop_numeric_t367
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_binop_numeric_t367
    cmp x1, #0
    b.le L_kuro_fn_VMStep_binop_numeric_t367
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_binop_numeric_t367
    b L_kuro_fn_VMStep_binop_text_t367
L_kuro_fn_VMStep_binop_numeric_t367:
    add x0, x0, x1
    b L_kuro_fn_VMStep_binop_done_t367
L_kuro_fn_VMStep_binop_text_t367:
    mov x0, #4096
    bl _malloc
    str x0, [sp, #4000]
    ldr x0, [sp, #4000]
    ldr x1, [sp, #3984]
    bl _strcpy
    ldr x0, [sp, #4000]
    ldr x1, [sp, #3992]
    bl _strcat
L_kuro_fn_VMStep_binop_done_t367:
    str x0, [sp, #4000]
    ldr x0, [sp, #4000]
    str x0, [sp, #416]
    b L_kuro_fn_VMStep_endif121
L_kuro_fn_VMStep_else120:
L_kuro_fn_VMStep_endif121:
    ldr x0, [sp, #344]
    str x0, [sp, #4008]
    ldr x0, [sp, #416]
    str x0, [sp, #4016]
    ldr x0, [sp, #4008]
    ldr x1, [sp, #4016]
    bl _kuro_fn_VMStore
    str x0, [sp, #4032]
    ldr x0, [sp, #4032]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4040]
    ldr x0, [sp, #4040]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif119
L_kuro_fn_VMStep_else118:
L_kuro_fn_VMStep_endif119:
    ldr x0, [sp, #360]
    str x0, [sp, #4048]
    adrp x0, L_kuro_data_161@PAGE
    add x0, x0, L_kuro_data_161@PAGEOFF
    str x0, [sp, #4056]
    ldr x0, [sp, #4048]
    ldr x1, [sp, #4056]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t374
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t374
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t374
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t374
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t374
L_kuro_fn_VMStep_cmp_numeric_t374:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t374:
    str x0, [sp, #4064]
    ldr x0, [sp, #4064]
    cbz w0, L_kuro_fn_VMStep_else122
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #4072]
    ldr x0, [sp, #4072]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4080]
    ldr x0, [sp, #4080]
    str x0, [sp, #344]
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #4088]
    ldr x0, [sp, #4088]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4096]
    ldr x0, [sp, #4096]
    str x0, [sp, #320]
    ldr x0, [sp, #344]
    str x0, [sp, #4104]
    mov x0, #0
    str x0, [sp, #4120]
    ldr x0, [sp, #4104]
    ldr x1, [sp, #4120]
    bl _kuro_fn_VMFindCollection
    str x0, [sp, #4128]
    ldr x0, [sp, #4128]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4136]
    ldr x0, [sp, #4136]
    str x0, [sp, #288]
    ldr x0, [sp, #288]
    str x0, [sp, #4144]
    mov x0, #0
    str x0, [sp, #4152]
    ldr x0, [sp, #4144]
    ldr x1, [sp, #4152]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #4160]
    ldr x0, [sp, #4160]
    cbz w0, L_kuro_fn_VMStep_else124
    bl _kuro_fn_VMPop
    str x0, [sp, #4168]
    ldr x0, [sp, #4168]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4176]
    ldr x0, [sp, #4176]
    str x0, [sp, #312]
    ldr x0, [sp, #344]
    str x0, [sp, #4184]
    ldr x0, [sp, #312]
    str x0, [sp, #4192]
    ldr x0, [sp, #4184]
    ldr x1, [sp, #4192]
    bl _kuro_fn_VMGetCollectionItem
    str x0, [sp, #4208]
    ldr x0, [sp, #4208]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4216]
    ldr x0, [sp, #4216]
    str x0, [sp, #304]
    b L_kuro_fn_VMStep_endif125
L_kuro_fn_VMStep_else124:
    ldr x0, [sp, #344]
    str x0, [sp, #4224]
    ldr x0, [sp, #4224]
    bl _kuro_fn_VMLoad
    str x0, [sp, #4232]
    ldr x0, [sp, #4232]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4240]
    ldr x0, [sp, #4240]
    str x0, [sp, #304]
    ldr x0, [sp, #320]
    str x0, [sp, #4248]
    adrp x0, L_kuro_data_162@PAGE
    add x0, x0, L_kuro_data_162@PAGEOFF
    str x0, [sp, #4256]
    ldr x0, [sp, #4248]
    ldr x1, [sp, #4256]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t397
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t397
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t397
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t397
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t397
L_kuro_fn_VMStep_cmp_numeric_t397:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t397:
    str x0, [sp, #4264]
    ldr x0, [sp, #4264]
    cbz w0, L_kuro_fn_VMStep_else126
    bl _kuro_fn_VMPop
    str x0, [sp, #4272]
    ldr x0, [sp, #4272]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4280]
    ldr x0, [sp, #4280]
    str x0, [sp, #312]
    ldr x0, [sp, #312]
    str x0, [sp, #4304]
    ldr x2, [sp, #304]
    ldr x1, [sp, #4304]
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
    str x0, [sp, #4312]
    ldr x0, [sp, #4312]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4320]
    ldr x0, [sp, #4320]
    str x0, [sp, #304]
    b L_kuro_fn_VMStep_endif127
L_kuro_fn_VMStep_else126:
L_kuro_fn_VMStep_endif127:
L_kuro_fn_VMStep_endif125:
    ldr x0, [sp, #304]
    str x0, [sp, #4328]
    ldr x0, [sp, #4328]
    bl _kuro_fn_VMSetResult
    str x0, [sp, #4336]
    ldr x0, [sp, #4336]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #304]
    str x0, [sp, #4344]
    ldr x0, [sp, #4344]
    bl _kuro_fn_VMPush
    str x0, [sp, #4352]
    ldr x0, [sp, #4352]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4360]
    ldr x0, [sp, #4360]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif123
L_kuro_fn_VMStep_else122:
L_kuro_fn_VMStep_endif123:
    ldr x0, [sp, #360]
    str x0, [sp, #4368]
    adrp x0, L_kuro_data_163@PAGE
    add x0, x0, L_kuro_data_163@PAGEOFF
    str x0, [sp, #4376]
    ldr x0, [sp, #4368]
    ldr x1, [sp, #4376]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t410
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t410
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t410
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t410
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t410
L_kuro_fn_VMStep_cmp_numeric_t410:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t410:
    str x0, [sp, #4392]
    ldr x0, [sp, #4392]
    cbz w0, L_kuro_fn_VMStep_else128
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #4400]
    ldr x0, [sp, #4400]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4408]
    ldr x0, [sp, #4408]
    str x0, [sp, #344]
    ldr x0, [sp, #344]
    str x0, [sp, #4416]
    mov x0, #0
    str x0, [sp, #4424]
    ldr x0, [sp, #4416]
    ldr x1, [sp, #4424]
    bl _kuro_fn_VMFindCollection
    str x0, [sp, #4432]
    ldr x0, [sp, #4432]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4440]
    mov x0, #0
    str x0, [sp, #4448]
    ldr x0, [sp, #4440]
    ldr x1, [sp, #4448]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #4456]
    ldr x0, [sp, #4456]
    cbz w0, L_kuro_fn_VMStep_else130
    ldr x0, [sp, #344]
    str x0, [sp, #4464]
    ldr x0, [sp, #4464]
    bl _kuro_fn_VMLengthCollection
    str x0, [sp, #4480]
    ldr x0, [sp, #4480]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4488]
    ldr x0, [sp, #4488]
    str x0, [sp, #336]
    b L_kuro_fn_VMStep_endif131
L_kuro_fn_VMStep_else130:
    ldr x0, [sp, #344]
    str x0, [sp, #4496]
    ldr x0, [sp, #4496]
    bl _kuro_fn_VMLoad
    str x0, [sp, #4504]
    ldr x0, [sp, #4504]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4512]
    ldr x0, [sp, #4512]
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    cbz x0, L_kuro_fn_VMStep_length_zero_t425
    bl _strlen
    b L_kuro_fn_VMStep_length_done_t425
L_kuro_fn_VMStep_length_zero_t425:
    mov x0, #0
L_kuro_fn_VMStep_length_done_t425:
    str x0, [sp, #4520]
    ldr x0, [sp, #4520]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4528]
    ldr x0, [sp, #4528]
    str x0, [sp, #336]
L_kuro_fn_VMStep_endif131:
    ldr x0, [sp, #336]
    str x0, [sp, #4536]
    ldr x0, [sp, #4536]
    bl _kuro_fn_VMSetResult
    str x0, [sp, #4544]
    ldr x0, [sp, #4544]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #336]
    str x0, [sp, #4552]
    ldr x0, [sp, #4552]
    bl _kuro_fn_VMPush
    str x0, [sp, #4568]
    ldr x0, [sp, #4568]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #4576]
    ldr x0, [sp, #4576]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif129
L_kuro_fn_VMStep_else128:
L_kuro_fn_VMStep_endif129:
    ldr x0, [sp, #360]
    str x0, [sp, #4584]
    adrp x0, L_kuro_data_164@PAGE
    add x0, x0, L_kuro_data_164@PAGEOFF
    str x0, [sp, #4592]
    ldr x0, [sp, #4584]
    ldr x1, [sp, #4592]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t434
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t434
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t434
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t434
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t434
L_kuro_fn_VMStep_cmp_numeric_t434:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t434:
    str x0, [sp, #4600]
    ldr x0, [sp, #4600]
    cbz w0, L_kuro_fn_VMStep_else132
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #4608]
    ldr x0, [sp, #4608]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4616]
    ldr x0, [sp, #4616]
    str x0, [sp, #344]
    bl _kuro_fn_VMPop
    str x0, [sp, #4624]
    ldr x0, [sp, #4624]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4632]
    ldr x0, [sp, #4632]
    str x0, [sp, #416]
    bl _kuro_fn_VMPop
    str x0, [sp, #4640]
    ldr x0, [sp, #4640]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4656]
    ldr x0, [sp, #4656]
    str x0, [sp, #312]
    ldr x0, [sp, #344]
    str x0, [sp, #4664]
    mov x0, #0
    str x0, [sp, #4672]
    ldr x0, [sp, #4664]
    ldr x1, [sp, #4672]
    bl _kuro_fn_VMFindCollection
    str x0, [sp, #4680]
    ldr x0, [sp, #4680]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4688]
    mov x0, #0
    str x0, [sp, #4696]
    ldr x0, [sp, #4688]
    ldr x1, [sp, #4696]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #4704]
    ldr x0, [sp, #4704]
    cbz w0, L_kuro_fn_VMStep_else134
    ldr x0, [sp, #344]
    str x0, [sp, #4712]
    ldr x0, [sp, #312]
    str x0, [sp, #4720]
    ldr x0, [sp, #416]
    str x0, [sp, #4728]
    ldr x0, [sp, #4712]
    ldr x1, [sp, #4720]
    ldr x2, [sp, #4728]
    bl _kuro_fn_VMSetCollectionItem
    str x0, [sp, #4744]
    ldr x0, [sp, #4744]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif135
L_kuro_fn_VMStep_else134:
    ldr x0, [sp, #344]
    str x0, [sp, #4752]
    ldr x0, [sp, #4752]
    bl _kuro_fn_VMLoad
    str x0, [sp, #4760]
    ldr x0, [sp, #4760]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4768]
    ldr x0, [sp, #4768]
    str x0, [sp, #304]
    ldr x0, [sp, #312]
    str x0, [sp, #4776]
    ldr x0, [sp, #416]
    str x0, [sp, #4784]
    ldr x2, [sp, #304]
    ldr x1, [sp, #4776]
    ldr x0, [sp, #4784]
    ldrb w0, [x0]
    strb w0, [x2, x1]
    ldr x0, [sp, #344]
    str x0, [sp, #4792]
    ldr x0, [sp, #304]
    str x0, [sp, #4800]
    ldr x0, [sp, #4792]
    ldr x1, [sp, #4800]
    bl _kuro_fn_VMStore
    str x0, [sp, #4808]
    ldr x0, [sp, #4808]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif135:
    mov x0, #0
    str x0, [sp, #4816]
    ldr x0, [sp, #4816]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif133
L_kuro_fn_VMStep_else132:
L_kuro_fn_VMStep_endif133:
    ldr x0, [sp, #360]
    str x0, [sp, #4832]
    adrp x0, L_kuro_data_165@PAGE
    add x0, x0, L_kuro_data_165@PAGEOFF
    str x0, [sp, #4840]
    ldr x0, [sp, #4832]
    ldr x1, [sp, #4840]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t462
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t462
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t462
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t462
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t462
L_kuro_fn_VMStep_cmp_numeric_t462:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t462:
    str x0, [sp, #4848]
    ldr x0, [sp, #4848]
    cbz w0, L_kuro_fn_VMStep_else136
    bl _kuro_fn_VMReadOperand
    str x0, [sp, #4856]
    ldr x0, [sp, #4856]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4864]
    ldr x0, [sp, #4864]
    str x0, [sp, #344]
    bl _kuro_fn_VMPop
    str x0, [sp, #4872]
    ldr x0, [sp, #4872]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4880]
    ldr x0, [sp, #4880]
    str x0, [sp, #416]
    ldr x0, [sp, #344]
    str x0, [sp, #4888]
    mov x0, #0
    str x0, [sp, #4896]
    ldr x0, [sp, #4888]
    ldr x1, [sp, #4896]
    bl _kuro_fn_VMFindName
    str x0, [sp, #4904]
    ldr x0, [sp, #4904]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #4920]
    ldr x0, [sp, #4920]
    str x0, [sp, #352]
    ldr x0, [sp, #352]
    str x0, [sp, #4928]
    mov x0, #0
    str x0, [sp, #4936]
    ldr x0, [sp, #4928]
    ldr x1, [sp, #4936]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #4944]
    ldr x0, [sp, #4944]
    cbz w0, L_kuro_fn_VMStep_else138
    ldr x0, [sp, #344]
    str x0, [sp, #4952]
    ldr x0, [sp, #4952]
    bl _kuro_fn_VMMarkCollection
    str x0, [sp, #4960]
    ldr x0, [sp, #4960]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    ldr x0, [sp, #344]
    str x0, [sp, #4968]
    ldr x0, [sp, #416]
    str x0, [sp, #4976]
    ldr x0, [sp, #4968]
    ldr x1, [sp, #4976]
    bl _kuro_fn_VMAppendCollectionItem
    str x0, [sp, #4984]
    ldr x0, [sp, #4984]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif139
L_kuro_fn_VMStep_else138:
    ldr x0, [sp, #344]
    str x0, [sp, #4992]
    mov x0, #0
    str x0, [sp, #5008]
    ldr x0, [sp, #4992]
    ldr x1, [sp, #5008]
    bl _kuro_fn_VMFindCollection
    str x0, [sp, #5016]
    ldr x0, [sp, #5016]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5024]
    mov x0, #0
    str x0, [sp, #5032]
    ldr x0, [sp, #5024]
    ldr x1, [sp, #5032]
    cmp x0, x1
    cset w0, ge
    str x0, [sp, #5040]
    ldr x0, [sp, #5040]
    cbz w0, L_kuro_fn_VMStep_else140
    ldr x0, [sp, #344]
    str x0, [sp, #5048]
    ldr x0, [sp, #416]
    str x0, [sp, #5056]
    ldr x0, [sp, #5048]
    ldr x1, [sp, #5056]
    bl _kuro_fn_VMAppendCollectionItem
    str x0, [sp, #5064]
    ldr x0, [sp, #5064]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMStep_endif141
L_kuro_fn_VMStep_else140:
    ldr x0, [sp, #344]
    str x0, [sp, #5072]
    ldr x0, [sp, #5072]
    bl _kuro_fn_VMLoad
    str x0, [sp, #5080]
    ldr x0, [sp, #5080]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5096]
    ldr x0, [sp, #5096]
    str x0, [sp, #304]
    ldr x0, [sp, #304]
    str x0, [sp, #5104]
    ldr x0, [sp, #416]
    str x0, [sp, #5112]
    ldr x0, [sp, #5104]
    ldr x1, [sp, #5112]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_binop_numeric_t493
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_binop_numeric_t493
    cmp x1, #0
    b.le L_kuro_fn_VMStep_binop_numeric_t493
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_binop_numeric_t493
    b L_kuro_fn_VMStep_binop_text_t493
L_kuro_fn_VMStep_binop_numeric_t493:
    add x0, x0, x1
    b L_kuro_fn_VMStep_binop_done_t493
L_kuro_fn_VMStep_binop_text_t493:
    mov x0, #4096
    bl _malloc
    str x0, [sp, #5120]
    ldr x0, [sp, #5120]
    ldr x1, [sp, #5104]
    bl _strcpy
    ldr x0, [sp, #5120]
    ldr x1, [sp, #5112]
    bl _strcat
L_kuro_fn_VMStep_binop_done_t493:
    str x0, [sp, #5120]
    ldr x0, [sp, #5120]
    str x0, [sp, #304]
    ldr x0, [sp, #344]
    str x0, [sp, #5128]
    ldr x0, [sp, #304]
    str x0, [sp, #5136]
    ldr x0, [sp, #5128]
    ldr x1, [sp, #5136]
    bl _kuro_fn_VMStore
    str x0, [sp, #5144]
    ldr x0, [sp, #5144]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif141:
L_kuro_fn_VMStep_endif139:
    mov x0, #0
    str x0, [sp, #5152]
    ldr x0, [sp, #5152]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif137
L_kuro_fn_VMStep_else136:
L_kuro_fn_VMStep_endif137:
    ldr x0, [sp, #360]
    str x0, [sp, #5160]
    adrp x0, L_kuro_data_166@PAGE
    add x0, x0, L_kuro_data_166@PAGEOFF
    str x0, [sp, #5168]
    ldr x0, [sp, #5160]
    ldr x1, [sp, #5168]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t500
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t500
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t500
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t500
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t500
L_kuro_fn_VMStep_cmp_numeric_t500:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t500:
    str x0, [sp, #5192]
    ldr x0, [sp, #5192]
    cbz w0, L_kuro_fn_VMStep_else142
    bl _kuro_fn_VMPop
    str x0, [sp, #5200]
    ldr x0, [sp, #5200]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5208]
    ldr x0, [sp, #5208]
    str x0, [sp, #416]
    adrp x0, _kuro_global_70@PAGE
    add x0, x0, _kuro_global_70@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5216]
    mov x0, #1
    str x0, [sp, #5224]
    ldr x0, [sp, #5216]
    ldr x1, [sp, #5224]
    cmp x0, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t505
    cmp x0, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t505
    cmp x1, #0
    b.le L_kuro_fn_VMStep_cmp_numeric_t505
    cmp x1, #0x1000
    b.lo L_kuro_fn_VMStep_cmp_numeric_t505
    bl _strcmp
    cmp x0, #0
    cset w0, eq
    b L_kuro_fn_VMStep_cmp_done_t505
L_kuro_fn_VMStep_cmp_numeric_t505:
    cmp x0, x1
    cset w0, eq
L_kuro_fn_VMStep_cmp_done_t505:
    str x0, [sp, #5232]
    ldr x0, [sp, #5232]
    cbz w0, L_kuro_fn_VMStep_else144
    mov x0, #0
    str x0, [sp, #5240]
    ldr x0, [sp, #5240]
    str x0, [sp, #384]
    ldr x0, [sp, #416]
    str x0, [sp, #5248]
    ldr x0, [sp, #5248]
    bl _kuro_fn_VMLengthCollection
    str x0, [sp, #5256]
    ldr x0, [sp, #5256]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5264]
    ldr x0, [sp, #5264]
    str x0, [sp, #376]
L_kuro_fn_VMStep_while_start146:
    ldr x0, [sp, #384]
    str x0, [sp, #5280]
    ldr x0, [sp, #376]
    str x0, [sp, #5288]
    ldr x0, [sp, #5280]
    ldr x1, [sp, #5288]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #5296]
    ldr x0, [sp, #5296]
    cbz w0, L_kuro_fn_VMStep_while_end147
    ldr x0, [sp, #416]
    str x0, [sp, #5304]
    ldr x0, [sp, #384]
    str x0, [sp, #5312]
    ldr x0, [sp, #5304]
    ldr x1, [sp, #5312]
    bl _kuro_fn_VMGetCollectionItem
    str x0, [sp, #5320]
    ldr x0, [sp, #5320]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #5328]
    adrp x1, _kuro_collection_len_10@PAGE
    add x1, x1, _kuro_collection_len_10@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_10@PAGE
    add x2, x2, _kuro_collection_10@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #5328]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_10@PAGE
    add x2, x2, _kuro_collection_len_10@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #5336]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #5336]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #5344]
    ldr x0, [sp, #384]
    ldr x1, [sp, #5344]
    add x0, x0, x1
    str x0, [sp, #384]
    b L_kuro_fn_VMStep_while_start146
L_kuro_fn_VMStep_while_end147:
    b L_kuro_fn_VMStep_endif145
L_kuro_fn_VMStep_else144:
    ldr x0, [sp, #416]
    str x0, [sp, #5352]
    adrp x1, _kuro_collection_len_10@PAGE
    add x1, x1, _kuro_collection_len_10@PAGEOFF
    ldr x1, [x1]
    adrp x2, _kuro_collection_10@PAGE
    add x2, x2, _kuro_collection_10@PAGEOFF
    cmp x1, #65536
    b.ge L_kuro_collection_overflow
    ldr x0, [sp, #5352]
    lsl x3, x1, #3
    str x0, [x2, x3]
    add x1, x1, #1
    adrp x2, _kuro_collection_len_10@PAGE
    add x2, x2, _kuro_collection_len_10@PAGEOFF
    str x1, [x2]
    mov x0, #1
    str x0, [sp, #5368]
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #5368]
    add x0, x0, x1
    adrp x2, _kuro_global_80@PAGE
    add x2, x2, _kuro_global_80@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMStep_endif145:
    mov x0, #0
    str x0, [sp, #5376]
    ldr x0, [sp, #5376]
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
    b L_kuro_fn_VMStep_endif143
L_kuro_fn_VMStep_else142:
L_kuro_fn_VMStep_endif143:
    mov x0, #1
    str x0, [sp, #5384]
    ldr x0, [sp, #5384]
    adrp x2, _kuro_global_48@PAGE
    add x2, x2, _kuro_global_48@PAGEOFF
    str x0, [x2]
    mov x0, #0
    mov x15, #5824
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_VMRun:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #160
    sub sp, sp, x15
    adrp x0, _kuro_collection_len_0@PAGE
    add x0, x0, _kuro_collection_len_0@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #56]
    ldr x0, [sp, #56]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #64]
    ldr x0, [sp, #64]
    adrp x2, _kuro_global_35@PAGE
    add x2, x2, _kuro_global_35@PAGEOFF
    str x0, [x2]
L_kuro_fn_VMRun_while_start0:
    adrp x0, _kuro_global_85@PAGE
    add x0, x0, _kuro_global_85@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #72]
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #80]
    ldr x0, [sp, #72]
    ldr x1, [sp, #80]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #88]
    ldr x0, [sp, #88]
    cbz w0, L_kuro_fn_VMRun_while_end1
    bl _kuro_fn_VMStep
    str x0, [sp, #96]
    ldr x0, [sp, #96]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    mov x0, #1
    str x0, [sp, #112]
    ldr x0, [sp, #104]
    ldr x1, [sp, #112]
    cmp x0, x1
    cset w0, eq
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    cbz w0, L_kuro_fn_VMRun_else3
    adrp x0, _kuro_global_35@PAGE
    add x0, x0, _kuro_global_35@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    ldr x0, [sp, #128]
    adrp x2, _kuro_global_85@PAGE
    add x2, x2, _kuro_global_85@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_VMRun_endif4
L_kuro_fn_VMRun_else3:
L_kuro_fn_VMRun_endif4:
    b L_kuro_fn_VMRun_while_start0
L_kuro_fn_VMRun_while_end1:
    mov x0, #0
    mov x15, #160
    add sp, sp, x15
    ldp x29, x30, [sp], #16
    ret
_kuro_fn_RuntimeRun:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x15, #272
    sub sp, sp, x15
    adrp x0, _kuro_global_48@PAGE
    add x0, x0, _kuro_global_48@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #104]
    mov x0, #0
    str x0, [sp, #112]
    ldr x0, [sp, #104]
    ldr x1, [sp, #112]
    cmp x0, x1
    cset w0, ne
    str x0, [sp, #192]
    ldr x0, [sp, #192]
    cbz w0, L_kuro_fn_RuntimeRun_else0
    mov x0, #1
    str x0, [sp, #200]
    ldr x0, [sp, #200]
    adrp x2, _kuro_global_30@PAGE
    add x2, x2, _kuro_global_30@PAGEOFF
    str x0, [x2]
    mov x0, #1
    str x0, [sp, #208]
    ldr x0, [sp, #208]
    adrp x2, _kuro_global_29@PAGE
    add x2, x2, _kuro_global_29@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_RuntimeRun_endif1
L_kuro_fn_RuntimeRun_else0:
    adrp x0, _kuro_global_80@PAGE
    add x0, x0, _kuro_global_80@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #216]
    ldr x0, [sp, #216]
    adrp x2, _kuro_global_28@PAGE
    add x2, x2, _kuro_global_28@PAGEOFF
    str x0, [x2]
    mov x0, #0
    str x0, [sp, #224]
    ldr x0, [sp, #224]
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_28@PAGE
    add x0, x0, _kuro_global_28@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #232]
    mov x0, #0
    str x0, [sp, #240]
    ldr x0, [sp, #232]
    ldr x1, [sp, #240]
    cmp x0, x1
    cset w0, gt
    str x0, [sp, #248]
    ldr x0, [sp, #248]
    cbz w0, L_kuro_fn_RuntimeRun_else2
    adrp x0, _kuro_collection_10@PAGE
    add x0, x0, _kuro_collection_10@PAGEOFF
    str x0, [sp, #120]
    ldr x0, [sp, #120]
    adrp x2, _kuro_global_32@PAGE
    add x2, x2, _kuro_global_32@PAGEOFF
    str x0, [x2]
L_kuro_fn_RuntimeRun_while_start4:
    adrp x0, _kuro_global_31@PAGE
    add x0, x0, _kuro_global_31@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #128]
    adrp x0, _kuro_global_28@PAGE
    add x0, x0, _kuro_global_28@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #136]
    ldr x0, [sp, #128]
    ldr x1, [sp, #136]
    cmp x0, x1
    cset w0, lt
    str x0, [sp, #144]
    ldr x0, [sp, #144]
    cbz w0, L_kuro_fn_RuntimeRun_while_end5
    adrp x0, _kuro_global_31@PAGE
    add x0, x0, _kuro_global_31@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #152]
    ldr x1, [sp, #152]
    adrp x2, _kuro_collection_10@PAGE
    add x2, x2, _kuro_collection_10@PAGEOFF
    lsl x1, x1, #3
    ldr x0, [x2, x1]
    str x0, [sp, #160]
    ldr x0, [sp, #160]
    adrp x2, _kuro_global_142@PAGE
    add x2, x2, _kuro_global_142@PAGEOFF
    str x0, [x2]
    adrp x0, _kuro_global_142@PAGE
    add x0, x0, _kuro_global_142@PAGEOFF
    ldr x0, [x0]
    str x0, [sp, #168]
    ldr x0, [sp, #168]
    cmp x0, #4096
    b.lo L_kuro_print_dynamic_number_RuntimeRun_t16
    mov x1, #0x100000000000
    cmp x0, x1
    b.lo L_kuro_print_dynamic_text_RuntimeRun_t16
L_kuro_print_dynamic_float_RuntimeRun_t16:
    sub sp, sp, #16
    str x0, [sp]
    adrp x0, L_kuro_float_format@PAGE
    add x0, x0, L_kuro_float_format@PAGEOFF
    bl _printf
    add sp, sp, #16
    b L_kuro_print_dynamic_done_RuntimeRun_t16
L_kuro_print_dynamic_text_RuntimeRun_t16:
    bl _puts
    b L_kuro_print_dynamic_done_RuntimeRun_t16
L_kuro_print_dynamic_number_RuntimeRun_t16:
    bl _kuro_print_int
L_kuro_print_dynamic_done_RuntimeRun_t16:
    mov x0, #1
    str x0, [sp, #176]
    adrp x0, _kuro_global_31@PAGE
    add x0, x0, _kuro_global_31@PAGEOFF
    ldr x0, [x0]
    ldr x1, [sp, #176]
    add x0, x0, x1
    adrp x2, _kuro_global_31@PAGE
    add x2, x2, _kuro_global_31@PAGEOFF
    str x0, [x2]
    b L_kuro_fn_RuntimeRun_while_start4
L_kuro_fn_RuntimeRun_while_end5:
    b L_kuro_fn_RuntimeRun_endif3
L_kuro_fn_RuntimeRun_else2:
    adrp x0, L_kuro_data_167@PAGE
    add x0, x0, L_kuro_data_167@PAGEOFF
    str x0, [sp, #184]
    ldr x0, [sp, #184]
    adrp x2, _kuro_global_32@PAGE
    add x2, x2, _kuro_global_32@PAGEOFF
    str x0, [x2]
L_kuro_fn_RuntimeRun_endif3:
L_kuro_fn_RuntimeRun_endif1:
    mov x0, #0
    mov x15, #272
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
L_kuro_data_54: .asciz "__vm_empty__"
L_kuro_data_55: .asciz "__vm_empty__"
L_kuro_data_56: .asciz "__vm_empty__"
L_kuro_data_57: .asciz "__vm_empty__"
L_kuro_data_58: .asciz "__vm_empty__"
L_kuro_data_59: .asciz "__vm_empty__"
L_kuro_data_60: .asciz "__vm_empty__"
L_kuro_data_61: .asciz "__vm_empty__"
L_kuro_data_62: .asciz "__vm_empty__"
L_kuro_data_63: .asciz "__vm_empty__"
L_kuro_data_64: .asciz ""
L_kuro_data_65: .asciz "__vm_empty__"
L_kuro_data_66: .asciz "__vm_empty__"
L_kuro_data_67: .asciz "__vm_empty__"
L_kuro_data_68: .asciz "__vm_empty__"
L_kuro_data_69: .asciz "__vm_empty__"
L_kuro_data_70: .asciz "__vm_empty__"
L_kuro_data_71: .asciz "__vm_empty__"
L_kuro_data_72: .asciz "__vm_empty__"
L_kuro_data_73: .asciz ""
L_kuro_data_74: .asciz "e"
L_kuro_data_75: .asciz "n"
L_kuro_data_76: .asciz "\n"
L_kuro_data_77: .asciz "i"
L_kuro_data_78: .asciz "r"
L_kuro_data_79: .asciz "\r"
L_kuro_data_80: .asciz "t"
L_kuro_data_81: .asciz "\t"
L_kuro_data_82: .asciz ""
L_kuro_data_83: .asciz ""
L_kuro_data_84: .asciz "_"
L_kuro_data_85: .asciz "BC_IF_BEGIN"
L_kuro_data_86: .asciz "BC_ELSE_BEGIN"
L_kuro_data_87: .asciz "BC_IF_END"
L_kuro_data_88: .asciz "BC_IF_BEGIN"
L_kuro_data_89: .asciz "BC_IF_END"
L_kuro_data_90: .asciz "BC_REPEAT_BEGIN"
L_kuro_data_91: .asciz "BC_REPEAT_END"
L_kuro_data_92: .asciz "BC_REPEAT_END"
L_kuro_data_93: .asciz "BC_WHILE_BEGIN"
L_kuro_data_94: .asciz "BC_WHILE_END"
L_kuro_data_95: .asciz "BC_WHILE_TEST"
L_kuro_data_96: .asciz "BC_WHILE_END"
L_kuro_data_97: .asciz "BC_FUNC_END"
L_kuro_data_98: .asciz "BC_PARAM"
L_kuro_data_99: .asciz "BC_FUNC_BEGIN"
L_kuro_data_100: .asciz "__vm_empty__"
L_kuro_data_101: .asciz "__vm_empty__"
L_kuro_data_102: .asciz "0"
L_kuro_data_103: .asciz "1"
L_kuro_data_104: .asciz "2"
L_kuro_data_105: .asciz "3"
L_kuro_data_106: .asciz "4"
L_kuro_data_107: .asciz "5"
L_kuro_data_108: .asciz "6"
L_kuro_data_109: .asciz "7"
L_kuro_data_110: .asciz "8"
L_kuro_data_111: .asciz "9"
L_kuro_data_112: .asciz "."
L_kuro_data_115: .asciz "BC_IF_BEGIN"
L_kuro_data_116: .asciz "BC_ELSE_BEGIN"
L_kuro_data_117: .asciz "BC_IF_END"
L_kuro_data_118: .asciz "BC_REPEAT_BEGIN"
L_kuro_data_119: .asciz "BC_REPEAT_END"
L_kuro_data_120: .asciz "BC_WHILE_BEGIN"
L_kuro_data_121: .asciz "BC_WHILE_TEST"
L_kuro_data_122: .asciz "BC_WHILE_END"
L_kuro_data_123: .asciz "BC_FUNC_BEGIN"
L_kuro_data_124: .asciz "BC_FUNC_END"
L_kuro_data_125: .asciz "BC_CALL_BEGIN"
L_kuro_data_126: .asciz "BC_CALL_END"
L_kuro_data_127: .asciz "BC_RETURN"
L_kuro_data_128: .asciz "BC_CONST"
L_kuro_data_129: .asciz "BC_LOADVAR"
L_kuro_data_130: .asciz "_"
L_kuro_data_131: .asciz "BC_STORE_LIST"
L_kuro_data_132: .asciz "BC_DECLTYPE"
L_kuro_data_133: .asciz "BC_INPUT"
L_kuro_data_134: .asciz ""
L_kuro_data_135: .asciz "BC_BINOP"
L_kuro_data_136: .asciz "+"
L_kuro_data_137: .asciz "-"
L_kuro_data_138: .asciz "*"
L_kuro_data_139: .asciz "/"
L_kuro_data_140: .asciz "BC_CMP"
L_kuro_data_141: .asciz "eq"
L_kuro_data_142: .asciz "neq"
L_kuro_data_143: .asciz "lt"
L_kuro_data_144: .asciz "lte"
L_kuro_data_145: .asciz "le"
L_kuro_data_146: .asciz "gt"
L_kuro_data_147: .asciz "gte"
L_kuro_data_148: .asciz "ge"
L_kuro_data_149: .asciz "BC_BOOL"
L_kuro_data_150: .asciz "AND"
L_kuro_data_151: .asciz "OR"
L_kuro_data_152: .asciz "BC_ISCLASS"
L_kuro_data_153: .asciz "digit"
L_kuro_data_154: .asciz "alpha"
L_kuro_data_155: .asciz "alnum"
L_kuro_data_156: .asciz "space"
L_kuro_data_157: .asciz "quote"
L_kuro_data_158: .asciz "BC_UPDATE"
L_kuro_data_159: .asciz "BC_ADD"
L_kuro_data_160: .asciz "BC_ADD"
L_kuro_data_161: .asciz "BC_GET"
L_kuro_data_162: .asciz "1"
L_kuro_data_163: .asciz "BC_LENGTH"
L_kuro_data_164: .asciz "BC_SET"
L_kuro_data_165: .asciz "BC_APPEND"
L_kuro_data_166: .asciz "BC_PRINT"
L_kuro_data_167: .asciz ""
.section __TEXT,__const
L_kuro_float_113: .double 1.0
L_kuro_float_114: .double 1.0
.section __TEXT,__cstring
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
.zerofill __DATA,__bss,_kuro_collection_10,524288,3
.zerofill __DATA,__bss,_kuro_collection_11,524288,3
.zerofill __DATA,__bss,_kuro_collection_12,524288,3
.zerofill __DATA,__bss,_kuro_collection_13,524288,3
.zerofill __DATA,__bss,_kuro_collection_14,524288,3
.zerofill __DATA,__bss,_kuro_collection_15,524288,3
.zerofill __DATA,__bss,_kuro_collection_16,524288,3
.zerofill __DATA,__bss,_kuro_collection_17,524288,3
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
.zerofill __DATA,__bss,_kuro_collection_len_10,8,3
.zerofill __DATA,__bss,_kuro_collection_len_11,8,3
.zerofill __DATA,__bss,_kuro_collection_len_12,8,3
.zerofill __DATA,__bss,_kuro_collection_len_13,8,3
.zerofill __DATA,__bss,_kuro_collection_len_14,8,3
.zerofill __DATA,__bss,_kuro_collection_len_15,8,3
.zerofill __DATA,__bss,_kuro_collection_len_16,8,3
.zerofill __DATA,__bss,_kuro_collection_len_17,8,3
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
.zerofill __DATA,__bss,_kuro_char_34,2,1
.zerofill __DATA,__bss,_kuro_char_1,2,1
.zerofill __DATA,__bss,_kuro_char_2,2,1
.zerofill __DATA,__bss,_kuro_char_3,2,1
.zerofill __DATA,__bss,_kuro_char_4,2,1
.zerofill __DATA,__bss,_kuro_char_5,2,1
.zerofill __DATA,__bss,_kuro_char_heap,2097152,4
.zerofill __DATA,__bss,_kuro_char_heap_cursor,8,3
.zerofill __DATA,__bss,_kuro_int_buffer,32,3
.zerofill __DATA,__bss,_kuro_input_buffer,1048576,4
