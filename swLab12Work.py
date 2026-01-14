#   -*-coding:UTF-8-*-
import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):
        (o, i) = inp
        # 观测：贝叶斯更新
        belief = self. __bayesEvidence(state, o)
        # 预测：全概率更新
        dSPrime = self.__totalProbability(belief, self.model.transitionDistribution(i))
        # 返回下一状态和输出
        return (dSPrime, dSPrime)


    # 基于观测值更新当前状态:贝叶斯更新
    def  __bayesEvidence(self,state,observation):
        state_name, p, dist_dict = state.support(), 0, {}
        # 计算未归一化的后验概率
        for name in state_name:
            prob = self.model.observationDistribution(name).prob(observation) * state.prob(name)
            dist.incrDictEntry(dist_dict, name, prob)
            p += prob
        # 归一化
        for i in dist_dict.keys():
            dist_dict[i] /= p
        return dist.DDist(dist_dict)


    # 基于input预测下一个状态:全概率更新
    def __totalProbability(self, belief, transDist):
        states, total = belief.support(), {}

        for s1 in states:
            for s2 in states:
                # 累加
                if s2 not in total.keys():
                    total[s2] = belief.prob(s1) * transDist(s1).prob(s2)
                else:
                    total[s2] += belief.prob(s1) * transDist(s1).prob(s2)

        return dist.DDist(total)

# Test

transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}

copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],
                lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]

cmse = StateEstimator(copyMachine)

print(cmse.transduce(obs))
