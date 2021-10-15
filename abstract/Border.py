# Border.py by CoccaGuo at 2021/10/14 16:14

import numpy as np
from utils import Pos


class Border:

    def __init__(self, energy=1, len=1, center=Pos(0, 0), angle=0) -> None:
        self.energy = energy
        self.len = len
        self.center = center
        self.angle = angle

    def get_border_points(self):
        relative_pos = Pos(self.len*0.5*np.cos(self.angle),
                           self.len*0.5*np.sin(self.angle))
        return (self.center+relative_pos, self.center-relative_pos)
