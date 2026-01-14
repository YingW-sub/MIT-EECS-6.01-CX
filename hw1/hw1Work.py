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
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

    # 求值
    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        return self.operation(left_val, right_val)

class Sum(BinaryOp):
    opStr = 'Sum'
    def compute(self, left, right):
        return operator.add(left, right)

class Prod(BinaryOp):
    opStr = 'Prod'
    def compute(self, left, right):
        return operator.mul(left, right)

class Quot(BinaryOp):
    opStr = 'Quot'
    def compute(self, left, right):
        return operator.div(left, right)

class Diff(BinaryOp):
    opStr = 'Diff'
    def compute(self, left, right):
        return operator.sub(left, right)

class Assign(BinaryOp):
    opStr = 'Assign'
    def eval(self, env): # 判断左边是否为Variable
        if not isinstance(self.left, Variable):
            raise Exception('not a Variable')
        # 赋值
        value = self.right.eval(env)
        env[self.left.name] = value
        return None

class Number:
    def __init__(self, val):
        self.value = float(val)
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__
    def eval(self, env):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__
    def eval(self, env):
        return env[self.name]

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenize(string):
    tokens = []  # 存储拆分结果
    current_token = "" # 临时存储数字

    for char in string:
        if char in seps:
            # 如果current_token里面有数字，优先存储
            if current_token:
                tokens.append(current_token)
                current_token = "" # 存储后清除
            # 存储运算符
            tokens.append(char)
        elif char.isspace():
            # 遇到空格，存储数字
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            # 不是运算符，存储数字
            current_token += char

    # 存储最后的数字
    if current_token:
        tokens.append(current_token)

    return tokens


# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        # <your code here>
        if index >= len(tokens):  # 溢出特判
            return None, index
        token = tokens[index]
        if numberTok(token):  # 拿到数字，进下一个
            return Number(float(token)), index + 1
        if variableTok(token):  # 拿到变量值，进下一个
            return Variable(token), index + 1

        # 遇到表达式，开始运算
        if token == '(':
            leftExp, nextIndex = parseExp(index + 1) # 解析左操作数
            # 获取运算符
            opToken = tokens[nextIndex]
            nextIndex += 1
            rightExp, nextIndex = parseExp(nextIndex) # 解析右操作数

            if tokens[nextIndex] != ')': # 缺右括号特判
                raise Exception("Expected ')'")
            nextIndex += 1

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
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')   # prints %, returns user input
        c = parse(tokenize(e))
        print '%', c.eval(env)  # your expression here
        print '   env =', env

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession 
        print  parse(tokenize(e)).eval(env)# your expression here
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
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

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

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

# 6.1 拓展

class SM:
    def start(self):
        self.state = self.startState

    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

class Tokenizer(SM): # 状态机

    def __init__(self):
        self.startState = ''

    def getNextValues(self, state, inp):
        if inp == ' ':
            return self.startState, self.state
        if (inp.isalpha() and self.state.isalpha()) or (inp.isdigit() and self.state.isdigit()):
            self.state=self.state+inp
            return self.state, self.startState
        else:
            return inp, self.state

def tokenize2(inputstring):
    list2=Tokenizer().transduce(inputstring)
    while '' in list2:
        list2.remove('')
    return list2

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)
