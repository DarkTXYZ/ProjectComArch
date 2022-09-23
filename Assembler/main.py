input = open('Assembler\input.txt' , 'r')

print(input.readlines())

# a = Assembler('','','','','')

# a.returnMachineCode()
# instruction = {
#     'label' : '' ,
#     'op' : '' ,
#     'rs1' : '' ,
#     'rs2' : '' ,
#     'imm' : '' 
# }

a = [1,2,3]

if 4 in a :
    print('yes')

for i in range(10) :
    print(i)

# for loop เก็บ label 
# for loop วนอ่านคำสั่ง
    # คำสั่งมี label , instruction , rs1 , ...
    # โยนข้อมูลให้ Assembler -> machine code
    # เอา machine code มา แสดง