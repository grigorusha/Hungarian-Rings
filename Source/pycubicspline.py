"""
Cubic Spline library on python
author Atsushi Sakai
https://github.com/AtsushiSakai/pycubicspline
"""

import bisect
import math
import numpy as np

class Spline:
    # Linear Cubic Spline class

    def __init__(self, x, y):
        self.b, self.c, self.d, self.w = [], [], [], []

        self.x = x
        self.y = y

        self.nx = len(x)  # dimension of x
        h = np.diff(x)

        # calc coefficient c
        self.a = [iy for iy in y]

        # calc coefficient c
        A = self.__calc_A(h)
        B = self.__calc_B(h)
        self.c = np.linalg.solve(A, B)

        # calc spline coefficient b and d
        for i in range(self.nx - 1):
            self.d.append((self.c[i + 1] - self.c[i]) / (3.0 * h[i]))
            tb = (self.a[i + 1] - self.a[i]) / h[i] - h[i] * \
                 (self.c[i + 1] + 2.0 * self.c[i]) / 3.0
            self.b.append(tb)

    def calc(self, t):
        """
        Calc position
        if t is outside of the input x, return None
        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = self.a[i] + self.b[i] * dx + self.c[i] * dx ** 2.0 + self.d[i] * dx ** 3.0

        return result

    def calc_d(self, t):
        """
        Calc first derivative
        if t is outside of the input x, return None
        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = self.b[i] + 2.0 * self.c[i] * dx + 3.0 * self.d[i] * dx ** 2.0
        return result

    def calc_dd(self, t):
        # Calc second derivative

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = 2.0 * self.c[i] + 6.0 * self.d[i] * dx
        return result

    def __search_index(self, x):
        return bisect.bisect(self.x, x) - 1

    def __calc_A(self, h):
        A = np.zeros((self.nx, self.nx))
        A[0, 0] = 1.0
        for i in range(self.nx - 1):
            if i != (self.nx - 2):
                A[i + 1, i + 1] = 2.0 * (h[i] + h[i + 1])
            A[i + 1, i] = h[i]
            A[i, i + 1] = h[i]

        A[0, 1] = 0.0
        A[self.nx - 1, self.nx - 2] = 0.0
        A[self.nx - 1, self.nx - 1] = 1.0
        #  print(A)
        return A

    def __calc_B(self, h):
        """
        calc matrix B for spline coefficient c
        """
        B = np.zeros(self.nx)
        for i in range(self.nx - 2):
            B[i + 1] = 3.0 * (self.a[i + 2] - self.a[i + 1]) / \
                       h[i + 1] - 3.0 * (self.a[i + 1] - self.a[i]) / h[i]
        #  print(B)
        return B

    def calc_curvature(self, t):
        j = int(math.floor(t))
        if j < 0:
            j = 0
        elif j >= len(self.a):
            j = len(self.a) - 1

        dt = t - j
        df = self.b[j] + 2.0 * self.c[j] * dt + 3.0 * self.d[j] * dt * dt
        ddf = 2.0 * self.c[j] + 6.0 * self.d[j] * dt
        k = ddf / ((1 + df ** 2) ** 1.5)
        return k

class Spline2D:
    # 2D Cubic Spline class

    def __init__(self, x, y):
        self.s = self.__calc_s(x, y)
        self.sx = Spline(self.s, x)
        self.sy = Spline(self.s, y)

    def __calc_s(self, x, y):
        dx = np.diff(x)
        dy = np.diff(y)
        self.ds = [math.sqrt(idx ** 2 + idy ** 2)
                   for (idx, idy) in zip(dx, dy)]
        s = [0.0]
        s.extend(np.cumsum(self.ds))
        return s

    def calc_position(self, s):
        x = self.sx.calc(s)
        y = self.sy.calc(s)
        return x, y

def calc_2d_spline(x, y, num=100, delta=True):
    """
    Calc 2d spline course with interpolation

    :param x: interpolated x positions
    :param y: interpolated y positions
    :param num: number of path points
    :return:
        - x     : x positions
        - y     : y positions
        - s     : Path length from start point
    """
    sp = Spline2D(x, y)
    s = np.linspace(0, sp.s[-1], num+1)[:-1]

    r_x, r_y = [], []
    for i_s in s:
        ix, iy = sp.calc_position(i_s)
        r_x.append(ix)
        r_y.append(iy)

    if delta:
        for nn in range(len(x)):
            nx, ny = x[nn], y[nn]
            min_delta = min_pos = 99999
            for mm in range(len(r_x)):
                mx, my = r_x[mm], r_y[mm]
                delta = (nx-mx)**2 + (ny-my)**2
                if delta<min_delta:
                    min_delta = delta
                    min_pos = mm
            r_x[min_pos], r_y[min_pos] = nx, ny

    return r_x, r_y

