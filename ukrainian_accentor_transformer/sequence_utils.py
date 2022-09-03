from difflib import SequenceMatcher



def accent_flag(code: list, output: str):
    flag = (   
        (code[2] - code[1] == 1) and
        (output[code[1]:code[2]] == "\u0301") and
        (code[0] == 'delete')
    )
    return flag


def get_opcodes(input: str, output: str):
    opcodes = SequenceMatcher(a=output, b=input, autojunk=False).get_opcodes()
    # Keep accent
    for idx in range(len(opcodes)):
        code = opcodes[idx]
        if accent_flag(code, output):
            opcodes[idx] = ("equal", *code[1:])
    return opcodes


def diff_fix(input: str, output: str):
    opcodes = get_opcodes(input = input, output = output)
    fixed = ""
    for code in opcodes:
        operation, idxs = code[0], code[1:]
        if operation == "equal":
            fixed += output[idxs[0]:idxs[1]]
        elif operation == "delete":
            pass
        elif (operation == "insert") or (operation == "replace"):
            fixed += input[idxs[2]:idxs[3]]
    return fixed