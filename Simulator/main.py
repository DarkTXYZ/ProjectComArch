REGISTER = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]

def op_add(regA , regB , destReg):
    print()

def op_nand(regA , regB , destReg):
    print()

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


def machinecodereader(input):
    str_input = '{:032b}'.format(input)
    bin_input = int(str_input)
    # print(type(bin_input))
    # print(bin_input)
    if ( str_input[7] == '0' and str_input[8] == '0') :
        if (str_input[9] == '0') :
            print("add")
        else:
            print("nand")
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

