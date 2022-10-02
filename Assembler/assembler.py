def Assembler(inst):
    """This function encodes assembly code to binary machine code

    Args:
        List of string contains
            - op (str): operation
            - [optional] f0 (int): field0 -> regA
            - [optional] f1 (int): field1 -> regB
            - [optional] f2 (int): field2 -> destReg , offsetField , symbolicAddress

    Returns:
        str: binary machine code
    """
    # Extract fields in instruction
    op = inst[0]
    if(len(inst) >= 2):
        f0 = inst[1]
    if(len(inst) >= 3):
        f1 = inst[2]
    if(len(inst) >= 4):
        f2 = inst[3]

    # Format-type classification
    if op == 'add' or op == 'nand':
        return R_type(op, f0, f1, f2)
    elif op == 'lw' or op == 'sw' or op == 'beq':
        return I_type(op, f0, f1, f2)
    elif op == 'jalr':
        return J_type(f0, f1)
    elif op == 'halt' or op == 'noop':
        return O_type(op)
    elif op == '.fill':
        return int(f0)
    else:
        return 'operation not found'

# R-type instructions (add, nand)
#                Bits 24-22 op
#                Bits 21-19 f0
#                Bits 18-16 f1
#                Bits 15-3 ไม่ใช้ (ควรตั้งไว้ที่ 0)
#                Bits 2-0  f2
def R_type(op, f0, f1, f2):
    bit = 0
    # generate op binary code
    if op == 'add':
        bit24_22 = int('000',2) << 22
    elif op == 'nand':
        bit24_22 = int('001',2) << 22
    
    # generate f0 , f1 , f2 binary code
    bit21_19 = int(f0) << 19
    bit18_16 = int(f1) << 16
    bit2_0 = int(f2)

    # instruction machine code
    bit = (bit24_22) + (bit21_19) + (bit18_16) + (bit2_0)

    return (bit)

# I-type instructions (lw, sw, beq)
#                Bits 24-22 opcode
#                Bits 21-19 f0
#                Bits 18-16 f1
#                Bits 15-0 f2
def I_type(op, f0, f1, f2):
    bit = 0
    # generate opcode 
    if op == 'lw':
        bit24_22 = int('010',2) << 22
    elif op == 'sw':
        bit24_22 = int('011',2) << 22
    elif op == 'beq':
        bit24_22 = int('100',2) << 22

    # generate f0 , f1 , f2 binary code
    bit21_19 = int(f0) << 19
    bit18_16 = int(f1) << 16
    if int(f2) < 0: # Check if f2 is negative number 
        bit15_0 = int(f2) & 0b1111111111111111  # 2's complement
    else:
        bit15_0 = int(f2)

    # instruction machine code
    bit = (bit24_22) + (bit21_19) + (bit18_16) + (bit15_0)
        
    return (bit)

# J-Type instructions (jalr)
#                Bits 24-22 opcode
#                Bits 21-19 reg A (rs)
#                Bits 18-16 reg B (rd)
#                Bits 15-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
def J_type(f0, f1):
    bit24_22 = int('101' , 2) << 22
    bit21_19 = int(f0) << 19
    bit18_16 = int(f1) << 16

    bit = (bit24_22) + (bit21_19) + (bit18_16)

    return (bit)

# O-type instructions (halt, noop)
#                Bits 24-22 opcode
#                Bits 21-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
def O_type(op):
    bit = 0
    if op == 'halt':
        bit = int('110',2) << 22

    elif op == 'noop':
        bit = int('111',2) << 22
    
    return (bit)
    