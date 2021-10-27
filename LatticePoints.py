# LatticePoints.py by CoccaGuo at 2021/10/14 20:16
from abstract.Border import Border
from abstract.I_LatticePoint import I_LatticePoint
import numpy as np

from utils import Pos


class LatticePoints(I_LatticePoint):

    def __init__(self, v, lat, pos, rad, offset=0) -> None:
        super().__init__(v, lat)
        self.pos = pos
        self.rad = rad
        self.offset = offset
        self.angle = 2*np.pi/self.v
        self.len = 2*self.rad*np.tan(self.angle/2)

    def pos_to_border_center(self):
        ang = 2*np.pi/self.v
        r0 = self.rad
        self.border_list = []
        for i in range(self.v):
            x = r0*np.cos(ang*i)
            y = r0*np.sin(ang*i)
            self.border_list.append(
                Border(center=self.pos+Pos(x, y), len=self.len, angle=np.pi/2+ang*i))


    def plot(self, ax, args='k'):
        self.pos_to_border_center()
        for border in self.border_list:
            pt1, pt2 = border.get_border_points()
            # ax.plot((pt1.x, pt2.x), (pt2.x, pt2.y), args)
            ax.scatter(border.center.x, border.center.y)
