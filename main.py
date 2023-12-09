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

def abjadInstr(inst, st1, st2, var):
    # lexed instructions
    if inst[0] == "if":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        if st1.pop(0) == 1:
            return abjadInstr(inst[1], st1, st2, var)
    
    elif inst[0] == "asgn":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        var[inst[1]] = st1.pop()
        return abjadInstr(inst[1], st1, st2, var)
    
    # literals
    elif parse_complex(inst) is not False:
        st1 = [parse_complex(inst)] + st1

    # consts
    elif inst == "e":
        st1 = [math.e + 0j] + st1

    elif inst == "j":
        st1 = [1j] + st1

    elif inst == "pi":
        st1 = [math.pi + 0j] + st1

    elif inst == "tau":
        st1 = [2 * math.pi + 0j] + st1

    elif inst == "eta":
        st1 = [math.pi / 2 + 0j] + st1

    elif inst == "inf":
        st1 = [math.inf + 0j] + st1

    elif inst == "eps":
        st1 = [sys.float_info.epsilon + 1 + 0j] + st1

    elif inst == "mu":
        st1 = [sys.float_info.min + 0j] + st1

    elif inst == "omg":
        st1 = [sys.float_info.max + 0j] + st1

    elif inst == "rand":
        st1 = [random.uniform(0, 1) + 0j] + st1

    # math
    elif inst == "add":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, a + b)

    elif inst == "neg":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = -st1[0]

    elif inst == "sub":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, a - b)

    elif inst == "mul":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, a * b)

    elif inst == "rcp":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        n = st1.pop(0)
        if n == 0:
            st1.insert(0, math.inf)
        else:
            st1.insert(0, 1/n)

    elif inst == "conj":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        n = st1.pop(0)
        st1.insert(0, n.real - 1j * n.imag)

    elif inst == "div":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        if a == b:
            st1.insert(0, 1)
        elif a == 0:
            st1.insert(0, math.inf * abs(b)/b)
        else:
            st1.insert(0, a/b)

    elif inst == "mod":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        if b == 0:
            st1.insert(0, 0)
        else:
            st1.insert(0, a % b)

    elif inst == "abs":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = abs(st1[0])

    elif inst == "sgn":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        n = st1.pop(0)
        if n == 0:
            st1.insert(0, 0)
        else:
            st1.insert(0, abs(n)/n)

    elif inst == "pow":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, a ** b)

    elif inst == "sqrt":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = st1[0] ** .5

    elif inst == "log":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, math.log(a, b))

    elif inst == "sin":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.sin(st1[0])

    elif inst == "cos":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.cos(st1[0])

    elif inst == "tan":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.tan(st1[0])

    elif inst == "asin":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.asin(st1[0])

    elif inst == "acos":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.acos(st1[0])

    elif inst == "atan":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.atan(st1[0])

    elif inst == "flr":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.floor(st1[0])

    elif inst == "ceil":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.ceil(st1[0])

    elif inst == "rnd":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1[0] = math.round(st1[0])

    # equality
    elif inst == "eq":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, float(a == b))

    elif inst == "neq":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, float(a != b))
    
    elif inst == "dir":
        a = st1.pop(0)
        b = st1.pop(0)
        c = b - a
        if c == 0:
            st1.insert(0, 0+0j)
        else:
            d = math.atan2(c.imag, c.real) / math.pi
            if d > 0.875:
                st1.insert(0, -1+0j)
            elif d > 0.625:
                st1.insert(0, -1+1j)
            elif d > 0.375:
                st1.insert(0, 0+1j)
            elif d > 0.125:
                st1.insert(0, 1+1j)
            elif d > -0.125:
                st1.insert(0, 1+0j)
            elif d > -0.375:
                st1.insert(0, 1-1j)
            elif d > -0.625:
                st1.insert(0, 0-1j)
            elif d > -0.875:
                st1.insert(0, -1-1j)
            else:
                st1.insert(0, -1+0j)

    elif inst == "min":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, min(a, b))

    elif inst == "max":
        if len(st1) < 2:
            raise AbjadArgumentException(len(st1), 2)
        a = st1.pop(0)
        b = st1.pop(0)
        st1.insert(0, max(a, b))

    # stack
    elif inst == "dup":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1.insert(0, st1[0])

    elif inst == "pop":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        st1.pop(0)

    elif inst == "swp":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        if len(st2) < 1:
            raise AbjadArgumentException(len(st2), 1)
        n1 = st1.pop(0)
        n2 = st2.pop(0)
        st1.insert(0, n2)
        st1.insert(0, n1)

    elif inst == "lft":
        if len(st2) < 1:
            raise AbjadArgumentException(len(st2), 1)
        n2 = st1.pop(0)
        st1.insert(0, n2)

    elif inst == "rgt":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        n1 = st1.pop(0)
        st1.insert(0, n1)

    # other
    elif inst == "asrt":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        elif st1[0] != 1:
            raise AbjadAssertException(st1[0])
        else:
            st1 = st1[1::]

    elif inst == "dbg":
        print((st1, st2))

    elif inst == "inp":
        inputted = parse_complex(input())
        if inputted is False:
            raise AbjadValueException(inputted)
        else:
            st1.insert(0, inputted)

    elif inst == "out":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        print(st1.pop(0))

    elif inst == "cout":
        if len(st1) < 1:
            raise AbjadArgumentException(len(st1), 1)
        if st1[0].imag != 0 or st1[0].real < 0 or st1[0].real % 1 != 0:
            raise AbjadValueException(st1[0])
        print(chr(round(st1.pop(0).real)), end="")

    elif inst == "nop":
        pass

    elif inst in var:
        if isinstance(var[inst], float):
            st1.insert(0, var[inst])
        elif isinstance(var[inst], str):
            st1 = abjad(var[inst], inp=st1, var=var)[0]

    else:
        raise AbjadTermException(inst)
    
    return (st1, st2, var)




def abjad(code: str, *, inp: list = None, var: dict = None):

    lines = [line.casefold().split() for line in code.splitlines()]
    var = {} if var is None else var
    stack1 = [] if inp is None else inp
    stack2 = []

    for line in lines:
        if len(line) == 0:
            continue

        elif line[0] == "def":
            var[line[1]] = concat(line[2::])
            continue

        elif line[0] == "import":
            with open(line[1] + ".abjad", "r") as code:
                var |= abjad(code.read(), line[2:], var)[1]
            continue
        
        for ind, lex in enumerate(line):
            if lex == "if":
                line = line[:ind:] + [("if", line[ind+1])] + line[ind+2::]
            elif lex == "asgn":
                line = line[:ind:] + [("asgn", line[ind+1])] + line[ind+2::]

        line = line[::-1]
        for term in line:
            if term == "comm":
                break
            else:
                stack1, stack2, var = abjadInstr(term, stack1, stack2, var)

    return stack1, var


def main():
    match sys.argv[1:]:
        case []:
            with open("main.abjad", "r") as code:
                abjad(code.read())
        case ["-e", *exprs]:
            abjad(concat(exprs))
        case [name, *exprs]:
            with open(name, "r") as code:
                abjad(code.read(), inp=exprs)
        case _:
            pass


if __name__ == "__main__":
    main()
