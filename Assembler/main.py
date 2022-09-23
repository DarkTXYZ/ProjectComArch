input = open('Assembler\input.txt' , 'r')

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
s= 0
print(readin)
for i in readin:
    spl = i.split(" ")[0] 
    print(i)
    if (spl not in b) and i != "noop": 
        a.update({spl:s})
        print(spl)
    print(s)
    s+=1
# for loop เก็บ label 
# for loop วนอ่านคำสั่ง
    # คำสั่งมี label , instruction , rs1 , ...
    # โยนข้อมูลให้ Assembler -> machine code
    # เอา machine code มา แสดง