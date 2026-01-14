#coding:utf-8
import lib601.sm as sm
import lib601.gfx as gfx
import lib601.util as util

# Wk.3.1.3部分
class PureFunction(sm.SM):
    def __init__(self, f):
        self.f = f

    def startState(self):
        return None

    def getNextValues(self, state, inp):
        return (state, self.f(inp))


class BA1(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        if inp != 0:
            newState = state * 1.02 + inp - 100
        else:
            newState = state * 1.02
        return (newState, newState)

class BA2(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        newState = state * 1.01 + inp
        return (newState, newState)

#Wk.3.1.4部分
# Part 1: Maximize
#创建一个状态机maxAccount，输出两种银行账户余额的最大值

#BA1和BA2，它们分别计算两种账户的余额
ba1 = BA1()
ba2 = BA2()

def max_balance(balances):  #   比较大小
    return max(balances)

# 创建一个包装器，将单个输入转换为两个相同的输入
#原因：在第一次运行时，代码出现报错，因为Parallel2期望的输入是一个元组，但因为原版代码输入直接给了整数，推测是在在尝试拆分整数时出错
def duplicate_input(inp):
    return (inp, inp)
# 使用Cascade将输入复制，然后并行运行两个account
duplicate_input_sm = PureFunction(duplicate_input)
combined_account = sm.Cascade(duplicate_input_sm, sm.Parallel2(BA1(), BA2()))
# 将并行的输入，比较大小，获取maximize
maxBalance = PureFunction(max_balance)
maxAccount = sm.Cascade(combined_account, maxBalance)


input_sequence = [1000,4000,5000,-1000,-5000]
print("Part 1 - Max Account Results:")
result1 = maxAccount.transduce(input_sequence, verbose=True)
print("Final results:", result1)
print()


#这是我的原版代码——3.1.4 Part1

#def max_balance(balances):  #   比较大小
#    return max(balances)
# 用sm.Parallel2(),并行运行两个account
#combined_account = sm.Parallel2(ba1, ba2)
#maxBalance = PureFunction(max_balance)  # PureFunction将会接受一个元组，并返回元组中两个数的最大值
# 将并行的输入，比较大小，获取maximize
#maxAccount = sm.Cascade(combined_account, maxBalance)
#input_sequence = [1000,4000,5000,-1000,-5000]
#maxAccount.transduce(input_sequence,verbose=True)


# Part 2: Investment
#方法split_inp()，它根据输入的绝对值是否大于3000来返回两个值：如果绝对值大于3000，则用BA1，返回(inp, 0)，否则用BA2，返回(0, inp)
#创建状态机，输入inp，然后输出一个元组：第一个元素是给BA1的输入，第二个元素是给BA2的输入
#用sm.Cascade将这个预处理状态机与sm.Parallel2(BA1, BA2)级联，这里给sm.Parallel2()的输入是预处理后的两个输入
#再与sm.PureFunction(sum_ba)级联，将两个账户的余额相加

# 分配交易金额
def split_inp(inp):
    if abs(inp) > 3000:
        return (inp, 0)  # 大额交易给BA1，BA2无交易
    else:
        return (0, inp)  # 小额交易给BA2，BA1无交易

# 计算两个余额的总和
def sum_ba(ba):
    return ba[0] + ba[1]

# 创建状态机
split_account=sm.Cascade(sm.PureFunction(split_inp), sm.Parallel2(BA1(), BA2()))# 不同的是，先分配操作，再执行
switchAccount = sm.Cascade(split_account,sm.PureFunction(sum_ba))

print("Part 2 - Switch Account Results:")
result2 = switchAccount.transduce(input_sequence, verbose=True)
print("Final results:", result2)