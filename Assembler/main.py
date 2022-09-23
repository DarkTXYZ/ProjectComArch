from textwrap import fill

from numpy import append


input = open('Assembler\input.txt' , 'r')
# print(input.readlines())
readin = input.readlines()



# a = Assembler('','','','','')

# a.returnMachineCode()
# instruction = {
#     'label' : '' ,
#     'op' : '' ,
#     'rs1' : '' ,
#     'rs2' : '' ,
#     'imm' : '' 
# }
a = {}
b = ["add","nand","lw","sw","beq","jalr","halt","noop","halt\n","noop\n"]
specialOP = ["halt","noop",".fill","halt\n","noop\n"]
s= 0
allLines =[]

for i in readin:
    operation = []
    line = i.split(" ")
    isLabel = 0
    if (line[0] not in b) and i != "noop\n": 
        a.update({line[0]:s})
        isLabel = 1
    # print(line)
    # print(isLabel)
    # print(line[isLabel])
    if(line[isLabel] not in specialOP):
        for j in range (4):
            it = j
            operation.append(line[it+isLabel])
    elif line[isLabel] == ".fill" :
        operation.append(line[isLabel])
        operation.append(line[isLabel+1])
    else: operation.append(line[isLabel])
    s+=1
    # print(operation)
    allLines.append(operation)
# print(allLines)
print(a)
for i in allLines:
    print(i)
# for i in allLines:
#     print(i)
    
# for loop เก็บ label 
# for loop วนอ่านคำสั่ง
    # คำสั่งมี label , instruction , rs1 , ...
    # โยนข้อมูลให้ Assembler -> machine code
    # เอา machine code มา แสดง