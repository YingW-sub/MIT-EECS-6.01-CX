import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
import lib601.sonarDist as sonarDist
from soar.io import io


class MySMClass(sm.SM):
    startState = 'go'

    def getNextValues(self, state, inp):
        sonarValues = inp.sonars
        print("State: {state}")
        for i, val in enumerate(sonarValues):
            print("{i + 1} {round(val, 2)}")

        right_soar = sonarValues[7]
        side_soar = sonarValues[6]
        front_right = min(sonarValues[4], sonarValues[5])  # Improved front obstacle detection

        if state == "go":
            if right_soar <= 0.5 and right_soar > 0.3 and front_right > 0.4:
                return ("go", io.Action(fvel=0.1, rvel=0))
            elif right_soar <= 0.5:
                return ("left", io.Action(fvel=0.1, rvel=0.5))
            elif front_right <= 0.5:
                return ("left", io.Action(fvel=0.1, rvel=0.5))
            else:
                return ("right", io.Action(fvel=0.15, rvel=-0.4))  # 减小转弯速度

        elif state == "right":
            # Optimized corner detection conditions
            if right_soar <= 0.5 and right_soar > 0.3 and side_soar <= 0.6:  # Lowered the side sonar threshold from 0.7 to 0.6
                return ("go", io.Action(fvel=0.05, rvel=0))
            elif right_soar <= 0.5:
                return ("left", io.Action(fvel=0.1, rvel=0.5))
            elif front_right <= 0.5:
                #  When encountering front obstacles in the right turn state, increased turning aggressiveness
                return ("left", io.Action(fvel=0.05, rvel=0.6))
            else:
                return ("right", io.Action(fvel=0.15, rvel=-0.4))  # Adjusted turning parameters

        elif state == "left":
            if right_soar <= 0.5 and right_soar > 0.3 and front_right > 0.4:
                return ("go", io.Action(fvel=0.1, rvel=0))
            elif right_soar <= 0.5:
                return ("left", io.Action(fvel=0.1, rvel=0.5))
            elif front_right <= 0.5:
                return ("left", io.Action(fvel=0.1, rvel=0.5))
            else:
                return ("right", io.Action(fvel=0.15, rvel=-0.4))  # 减小转弯速度

        return (state, io.Action(fvel=0, rvel=0))


mySM = MySMClass()
mySM.name = 'brainSM'


######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar' + str(sonarNum),
                                        lambda:
                                        io.SensorInput().sonars[sonarNum]))


# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True,  # slime trails
                                  sonarMonitor=False)  # sonar monitor widget

    # set robot's behavior
    robot.behavior = mySM


# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks=robot.gfx.tasks())


# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    # print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())


# called when the stop button is pushed
def brainStop():
    pass


# called when brain or world is reloaded (before setup)
def shutdown():
    pass
