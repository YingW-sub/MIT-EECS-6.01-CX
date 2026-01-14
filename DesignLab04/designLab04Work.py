#   -*- coding:utf-8 -*-
import lib601.sig  as sig # Signal
import lib601.ts as ts  # TransducedSignal
import lib601.sm as sm  # SM

######################################################################
##  Make a state machine model using primitives and combinators
######################################################################

def plant(T, initD):
    return sm.Cascade(sm.Cascade(sm.R(initD),sm.Gain(T)),sm.FeedbackAdd(sm.Wire(),sm.R(initD)))
def controller(k):
    return sm.Gain(k)

def sensor(initD):
    return sm.R(initD)

def wallFinderSystem(T, initD, k):
    pla=plant(T, initD)
    con=controller(k)
    sen=sensor(initD)
    return sm.FeedbackSubtract(sm.Cascade(con,pla),sen)

# Plots the sequence of distances when the robot starts at distance
# initD from the wall, and desires to be at distance 0.7 m.  Time step
# is 0.1 s.  Parameter k is the gain;  end specifies how many steps to
# plot. 

initD = 1.5

def plotD(k, end = 50):
  d = ts.TransducedSignal(sig.ConstantSignal(0.7),
                          wallFinderSystem(0.1, initD, k))
  d.plot(0, end, newWindow = 'Gain '+str(k))


  ###################################
  ###   以下是Wk4_3_3的代码
  ###################################

  '''
  def accumulator(init):
      return sm.FeedbackAdd(sm.Wire(), sm.R(init))

  def accumulatorDelay(init):
      return sm.Cascade(sm.R(0), accumulator(init))

  def accumulatorDelayScaled(s, init):
      return sm.Cascade(accumulatorDelay(init), sm.Gain(s))

  '''

  ###################################
  ###   用于测试Wk4_3_3
  ###################################

  '''
  if __name__ == '__main__':
      def test_accumulator():
          y = accumulator(0)
          print y.transduce( list( range(10)))

      def test_accumulatorDelay():
          y = accumulatorDelay(0)
          print y.transduce( list( range(10)))

      def test_accumulatorDelayScaled():
          y = accumulatorDelayScaled(0.5, 0)
          print y.transduce( list( range(10)))

      test_accumulator()
      test_accumulatorDelay()
      test_accumulatorDelayScaled()
  '''