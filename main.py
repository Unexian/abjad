import math
import random
import sys


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
    return " ".join(map(str, arr))


def parse_complex(num):
    try:
        return complex(num)
    except ValueError:
        return False


def abjad(code: str, *, inp: list = None, var: dict = None):

    lines = [line.casefold().split() for line in code.splitlines()]
    inp = [] if inp is None else inp
    var = {} if var is None else var
    stack1 = inp
    stack2 = []

    for line in lines:
        if len(line) == 0:
            continue
        assign = None
        if line[0] == "asgn":
            assign = line[1]
            line = line[2:]
        elif line[0] == "def":
            var[line[1]] = concat(line[2::])
            continue
        elif line[0] == "import":
            with open(line[1] + ".abjad", "r") as code:
                var |= abjad(code.read(), line[2:])[1]
            continue
        elif line[0] == "comm":
            continue
        line = line[::-1]
        for term in line:
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
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, a + b)
            elif term == "neg":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = -stack1[0]
            elif term == "sub":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, a - b)
            elif term == "mul":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, a * b)
            elif term == "rcp":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                n = stack1.pop(0)
                if n == 0:
                    stack1.insert(0, math.inf)
                else:
                    stack1.insert(0, 1/n)
            elif term == "div":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                if a == b:
                    stack1.insert(0, 1)
                elif a == 0:
                    stack1.insert(0, math.inf * abs(b)/b)
                else:
                    stack1.insert(0, a/b)
            elif term == "mod":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                if b == 0:
                    stack1.insert(0, 0)
                else:
                    stack1.insert(0, a % b)
            elif term == "abs":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = abs(stack1[0])
            elif term == "sgn":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                n = stack1.pop(0)
                if n == 0:
                    stack1.insert(0, 0)
                else:
                    stack1.insert(0, abs(n)/n)
            elif term == "pow":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, a ** b)
            elif term == "sqrt":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = stack1[0] ** .5
            elif term == "log":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, math.log(a, b))
            elif term == "sin":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.sin(stack1[0])
            elif term == "cos":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.cos(stack1[0])
            elif term == "tan":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.tan(stack1[0])
            elif term == "asin":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.asin(stack1[0])
            elif term == "acos":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.acos(stack1[0])
            elif term == "atan":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.atan(stack1[0])
            elif term == "flr":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.floor(stack1[0])
            elif term == "ceil":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.ceil(stack1[0])
            elif term == "rnd":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1[0] = math.round(stack1[0])
            # equality
            elif term == "eq":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, float(a == b))
            elif term == "neq":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, float(a != b))
            elif term == "lt":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, float(a < b))
            elif term == "gt":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, float(a > b))
            elif term == "lte":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, float(a <= b))
            elif term == "gte":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, float(a >= b))
            elif term == "min":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, min(a, b))
            elif term == "max":
                if len(stack1) < 2:
                    raise AbjadArgumentException(len(stack1), 2)
                a = stack1.pop(0)
                b = stack1.pop(0)
                stack1.insert(0, max(a, b))
            # stack
            elif term == "dup":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1.insert(0, stack1[0])
            elif term == "pop":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                stack1.pop(0)
            elif term == "swp":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                if len(stack2) < 1:
                    raise AbjadArgumentException(len(stack2), 1)
                n1 = stack1.pop(0)
                n2 = stack2.pop(0)
                stack1.insert(0, n2)
                stack1.insert(0, n1)
            elif term == "lft":
                if len(stack2) < 1:
                    raise AbjadArgumentException(len(stack2), 1)
                n2 = stack1.pop(0)
                stack1.insert(0, n2)
            elif term == "rgt":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                n1 = stack1.pop(0)
                stack1.insert(0, n1)
            # other
            elif term == "asrt":
                if len(stack1) < 1:
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
                    stack1.insert(0, inputted)
            elif term == "out":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                print(stack1.pop(0))
            elif term == "cout":
                if len(stack1) < 1:
                    raise AbjadArgumentException(len(stack1), 1)
                if stack1[0].imag != 0 or stack1[0].real < 0 or stack1[0].real % 1 != 0:
                    raise AbjadValueException(stack1[0])
                print(chr(round(stack1.pop(0).real)), end="")
            elif term == "nop":
                pass
            elif term in var:
                if isinstance(var[term], float):
                    stack1.insert(0, var[term])
                elif isinstance(var[term], str):
                    stack1 = abjad(var[term], stack1, var)[0]
            else:
                raise AbjadTermException(term)
        if assign is not None:
            var[assign] = stack1[0]
            stack1 = stack1[1::]

    return stack1, var


def main():
    match sys.argv[1:]:
        case []:
            with open("main.abjad", "r") as code:
                abjad(code.read())
        case ["-e", expr]:
            abjad(expr)
        case [name, *exprs]:
            with open(name, "r") as code:
                abjad(code.read(), exprs)
        case _:
            pass


if __name__ == "__main__":
    main()
