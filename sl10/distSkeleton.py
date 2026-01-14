# -*- coding: utf-8 -*-
"""
Discrete probability distributions
"""

import random
import operator
import copy

import lib601.util as util

class DDist:
    """
    Discrete distribution represented as a dictionary.  Can be
    sparse, in the sense that elements that are not explicitly
    contained in the dictionary are assumed to have zero probability.
    """
    def __init__(self, dictionary):
        self.d = dictionary
        """ Dictionary whose keys are elements of the domain and values
        are their probabilities. """

    def dictCopy(self):
        """
        @returns: A copy of the dictionary for this distribution.
        """
        return self.d.copy()

    def prob(self, elt):
        """
        @param elt: an element of the domain of this distribution
        (does not need to be explicitly represented in the dictionary;
        in fact, for any element not in the dictionary, we return
        probability 0 without error.)
        @returns: the probability associated with C{elt}
        """
        if self.d.has_key(elt):
            return self.d[elt]
        else:
            return 0

    def support(self):
        """
        @returns: A list (in arbitrary order) of the elements of this
        distribution with non-zero probabability.
        """
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            dictRepr = reduce(operator.add,
                              [util.prettyString(k)+": "+\
                               util.prettyString(p)+", " \
                               for (k, p) in self.d.items()])
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__

# 这是10.1.7 part1 的代码

def bayesEvidence(PBgA,PA,b):
    """""
    PBgA: 条件概率 P(B | A)，是一个函数，输入A的取值，输出关于B的分布
    PA: 先验概率 P(A)，是一个DDist
    b: B的观测值
    
    return:
    DDist: 后验概率分布 P(A|B=b)
    """""
    # 首先计算B的边缘概率 P(B)
    PB = totalProbability(PBgA, PA)
    result_dict = {}

    # 为每个A的值计算后验概率
    for a in PA.support():
        # 此处应用贝叶斯公式
        result_dict[a] = (PBgA(a).prob(b) * PA.prob(a)) / PB.prob(b)
    return DDist(result_dict)


# 这是10.1.7 part2 的代码

def totalProbability(PBgA,PA):
    """""
    PBgA: 条件概率 P(B|A)，是一个函数，输入A的取值，输出关于B的分布  
    PA: 先验概率 P(A)，是一个DDist
    
    return:
    DDist: B的边缘概率分布 P(B)
    """""
    result_dict = {}
    # 收集所有可能的B值
    all_b = set()
    for a in PA.support():
        # 将每个A值对应的B分布的支持集添加到所有B值的集合中
        all_b.update(PBgA(a).support())

    # 为每个B值计算边缘概率
    for b in all_b:
        # 此处为全概率公式
        result_dict[b] = sum(PBgA(a).prob(b) * PA.prob(a) for a in PA.support())
    return DDist(result_dict)


print("-----TestSL10.txt-----\n")

def PTgD(val):
    if val == 'disease':
        return DDist({'posTest':0.9, 'negTest':0.1})
    else:
        return DDist({'posTest':0.5, 'negTest':0.5})
PD = DDist({'disease':0.1, 'noDisease':0.9})

def PRgF(val):
    if val == 'f1':
        return DDist({'r1':0.25, 'r2':0.25, 'r3':0.25, 'r4':0.25})
    else:
        return DDist({'r1':0.1, 'r2':0.1, 'r3':0.1, 'r4':0.7})
PF = DDist({'f1':0.5, 'f2':0.5})

print('-------WK10.1.7  Part1-------')
print(bayesEvidence(PTgD, PD, 'posTest'))
print(bayesEvidence(PTgD, PD, 'negTest'))
print(bayesEvidence(PRgF, PF, 'r3'))
print(bayesEvidence(PRgF, PF, 'r4'))
print('-------WK10.1.7  Part2-------')
print(totalProbability(PTgD, PD))
print(totalProbability(PRgF, PF))
######################################################################
#   Utilities


def removeElt(items, i):
    """
    non-destructively remove the element at index i from a list;
    returns a copy;  if the result is a list of length 1, just return
    the element  
    """
    result = items[:i] + items[i+1:]
    if len(result) == 1:
        return result[0]
    else:
        return result

def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}.
    Else set C{d[k] = v}.
    
    @param d: dictionary
    @param k: legal dictionary key (doesn't have to be in C{d})
    @param v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v



# If you want to plot your distributions for debugging, put this file
# in a directory that contains lib601, and where that lib601 contains
# sig.pyc.  Uncomment all of the following.  Then you can plot a
# distribution with something like:
# plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)

# import lib601.sig as sig

# class IntDistSignal(sig.Signal):
#     def __init__(self, d):
#         self.dist = d
#     def sample(self, n):
#         return self.dist.prob(n)
# def plotIntDist(d, n):
#     IntDistSignal(d).plot(end = n, yOrigin = 0)
