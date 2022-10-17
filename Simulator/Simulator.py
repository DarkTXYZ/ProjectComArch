#! open in your file directory
#! variable
output = None
REGISTER = []
memory = []
pc = 0
instruction_execute = 0
count = 0



def inputFromAssembler(): #assign text from assembler to memory
    file = open("machine_code.txt", "r") #open machine code file
    file_read = file.read() #read file
    
    global memory #call memory variable from global
    input_split = file_read.split() #split text by \n
    for i in range(8):
        REGISTER.append(0) #push 0 to register list
    for i in range(len(input_split)):
        memory.append(int(input_split[i])) #push text that split by \n to memory list

    file.close() #close file


#! 2’s complement
def two2dec(s): #convert binary to dec
    if s[0] == '1':
        return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
    else:
        return int(s, 2)


def op_add(regA, regB, destReg): #add operator
    global pc, count
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    REGISTER[destReg] = REGISTER[regA] + REGISTER[regB] #bring register[regA] + register[regB] assign to register[destReg]
    printState() #call printState func


def op_nand(regA, regB, destReg): #nand operator
    global pc, count #call pc, count variable from global
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    REGISTER[destReg] = ~(REGISTER[regA] & REGISTER[regB]) #bring register[regA] nand register[regB] assign to register[destReg]
    printState() #call printState func


def op_lw(regA, regB, offset): #load word operator
    global pc, count #call pc, count variable from global
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    while REGISTER[regA] + offset >= len(memory) :
        memory.append(0)
    REGISTER[regB] = memory[(REGISTER[regA] + offset)] #load memory[(REGISTER[regA] + offset)] to register[regB]
    printState() #call printState func


def op_sw(regA, regB, offset): #store word operator
    global pc, count #call pc, count variable from global
    pc += 1
    count += 1
    global REGISTER #call register variable from global
    while REGISTER[regA] + offset >= len(memory) :
        memory.append(0)
    memory[REGISTER[regA] + offset] = REGISTER[regB] #load register[regB] to memory[REGISTER[regA] + offset]
    printState() #call printState func


def op_beq(regA, regB, offset): #branch equal operator
    global REGISTER #call register variable from global
    global pc, count #call pc, count variable from global
    count += 1
    if(REGISTER[regA] == REGISTER[regB]): #compare value of register[regA] and register[regB]
        if(pc+1+offset >= 0 and pc+1+offset <=65535):
            pc = pc+1+offset #if equal do pc += 1+offset
        else:
            print("Jump index out of range")
            exit(1)
        printState() #call printState func
    else:
        pc += 1
        printState() #call printState func


def op_jalr(regA, regB): #jalr operator
    global REGISTER #call register variable from global
    global pc, count #call pc & count variable from global
    count += 1
    if(regA == regB): #compare if regA and regB is the same register
        REGISTER[regB] = pc+1 #if equal do register[regB] = pc+1
        pc = pc+1
    else:
        REGISTER[regB] = pc+1 #if not equal assign register[regA] to pc
        pc = REGISTER[regA]


def op_halt():
    global pc, count #call pc, count variable from global
    pc = pc+1
    count += 1
    output.write("machine halted\n")
    output.write("total of " + str(count) + " instructions executed\n")
    output.write("final state of machine:\n\n")
    printState() #call printState func


def op_noop():
    global pc, count #call pc, count variable from global
    pc = pc+1
    count += 1
    pass #pass the function


def printState(): #printState func
    global instruction_execute, pc #call instruction_execute, pc from global
    instruction_execute += 1
    output.write("@@@" + "\n" + "state:\n")
    output.write("\tpc " + str(pc) + '\n')
    output.write("\tmemory:\n")
    for i in range(len(memory)): #loop of represent value in memory list
        output.write("\t\tmem[ " + str(i) + " ] " + str(memory[i]) + '\n')
    output.write("\tregisters:\n")
    for i in range(8): #loop of represent value in register list
        output.write("\t\treg[ " + str(i) + " ] " + str(REGISTER[i]) + '\n')
    output.write("end state\n\n")

def printHeader():
    for i in range(len(memory)): #loop of represent value in memory list
        output.write("memory[" + str(i) + "]=" + str(memory[i]) + '\n')
    for i in range(2):
        output.write('\n')
def machinecodereader(input):
    REGISTER[0] = 0
    str_input = '{:032b}'.format(input)
    stop_loop = False #set stop_loop is false in the beginning
    if (str_input[7] == '0' and str_input[8] == '0'):
        str_rd = str_input[29:32] #bring position of string at 29-32 to str_rd
        str_rs = str_input[10:13] #bring position of string at 10-13 to str_rd
        str_rt = str_input[13:16] #bring position of string at 13-16 to str_rd
        int_rd = int(str_rd, 2)
        int_rs = int(str_rs, 2)
        int_rt = int(str_rt, 2)
        if (str_input[9] == '0'):
            op_add(int_rs, int_rt, int_rd) #call add func
        else:
            op_nand(int_rs, int_rt, int_rd) #call nand func
    elif (str_input[7] == '0' and str_input[8] == '1'):
        str_off = str_input[16:32] #bring position of string at 16-32 to str_rd
        str_rs = str_input[10:13] #bring position of string at 10-13 to str_rd
        str_rd = str_input[13:16] #bring position of string at 13-16 to str_rd
        int_off = int(str_off, 2)
        int_rs = int(str_rs, 2)
        int_rd = int(str_rd, 2)

        if (str_input[9] == '0'):
            op_lw(int_rs, int_rd, int_off) #call load func
        else:
            op_sw(int_rs, int_rd, int_off) #call store func
    elif (str_input[7] == '1' and str_input[8] == '0'):
        str_off = str_input[16:32] #bring position of string at 16-32 to str_rd
        str_rs = str_input[10:13] #bring position of string at 10-13 to str_rd
        str_rd = str_input[13:16] #bring position of string at 13-16 to str_rd
        int_off = two2dec(str_off) #call two2dec func
        int_rs = int(str_rs, 2)
        int_rd = int(str_rd, 2)

        if (str_input[9] == '0'):
            op_beq(int_rs, int_rd, int_off) #call beq func
        else:
            op_jalr(int_rs, int_rd) #call jalr func
    elif (str_input[7] == '1' and str_input[8] == '1'):
        if (str_input[9] == '0'):
            op_halt() #call halt func
            stop_loop = True #set stop loop variable to true
        else:
            op_noop() #call noop func
    else:
        pass
    return stop_loop


def run_simulator(): #main func of simulator
    global output
    output = open("simulator_output.txt", "w") #read file from text
    inputFromAssembler()
    printHeader()
    printState()
    
    global pc, count
    while(True): #while loop until return of machinecodereader func is true
        stop_loop = machinecodereader(int(memory[pc]))
        if stop_loop == True:
            break
        elif count >= 5000: #check if count >= 5000 than break the loop
            print("infinite loop")
            exit(1)
        elif pc < 0 or pc > 65535 :
            print("Jump index out of range")
            exit(1)

    output.close()

