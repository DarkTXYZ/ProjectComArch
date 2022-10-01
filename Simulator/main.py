# display32bit(REGISTER[0])

#! open in your file directory
from asyncio.windows_events import NULL


file = open("C:\\Users\Acer\OneDrive - Chiang Mai University\Desktop\Com Archietecture\Project(PHP 8.4)\ProjectComArch\Simulator\input.txt", "r")
file_read = file.read()

#! variable
REGISTER = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
memory = []
pc = 0
instruction_execute= 0
    

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
    global pc
    pc += 1
    global REGISTER
    REGISTER[destReg] = REGISTER[regA] + REGISTER[regB]
    printState()
    return True

def op_nand(regA , regB , destReg):
    global pc
    pc += 1
    global REGISTER
    REGISTER[destReg] = ~(REGISTER[regA] & REGISTER[regB])
    printState()
    return True
    
def op_lw(regA , regB , offset):
    global pc
    pc += 1
    global REGISTER
    REGISTER[regB] = memory[(REGISTER[regA] + offset)]
    printState()
    return True

def op_sw(regA , regB , offset):
    global pc
    pc += 1
    global REGISTER
    memory[REGISTER[regA] + offset] = REGISTER[regB] 
    printState()
    return True

def op_beq(regA , regB , offset):
    global REGISTER
    global pc
    n_loop = pc
    if( REGISTER[regA] == REGISTER[regB] ):
        pc = pc+1+offset
        printState()
        if offset < 0:
            loop(pc, n_loop+1)
            return True
        else:
            return False
    else: 
        pc += 1
        printState()
        return True

def loop(n, m):
    for i in range(n,m):
        check = machinecodereader(int(memory[i]))
        if check == False: break

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

def op_halt():
    global pc
    print("halted")
    pc = pc+1

def op_noop():
    global pc
    pc = pc+1

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
    print("end state\n")
    # pc += 1

def machinecodereader(input):
    REGISTER[0] = 0
    str_input = '{:032b}'.format(input)
    bin_input = int(str_input)
    new_strList = []
    check_loop = True
    # print(check_loop)
    if ( str_input[7] == '0' and str_input[8] == '0') :
        str_rd = str_input[29:32]
        str_rs = str_input[10:13]
        str_rt = str_input[13:16]
        int_rd = int(str_rd , 2)
        int_rs = int(str_rs , 2)
        int_rt = int(str_rt , 2)
        if (str_input[9] == '0') :
            check_loop = op_add(int_rs, int_rt, int_rd)
        else:
            check_loop = op_nand(int_rs, int_rt, int_rd)
    elif ( str_input[7] == '0' and str_input[8] == '1') :
        str_off = str_input[16:32]
        str_rs = str_input[10:13]
        str_rd = str_input[13:16]
        int_off = int(str_off , 2)
        int_rs = int(str_rs , 2)
        int_rd = int(str_rd , 2)

        if (str_input[9] == '0') :
            check_loop = op_lw(int_rs, int_rd, int_off)
        else:
            op_sw(int_rs, int_rd, int_off)
    elif ( str_input[7] == '1' and str_input[8] == '0') :
        if (str_input[9] == '0') :
            str_off = str_input[16:32]
            str_rs = str_input[10:13]
            str_rd = str_input[13:16]
            int_off = two2dec(str_off)
            int_rs = int(str_rs , 2)
            int_rd = int(str_rd , 2)

            check_loop = op_beq(int_rs, int_rd, int_off)
        else:
            print("jalr")
    elif ( str_input[7] == '1' and str_input[8] == '1') :
        if (str_input[9] == '0') :
             # print("halt")
            op_halt()
        else:
            # print("noop")
            op_noop()
    else : pass
    return check_loop


def main():
    inputFromAssembler()
    printState()
    # loop()
    for i in range(len(memory)):
           machinecodereader(int(memory[i]))


main()