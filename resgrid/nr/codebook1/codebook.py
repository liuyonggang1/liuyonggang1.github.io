from fractions import Fraction
from browser import window

F1  = Fraction(0, 1)  #  1 = e^(i*pi*0)
FN1 = Fraction(1, 1)  # -1 = e^(i*pi*1)
FI  = Fraction(1, 2)  #  i = e^(i*pi/2)
FNI = Fraction(3, 2)  # -i = e^(i*pi*3/2)

# 'codebookMode',
# 'pcsirs',
# 'n1n2',
# 'o1o2',
# 'nlayers',

# base is e^(i*pi)
# 38.214 section 5.2.2
class Codebook:
    def __init__(self, cfg):
        cfg.copy_cfg(self)
        self.n1, self.n2 = [int(i) for i in self.n1n2.split(",")]
        self.o1, self.o2 = [int(i) for i in self.o1o2.split(",")]
        self.norm_pcsirs = self.nlayers*self.pcsirs

    def phi_n(self, n):
        return Fraction(n, 2)
        
    def theta_p(self, p):
        return Fraction(p, 4)

    def u_m(self, m):
        return u_m(m=m, n2=self.n2, o2=self.o2)

    def v_l_m(self, l, m):
        return v_l_m(l=l, m=m, n1=self.n1, n2=self.n2, o1=self.o1, o2=self.o2)

    def v_bar_l_m(self, l, m):
        return v_bar_l_m(l=l, m=m, n1=self.n1, n2=self.n2, o1=self.o1, o2=self.o2)

    def bit_a(self, l, m):
        return self.n2*self.o2*l+m
    
    def tex_w(self, w):
        return tex_w(w, self.norm_pcsirs)

    def get_table(self):
        name = f"cal_w_layer{self.nlayers}_mode{self.codebookMode}"
        return getattr(self, name)()
        # head = ["NO.", "i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "k<sub>1</sub>", "k<sub>2</sub>", "i<sub>2</sub>", "W", "e<sup>i<b class='red'>&theta;</b></sup>"]

    #####################################################################
    # table 5.2.2.2.1-5 layer 1, mode 1
    #####################################################################
    def cal_w_layer1_mode1(self):
        result = []
        i11_list = range(self.n1*self.o1)
        i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
        i2_list = [0,1,2,3]
        for i11 in i11_list:
            for i12 in i12_list:
                for i2 in i2_list:
                    l, m, n = i11, i12, i2
                    vlm = self.v_l_m(l, m)
                    phi = self.phi_n(n)
                    t0 = vlm
                    t1 = multiple_vlm(phi, vlm)
                    w = combine_by_row(t0, t1)
                    tw = self.tex_w(w)
                    tw3 = tex_w_3(w)
                    row = [i11, i12, i2, tw, tw3, self.bit_a(l, m)]
                    result.append(row)
        head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>2</sub>", "W", "e<sup>i&pi;<b class='red'>x</b></sup>", "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        return head, result

    #####################################################################
    # table 5.2.2.2.1-5 layer 1, mode 2
    #####################################################################
    def cal_w_layer1_mode2(self):
        result = []
        if self.n2 > 1:
            i11_list = range(self.n1*self.o1//2)
            i12_list = range(self.n2*self.o2//2)
            i2_list = range(16)
            for i11 in i11_list:
                for i12 in i12_list:
                    for i2 in i2_list:
                        n = divmod(i2, 4)
                        a1 = 0 if i2 in (0,1,2,3,8,9,10,11) else 1
                        a2 = 0 if i2 in (0,1,2,3,4,5,6,7) else 1
                        l = 2*i11 + a1
                        m = 2*i12 + a2
                        vlm = self.v_l_m(l, m)
                        phi = self.phi_n(n)
                        t0 = vlm
                        t1 = multiple_vlm(phi, vlm)
                        w = combine_by_row(t0, t1)
                        tw = self.tex_w(w)
                        tw3 = tex_w_3(w)
                        row = [i11, i12, i2, tw, tw3, self.bit_a(l, m)]
                        result.append(row)
        else: # self.n2 == 1
            i11_list = range(self.n1*self.o1//2)
            i12_list = [0]
            i2_list = range(16)
            for i11 in i11_list:
                for i12 in i12_list:
                    for i2 in i2_list:
                        a1, n = divmod(i2, 4)
                        l = 2*i11 + a1
                        m = 0
                        vlm = self.v_l_m(l, m)
                        phi = self.phi_n(n)
                        t0 = vlm
                        t1 = multiple_vlm(phi, vlm)
                        w = combine_by_row(t0, t1)
                        tw = self.tex_w(w)
                        tw3 = tex_w_3(w)
                        row = [i11, i12, i2, tw, tw3, self.bit_a(l, m)]
                        result.append(row)
        head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>2</sub>", "W", "e<sup>i&pi;<b class='red'>x</b></sup>", "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result

    #####################################################################
    # table 5.2.2.2.1-6 layer 2, mode 1
    #####################################################################
    def get_i13_list_layer2(self):
        # 38.214 table 5.2.2.2.1-3
        if self.n1 > self.n2 > 1:
            return range(4)
        elif self.n1 == self.n2:
            return range(4)
        elif self.n1 == 2 and self.n2 == 1:
            return range(2)
        elif self.n1 > 2 and self.n2 == 1:
            return range(4)

    def get_k1_k2_layer2(self, i13):
        # 38.214 table 5.2.2.2.1-3
        if self.n1 > self.n2 > 1:
            return {0:(0, 0), 1:(self.o1, 0), 2:(0, self.o2), 3:(2*self.o1, 0)}[i13]
        elif self.n1 == self.n2:
            return {0:(0, 0), 1:(self.o1, 0), 2:(0, self.o2), 3:(self.o1, self.o2)}[i13]
        elif self.n1 == 2 and self.n2 == 1:
            return {0:(0, 0), 1:(self.o1, 0)}[i13]
        elif self.n1 > 2 and self.n2 == 1:
            return {0:(0, 0), 1:(self.o1, 0), 2:(2*self.o1, 0), 3:(3*self.o1, 0)}[i13]

    # table 5.2.2.2.1-6 mode 1
    def cal_w_layer2_mode1(self):
        result = []
        i11_list = range(self.n1*self.o1)
        i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
        i2_list = [0,1]
        i13_list = self.get_i13_list_layer2()
        for i11 in i11_list:
            for i12 in i12_list:
                for i13 in i13_list:
                    k1, k2 = self.get_k1_k2_layer2(i13)
                    for i2 in i2_list:
                        l, l_prime, m, m_prime, n = i11, i11+k1, i12, i12+k2, i2
                        vlm = self.v_l_m(l, m)
                        vlm_prime = self.v_l_m(l_prime, m_prime)
                        phi = self.phi_n(n)
                        t00 = vlm
                        t01 = vlm_prime
                        t0 = combine_by_col(t00, t01)
                        t10 = multiple_vlm(phi, vlm)
                        t11 = multiple_vlm(FN1, phi, vlm_prime)
                        t1 = combine_by_col(t10, t11)
                        w = combine_by_row(t0, t1)
                        tw = self.tex_w(w)
                        tw3 = tex_w_3(w)
                        row = [i11, i12, i13, k1, k2, i2, tw, tw3, self.bit_a(l, m)]
                        result.append(row)
        head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "k<sub>1</sub>", "k<sub>2</sub>", "i<sub>2</sub>", 
                "W", 
                "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result

    #####################################################################
    # table 5.2.2.2.1-6 layer 2, mode 2
    #####################################################################
    def cal_w_layer2_mode2(self):
        result = []
        if self.n2 > 1:
            i11_list = range(self.n1*self.o1//2)
            i12_list = range(self.n2*self.o2//2)
            i2_list = range(8)
            for i11 in i11_list:
                for i12 in i12_list:
                    for i13 in i13_list:
                        k1, k2 = self.get_k1_k2_layer2(i13)
                        for i2 in i2_list:
                            n = i2 % 2
                            a1 = 0 if i2 in (0,1,4,5) else 1
                            a2 = 0 if i2 in (0,1,2,3) else 1
                            l = 2*i11 + a1
                            m = 2*i12 + a2
                            l_prime = l + k1
                            m_prime = m + k2
                            vlm = self.v_l_m(l, m)
                            vlm_prime = self.v_l_m(l_prime, m_prime)
                            t00 = vlm
                            t01 = vlm_prime
                            t0 = combine_by_col(t00, t01)
                            phi = self.phi_n(n)
                            t10 = multiple_vlm(phi, vlm)
                            t11 = multiple_vlm(FN1, phi, vlm_prime)
                            t1 = combine_by_col(t10, t11)
                            w = combine_by_row(t0, t1)
                            tw = self.tex_w(w)
                            tw3 = tex_w_3(w)
                            row = [i11, i12, i13, k1, k2, i2, tw, tw3, self.bit_a(l, m)]
                            result.append(row)
            head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "k<sub>1</sub>", "k<sub>2</sub>", "i<sub>2</sub>", 
                    "W", 
                    "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                    "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        else: # self.n2 == 1
            i11_list = range(self.n1*self.o1//2)
            i12_list = [0]
            i2_list = range(8)
            for i11 in i11_list:
                for i12 in i12_list:
                    for i13 in i13_list:
                        k1, k2 = self.get_k1_k2_layer2(i13)
                        for i2 in i2_list:
                            a1, n = divmod(i2, 2)
                            l = 2*i11 + a1
                            l_prime = l + k1
                            m, m_prime = 0, 0
                            vlm = self.v_l_m(l, m)
                            vlm_prime = self.v_l_m(l_prime, m_prime)
                            t00 = vlm
                            t01 = vlm_prime
                            t0 = combine_by_col(t00, t01)
                            phi = self.phi_n(n)
                            t10 = multiple_vlm(phi, vlm)
                            t11 = multiple_vlm(FN1, phi, vlm_prime)
                            t1 = combine_by_col(t10, t11)
                            w = combine_by_row(t0, t1)
                            tw = self.tex_w(w)
                            tw3 = tex_w_3(w)
                            row = [i11, i12, i13, k1, i2, tw, tw3, self.bit_a(l, m)]
                            result.append(row)
            head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "k<sub>1</sub>", "i<sub>2</sub>", 
                    "W", 
                    "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                    "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result

    #####################################################################
    # table 5.2.2.2.1-7 layer 3, mode 1, 2
    #####################################################################
    def get_i13_list_layer34(self):
        # 38.214 table 5.2.2.2.1-4
        if self.n1 == 2 and self.n2 == 1:
            return [0]
        elif self.n1 == 4 and self.n2 == 1:
            return range(3)
        elif self.n1 == 6 and self.n2 == 1:
            return range(4)
        elif self.n1 == 2 and self.n2 == 2:
            return range(3)
        elif self.n1 == 3 and self.n2 == 2:
            return range(4)

    def get_k1_k2_layer34(self, i13):
        # 38.214 table 5.2.2.2.1-4
        if self.n1 == 2 and self.n2 == 1:
            return (self.o1, 0)
        elif self.n1 == 2 and self.n2 == 1:
            return ((i3+1)*self.o1, 0)
        elif self.n1 == 6 and self.n2 == 1:
            return ((i3+1)*self.o1, 0)
        elif self.n1 == 2 and self.n2 == 2:
            return {0:(self.o1, 0), 1:(0, self.o2), 2:(self.o1, self.o2)}[i13]
        elif self.n1 == 3 and self.n2 == 2:
            return {0:(self.o1, 0), 1:(0, self.o2), 2:(self.o1, self.o2), 3:(2*self.o1, self.o2)}[i13]

    # table 5.2.2.2.1-7 layer 3
    def cal_w_layer3_mode1(self):
        result = []
        if self.pcsirs < 16:
            i11_list = range(self.n1*self.o1)
            i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
            i2_list = [0,1]
            i13_list = self.get_i13_list_layer34()
            for i11 in i11_list:
                for i12 in i12_list:
                    for i13 in i13_list:
                        k1, k2 = self.get_k1_k2_layer2(i13)
                        for i2 in i2_list:
                            l, l_prime, m, m_prime, n = i11, i11+k1, i12, i12+k2, i2
                            vlm = self.v_l_m(l, m)
                            vlm_prime = self.v_l_m(l_prime, m_prime)
                            phi = self.phi_n(n)
                            t00 = vlm
                            t01 = vlm_prime
                            t02 = vlm
                            t0 = combine_by_col(t00, t01, t02)
                            t10 = multiple_vlm(phi, vlm)
                            t11 = multiple_vlm(phi, vlm_prime)
                            t12 = multiple_vlm(FN1, phi, vlm)
                            t1 = combine_by_col(t10, t11, t12)
                            w = combine_by_row(t0, t1)
                            tw = self.tex_w(w)
                            tw3 = tex_w_3(w)
                            row = [i11, i12, i13, k1, k2, i2, tw, tw3, self.bit_a(l, m)]
                            result.append(row)
            head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "k<sub>1</sub>", "k<sub>2</sub>", "i<sub>2</sub>", 
                    "W", 
                    "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                    "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        else:
            i11_list = range(self.n1*self.o1//2)
            i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
            i2_list = [0,1]
            i13_list = range(4)
            for i11 in i11_list:
                for i12 in i12_list:
                    for i13 in i13_list:
                        for i2 in i2_list:
                            l, m, p, n = i11, i12, i13, i2
                            phi = self.phi_n(n)
                            theta = self.theta_p(p)
                            v = self.v_bar_l_m(l, m)
                            t0 = combine_by_col(v, v, v)
                            t10 = multiple_vlm(theta, v)
                            t11 = multiple_vlm(FN1, theta, v)
                            t1 = combine_by_col(t10, t11, t10)
                            t20 = multiple_vlm(phi, v)
                            t22 = multiple_vlm(FN1, phi, v)
                            t2 = combine_by_col(t20, t20, t22)
                            t30 = multiple_vlm(phi, theta, v)
                            t31 = multiple_vlm(-1, phi, theta, v)
                            t3 = combine_by_col(t30, t31, t31)
                            w = combine_by_col(t0, t1, t2, t3)
                            tw = self.tex_w(w)
                            tw3 = tex_w_3(w)
                            row = [i11, i12, i13, i2, tw, tw3, self.bit_a(l, m)]
                            result.append(row)
            head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "i<sub>2</sub>", 
                    "W", 
                    "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                    "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result

    def cal_w_layer3_mode2(self):
        return self.cal_w_layer3_mode1()

    #####################################################################
    # table 5.2.2.2.1-8 layer 4, mode 1, 2
    #####################################################################    
    def cal_w_layer4_mode2(self):
        return self.cal_w_layer4_mode1()

    def cal_w_layer4_mode1(self):
        result = []
        if self.pcsirs < 16:
            i11_list = range(self.n1*self.o1)
            i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
            i2_list = [0,1]
            i13_list = self.get_i13_list_layer34()
            for i11 in i11_list:
                for i12 in i12_list:
                    for i13 in i13_list:
                        k1, k2 = self.get_k1_k2_layer2(i13)
                        for i2 in i2_list:
                            l, l_prime, m, m_prime, n = i11, i11+k1, i12, i12+k2, i2
                            vlm = self.v_l_m(l, m)
                            vlm_prime = self.v_l_m(l_prime, m_prime)
                            phi = self.phi_n(n)
                            t00 = vlm
                            t01 = vlm_prime
                            t02 = vlm
                            t03 = vlm_prime
                            t0 = combine_by_col(t00, t01, t02, t03)
                            t10 = multiple_vlm(phi, vlm)
                            t11 = multiple_vlm(phi, vlm_prime)
                            t12 = multiple_vlm(FN1, phi, vlm)
                            t13 = multiple_vlm(phi, phi, vlm_prime)
                            t1 = combine_by_col(t10, t11, t12, t13)
                            w = combine_by_row(t0, t1)
                            tw = self.tex_w(w)
                            tw3 = tex_w_3(w)
                            row = [i11, i12, i13, k1, k2, i2, tw, tw3, self.bit_a(l, m)]
                            result.append(row)
            head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "k<sub>1</sub>", "k<sub>2</sub>", "i<sub>2</sub>", 
                    "W", 
                    "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                    "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        else:
            i11_list = range(self.n1*self.o1//2)
            i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
            i2_list = [0,1]
            i13_list = range(4)
            for i11 in i11_list:
                for i12 in i12_list:
                    for i13 in i13_list:
                        for i2 in i2_list:
                            l, m, p, n = i11, i12, i13, i2
                            phi = self.phi_n(n)
                            theta = self.theta_p(p)
                            v = self.v_bar_l_m(l, m)
                            t0 = combine_by_col(v, v, v, v)
                            t10 = multiple_vlm(theta, v)
                            t11 = multiple_vlm(FN1, theta, v)
                            t1 = combine_by_col(t10, t11, t10, t11)
                            t20 = multiple_vlm(phi, v)
                            t22 = multiple_vlm(FN1, phi, v)
                            t2 = combine_by_col(t20, t20, t22, t22)
                            t30 = multiple_vlm(phi, theta, v)
                            t31 = multiple_vlm(-1, phi, theta, v)
                            t3 = combine_by_col(t30, t31, t31, t30)
                            w = combine_by_col(t0, t1, t2, t3)
                            tw = self.tex_w(w)
                            tw3 = tex_w_3(w)
                            row = [i11, i12, i13, i2, tw, tw3, self.bit_a(l, m)]
                            result.append(row)
            head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>1,3</sub>", "i<sub>2</sub>", 
                    "W", 
                    "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                    "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result

    #####################################################################
    # table 5.2.2.2.1-9 layer 5, mode 1, 2
    #####################################################################    
    def cal_w_layer5_mode2(self):
        return self.cal_w_layer5_mode1()

    def cal_w_layer5_mode1(self):
        result = []
        i11_list = range(self.n1*self.o1)
        i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
        i2_list = [0,1]
        for i11 in i11_list:
            for i12 in i12_list:
                for i2 in i2_list:
                    if self.n2 > 1:
                        l, l1, l2, m, m1, m2, n = i11, i11+self.o1, i11+self.o1, i12, i12, i12+self.o2, i2
                    else:
                        l, l1, l2, m, m1, m2, n = i11, i11+self.o1, i11+2*self.o1, 0,0,0, i2
                    v = self.v_l_m(l, m)
                    v1 = self.v_l_m(l1, m1)
                    v2 = self.v_l_m(l2, m2)
                    phi = self.phi_n(n)
                    t0 = combine_by_col(v, v, v1, v1, v2)
                    t10 = multiple_vlm(phi, v)
                    t11 = multiple_vlm(-1, phi, v)
                    t13 = multiple_vlm(-1, v1)
                    t1 = combine_by_col(t10, t11, v1, t13, v2)
                    w = combine_by_row(t0, t1)
                    tw = self.tex_w(w)
                    tw3 = tex_w_3(w)
                    row = [i11, i12, i2, tw, tw3, self.bit_a(l, m)]
                    result.append(row)
        head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>2</sub>", 
                "W", 
                "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result


    #####################################################################
    # table 5.2.2.2.1-10 layer 6, mode 1, 2
    #####################################################################    
    def cal_w_layer6_mode2(self):
        return self.cal_w_layer6_mode1()

    def cal_w_layer6_mode1(self):
        result = []
        i11_list = range(self.n1*self.o1)
        i12_list = [0] if self.n2 == 1 else range(self.n2*self.o2)
        i2_list = [0,1]
        for i11 in i11_list:
            for i12 in i12_list:
                for i2 in i2_list:
                    if self.n2 > 1:
                        l, l1, l2, m, m1, m2, n = i11, i11+self.o1, i11+self.o1, i12, i12, i12+self.o2, i2
                    else:
                        l, l1, l2, m, m1, m2, n = i11, i11+self.o1, i11+2*self.o1, 0,0,0, i2
                    v = self.v_l_m(l, m)
                    v1 = self.v_l_m(l1, m1)
                    v2 = self.v_l_m(l2, m2)
                    phi = self.phi_n(n)
                    t0 = combine_by_col(v, v, v1, v1, v2, v2)
                    t10 = multiple_vlm(phi, v)
                    t11 = multiple_vlm(-1, phi, v)
                    t12 = multiple_vlm(phi, v1)
                    t13 = multiple_vlm(-1, phi, v1)
                    t14 = v2
                    t15 = multiple_vlm(-1, v2)
                    t1 = combine_by_col(t10, t11, t12, t13, t14, t15)
                    w = combine_by_row(t0, t1)
                    tw = self.tex_w(w)
                    tw3 = tex_w_3(w)
                    row = [i11, i12, i2, tw, tw3, self.bit_a(l, m)]
                    result.append(row)
        head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>2</sub>", 
                "W", 
                "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result

    #####################################################################
    # table 5.2.2.2.1-11 layer 7, mode 1, 2
    #####################################################################    
    def cal_w_layer7_mode2(self):
        return self.cal_w_layer7_mode1()

    def cal_w_layer7_mode1(self):
        result = []
        if self.n1 == 4 and self.n2 == 1:
            i11_list = range(self.n1*self.o1//2)
        else:
            i11_list = range(self.n1*self.o1)
        if self.n2 == 1:
            i12_list = [0]
        elif self.n1 == 2 and self.n2 == 2:
            i12_list = range(self.n2*self.o2)
        elif self.n1 > 2 and self.n2 == 2:
            i12_list = range(self.n2*self.o2//2)
        elif self.n1 > 2 and self.n2 > 2:
            i12_list = range(self.n2*self.o2)
        i2_list = [0,1]
        for i11 in i11_list:
            for i12 in i12_list:
                for i2 in i2_list:
                    if self.n1 == 4 and self.n2 == 1:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11+2*self.o1, i11+3*self.o1, 0, 0, 0, 0, i2
                    elif self.n1 > 4 and self.n2 == 1:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11+2*self.o1, i11+3*self.o1, 0, 0, 0, 0, i2
                    elif self.n1 == 2 and self.n2 == 2:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11, i11+self.o1, i12, i12, i12+*self.o2, i12+*self.o2, i2
                    elif self.n1 > 2 and self.n2 == 2:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11, i11+self.o1, i12, i12, i12+*self.o2, i12+*self.o2, i2
                    elif self.n1 > 2 and self.n2 > 2:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11, i11+self.o1, i12, i12, i12+*self.o2, i12+*self.o2, i2
                    v = self.v_l_m(l, m)
                    v1 = self.v_l_m(l1, m1)
                    v2 = self.v_l_m(l2, m2)
                    v3 = self.v_l_m(l3, m3)
                    phi = self.phi_n(n)
                    t0 = combine_by_col(v, v, v1, v2, v2, v3, v3)
                    pv =  multiple_vlm(phi, v)
                    npv = multiple_vlm(FN1, phi, v)
                    pv1 =  multiple_vlm(phi, v1)
                    nv2 = multiple_vlm(FN1, v2)
                    nv3 = multiple_vlm(FN1, v3)
                    t1 = combine_by_col(pv, npv, pv1, v2, nv2, v3, nv3)
                    w = combine_by_row(t0, t1)
                    tw = self.tex_w(w)
                    tw3 = tex_w_3(w)
                    row = [i11, i12, i2, tw, tw3, self.bit_a(l, m)]
                    result.append(row)
        head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>2</sub>", 
                "W", 
                "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result


    #####################################################################
    # table 5.2.2.2.1-12 layer 8, mode 1, 2
    #####################################################################    
    def cal_w_layer8_mode2(self):
        return self.cal_w_layer8_mode1()

    def cal_w_layer8_mode1(self):
        result = []
        if self.n1 == 4 and self.n2 == 1:
            i11_list = range(self.n1*self.o1//2)
        else:
            i11_list = range(self.n1*self.o1)
        if self.n2 == 1:
            i12_list = [0]
        elif self.n1 == 2 and self.n2 == 2:
            i12_list = range(self.n2*self.o2)
        elif self.n1 > 2 and self.n2 == 2:
            i12_list = range(self.n2*self.o2//2)
        elif self.n1 > 2 and self.n2 > 2:
            i12_list = range(self.n2*self.o2)
        i2_list = [0,1]
        for i11 in i11_list:
            for i12 in i12_list:
                for i2 in i2_list:
                    if self.n1 == 4 and self.n2 == 1:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11+2*self.o1, i11+3*self.o1, 0, 0, 0, 0, i2
                    elif self.n1 > 4 and self.n2 == 1:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11+2*self.o1, i11+3*self.o1, 0, 0, 0, 0, i2
                    elif self.n1 == 2 and self.n2 == 2:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11, i11+self.o1, i12, i12, i12+*self.o2, i12+*self.o2, i2
                    elif self.n1 > 2 and self.n2 == 2:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11, i11+self.o1, i12, i12, i12+*self.o2, i12+*self.o2, i2
                    elif self.n1 > 2 and self.n2 > 2:
                        l, l1, l2, l3, m, m1, m2, m3, n = i11, i11+self.o1, i11, i11+self.o1, i12, i12, i12+*self.o2, i12+*self.o2, i2
                    v = self.v_l_m(l, m)
                    v1 = self.v_l_m(l1, m1)
                    v2 = self.v_l_m(l2, m2)
                    v3 = self.v_l_m(l3, m3)
                    phi = self.phi_n(n)
                    t0 = combine_by_col(v, v, v1, v1, v2, v2, v3, v3)
                    pv =  multiple_vlm(phi, v)
                    npv = multiple_vlm(FN1, phi, v)
                    pv1 =  multiple_vlm(phi, v1)
                    npv1 =  multiple_vlm(FN1, phi, v1)
                    nv2 = multiple_vlm(FN1, v2)
                    nv3 = multiple_vlm(FN1, v3)
                    t1 = combine_by_col(pv, npv, pv1, npv1, v2, nv2, v3, nv3)
                    w = combine_by_row(t0, t1)
                    tw = self.tex_w(w)
                    tw3 = tex_w_3(w)
                    row = [i11, i12, i2, tw, tw3, self.bit_a(l, m)]
                    result.append(row)
        head = ["i<sub>1,1<sub>", "i<sub>1,2</sub>", "i<sub>2</sub>", 
                "W", 
                "e<sup>i<span>&pi;</span><b class='red'>x</b></sup>",
                "bit a<sub>N<sub>2</sub>O<sub>2</sub>l+m</sub>"]
        result = sorted(result, key=lambda t: t[-1])
        return head, result

def u_m(m=None, n2=None, o2=None):
    return [Fraction(i*m, n2*o2) for i in range(n2)]

def v_l_m(factor=2, l=None, m=None, n1=None, n2=None, o1=None, o2=None):
    um = u_m(m=m, n2=n2, o2=o2)
    t = Fraction(factor*l, n1*o1)
    return [[t * i + x] for i in range(n1) for x in um]

def v_bar_l_m(l=None, m=None, n1=None, n2=None, o1=None, o2=None):
    return v_l_m(factor=4, l=l, m=m, n1=n1, n2=n2, o1=o1, o2=o2)

def multiple_vlm(*args):
    if isinstance(args[0], int) and args[0] == -1:
        prefix = FN1
    else:
        prefix = F1
    for arg in args[:-1]:
        prefix = prefix + arg
    vlm = args[-1]    
    return [[prefix+c for c in r] for r in vlm]

def combine_by_row(*args):
    result = []
    for vlm in args:
        for row in vlm:
            result.append(row[:])
    return result

def combine_by_col(*args):
    result = []
    for row in args[0]:
        result.append(row[:])
    for vlm in args[1:]:
        for i, row in enumerate(vlm):
            for c in row:
                result[i].append(c)
    return result

def tex(s):
    s1 = '$$' + window.math.parse(s).toTex({"parenthesis": "auto", "implicit": "hide"}) + '$$'
    return s1

def tex_w(w, pcsirs):
    result = [[to_exp_str(c) for c in row] for row in w]
    s = str_pcsirs(pcsirs) + str_aoa(result)
    return tex(s)

def str_aoa(aoa):
    return str(aoa).replace("'", "")

def str_pcsirs(p):
    if p % 64 == 0:
        b = 8
    elif p % 16 == 0:
        b = 4
    else:
        b = 2
    r = p // (b**2)
    if r == 1:
        s = f"1/{b}*"
    else:
        s = f"1/({b}sqrt({r}))*"
    return s

def to_exp_str(c):
    c = c % 2
    if c == F1:
        return 1
    elif c == FN1:
        return -1
    elif c == FI:
        return "j"
    elif c == FN1:
        return "-j"
    if c.numerator == 1:
        return f"e^(j*pi/{c.denominator})"
    else:
        return f"e^(j*pi*{c.numerator}/{c.denominator})"

def to_exp_str2(c):
    c = c % 2
    if c.numerator == 0:
        return "0"
    if c.denominator == 1:
        return "pi"
    if c.numerator == 1:
        return f"pi/{c.denominator}"
    else:
        return f"{c.numerator}pi/{c.denominator}"

def tex_w_3(w):
    result = [[to_exp_str3(c) for c in row] for row in w]
    s = str_aoa(result)
    return tex(s)

def to_exp_str3(c):
    c = c % 2
    if c.numerator == 0:
        return "0"
    if c.denominator == 1:
        return "1"
    return f"{c.numerator/c.denominator}"
