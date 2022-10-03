# display32bit(REGISTER[0])

#! open in your file directory
file = open("Simulator\input.txt", "r")
file_read = file.read()
output = open("Simulator\output.txt", "w")

#! variable
REGISTER = []
memory = []
pc = 0
instruction_execute= 0
count = 0
    

#! read from .txt
def inputFromAssembler():
    global memory
    input_split = file_read.split()
    for i in range(8):
        REGISTER.append(0)
    for i in range(len(input_split)):
        memory.append(int(input_split[i]))
    # print(REGISTER)

#! 2’s complement
def two2dec(s):
  if s[0] == '1':
    return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
  else:
    return int(s, 2)

def display32bit(input):
    print('{:032b}'.format(input))

def op_add(regA , regB , destReg):
    global pc, count 
    pc += 1
    count += 1
    global REGISTER
    REGISTER[destReg] = REGISTER[regA] + REGISTER[regB]
    printState()
    # return False

def op_nand(regA , regB , destReg):
    global pc, count 
    pc += 1
    count += 1
    global REGISTER
    REGISTER[destReg] = ~(REGISTER[regA] & REGISTER[regB])
    printState()
    # return False
    
def op_lw(regA , regB , offset):
    global pc, count 
    pc += 1
    count += 1
    global REGISTER
    REGISTER[regB] = memory[(REGISTER[regA] + offset)]
    printState()
    # return False

def op_sw(regA , regB , offset):
    global pc, count 
    pc += 1
    count += 1
    global REGISTER
    memory[REGISTER[regA] + offset] = REGISTER[regB] 
    printState()
    # return False

def op_beq(regA , regB , offset):
    global REGISTER
    global pc, count 
    count += 1
    n_loop = pc
    if( REGISTER[regA] == REGISTER[regB] ):
        pc = pc+1+offset
        printState()
    else: 
        pc += 1
        printState()
        # return False

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
    global pc, count
    pc = pc+1
    count += 1

    print("machine halted")
    print("total of ", count, " instructions executed")
    print("final state of machine: \n")
    
    output.write("machine halted\n")
    output.write("total of " + str(count) + " instructions executed\n")
    output.write("final state of machine:\n\n")
    
    printState()
    # return True

def op_noop():
    pass
    # return False

def printState():
    global instruction_execute, pc
    instruction_execute += 1
    print("@@@" + "\n" + "state:")
    print("\t PC " + str(pc))
    print("\t memory:")
    for i in range(len(memory)):
        print("\t\t mem[" + str(i) + "] " + str(memory[i]))
    print("\t register:")
    for i in range(len(REGISTER)):
        print("\t\t register[" + str(i) + "] " + str(REGISTER[i]))
    print("end state\n")
    # pc += 1
    
    output.write("@@@" + "\n" + "state:\n")
    output.write("\tpc " + str(pc) + '\n')
    output.write("\tmemory:\n")
    for i in range(len(memory)):
        output.write("\t\tmem[ " + str(i) + " ] " + str(memory[i]) + '\n')
    output.write("\tregisters:\n")
    for i in range(len(REGISTER)):
        output.write("\t\treg[ " + str(i) + " ] " + str(REGISTER[i]) + '\n')
    output.write("end state\n\n")

def machinecodereader(input):
    REGISTER[0] = 0
    str_input = '{:032b}'.format(input)
    bin_input = int(str_input)
    new_strList = []
    stop_loop = False
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
            op_sw(int_rs, int_rd, int_off)
    elif ( str_input[7] == '1' and str_input[8] == '0') :
        str_off = str_input[16:32]
        str_rs = str_input[10:13]
        str_rd = str_input[13:16]
        int_off = two2dec(str_off)
        int_rs = int(str_rs , 2)
        int_rd = int(str_rd , 2)
            
        if (str_input[9] == '0') :
            op_beq(int_rs, int_rd, int_off)
        else:
            op_jalr(int_rs , int_rd)
    elif ( str_input[7] == '1' and str_input[8] == '1') :
        if (str_input[9] == '0') :
             # print("halt")
            op_halt()
            stop_loop = True
        else:
            # print("noop")
            op_noop()
    else : 
        pass
        # print("in this")
    return stop_loop


def main():
    inputFromAssembler()
    printState()
    # loop()

    global pc
    while(True):
        print(pc)
        stop_loop = machinecodereader(int(memory[pc]))
        if stop_loop == True: break



main()