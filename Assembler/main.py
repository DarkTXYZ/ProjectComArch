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
b = ["add","nand","lw","sw","beq","jalr","halt","noop"]
specialOP = ["halt","noop",".fill"]
s= 0
allLines =[]
for i in readin:
    line = i.split(" ")
    line[len(line)-1] = line[len(line)-1].replace("\n","")
    if (line[0] not in b): 
        a.update({line[0]:s})
    s+=1 
print(a) 

for i in readin:
    operation = []
    line = i.split(" ")
    line[len(line)-1] = line[len(line)-1].replace("\n","")
    # print(line)
    # print(line[len(line)-1])
   
    isLabel = 0
    if (line[0] not in b) and i != "noop\n": 
        isLabel = 1
    # print(line)
    # print(isLabel)
    # print(line[isLabel])
    if(line[isLabel] not in specialOP):
        for j in range (4): 
            it = j
            if(j == 3 and line[it+isLabel] in a):
                # print(a[line[it+isLabel]])
                line[it+isLabel] = a[line[it+isLabel]]
            operation.append(line[it+isLabel])
    elif line[isLabel] == ".fill" :
        operation.append(line[isLabel])
        if(line[isLabel+1] in a):
            line[isLabel+1] = a[line[isLabel+1]]
        operation.append(line[isLabel+1])
    else: operation.append(line[isLabel])
    # print(operation)
    allLines.append(operation)
# print(allLines)
# print(a)
for i in allLines:
    print(i)
    
# for loop เก็บ label 
# for loop วนอ่านคำสั่ง
    # คำสั่งมี label , instruction , rs1 , ...
    # โยนข้อมูลให้ Assembler -> machine code
    # เอา machine code มา แสดง