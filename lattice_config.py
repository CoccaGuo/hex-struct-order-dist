# lattice_config.py by CoccaGuo at 2021/10/14 15:48

import numpy as np
from LatticePoints import LatticePoints
from abstract.I_Lattice import I_Lattice
from hex_lat import main
from utils import Pos


class Lattice(I_Lattice):
    # 一种六角蜂巢的格子
    def __init__(self, a=2, n=6, size=20) -> None:
        super().__init__(n)
        self.a = a
        self.size = size
        self.state = 0.9  # 有序程度
        self.percentage_ratio = {
            6: self.state, 
            5: (1-self.state)*0.4,
            7: (1-self.state)*0.4,
            8: (1-self.state)*0.2}

    # get lattice points (position) list
    def fetch_lp_list(self):
        ang = 2*np.pi/self.n
        # x_axis = list()
        # y_axis = list()
        lp_center_list = list()
        # for i in range(self.size):
        #     x_axis.append(Pos(i*self.a, 0))
        #     y_axis.append(Pos(i*self.a*np.cos(ang), i*self.a*np.sin(ang)))   
        for i in range(self.size):
            lp_center_list.extend(
                [Pos(i*self.a*np.cos(ang) + j*self.a,
                i*self.a*np.sin(ang)) for j in range(self.size)])
        return lp_center_list

    
    def get_lattice_point_list(self) -> list:
        lp_center_list = self.fetch_lp_list()
        lp_list = list()
        for lp_center in lp_center_list:
            lp_list.append(LatticePoints(v=self.n, lat=self, pos=lp_center, rad=self.a/2, offset=0))
        return lp_list
    

if __name__ == '__main__':
    l = Lattice(n=6, a=1, size=3)
    lp_center = l.fetch_lp_list()
    lp_list = l.get_lattice_point_list()

    x = [pos.x for pos in lp_center]
    y = [pos.y for pos in lp_center]
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for lp in lp_list:
        lp.plot(ax)
    ax.scatter(x, y, color='k')
    plt.show()


        
    

