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
        if (line[0] not in operations):
            if(line[0] not in labelMapping):
                if(len(line) == 1):
                    print("wrong opcode: probably input only a label no opeation")
                    exit(1)
                elif(len(line[0])>6):
                    print("label exceeds 6 character")
                    exit(1)
                else:
                    labelMapping.update({line[0]: count})
            else:
                print("label already define: "+line[0])
        count += 1
    count = 0

    # Input Loop
    # loop whole input to make a list of string of opcode and field of each input line
    for i in readIn:
        operation = []
        line = i.split()
        line[len(line)-1] = line[len(line)-1].replace("\n", "")
        isLabel = 0
        # checking if this line has label or not if yes skip the [0]
        #                   line[0]     line[1]
        # with label         label       opcode
        # without label      opcode      field1
        if(line[0] in labelMapping):
            isLabel = 1
        if(isLabel == 1 and line[1] in operations):
            print("label cannot be operation")
            exit(1)
        # check if opcode is known in requirement
        if(line[isLabel] not in operations):
            print("wrong opcode")
            exit(1)
        # check offset field
        if(line[isLabel] in branchOP and numcheck(line[isLabel+3])):
            lowest = -32768
            if(int(line[3+isLabel]) < lowest or int(line[3+isLabel]) > 32767):
                print("too greedy")
                exit(1)
        # spliting sessions
        # 3 field operation ex add r1 r2 r3
        if(line[isLabel] not in specialOP):
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
                        operation.append(
                            str(labelMapping[line[isLabel+3]]-count-1))
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

    for i in allLines:
        machineCode = Assembler(i)
        output.write(str(machineCode) + '\n')
        
    input.close()
    output.close()