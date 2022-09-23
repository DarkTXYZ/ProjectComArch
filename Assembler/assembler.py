def Assembler(op, f0 = None, f1 = None, f2 = None):
    """This function encodes assembly to binary machine code

    Args:
        op (str): operation
        f0 (int): field0 -> regA
        f1 (int): field1 -> regB
        f2 (int): field2 -> destReg , offsetField , symbolicAddress

    Returns:
        str: binary machine code
    """
    if op == 'add':
        return R_type(op, f0, f1, f2)
    else:
        return 'can\'t encode'


def R_type(op, f0, f1, f2):
    return op


def I_type(op, f0, f1, f2):
    pass


def J_type(op, f0, f1):
    pass


def O_type(op):
    pass
