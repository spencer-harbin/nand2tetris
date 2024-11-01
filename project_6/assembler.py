class Parser: 
    def __init__(self, input_file):
        with open(input_file, 'r') as file:
            self.lines = file.readlines()

        self.current_command = -1

    def hasMoreCommands(self):
        if self.current_command < len(self.lines) - 1:
            return True
        else:
            return False

    def advance(self):
        self.current_command += 1

    def commandType(self):
        first_char = self.lines[self.current_command][0]
        if '//' in self.lines[self.current_command]:
            return 'COMMENT' 
        if first_char == '@':
            return 'A_COMMAND'
        elif first_char == '(':
            return 'L_COMMAND'
        elif '=' in self.lines[self.current_command] or ';' in self.lines[self.current_command]:  
            return 'C_COMMAND'
        else:
            return None

    def symbol(self):
        curr_command = self.lines[self.current_command]

        if '@' in curr_command:
            s = curr_command.replace('@', '')
            return s.strip() 
        elif '(' in curr_command: 
            s = curr_command.replace('(', '')
            s = curr_command.replace(')', '')
            return s.strip() 

    def dest(self):
        if not '=' in self.lines[self.current_command]:
            return 'null'
        else:
            # dest corresponds to whatever is on the left-hand side of the "=" sign 
            dest = self.lines[self.current_command].split('=')[0]
            return dest

    def comp(self):
        comp = self.lines[self.current_command].split('=')[-1].strip()
        return comp  

    def jump(self):
        if not ';' in self.lines[self.current_command]:
            return 'null'
        else:
            return self.lines[self.current_command].split(';')[-1]

class Code:
    def __init__(self): 
        self.dest_table = {
            'null': '000', 
            'M': '001', 
            'D': '010',
            'MD': '011',
            'A': '100', 
            'AM': '101', 
            'AD': '110', 
            'AMD': '111'
        }

        self.comp_table = {
            '0': '0101010', 
            '1': '0111111', 
            '-1': '0111010',
            'D': '0001100', 
            'A': '0110000', 
            '!D': '0001101', 
            '!A': '0110001', 
            '-D': '0001111', 
            '-A': '0110011', 
            'D+1': '0011111', 
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010', 
            'D+A': '0000010', 
            'D-A': '0010011', 
            'A-D': '0000111', 
            'D&A': '0000000', 
            'D|A': '0010101', 

            'M': '1110000', 
            '!M': '1110001', 
            '-M': '1110011', 
            'M+1': '1110111', 
            'M-1': '1110010', 
            'D+M': '1000010', 
            'D-M': '1010011', 
            'M-D': '1000111', 
            'D&M': '1000000', 
            'D|M': '1010101'
        }

        self.jump_table = {
            'null': '000', 
            'JGT': '001', 
            'JEQ': '010', 
            'JGE': '011', 
            'JLT': '100', 
            'JNE': '101', 
            'JLE': '110', 
            'JMP': '111'
        }

class SymbolTable: 
    def __init__(self):
        # map symbols to addresses ({'symbol':'address'})
        self.symbol_table = {
            'SP': '0000000000000000',
            'LCL': '0000000000000001',
            'ARG': '0000000000000010',
            'THIS': '0000000000000011', 
            'THAT': '0000000000000100',
            'R0 ': '0000000000000000', 
            'R1': '0000000000000001', 
            'R2': '0000000000000010', 
            'R3': '0000000000000011', 
            'R4': '0000000000000100', 
            'R5': '0000000000000101', 
            'R6': '0000000000000110', 
            'R7': '0000000000000111', 
            'R8': '0000000000001000', 
            'R9': '0000000000001001', 
            'R10': '0000000000001010', 
            'R11': '0000000000001011', 
            'R12': '0000000000001100', 
            'R13': '0000000000001101', 
            'R14': '0000000000001110', 
            'R15': '0000000000001111', 
            'SCREEN': '0100000000000000', 
            'KBD': '0110000000000000' 
        }

    def addEntry(self, symbol, address):
        self.symbol_table[symbol] = address

    def contains(self, string): 
        if string in self.symbol_table.keys():
            return True
        else:
            return False 

    def getAddress(self, string): 
        return self.symbol_table[string] 

if __name__ == '__main__':
    binary_commands = []

    assemb = Parser('./add.asm')
    codes = Code()
    symbTable = SymbolTable() 

    # first run through to update symbol table 
    with open('./max.asm') as file:
        lines = file.readlines()
        ROM_inst = 0 
        for line in lines:
            line = line.strip()
            if line and line[0] == '(':
                symbol = line.replace('(', '')
                symbol = symbol.replace(')', '')
                symbol = symbol.strip()

                # convert ROM instruction to 16-bit binary 
                ROM_inst_binary = bin(int(ROM_inst))[2:].zfill(16)
                symbTable.addEntry(symbol, ROM_inst)
            
            elif line[:2] == '//' or line == '':
                pass 

            else:
                ROM_inst += 1 

    # reset command count for second run 
    assemb.current_command = -1

    while assemb.hasMoreCommands():
        binary_command = ''
        # current_command is initialized to -1; starting w/ "advance()" changes that to 0
        assemb.advance() 
        current_command_type = assemb.commandType() 

        if current_command_type == 'A_COMMAND': 
            # bin_com = bin(assemb.symbol) 
            opcode = '0'
            value = assemb.symbol()
            value = bin(int(value))[2:].zfill(15)
            binary_command = opcode + value
            binary_commands.append(binary_command)

        elif current_command_type == 'C_COMMAND':
            opcode = '111'
            computation = codes.comp_table[assemb.comp()]
            destination = codes.dest_table[assemb.dest()]
            jump = codes.jump_table[assemb.jump()]
            binary_command = opcode + computation + destination + jump
            binary_commands.append(binary_command) 

        elif current_command_type == 'COMMENT' or current_command_type == 'L_COMMAND':
            pass

    print(binary_commands)
    # with open('add.hack', 'w') as newfile: 
    #     for command in binary_commands:
    #         newfile.write(command + '\n')