# utils.py by CoccaGuo at 2021/10/14 20:37
import numpy as np

class Pos:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, oPos):
        return Pos(self.x+oPos.x, self.y+oPos.y)
    
    def __sub__(self, oPos):
        return Pos(self.x-oPos.x, self.y-oPos.y)
    
    def __len__(self):
        return np.sqrt(self.x**2 + self.y**2)
    
    