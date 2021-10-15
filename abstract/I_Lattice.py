# I_Lattice.py by CoccaGuo at 2021/10/14 15:53

# INTERFACE I_Lattice

from abc import abstractmethod


class I_Lattice:

    # 描述格子的形状
    def __init__(self, n) -> None:
        self.n = n

    # 遍历格点
    @abstractmethod
    def get_lattice_point_list(self) -> list:
        pass
    
    # 能量的修饰和调整
    # map中对应各种格点和状态 对应的修饰
    @abstractmethod
    def get_modifier(self) -> map:
        pass