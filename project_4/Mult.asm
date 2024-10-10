@R2
M=0

@R0
D=M
@END
D;JEQ

@R0
D=M
@END
D;JEQ

@R1
D=M
@END
D;JEQ

(beginWhile)
    @R0
    D=M
    @R2
    M=D+M
    @R1
    M=M-1
    D=M
    @END
    D;JEQ
    @beginWhile
    0;JMP

(END)
    @END
    0;JMP