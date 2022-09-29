# display32bit(REGISTER[0])

#! open in your file directory
file = open("Simulator\input.txt", "r")
file_read = file.read()

#! variable
REGISTER = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
memory = []
pc = 0
instruction_execute= 0
test_mem = []

#! read from .txt
def inputFromAssembler():
    global memory
    input_split = file_read.split("\n")
    for i in range(len(input_split)):
        memory.append(int(input_split[i]))

#! 2’s complement
def two2dec(s):
  if s[0] == '1':
    return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
  else:
    return int(s, 2)

def display32bit(input):
    print('{:032b}'.format(input))

def op_add(regA , regB , destReg):
    global REGISTER
    REGISTER[destReg] = REGISTER[regA] + REGISTER[regB]
    global pc
    printState()
    # pc = pc+1
    return False

def op_nand(regA , regB , destReg):
    global REGISTER
    REGISTER[destReg] = ~(REGISTER[regA] & REGISTER[regB])
    global pc
    printState()
    # pc = pc+1
    return False
    

def op_lw(regA , regB , offset):
    global REGISTER
    REGISTER[regB] = memory[(REGISTER[regA] + offset)]
    global pc
    printState()
    # pc = pc+1
    return False

def op_sw(regA , regB , offset):
    global REGISTER
    memory[REGISTER[regA] + offset] = REGISTER[regB] 
    global pc
    printState()
    # pc = pc+1
    return False

def op_beq(regA , regB , offset):
    global REGISTER
    global pc
    if( REGISTER[regA] == REGISTER[regB] ):
        pc = pc+1+offset
    printState()
    return False

def op_jalr(regA , regB):
    global REGISTER
    global pc
    if(REGISTER[regA] == REGISTER[regB]):
        REGISTER[regB] = pc+1
        pc = pc+1
        # printState()
    else:
        REGISTER[regB] = pc+1
        pc = REGISTER[regA]
        # printState()
    return False

def op_halt():
    global pc
    print("halted")
    pc = pc+1
    # printState()
    return True

def op_noop():
    global pc
    pc = pc+1
    # printState()
    return False

def printState():
    global instruction_execute, pc
    instruction_execute += 1
    print("@@@" + "\n" + "state:")
    print("\t PC " + str(pc))
    print("\t memory:")
    for i in range(10):
        print("\t\t mem[" + str(i) + "] " + str(memory[i]))
    print("\t register:")
    for i in range(8):
        print("\t\t register[" + str(i) + "] " + str(REGISTER[i]))
    print("end state")
    pc += 1

def machinecodereader(input):
    REGISTER[0] = 0
    str_input = '{:032b}'.format(input)
    bin_input = int(str_input)
    new_strList = []

    if ( str_input[7] == '0' and str_input[8] == '0') :
        str_rd = str_input[29:32]
        str_rs = str_input[10:13]
        str_rt = str_input[13:16]
        int_rd = int(str_rd , 2)
        int_rs = int(str_rs , 2)
        int_rt = int(str_rt , 2)
        if (str_input[9] == '0') :
            op_add(int_rs, int_rt, int_rd)
        else:
            op_nand(int_rs, int_rt, int_rd)
    elif ( str_input[7] == '0' and str_input[8] == '1') :
        str_off = str_input[16:32]
        str_rs = str_input[10:13]
        str_rd = str_input[13:16]
        int_off = int(str_off , 2)
        int_rs = int(str_rs , 2)
        int_rd = int(str_rd , 2)

        if (str_input[9] == '0') :
            op_lw(int_rs, int_rd, int_off)
        else:
            print("sw")
    elif ( str_input[7] == '1' and str_input[8] == '0') :
        if (str_input[9] == '0') :
            str_off = str_input[16:32]
            str_rs = str_input[10:13]
            str_rd = str_input[13:16]
            int_off = two2dec(str_off)
            int_rs = int(str_rs , 2)
            int_rd = int(str_rd , 2)

            op_beq(int_rs, int_rd, int_off)
        else:
            print("jalr")
    elif ( str_input[7] == '1' and str_input[8] == '1') :
        if (str_input[9] == '0') :
            print("halt")
        else:
            print("noop")
    else : pass



def main():
    inputFromAssembler()
    printState()
    # loop()
    for i in range(5):
            machinecodereader(int(memory[i]))
    # machinecodereader(16842754)

    
def loop(check):
    if check == True:
        return 0
    else:
        for i in range(3):
            machinecodereader(int(memory[i]))
main()