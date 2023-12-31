# The ABJAD programming language
By Nif

## The basics of Abjad
The Abjad programming language is a tacit, stack-based language, quite similar to [Uiua](https://www.uiua.org).
However, the main difference is the removal of planet notation. Instead, you get a second stack to store items not being used.
All functions in Abjad work on the primary "left" stack, except for built-in stack manipulation functions.

## The basics of [Tacit](https://en.wikipedia.org/wiki/Tacit_programming)
Tacit programming is the practise of not naming your function arguments.
There are 3 kinds of programming languages: languages that don't let you tacit, languages that let you tacit, and languages that force you to tacit.
Abjad is mostly the third type.
However, if stack manipulation is too annoying for you, the `asgn` function will let you store variables.
Apparently, writing tacit code also makes your code more readable.

## Q&A
- Why is the only data type complex numbers?
    - Because I haven't implemented any others yet
- Why can I not have multiline functions
    - Because I can't be bothered to try and do that
- How do I make a loop?
    - Function that calls itself.
- What is even the point of this language
    - Admittedly, that is one of the flaws of my argument
- How do I break out of a loop?
    - Put the recursion call in an `if`

## Function library
### Mathematical functions
- `add`: add the two top values together
- `sub`: take the top value from the second
- `mul`: multiply the two top values together
- `div`: divide the second value by the top
- `mod`: take the second value mod the top
- `pow`: take the second value raised to the first
- `log`: take the logarithm with the base of the top value, of the second

- `neg`: negate the top value
- `rcp`: take the reciprocal of the top value
- `conj`: take the complex conjugate of the top value
- `abs`: take the absolute value of the top value
- `sgn`: take the sign of the top value
- `sqrt`: find the square root of the top value

- `sin`: find the sine of the top value
- `cos`: find the cosine of the top value
- `tan`: find the tangent of the top value
- `asin`: find the arcsine of the top value
- `acos`: find the arccosine of the top value
- `atan`: find the arctangent of the top value

- `flr`: find the next whole number below the top value
- `ceil`: find the next whole number above the top value
- `rnd`: find the closest whole number to the top value

### Comparison functions
- `eq`: push `(1.0+0.0j)` if the top two values on the stack are equal, and `(0.0+0.0j)` otherwise
- `neq`: push `(0.0+0.0j)` if the top two values on the stack are equal, and `(1.0+0.0j)` otherwise
- `dir`: get a normalized direction between two values
- `min`: find the lowest of the top two values
- `min`: find the greatest of the top two values

### Stack functions
- `dup`: duplicate the top value on the stack
- `pop`: remove the top value on the stack
- `swp`: swap the top values on both stacks
- `lft`: move a value from the second stack to the first
- `rgt`: move a value from the first stack to the second

### Other functions
- `asrt`: error if the top stack value is not (1.0+0.0j)
- `dbg`: print both stacks. Not reccommended for released code
- `inp`: take a number as user input
- `out`: print the top stack value
- `cout`: print the character with the ascii codepoint of the top stack value
- `nop`: do nothing
- `comm`: denote the rest of the line as a comment
- `if`: execute the proceeding instruction if and only if the top stack value is (1.0+0.0j)
- `asgn`: define a variable with a value

### Prefix functions
Prefix functions must only come at the start of a line
- `def`: define a function
- `import`: import variables from another file

### Notes
You can use brackets `()` to partition code into blocks. This can be used for extended `if`s, multiline `def`s, and other stuff