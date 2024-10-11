@SCREEN
D=A
@nextScreenLocation
M=D

(loop)
    @KBD
    D=M
    @darkenScreen
    D;JNE
    @lightenScreen
    D;JEQ
    @loop
    0;JMP

(darkenScreen)
    @nextScreenLocation
    // this bit was not obvious to me at first (and I did shamelessly take inspiration 
    // from the pre-built Rect.asm file); @nextScreenLocation contains the next 
    // screen location in its M; when you do "A=M" right afterwards, the A register changes,
    // but on this line you're still referring to the M located at nextScreenLocation. Once this 
    // is done (i.e, after this line), you have a "new" M at the "new" A register location 
    // that you set to -1 (or 0) to darken/lighten the screen
    A=M
    // set to -1 (b/c -1 is 1111111111111111 in binary, meaning that every bit in the 
    // 16-bit register is set to 1)
    M=-1
    @nextScreenLocation
    D=M
    @1
    D=D+A
    @nextScreenLocation
    M=D
    @loop
    0;JMP

(lightenScreen)
    @nextScreenLocation
    A=M 
    M=0
    @nextScreenLocation
    D=M
    @1
    D=D-A
    @nextScreenLocation
    M=D
    @loop
    0;JMP