# main.py by CoccaGuo at 2021/10/26 18:46
import numpy as np
import random
from itertools import combinations

class Point:
    def __init__(self, a, b, edge=None):
        self.a = a
        self.b = b
        self.edge = edge
        if not edge:
            self.edge = random.choice([4, 5, 6, 7, 8])
        self.angle = 2*np.pi/self.edge

    def neighbour(self, net):
        a, b = self.a, self.b
        n_list = [Point(i, j) for i, j in zip((a, a, a+1, a-1, a+1, a-1), (b+1, b-1, b, b, b-1, b+1))]
        for pt in n_list:
            px, py = pt.pos()
            if net[px, py] != 0:
                pt.edge = net[px, py]
        return n_list
    
    def __eq__(self, o: object) -> bool:
        if self.a == o.a and self.b == o.b:
            return True
        else: return False


    def pos(self):
        return self.a, self.b
    
    def __str__(self) -> str:
        return f"({self.a}, {self.b})"
    
    def __repr__(self) -> str:
        return self.__str__()


def search_a_list(point_list, net):
    all_energy_list = list()
    position_list = list()
    # 遍历所有晶化区域
    for init_point in point_list:
        # 每个晶化点周围可能的能量list
        energy_list = list()
        nb_list = init_point.neighbour(net)
        for nei in nb_list: # 计算周围怎样生长能量最低
            nei_x, nei_y = nei.pos()
            net[nei_x, nei_y] = nei.edge
            # 键能
            side_counter = list() # 统计周围有多少键是已经有序的
            for nei_nei in nei.neighbour(net): # 虚操作，二级计算不会影响格子
                x, y = nei_nei.pos()
                if net[x, y] == 6:
                    side_counter.append(nei_nei)
            _bond_energy = (nei.edge - len(side_counter)) * bond_energy
            # 角能
            side_angle_counter = 0
            for side_comb in combinations(side_counter, 2):
                for nei_nei in side_comb[0].neighbour(net):
                    a, b = nei_nei.pos()
                    _a, _b = side_comb[1].pos()
                    if a == _a and b == _b:
                        side_angle_counter += 1
        
            _angular_energy = (nei.edge - side_angle_counter)* angular_energy* np.abs(nei.angle - 2*np.pi/3)
        # 总能量
            add_up_energy = _bond_energy + _angular_energy
            energy_list.append(add_up_energy)
        # energy_list_without_6_mask = np.array(list(map(lambda x: np.inf if x.edge==6 else 1, nb_list)))
        # print(energy_list_without_6_mask)
        # energy_list_without_6 = np.array(energy_list)*energy_list_without_6_mask
        energy_list_without_6 = list()
        for index, qpt in enumerate(nb_list):
            if qpt.edge == 6:
                energy_list_without_6.append(np.inf)
            else:
                energy_list_without_6.append(energy_list[index])

        print(init_point ,energy_list_without_6)
        ind = np.argmin(energy_list_without_6)
        ener = np.min(energy_list_without_6)
        next_point = nb_list[ind]
        all_energy_list.append(ener)
        position_list.append(next_point)
    # min_energy = np.min(all_energy_list)
    real_next_point = position_list[np.argmin(all_energy_list)]
    rx, ry = real_next_point.pos()
    print("real point", real_next_point)
    net[rx, ry] = 6
    point_list.append(real_next_point)
    return real_next_point, net



if __name__ == '__main__':
    size = 20
    bond_energy = 4 # +2D 破坏、形成C-C键需要的能量
    angular_energy = -4 # +1D 无序圆环内角处在不自然的状态含有的能量的系数
    # \delta E = angular_energy * f(\theta - \theta_0), \theta_0 = 2*pi/3
    net = np.zeros((size, size)) # 用于标记哪些是已经成键的区域
    init_point = Point(size//2, size//2) # 在中心开始晶化
    net[size//2, size//2] = 6
    point_list = list()
    point_list.append(init_point)
    for i in range(35):
        point, net = search_a_list(point_list, net)
        print(point_list)
        print(net)