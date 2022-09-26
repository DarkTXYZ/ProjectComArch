from re import L


def display32bit(input):
    print('{:032b}'.format(input))

REGISTER = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
memory = [0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
pc = 0
# display32bit(REGISTER[0])

def op_add(regA , regB , destReg):
    REGISTER[destReg] = REGISTER[regA] + REGISTER[regB]
    pc = pc+1

def op_nand(regA , regB , destReg):
    REGISTER[destReg] = ~(REGISTER[regA] & REGISTER[regB])
    pc = pc+1

def op_lw(regA , regB , offset):
    REGISTER[regB] = memory[(REGISTER[regA] + offset)]
    pc = pc+1

def op_sw(regA , regB , offset):
    memory[REGISTER[regA] + offset] = REGISTER[regB] 
    pc = pc+1

def op_beq(regA , regB , offset):
    if( REGISTER[regA] == REGISTER[regB] ):
        pc = pc+1+offset

def op_jalr(regA , regB):
    if(REGISTER[regA] == REGISTER[regB]):
        REGISTER[regB] = pc+1
        pc = pc+1
    else:
        REGISTER[regB] = pc+1
        pc = REGISTER[regA]

def op_halt():
    print("halted")
    pc = pc+1

def op_noop():
    pass


def machinecodereader(input):
    str_input = '{:032b}'.format(input)
    bin_input = int(str_input)
    if ( str_input[7] == '0' and str_input[8] == '0') :
        rd = str_input[29:32]
        rs = str_input[10:13]
        rt = str_input[13:16]
        if (str_input[9] == '0') :
            print("add")
            op_add(rs, rt, rd)
        else:
            print("nand")
            op_nand(rs, rt, rd)
    elif ( str_input[7] == '0' and str_input[8] == '1') :
        if (str_input[9] == '0') :
            print("lw")
        else:
            print("sw")
    elif ( str_input[7] == '1' and str_input[8] == '0') :
        if (str_input[9] == '0') :
            print("beq")
        else:
            print("jalr")
    elif ( str_input[7] == '1' and str_input[8] == '1') :
        if (str_input[9] == '0') :
            print("halt")
        else:
            print("noop")
    else : pass

# machinecodereader(8454151)
# machinecodereader(9043971)
# machinecodereader(655361)
# machinecodereader(16842754)
# machinecodereader(16842749)
# machinecodereader(29360128)
# machinecodereader(25165824)




