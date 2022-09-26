from dis import Instruction


def display32bit(input):
    print('{:032b}'.format(input))

MEMORY = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0, 0, 0]
REGISTER = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
instruction_execute= 0
PC = 0

# display32bit(REGISTER[0])
def op_add(regA , regB , destReg):
    REGISTER[destReg] = REGISTER[regA] + REGISTER[regB]

def op_nand(regA , regB , destReg):
    REGISTER[destReg] = ~(REGISTER[regA] & REGISTER[regB])

def op_lw(regA , regB , offset):
    print()

def op_sw(regA , regB , offset):
    print()

def op_beq(regA , regB , offset):
    print()

def op_jalr(regA , regB):
    print()

def op_halt():
    print()

def op_noop():
    print()

def printState():
    global instruction_execute
    instruction_execute += 1
    print("@@@" + "\n" + "state:")
    print("\t PC " + str(PC))
    print("\t memory:")
    for i in range(10):
        print("\t\t mem[" + str(i) + "] " + str(MEMORY[i]))
    print("\t register:")
    for i in range(8):
        print("\t\t register[" + str(i) + "] " + str(REGISTER[i]))
    print("end state")

def machinecodereader(input):
    str_input = '{:032b}'.format(input)
    bin_input = int(str_input)
    # print(type(bin_input))
    # print(bin_input)
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
printState()




