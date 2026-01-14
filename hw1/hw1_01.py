import pdb
import lib601.sm as sm
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
            str(self.left) + ', ' + \
            str(self.right) + ')'

    __repr__ = __str__

    def eval(self, env):
        # Eager evaluation for binary operations
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        return self.operation(left_val, right_val)


class Sum(BinaryOp):
    opStr = 'Sum'

    def operation(self, left, right):
        return left + right


class Prod(BinaryOp):
    opStr = 'Prod'

    def operation(self, left, right):
        return left * right


class Quot(BinaryOp):
    opStr = 'Quot'

    def operation(self, left, right):
        return left / right


class Diff(BinaryOp):
    opStr = 'Diff'

    def operation(self, left, right):
        return left - right


class Assign(BinaryOp):
    opStr = 'Assign'

    def eval(self, env):
        # For assignment, left must be a Variable
        if not isinstance(self.left, Variable):
            raise Exception('Not a Variable')
        # Evaluate the right side and assign to variable
        value = self.right.eval(env)
        env[self.left.name] = value
        return None  # Assignment returns None


class Number:
    def __init__(self, val):
        self.value = float(val)  # Convert to float as specified

    def __str__(self):
        return 'Num(' + str(self.value) + ')'

    __repr__ = __str__

    def eval(self, env):
        return self.value


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Var(' + self.name + ')'

    __repr__ = __str__

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            raise Exception("Undefined variable: " + self.name)


# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']


# Convert strings into a list of tokens (strings)
def tokenize(inputString):
    tokens = []
    current_token = ""

    for char in inputString:
        if char in seps:
            # If we have a current token, add it first
            if current_token:
                tokens.append(current_token)
                current_token = ""
            # Add the separator as a token
            tokens.append(char)
        elif char.isspace():
            # Space ends current token
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            # Add character to current token
            current_token += char

    # Don't forget the last token if there is one
    if current_token:
        tokens.append(current_token)

    return tokens


# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp}
def parse(tokens):
    def parseExp(index):
        token = tokens[index]

        # Case 1: Number
        if numberTok(token):
            return (Number(token), index + 1)

        # Case 2: Variable
        if variableTok(token):
            return (Variable(token), index + 1)

        # Case 3: Parenthesized expression
        if token == '(':
            # Parse left expression
            leftExp, nextIndex = parseExp(index + 1)

            # Get operator
            opToken = tokens[nextIndex]
            nextIndex += 1

            # Parse right expression
            rightExp, nextIndex = parseExp(nextIndex)

            # Check for closing parenthesis
            if tokens[nextIndex] != ')':
                raise Exception("Expected closing parenthesis")
            nextIndex += 1

            # Create appropriate operator node
            if opToken == '+':
                return (Sum(leftExp, rightExp), nextIndex)
            elif opToken == '-':
                return (Diff(leftExp, rightExp), nextIndex)
            elif opToken == '*':
                return (Prod(leftExp, rightExp), nextIndex)
            elif opToken == '/':
                return (Quot(leftExp, rightExp), nextIndex)
            elif opToken == '=':
                return (Assign(leftExp, rightExp), nextIndex)
            else:
                raise Exception("Unknown operator: " + opToken)

        raise Exception("Unexpected token: " + token)

    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp


# token is a string
# returns True if contains only digits
def numberTok(token):
    # Allow decimal points and negative numbers
    try:
        float(token)
        return True
    except ValueError:
        return False


# token is a string
# returns True its first character is a letter
def variableTok(token):
    if not token:
        return False
    # Variable names must start with a letter
    return token[0] in string.ascii_letters


# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float


# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('% ')  # prints %, returns user input
        # Tokenize, parse and evaluate
        tokens = tokenize(e)
        expr = parse(tokens)
        result = expr.eval(env)
        if result is not None:
            print result
        print '   env =', env


# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e  # e is the expression
        # Tokenize, parse and evaluate
        tokens = tokenize(e)
        expr = parse(tokens)
        result = expr.eval(env)
        if result is not None:
            print result
        print '   env =', env


# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''


def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi * ho)')
    print tokenize('( fred+george )')


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''


def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')', ')'])
    print parse(['(', 'a', '=', '(', '3', '*', '5', ')', ')'])


# Test the calculator
def testCalc():
    calcTest(['a = 3', 'b = 4', 'a * b'])


####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# testTokenize()
# testParse()
# testEval()
# testCalc()