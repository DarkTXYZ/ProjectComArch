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
    elif op == 'jalr':
        return J_type(f0, f1)
    elif op == '.fill':
        return int(f0)
    else:
        return 'not implement yet'


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


def I_type(op, f0, f1, f2):
    pass


def J_type(f0, f1):
    bit24_22 = int('101' , 2) << 22
    bit21_19 = int(f0) << 19
    bit18_16 = int(f1) << 16

    bit = bit24_22 + bit21_19 + bit18_16

    return bit


def O_type(op):
    pass
    