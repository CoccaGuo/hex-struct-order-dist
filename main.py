# main.py by CoccaGuo at 2021/10/26 18:46
from matplotlib import pyplot as plt
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
        x_m, y_m = net.shape
        a, b = self.a, self.b
        n_list = [Point(i, j) for i, j in zip(
            (a, a, a+1, a-1, a+1, a-1), (b+1, b-1, b, b, b-1, b+1))]
        for pt in n_list:
            if pt.a >= x_m:
                pt.a = pt.a % x_m
            if pt.b >= y_m:
                pt.b = pt.b % y_m
            if net[pt.a, pt.b] != 0:
                pt.edge = net[pt.a, pt.b]
        return n_list

    def __eq__(self, o: object) -> bool:
        if self.a == o.a and self.b == o.b:
            return True
        else:
            return False

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
        for nei in nb_list:  # 计算周围怎样生长能量最低
            nei_x, nei_y = nei.pos()
            net[nei_x, nei_y] = nei.edge
            # 键能
            side_counter = list()  # 统计周围有多少键是已经有序的
            for nei_nei in nei.neighbour(net):  # 虚操作，二级计算不会影响格子
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

            _angular_energy = (nei.edge - side_angle_counter) * \
                angular_energy * np.abs(nei.angle - 2*np.pi/3)
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

        # print(init_point ,energy_list_without_6)
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


def plot_mtx(mat):
    xm, ym = mat.shape
    xlist = list()
    ylist = list()
    vlist = list()
    for i in range(xm):
        for j in range(ym):
            if mat[i, j] != 0:
                xlist.append(i+0.5*j)
                ylist.append(j*np.sqrt(3)/2)
                vlist.append(mat[i, j])

    def map_int_to_color(x):
        if x == 4:
            return 'cornflowerblue'
        if x == 5:
            return 'lightsteelblue'
        if x == 6:
            return 'red'
        if x == 7:
            return 'wheat'
        if x == 8:
            return 'orange'
    clist = list(map(map_int_to_color, vlist))
    plt.axis('scaled')
    plt.xlim((0, 1.5*xm))
    plt.ylim((0, 0.867*ym))
    plt.scatter(xlist, ylist, c=clist, marker='o')
    plt.pause(0.1)


if __name__ == '__main__':
    size = 30
    bond_energy = 4  # +2D 破坏、形成C-C键需要的能量
    angular_energy = -2  # +1D 无序圆环内角处在不自然的状态含有的能量的系数
    # \delta E = angular_energy * f(\theta - \theta_0), \theta_0 = 2*pi/3
    net = np.zeros((size, size))  # 用于标记哪些是已经成键的区域
    # init_point = Point(size//2, size//2) # 在中心开始晶化
    init_point = Point(3*size//5, 3*size//5)  # 在中心开始晶化
    init_point_2 = Point(2*size//5, 2*size//5) # 在中心开始晶化
    init_point_3 = Point(size//5, size//5) # 在中心开始晶化
    # net[size//2, size//2] = 6
    net[3*size//5, 3*size//5] = 6
    net[2*size//5, 2*size//5] = 6
    net[size//5, size//5] = 6
    point_list = list()
    point_list.append(init_point)
    point_list.append(init_point_2)
    point_list.append(init_point_3)
    plt.show()
    for i in range(400):
        try:
            point, net = search_a_list(point_list, net)
            plot_mtx(net)
        except IndexError as e:
            print(e)
            plt.show()
        # print(point_list)
        # print(net)
    plt.show()
    # np.savetxt("C:\\Users\\Admin\\Desktop\\data.txt", net, fmt='%d',delimiter=', ')
