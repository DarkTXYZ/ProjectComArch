def MachineCodeGenerator():
    from Assembler.assembler import Assembler

    input = open('assembly_program.txt', 'r')
    output = open('machine_code.txt', "w")
    readIn = input.readlines()
    labelMapping = {}
    operations = ["add", "nand", "lw", "sw",
                  "beq", "jalr", "halt", "noop", ".fill"]
    Itype = ["lw", "sw", "beq"]
    Rtype = ["add", "nand"]
    Otype = ["noop", "halt"]
    count = 0
    allLines = []
    labelLine = []
    # function for checking input's field

    def numcheck(s):
        try:
            num = int(s)
            isNumber = True
        except:
            isNumber = False
        return isNumber
    # function for checking register range

    def outRange(c):
        try:
            regC = int(c)
            if(regC <= 7 and regC >= 0):
                retBool = False
            else:
                retBool = True
            return retBool
        except:
            print("register cannot be symbolic")
            exit(1)

    # Verify if the number of instructions exceeds 65536 or not.
    if len(readIn) > 65536:
        print('instructions number exceeded')
        exit(1)

    # 1st loop for labeling
    for i in readIn:
        line = i.split()
        line[len(line)-1] = line[len(line)-1].replace("\n", "")
        # check first string
        if(line[0] not in operations):
            # check if input only label
            if(len(line) == 1):
                print("wrong syntax: input only label")
                exit(1)
            # check if first char is number
            if(numcheck(line[0][0])):
                print("first char is number")
                exit(1)
            # check if label exceed 6 char
            if(len(line[0]) > 6):
                print("label exceeds 6 character")
                exit(1)
            # check if label was already defined
            if(line[0] not in labelMapping):
                labelMapping.update({line[0]: count})
                labelLine.append(count)
            else:
                print("label was already defined: "+line[0])
                exit(1)
        count += 1

    count = 0

    for i in readIn:
        operation = []
        line = i.split()
        line[len(line)-1] = line[len(line)-1].replace("\n", "")
        isLabel = 0
        # skipping label for line with label
        #                   line[0]     line[1]
        # with label         label       opcode
        # without label      opcode      field1
        if(count in labelLine):
            isLabel = 1
        # checking if opcode is wrong
        if(line[isLabel] not in operations):
            print("wrong opcode")
            exit(1)
        # checking if offset field input is out of range
        if(line[isLabel] in Itype and numcheck(line[isLabel+3])):
            lowest = -32768
            if(int(line[3+isLabel]) < lowest or int(line[3+isLabel]) > 32767):
                print("offset field is out of range ")
                exit(1)
        # R-type 3 field register only
        if(line[isLabel] in Rtype):
            # check symbolic register input
            if(not numcheck(line[isLabel+1]) or not numcheck(line[isLabel+2]) or not numcheck(line[isLabel+3])):
                print("R-type: register cannot be symbolic")
                exit(1)
            # check if register is out of range
            if(outRange(line[isLabel+1]) or outRange(line[isLabel+2]) or outRange(line[isLabel+3])):
                print("R-type: register out of range ")
                exit(1)
            operation.append(line[isLabel])
            operation.append(line[isLabel+1])
            operation.append(line[isLabel+2])
            operation.append(line[isLabel+3])
        # I-type 2 registers 1 offsetfiled
        elif(line[isLabel] in Itype):
            # check symbolic register input
            if(not numcheck(line[isLabel+1]) or not numcheck(line[isLabel+2])):
                print("I-type: register cannot be symbolic")
                exit(1)
            # check if register is out of range
            if(outRange(line[isLabel+1]) or outRange(line[isLabel+2])):
                print("I-type: register out of range ")
                exit(1)
            operation.append(line[isLabel])
            operation.append(line[isLabel+1])
            operation.append(line[isLabel+2])
            # check if offsetField is label
            if(numcheck(line[isLabel+3])):
                operation.append(line[isLabel+3])
            else:
                # check label
                if(line[isLabel+3] in labelMapping):
                    # branching have deferent value replacement (relatively)
                    if(line[isLabel] == 'beq'):
                        operation.append(
                            str(labelMapping[line[isLabel+3]]-count-1))
                    else:
                        operation.append(str(labelMapping[line[isLabel+3]]))
                else:
                    print("Itype: undefined label")
                    exit(1)
        # J-type 2 registers
        elif(line[isLabel] == "jalr"):
            # check symbolic register input
            if(not numcheck(line[isLabel+1]) or not numcheck(line[isLabel+2])):
                print("J-type: register cannot be symbolic")
                exit(1)
            if(outRange(line[isLabel+1]) or outRange(line[isLabel+2])):
                print("J-type: register out of range ")
                exit(1)
            operation.append(line[isLabel])
            operation.append(line[isLabel+1])
            operation.append(line[isLabel+2])
        # O-type no field
        elif(line[isLabel] in Otype):
            operation.append(line[isLabel])
        # .fill special 1 offset field
        elif(line[isLabel] == ".fill"):
            operation.append(line[isLabel])
            # check for last field label
            if(numcheck(line[isLabel+1])):
                if(int(line[isLabel+1]) > 32767):
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

    input.close()
    output.close()
