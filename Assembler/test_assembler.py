from assembler import Assembler

a = Assembler(['.fill' , '32'])
print(bin(a))


# undefine label
# same label
# offsetField out of bound (-32768 to 32767)
# undefine opcode
# negative value
# beq