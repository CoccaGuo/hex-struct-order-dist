# I_LatticePoint.py by CoccaGuo at 2021/10/14 16:02

# INTERFACE I_LatticePoint

from abc import abstractmethod
from abstract.Border import Border

class I_LatticePoint:
    # 定义具体的某个格点
    # v为圆环边界数目 lattice为该当格点所在的格子
    def __init__(self, v, lat) -> None:
        self.v = v
        self.lattice = lat

    # 周边格点
    @abstractmethod
    def get_neighbor(self) -> list:
        pass

    # 遍历边界
    @abstractmethod
    def get_borders(self) -> list:
        return [Border() for i in range(self.v)]