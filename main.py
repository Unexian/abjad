import re
import math
import random
import sys
import functools

class AbjadGenericException(Exception):
    pass
class AbjadTermException(AbjadGenericException):
    pass
class AbjadArgumentException(AbjadGenericException):
    pass
class AbjadAssertException(AbjadGenericException):
    pass
class AbjadValueException(AbjadGenericException):
    pass

def concat(arr):
    return functools.reduce(lambda x, y: x + " " + y, arr, "")

def parse_complex(num):
    if re.search("^(-?\d+(\.\d+)?)$", num):
        return float(re.search("^(-?\d+(\.\d+)?)$", num).groups()[0]) + 0j
    elif re.search("^(-?\d+(\.\d+)?)j$", num):
        return float(re.search("^(-?\d+(\.\d+)?)j$", num).groups()[0]) * 1j
    elif re.search("^(-?\d+(\.\d+)?)([+-]\d+(\.\d+)?)j$", num):
        return float(re.search("^(-?\d+(\.\d+)?)([+-]\d+(\.\d+)?)j$", num).groups()[0]) + float(re.search("^(-?\d+(\.\d+)?)([+-]\d+(\.\d+)?)j$", num).groups()[2]) * 1j
    else:
        return False

def abjad(code, inp=[], vars={}):
    lines = re.split('\n|//|nl', code)
    split = []
    for ln in lines:
        split += [ln.casefold().split()]
    stack1 = inp
    stack2 = []
    variables = vars
    for ln in split:
        if len(ln) == 0:
            continue
        assign = None
        if ln[0] == "asgn":
            assign = ln[1]
            ln = ln[2:]
        elif ln[0] == "def":
            variables[ln[1]] = concat(ln[2::])
            continue
        elif ln[0] == "import":
            with open(ln[1] + ".abjad", 'r') as code:
                variables |= abjad(code.read(), ln[2::])[1]
            continue
        elif ln[0] == "comm":
            continue
        ln = ln[::-1]
        for term in ln:
            # literals
            if parse_complex(term) is not False:
                stack1 = [parse_complex(term)] + stack1
            # consts
            elif term == "e":
                stack1 = [math.e + 0j] + stack1
            elif term == "j":
                stack1 = [1j] + stack1
            elif term == "pi":
                stack1 = [math.pi + 0j] + stack1
            elif term == "tau":
                stack1 = [2 * math.pi + 0j] + stack1
            elif term == "eta":
                stack1 = [math.pi / 2 + 0j] + stack1
            elif term == "inf":
                stack1 = [math.inf + 0j] + stack1
            elif term == "eps":
                stack1 = [sys.float_info.epsilon + 1 + 0j] + stack1
            elif term == "mu":
                stack1 = [sys.float_info.min + 0j] + stack1
            elif term == "omg":
                stack1 = [sys.float_info.max + 0j] + stack1
            elif term == "rand":
                stack1 = [random.uniform(0, 1) + 0j] + stack1
            # math
            elif term == "add":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = top[1] + top[0]
            elif term == "neg":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = -stack1[0]
            elif term == "sub":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = top[1] - top[0]
            elif term == "mul":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = top[1] * top[0]
            elif term == "rcp":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                if stack1[0] == 0:
                    stack1[0] = math.inf
                stack1[0] = 1/stack1[0]
            elif term == "div":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                if top[0] == top[1]:
                    stack1[0] = 1
                elif top[0] == 0:
                    stack1[0] = math.inf * abs(top[1]) / top[1]
                else:
                    stack1[0] = top[1] / top[0]
            elif term == "mod":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                if top[0] == 0:
                    stack1[0] = 0
                else:
                    stack1[0] = top[1] % top[0]
            elif term == "abs":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = abs(stack1[0])
            elif term == "sgn":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = abs(stack1[0]) / stack1[0]
            elif term == "pow":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = top[1] ** top[0]
            elif term == "sqrt":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                top = stack1[0]
                stack1[0] = top ** 0.5
            elif term == "log":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = math.log(top[1], top[0])
            elif term == "sin":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.sin(stack1[0])
            elif term == "cos":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.cos(stack1[0])
            elif term == "tan":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.tan(stack1[0])
            elif term == "asin":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.asin(stack1[0])
            elif term == "acos":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.acos(stack1[0])
            elif term == "atan":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.atan(stack1[0])
            elif term == "flr":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.floor(stack1[0])
            elif term == "ceil":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.ceil(stack1[0])
            elif term == "rnd":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.round(stack1[0])
            # equality
            elif term == "eq":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = float(top[1] == top[0])
            elif term == "neq":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = float(top[1] != top[0])
            elif term == "lt":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = float(top[1] < top[0])
            elif term == "gt":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = float(top[1] > top[0])
            elif term == "lte":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = float(top[1] <= top[0])
            elif term == "gte":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = float(top[1] >= top[0])
            elif term == "min":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = min(top[1], top[0])
            elif term == "max":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                top = stack1[:2:]
                stack1 = stack1[1::]
                stack1[0] = max(top[1], top[0])
            # stack
            elif term == "dup":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1 = [stack1[0]] + stack1
            elif term == "pop":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1 = stack1[1::]
            elif term == "swp":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                if len(stack2) == 0:
                    raise AbjadArgumentException(len(stack2), 1)
                top1 = stack1[0]
                top2 = stack2[0]
                stack1 = stack1[1::]
                stack2 = stack2[1::]
                stack1 = [top2] + stack1
                stack2 = [top1] + stack2
            elif term == "lft":
                if len(stack2) == 0:
                    raise AbjadArgumentException(len(stack2), 1)
                stack1 = [stack2[0]] + stack1
                stack2 = stack2[1::]
            elif term == "rgt":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                stack2 = [stack1[0]] + stack2
                stack1 = stack1[1::]
            # other
            elif term == "asrt":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                elif stack1[0] != 1:
                    raise AbjadAssertException(stack1[0])
                else:
                    stack1 = stack1[1::]
            elif term == "dbg":
                print((stack1, stack2))
            elif term == "inp":
                inputted = parse_complex(input())
                if inputted is False:
                    raise AbjadValueException(inputted)
                else:
                    stack1 = [inputted] + stack1
            elif term == "out":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                print(stack1[0])
                stack1 = stack1[1::]
            elif term == "cout":
                if len(stack1) == 0:
                    raise AbjadArgumentException(len(stack1), 1)
                if stack1[0].imag != 0 or stack1[0].real < 0 or stack1[0].real % 1 != 0:
                    raise AbjadValueException(stack1[0])
                print(chr(round(stack1[0].real)), end="")
                stack1 = stack1[1::]
            elif term == "nop":
                pass
            elif term in variables:
                if isinstance(variables[term], float):
                    stack1 = [variables[term]] + stack1
                elif isinstance(variables[term], str):
                    stack1 = abjad(variables[term], stack1, variables)[0]
            else:
                raise AbjadTermException(term)
        if assign is not None:
            variables[assign] = stack1[0]
            stack1 = stack1[1::]

    return stack1, variables

if __name__ == '__main__':
    if len(sys.argv) < 2:
        with open("main.abjad", 'r') as code:
            abjad(code.read())
    elif re.fullmatch(r"^\w+\.abjad", sys.argv[1]):
        with open(sys.argv[1], 'r') as code:
            abjad(code.read(), sys.argv[2:])
    else:
        abjad(concat(sys.argv[1::]))
