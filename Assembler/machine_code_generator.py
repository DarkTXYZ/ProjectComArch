from atexit import register


def MachineCodeGenerator() : 
    from Assembler.assembler import Assembler

    input = open('assembly_program.txt', 'r')
    output = open('machine_code.txt', "w")
    readIn = input.readlines()
    labelMapping = {}
    operations = ["add", "nand", "lw", "sw",
                "beq", "jalr", "halt", "noop", ".fill"]
    specialOP = ["halt", "noop", ".fill", "jalr"]
    branchOP = ["lw", "sw", "beq"]
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

    # Verify if the number of instructions exceeds 65536 or not.
    if len(readIn) > 65536 :
        print('instructions number exceeded')
        exit(1)

    # Mapping Loop
    # loop whole input to extract label and it's memory
    for i in readIn:
        line = i.split()
        line[len(line)-1] = line[len(line)-1].replace("\n", "")
        #check if 
        if (line[0] not in operations):
            if(len(line) == 1):
                    print("wrong opcode: probably input only a label no opeation")
                    exit(1)
            #check wrong opcode
            if(line[1] not in operations):
                print("wrong syntax: maybe inputing 2 label or wrong opcode")
                exit(1)
            if(line[0] not in labelMapping):
                #check if the line only has a label
                if(len(line) == 1):
                    print("wrong opcode: probably input only a label no opeation")
                    exit(1)
                #check if the first char is numberic
                elif(numcheck(line[0][0])):
                    print("first char is numberic")
                    exit(1)
                #check if the label is longer than 6 char
                elif(len(line[0])>6):
                    print("label exceeds 6 character")
                    exit(1)
                else:
                    labelMapping.update({line[0]: count})
                    labelLine.append(count)
            else:
                print("label already define: "+line[0])
                exit(1)
        count += 1
        
    count = 0

    # Input Loop
    # loop whole input to make a list of string of opcode and field of each input line
    labelcounter = 0
    for i in readIn:
        operation = []
        line = i.split()
        line[len(line)-1] = line[len(line)-1].replace("\n", "")
        isLabel = 0
        # checking if this line has label or not if yes skip the [0]
        #                   line[0]     line[1]
        # with label         label       opcode
        # without label      opcode      field1
        if(labelcounter in labelLine):
            isLabel = 1
        # check if opcode is known in requirement
        if(line[isLabel] not in operations):
            print("wrong opcode")
            exit(1)
        # check offset field
        if(line[isLabel] in branchOP and numcheck(line[isLabel+3])):
            lowest = -32768
            if(int(line[3+isLabel]) < lowest or int(line[3+isLabel]) > 32767):
                print("offsetfiled is out of range ")
                exit(1)
        # spliting sessions
        # 3 field operation ex add r1 r2 r3
        if(line[isLabel] not in specialOP):
            #check symbolic reg
            if(not numcheck(line[isLabel+1]) and not numcheck(line[isLabel+2]) ):
                print("register cannot be symbolic")
                exit(1)
            if(int(line[isLabel+1]) > 7  or int(line[isLabel+2]) >7):
                print("register out of range")
            operation.append(line[isLabel])
            operation.append(line[isLabel+1])
            operation.append(line[isLabel+2])
            if(numcheck(line[isLabel+3])):
                operation.append(line[isLabel+3])
            else:
                # check the last field if it's label replace with the mapped value
                if(line[isLabel+3] in labelMapping):
                    # branching have deferent value replacement (relatively)
                    if(line[isLabel] == 'beq'):
                        operation.append(str(labelMapping[line[isLabel+3]]-count-1))
                    else:
                        operation.append(str(labelMapping[line[isLabel+3]]))
                else:
                    print("undefined label: 3field operation")
                    exit(1)
        # .fill
        elif line[isLabel] == ".fill":
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
        # 2 field operation
        elif line[isLabel] == "jalr":
            operation.append(line[isLabel])
            #check symbolic reg
            if(not numcheck(line[isLabel+1])):
                print("register cannot be symbolic")
                exit(1)
            if(int(line[isLabel+1]) > 7):
                print("register out of range")
            operation.append(line[isLabel+1])
            # check label
            if(numcheck(line[isLabel+2])):
                operation.append(line[isLabel+2])
            else:
                if(line[isLabel+2] in labelMapping):
                    operation.append(str(labelMapping[line[isLabel+2]]))
                else:
                    print("undefined label: jalr")
                    exit(1)
        # no field operation
        elif line[isLabel] == "halt" or line[isLabel] == "noop":
            operation.append(line[isLabel])
        count += 1
        allLines.append(operation)
        labelcounter +=1

    for i in allLines:
        machineCode = Assembler(i)
        print(i)
        print(machineCode)
        output.write(str(machineCode) + '\n')
        
    input.close()
    output.close()
