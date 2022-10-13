# display32bit(REGISTER[0])

#! open in your file directory
from asyncio.windows_events import NULL


file = open("C:\\Users\Acer\OneDrive - Chiang Mai University\Desktop\Com Archietecture\Project(PHP 8.4)\ProjectComArch\Simulator\input.txt", "r")
file_read = file.read()

#! variable
REGISTER = []
memory = []
pc = 0
instruction_execute= 0
count = 0
    

#! read from .txt
def inputFromAssembler(): #assign text from assembler to memory
    global memory #call memory variable from global
    input_split = file_read.split("\n") #split text by \n
    for i in range(8):
        REGISTER.append(0) #push 0 to register list
    for i in range(len(input_split)):
        memory.append(int(input_split[i])) #push text that split by \n to memory list
    # print(REGISTER)

#! 2’s complement
def two2dec(s): #convert binary to dec
  if s[0] == '1':
    return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
  else:
    return int(s, 2)

def display32bit(input):
    print('{:032b}'.format(input))

def op_add(regA , regB , destReg): #add operator
    global pc, count #call pc, count variable from global
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    REGISTER[destReg] = REGISTER[regA] + REGISTER[regB] #bring register[regA] + register[regB] assign to register[destReg]
    printState() #call printState func

def op_nand(regA , regB , destReg): #nand operator
    global pc, count #call pc, count variable from global
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    REGISTER[destReg] = ~(REGISTER[regA] & REGISTER[regB]) #bring register[regA] nand register[regB] assign to register[destReg]
    printState() #call printState func
    
def op_lw(regA , regB , offset):
    global pc, count #call pc, count variable from global
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    REGISTER[regB] = memory[(REGISTER[regA] + offset)] #load memory[(REGISTER[regA] + offset)] to register[regB]
    printState() #call printState func

def op_sw(regA , regB , offset):
    global pc, count #call pc, count variable from global
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    memory[REGISTER[regA] + offset] = REGISTER[regB] #load register[regB] to memory[REGISTER[regA] + offset]
    printState() #call printState func

def op_beq(regA , regB , offset):
    global REGISTER #call register variable from global
    global pc, count #call pc, count variable from global
    count += 1
    if( REGISTER[regA] == REGISTER[regB] ): #compare value of register[regA] and register[regB]
        pc = pc+1+offset #if equal do pc += 1+offset
        printState() #call printState func
    else: 
        pc += 1 #if not equal do pc += 1
        printState() #call printState func

def op_jalr(regA , regB):
    global REGISTER #call register variable from global
    global pc #call pc variable from global
    if(REGISTER[regA] == REGISTER[regB]): #compare value of register[regA] and register[regB]
        REGISTER[regB] = pc+1 #if equal do register[regB] = pc+1
        pc = pc+1
        # printState()
    else:
        REGISTER[regB] = pc+1
        pc = REGISTER[regA] #if not equal assign register[regA] to pc
        # printState()

def op_halt():
    global pc, count #call pc, count variable from global
    pc = pc+1
    count += 1

    print("machine halted")
    print("total of ", count, " instructions executed")
    print("final state of machine: \n")
    printState() #call printState func

def op_noop():
    pass #pass the function

def printState(): #printState func
    global instruction_execute, pc #call instruction_execute, pc from global
    instruction_execute += 1
    print("@@@" + "\n" + "state:")
    print("\t PC " + str(pc))
    print("\t memory:")
    for i in range(len(memory)): #loop of represent value in memory list
        print("\t\t mem[" + str(i) + "] " + str(memory[i]))
    print("\t register:")
    for i in range(len(REGISTER)): #loop of represent value in register list
        print("\t\t register[" + str(i) + "] " + str(REGISTER[i]))
    print("end state\n")
    # pc += 1

def machinecodereader(input):
    REGISTER[0] = 0
    str_input = '{:032b}'.format(input)
    bin_input = int(str_input)
    new_strList = []
    stop_loop = False #set stop_loop is false in the beginning
    if ( str_input[7] == '0' and str_input[8] == '0') :
        str_rd = str_input[29:32] #bring position of string at 29-32 to str_rd
        str_rs = str_input[10:13] #bring position of string at 10-13 to str_rd
        str_rt = str_input[13:16] #bring position of string at 13-16 to str_rd
        int_rd = int(str_rd , 2)
        int_rs = int(str_rs , 2)
        int_rt = int(str_rt , 2)
        if (str_input[9] == '0') :
            op_add(int_rs, int_rt, int_rd) #call add func
        else:
            op_nand(int_rs, int_rt, int_rd) #call nand func
    elif ( str_input[7] == '0' and str_input[8] == '1') :
        str_off = str_input[16:32] #bring position of string at 16-32 to str_rd
        str_rs = str_input[10:13] #bring position of string at 10-13 to str_rd
        str_rd = str_input[13:16] #bring position of string at 13-16 to str_rd
        int_off = int(str_off , 2)
        int_rs = int(str_rs , 2)
        int_rd = int(str_rd , 2)

        if (str_input[9] == '0') :
            op_lw(int_rs, int_rd, int_off) #call load func
        else:
            op_sw(int_rs, int_rd, int_off) #call store func
    elif ( str_input[7] == '1' and str_input[8] == '0') :
        if (str_input[9] == '0') :
            str_off = str_input[16:32] #bring position of string at 16-32 to str_rd
            str_rs = str_input[10:13] #bring position of string at 10-13 to str_rd
            str_rd = str_input[13:16] #bring position of string at 13-16 to str_rd
            int_off = two2dec(str_off) #call two2dec func
            int_rs = int(str_rs , 2)
            int_rd = int(str_rd , 2)

            op_beq(int_rs, int_rd, int_off) #call beq func
        else:
            print("jalr")
    elif ( str_input[7] == '1' and str_input[8] == '1') :
        if (str_input[9] == '0') :
             # print("halt")
            op_halt() #call halt func
            stop_loop = True
        else:
            # print("noop")
            op_noop() #call noop func
    else : 
        pass
        print("in this")
    return stop_loop


def main(): #main func
    inputFromAssembler()
    printState()

    global pc
    while(True): #while loop until return of machinecodereader func is true
        print(pc)
        stop_loop = machinecodereader(int(memory[pc]))
        if stop_loop == True: break



main()