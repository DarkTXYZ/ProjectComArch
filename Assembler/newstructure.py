from Assembler.assembler import Assembler

input = open('assembly_program.txt', 'r')
output = open('machine_code.txt', "w")
readIn = input.readlines()
labelMapping = {}
operations = ["add", "nand", "lw", "sw",
            "beq", "jalr", "halt", "noop", ".fill"]
specialOP = ["halt", "noop", ".fill", "jalr"]
Itype = ["lw", "sw", "beq"]
Rtype = ["add", "nand"]
Otype = ["noop","halt"]
count = 0
allLines = []
labelLine =[]

def numcheck(s):
    try:
        num = int(s)
        isNumber = True
    except:
        isNumber = False
    return isNumber

def outRange(c):
    try:
        regC = int(c)
        if(regC <= 7 and regC >= 0):
            retBool = False
        else:
            retBool = True
    except:
        print("register cannot be symbolic")
        exit(1)
        
# Verify if the number of instructions exceeds 65536 or not.
if len(readIn) > 65536 :
    print('instructions number exceeded')
    exit(1)
#label check loop

for i in readIn:
    line = i.split()
    line[len(line)-1] = line[len(line)-1].replace("\n", "")
    #check first string
    if(line[0] not in operations):
        #check if input only label
        if(len(line) == 1):
            print("wrong syntax: input only label")
            exit(1)
        if(numcheck(line[0][0])):
            print("first char is number")
            exit(1)
        if(len(line[0])>6):
            print("label exceeds 6 character")
            exit(1)
        if(line[0] not in labelMapping):
            labelMapping.update({line[0]: count})
            labelLine.append(count)
        else:
            print("label already define: "+line[0])
            exit(1)
    count+=1

count = 0

for i in readIn:
    operation = []
    line = i.split()
    line[len(line)-1] = line[len(line)-1].replace("\n", "")
    isLabel = 0
    if(count in labelLine):
        isLabel = 1
    if(line[isLabel] not in operations):
        print("wrong opcode")
        exit(1)
    if(line[isLabel] in Itype and numcheck(line[isLabel+3])):
            lowest = -32768
            if(int(line[3+isLabel]) < lowest or int(line[3+isLabel]) > 32767):
                print("offsetfiled is out of range ")
                exit(1)
    if(line[isLabel] in Rtype):
        if(not numcheck(line[isLabel+1]) or not numcheck(line[isLabel+2]) or not numcheck(line[isLabel+3])):
            print("Rtype: register cannot be symbolic")
            exit(1)
        if(outRange(line[isLabel+1]) or outRange(line[isLabel+2]) or outRange(line[isLabel+3])):
            print("Rype: register out of range ")
            exit(1)
        operation.append(line[isLabel])
        operation.append(line[isLabel+1])
        operation.append(line[isLabel+2])
        operation.append(line[isLabel+3])
    elif(line[isLabel] in Itype):
        if(not numcheck(line[isLabel+1]) or not numcheck(line[isLabel+2])):
            print("Itype: register cannot be symbolic")
            exit(1)
        if(outRange(line[isLabel+1]) or outRange(line[isLabel+2])):
            print("Rype: register out of range ")
            exit(1)
        operation.append(line[isLabel])
        operation.append(line[isLabel+1])
        operation.append(line[isLabel+2])
        if(numcheck(line[isLabel+3])):
            operation.append(line[isLabel+3])
        else:
            if(line[isLabel+3] in labelMapping):
                # branching have deferent value replacement (relatively)
                if(line[isLabel] == 'beq'):
                    operation.append(str(labelMapping[line[isLabel+3]]-count-1))
                else:
                    operation.append(str(labelMapping[line[isLabel+3]]))
            else:
                print("Itype: undefined label")
                exit(1)
    elif(line[isLabel] == "jalr"):
        if(not numcheck(line[isLabel+1])):
            print("register cannot be symbolic")
            exit(1)
        if(not numcheck(line[isLabel+1]) or not numcheck(line[isLabel+2])):
            print("Itype: register cannot be symbolic")
            exit(1)
        if(outRange(line[isLabel+1]) or outRange(line[isLabel+2])):
            print("Rype: register out of range ")
            exit(1)
        operation.append(line[isLabel])
        operation.append(line[isLabel+1])
        operation.append(line[isLabel+2])
    elif(line[isLabel] in Otype):
        operation.append(line[isLabel])
    elif(line[isLabel] ==".fill"):
        operation.append(line[isLabel])
        # check for last field label
        if(numcheck(line[isLabel+1])):
            if(int(line[isLabel+1]) >32767):
                print("number is out of range .fill")
                exit(1)
            elif(int(line[isLabel+1]) < -32768):
                print("number is out of range .fill")
                exit(1)
            else:
                operation.append(line[isLabel+1])
        else:
            if(line[isLabel+1] in labelMapping):
                operation.append(str(labelMapping[line[isLabel+1]]))
            else:
                print("undefined label: .fill")
                exit(1)
    count += 1
    allLines.append(operation)

for i in allLines:
    machineCode = Assembler(i)
    print(i)
    print(machineCode)
    output.write(str(machineCode) + '\n')

        
        


    