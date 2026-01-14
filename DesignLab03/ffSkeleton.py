# -*- coding: UTF-8 -*-
import lib601.sm as sm
import lib601.util as util

'''''
class FollowFigure(sm.SM):
    distEps = 0.02
    index = 0

    def __init__(self, points):
        self.points = points
        self.startState = None

    def getNextValues(self, state, inp):
        nextPoint = state
        robotCurrentPoint = inp.odometry.point()
        if nextPoint is None:
            nextPoint = self.points[0]
        # 判断小车是否靠近目标点
        if robotCurrentPoint.isNear(nextPoint, self.distEps):
            index = search(self.points, nextPoint)
            self.index = index
            if index == len(self.points) - 1:
                nextPoint = self.points[-1]
            else:
                # if self.points[index] == nextPoint:
                nextPoint = self.points[index + 1]

            # index = findPoint(self.points, nextPoint)
            # nextPoint = self.points[index]
            # if index != len(self.points) - 1:
            #     nextPoint = self.points[index + 1]
            # else:
            #     nextPoint = self.points[-1]
        print('NextPoint', nextPoint, self.index)
        return nextPoint, nextPoint


def search(points, point):
    index = 0
    while index < len(points):
        if points[index] == point:
            return index
        index += 1
    return -1
'''


class FollowFigure(sm.SM):
    distEps = 0.02

    def __init__(self, points):
        self.points = points
        # 使用索引作为状态，更清晰
        self.startState = 0  # 从第一个点开始

    def getNextValues(self, state, inp):
        current_index = state
        robot_pos = inp.odometry.point()
        current_target = self.points[current_index]

        # 检查是否接近当前目标点
        if robot_pos.isNear(current_target, self.distEps):
            # 如果还有下一个点，前进到下一个
            if current_index < len(self.points) - 1:
                next_index = current_index + 1
            else:
                # 已经是最后一个点，保持不变
                next_index = current_index
        else:
            # 还没到达当前目标点，保持当前索引
            next_index = current_index

        next_target = self.points[next_index]
        return next_index, next_target