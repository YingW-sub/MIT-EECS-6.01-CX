import lib601.dist as dist
import lib601.util as util
import lib601.colors as colors
import lib601.ssm as ssm
import lib601.seFast as seFast
import lib601.dynamicGridMap as dynamicGridMap


# Define the stochastic state-machine model for a given cell here.

# Observation model:  P(obs | state)
def oGivenS(s):
    if s == 'occupied':
        return dist.DDist({'hit': 0.75, 'free': 0.25}) #0.7 0.3
    elif s == 'notOccupied':
        return dist.DDist({'hit': 0.2, 'free': 0.8}) #0.05 0.95


# Transition model: P(newState | s | a)
def uGivenAS(a):
    def GivenS(s):
        if s == 'occupied':
            return dist.DDist({'occupied': 0.8, 'notOccupied': 0.2})  #0.7 0.3
        elif s == 'notOccupied':
            return dist.DDist({'occupied': 0.2, 'notOccupied': 0.8})
    return GivenS
startDistribution = dist.DDist({'occupied': 0.25, 'notOccupied': 0.75})
cellSSM = ssm.StochasticSM(startDistribution, uGivenAS, oGivenS)


class BayesGridMap(dynamicGridMap.DynamicGridMap):

    def squareColor(self, (xIndex, yIndex)):
        p = self.occProb((xIndex, yIndex))
        if self.robotCanOccupy((xIndex,yIndex)):
            return colors.probToMapColor(p, colors.greenHue)
        elif self.occupied((xIndex, yIndex)):
            return 'black'
        else:
            return 'red'
        
    def occProb(self, (xIndex, yIndex)):
        return self.grid[xIndex][yIndex].state.prob('occupied')
    def makeStartingGrid(self):
        def starting(ix, iy):
            mySM = seFast.StateEstimator(cellSSM)
            mySM.start()
            return mySM
        return util.make2DArrayFill(self.xN, self.yN, starting)

    def setCell(self, (xIndex, yIndex)):
        self.grid[xIndex][yIndex].step(('hit', None))
        self.drawSquare((xIndex, yIndex))
        return

    def clearCell(self, (xIndex, yIndex)):
        self.grid[xIndex][yIndex].step(('free', None))
        self.drawSquare((xIndex, yIndex))
        return
    def occupied(self, (xIndex, yIndex)):
        if self.occProb((xIndex, yIndex)) >= 0.72: #0.75
            return True
        else:
            return False


mostlyHits = [('hit', None), ('hit', None), ('hit', None), ('free', None)]
mostlyFree = [('free', None), ('free', None), ('free', None), ('hit', None)]

def testCellDynamics(cellSSM, input):
    se = seFast.StateEstimator(cellSSM)
    return se.transduce(input)