def test_spline2d():
    print("Spline 2D test")
    import matplotlib.pyplot as plt
    
    # input_x = [-2.5, 0.0, 2.5, 5.0, 7.5, 3.0, -1.0]
    # input_y = [0.7, -6, 5, 6.5, 0.0, 5.0, -2.0]

    # input_x = [0, 70, 70, 45, 45,  95,  95,  -25, -25, 25,  25, 0,  0]
    # input_y = [0, 0,  25, 45, 180,188,200,200,188,180,45, 25, 0]

    input_x = [159.78980338999997, 183.61436315000003, 222.16331063      , 268.77118259      , 315.37905452      , 353.928002        , 377.75256179      , 394.59111089      , 411.42966002      , 428.26820914999996, 445.10675825000004,  450.0874475       , 435.36305981000004, 403.47957554      , 359.94993883999996, 312.30081929      , 268.77118259      , 225.24154585999997, 177.59242631      , 134.06278961      , 102.17930534      , 87.45491765       , 92.43560690000001 ,  109.274156        , 126.11270513000001, 142.95125425999998, 159.78980338999997]
    input_y = [124.37960674999988, 83.11425874999992 , 55.10680900999989 , 45.19999999999993 , 55.10680900999989 , 83.11425874999992 , 124.37960674999988, 176.2033321699999 , 228.02705758999986, 279.8507830099999 , 331.6745084299999 , 379.0626010999999 , 424.3796067499999 , 459.7898033599999 , 479.17044628999986, 479.17044628999986, 459.7898033599999 , 479.17044628999986, 479.17044628999986, 459.7898033599999 , 424.3796067499999 , 379.0626010999999 , 331.6745084299999 , 279.8507830099999 , 228.02705758999986, 176.2033321699999 , 124.37960674999988]

    input_x = [ 85.35533906, 101.5765065 , 120.71067812, 139.84484974, 156.06601718, 166.90465474, 170.71067812, 166.90465474, 156.06601718, 138.38834765, 120.71067812, 103.03300859,  85.35533906,  69.13417162,  50,           30.86582838,  14.64466094,   3.80602337,   0,            3.80602337,  14.64466094,  32.32233047,  50,           67.67766953,  85.35533906]
    input_y = [156.06601718, 166.90465474,170.71067812,166.90465474,156.06601718,139.84484974,120.71067812,101.5765065,  85.35533906, 67.67766953, 50,          32.32233047, 14.64466094,  3.80602337,  0,           3.80602337, 14.64466094, 30.86582838, 50,          69.13417162, 85.35533906,103.03300859,120.71067812,138.38834765,156.06601718]

    input_x = [159.78980338999997, 214.28049299000003, 268.77118259      , 323.26187219      , 377.75256179      , 424.36043372      , 462.9093812       , 486.73394099      , 491.71463021      , 476.99024252      , 445.10675825000004,  398.93630432      , 348.58223624      , 295.66297526      , 241.87938992      , 188.96012890999998, 138.60606083      , 92.43560690000001 ,  60.55212263       , 45.827734940000006, 50.80842416       , 74.63298395000001 , 113.18193143, 159.78980338999997]
    input_y = [124.37960674999988, 124.37960674999988, 124.37960674999988, 124.37960674999988, 124.37960674999988, 134.2864157599999 , 162.29386549999987, 203.55921349999988, 250.94730616999988, 296.26431178999985, 331.6745084299999 , 359.26007047999985, 378.1582683199999 , 387.7616983099999 , 387.7616983099999 , 378.1582683199999 , 359.26007047999985, 331.6745084299999 , 296.26431178999985, 250.94730616999988, 203.55921349999988, 162.29386549999987, 134.2864157599999, 124.37960674999988]

    input_x = [315.06601717798213, 353.88887394409886, 353.8888739426217, 315.06601717596425, 247.82285676262165, 170.17714323186547, 102.93398282000001, 64.11112605590117 , 64.11112605737833 , 102.93398282403572, 170.17714323737826, 247.8228567681345, 315.06601717798213]
    input_y = [102.93398282201787,170.17714323737835, 247.82285676813456, 315.06601718, 353.88887394409886, 353.8888739426217 , 315.06601717596425, 247.82285676262168, 170.17714323186547, 102.93398281999998, 64.1111260559012, 64.11112605737833, 102.93398282201787]

    x, y = calc_2d_spline(input_x, input_y, num=200)

    plt.subplots(1)
    plt.plot(input_x, input_y, "xb", label="input")
    plt.plot(x, y, "-r", label="spline")
    plt.grid(True)
    plt.axis("equal")
    plt.xlabel("x[m]")
    plt.ylabel("y[m]")
    plt.legend()

    plt.show()

if __name__ == '__main__':
    test_spline2d()