def Assembler(inst):
    """This function encodes assembly to binary machine code

    Args:
        List of string contains
            - op (str): operation
            - f0 (int): field0 -> regA
            - f1 (int): field1 -> regB
            - f2 (int): field2 -> destReg , offsetField , symbolicAddress

    Returns:
        str: binary machine code
    """
    op = inst[0]
    if(len(inst) >= 2):
        f0 = inst[1]
    if(len(inst) >= 3):
        f1 = inst[2]
    if(len(inst) >= 4):
        f2 = inst[3]

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
        return 'not implement yet'

# R-type instructions (add, nand)
#                Bits 24-22 opcode
#                Bits 21-19 reg A (rs)
#                Bits 18-16 res B (rt)
#                Bits 15-3 ไม่ใช้ (ควรตั้งไว้ที่ 0)
#                Bits 2-0  destReg (rd)
def R_type(op, f0, f1, f2):
    bit = 0
    if op == 'add':
        bit24_22 = int('000',2) << 22
        bit21_19 = int(f0) << 19
        bit18_16 = int(f1) << 16
        bit2_0 = int(f2)

        bit = bit21_19 + bit18_16 + bit2_0

    elif op == 'nand':
        bit24_22 = int('001',2) << 22
        bit21_19 = int(f0) << 19
        bit18_16 = int(f1) << 16
        bit2_0 = int(f2)

        bit = bit24_22 + bit21_19 + bit18_16 + bit2_0

    return bit

# I-type instructions (lw, sw, beq)
#                Bits 24-22 opcode
#                Bits 21-19 reg A (rs)
#                Bits 18-16 reg B (rt)
#                Bits 15-0 offsetField (เลข16-bit และเป็น 2’s complement  โดยอยู่ในช่วง –32768 ถึง 32767)
def I_type(op, f0, f1, f2):
    bit = 0
    if op == 'lw':
        bit24_22 = 1 << 23
        bit21_19 = int(f0) << 19
        bit18_16 = int(f1) << 16
        bit15_0 = int(f2)
        
        bit = bit24_22 + bit21_19 + bit18_16 + bit15_0
        
    elif op == 'sw':
        bit24_22 = 3 << 22
        bit21_19 = int(f0) << 19
        bit18_16 = int(f1) << 16
        bit15_0 = int(f2)
        
        bit = bit24_22 + bit21_19 + bit18_16 + bit15_0
        
    elif op == 'beq':
        bit24_22 = 1 << 24
        bit21_19 = int(f0) << 19
        bit18_16 = int(f1) << 16
        bit15_0 = int(f2)

        bit = bit24_22 + bit21_19 + bit18_16 + bit15_0
        
    return bit

# J-Type instructions (jalr)
#                Bits 24-22 opcode
#                Bits 21-19 reg A (rs)
#                Bits 18-16 reg B (rd)
#                Bits 15-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
def J_type(f0, f1):
    bit24_22 = int('101' , 2) << 22
    bit21_19 = int(f0) << 19
    bit18_16 = int(f1) << 16

    bit = bit24_22 + bit21_19 + bit18_16

    return bit

# O-type instructions (halt, noop)
#                Bits 24-22 opcode
#                Bits 21-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
def O_type(op):
    bit = 0
    if op == 'halt':
        bit = 3 << 23

    elif op == 'noop':
        bit = 7 << 22
    
    return bit
    