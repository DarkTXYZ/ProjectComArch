# from assembler import Assembler

input = open('Assembler\input.txt', 'r')
output = open('Assembler\output.txt', "w")
readIn = input.readlines()
labelMapping = {}
operations = ["add", "nand", "lw", "sw", "beq", "jalr", "halt", "noop",".fill"]
specialOP = ["halt", "noop", ".fill"]
branchOP = ["lw","sw","beq"]
count = 0
allLines = []

#Mapping Loop
for i in readIn:
    line = i.split(" ")
    line[len(line)-1] = line[len(line)-1].replace("\n", "")
    if (line[0] not in operations and line[0] not in labelMapping):
        if(len(line)==1):
            print("wrong opcode")
            exit(1)
        labelMapping.update({line[0]: count})
    count += 1
print(labelMapping)
count = 0

#Input Loop
for i in readIn:
    operation=[]
    line = i.split(" ")
    line[len(line)-1] = line[len(line)-1].replace("\n", "")
    isLabel = 0
    if(line[0] in labelMapping): isLabel = 1
    print(line)
    if(line[isLabel] not in operations):
        print("wrong opcode")
        exit(1)
    if(line[isLabel] in branchOP and line[isLabel+3].isnumeric()):
        lowest = -32768
        if(int(line[3+isLabel]) < lowest  or int(line[3+isLabel])>32767):
            print("too greedy")
            exit(1) 
    if(line[isLabel] not in specialOP):
        operation.append(line[isLabel])
        operation.append(line[isLabel+1])
        operation.append(line[isLabel+2])
        if(line[isLabel+3].isnumeric()) : operation.append(line[isLabel+3])
        else:
            if(line[isLabel+3] in labelMapping):
                if(line[isLabel] == 'beq'): operation.append(str(labelMapping[line[isLabel+3]]-count-1))
                else:operation.append(str(labelMapping[line[isLabel+3]]))
            else:
                print("undefined label")
                exit(1)
    elif line[isLabel] == ".fill":
        operation.append(line[isLabel])
        print(line[isLabel+1])
        if(line[isLabel+1].isnumeric()): operation.append(line[isLabel+1])
        else:
            if(line[isLabel+1] in labelMapping): operation.append(str(labelMapping[line[isLabel+1]]))
            else:
                print("undefined label")
                exit(1)
    elif line[isLabel] == "halt" or line[isLabel] == "noop":
        operation.append(line[isLabel])
    count+=1
    allLines.append(operation)










# for i in readIn:
#     operation = []
#     line = i.split(" ")
#     line[len(line)-1] = line[len(line)-1].replace("\n", "")
#     isLabel = 0
#     if (line[0] not in operations) and i != "noop\n":
#         isLabel = 1
#     if (line[isLabel] not in specialOP and line[isLabel] not in operations):
#         print("wrong input")
#         exit(1)
  
#     if (line[isLabel] not in specialOP):
#         for j in range(4):
#             if(j==3 and not line[3+isLabel].isnumeric()):
#                 if (line[3+isLabel] in labelMapping):
#                     if (line[isLabel] == 'beq'):
#                         line[3+isLabel] = str(labelMapping[line[3+isLabel]]-count-1)
#                     else:
#                         line[3+isLabel] = str(labelMapping[line[3+isLabel]])
#                 else: 
#                     print("wrong label")
#                     exit(1)
#             operation.append(line[j+isLabel])
#     elif line[isLabel] == ".fill":
#         operation.append(line[isLabel])
#         if (line[isLabel+1] in labelMapping):
#             line[isLabel+1] = str(labelMapping[line[isLabel+1]])
#         if(line[isLabel+1] not in labelMapping and not line[isLabel+1].isnumeric()):
#             print("undefine label")
#             exit(1)
#         operation.append(line[isLabel+1])
#     else:
#         operation.append(line[isLabel])
#     if(line[isLabel] in branchOP):
#         lowest = -32768
#         if(int(line[3+isLabel]) < lowest  or int(line[3+isLabel])>32767):
#             print("too greedy")
#             exit(1) 
#     allLines.append(operation)
#     count += 1
#Correction Loop

for i in allLines:
    # machineCode = Assembler(i)
    # print(i, machineCode)
    # output.write(str(machineCode) + '\n')
    print(i)
