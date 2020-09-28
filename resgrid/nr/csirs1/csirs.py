# names = [
# 'frequencyDomainAllocation',
# 'nrofPorts',
# 'cdmType',
# 'firstOFDMSymbolInTimeDomain',
# 'firstOFDMSymbolInTimeDomain2',
# 'density'
# ]
import math


wf_table_38211_741532 = {
'noCDM': [[1]],
'fd-CDM2': [[1, 1], [1, -1]],
'cdm4-FD2-TD2': [[1, 1], [1, -1], [1, 1], [1, -1]],
'cdm8-FD2-TD4': [[1, 1], [1, -1], [1, 1], [1, -1], [1, 1], [1, -1], [1, 1], [1, -1]]}

wt_table_38211_741532 = {
'noCDM': [[1]],
'fd-CDM2': [[1], [1]],
'cdm4-FD2-TD2': [[1, 1], [1, 1], [1, -1], [1, -1]],
'cdm8-FD2-TD4': [[1, 1, 1, 1], [1, 1, 1, 1], [1, -1, 1, -1], [1, -1, 1, -1], [1, 1, -1, -1], [1, 1, -1, -1], [1, -1, -1, 1], [1, -1, -1, 1]] }

N_sc_RB = 12
N_symb_slot = 14
sqrt__2 = round(1/math.sqrt(2), 4)

def get_wf(cdmType, index, k_prime):
    return wf_table_38211_741532[cdmType][index][k_prime]

def get_wt(cdmType, index, l_prime):
    return wt_table_38211_741532[cdmType][index][l_prime]


class CsiRsSequence:
    def __init__(self, slot, l, nid):
        self.x1 = [0 for i in range(10000)]
        self.x1[0] = 1
        for a in range(31, 10000):
            self.x1[a] = (self.x1[a-31+3] + self.x1[a-31]) % 2
            
        self.x2_list = self.c_init(slot, l, nid) + [0 for i in range(10000-31)]
        for a in range(31, 10000):
            self.x2[a] = (self.x1[a-31+3] + self.x1[a-31+2] + self.x1[a-31+1] + self.x1[a-31]) % 2

    def init_c(self, slot, l, nid):
        i = (2**10 * (N_symb_slot * slot + l +1)(2*nid + 1) + nid) % (2**31)
        s = "0"*31 + bin(i)[2:]
        return [int(j) for j in s[-31:]]

    def cal_c_n(self, n):
        return (self.x1(n + 1600) + self.x2(n+1600)) % 2

    def cal_r_m(self, m):
        real = (1-2*self.cal_c_n(2*m))/math.sqrt(2)
        imag = (1-2*self.cal_c_n(2*m+1))/math.sqrt(2)
        return complex(real, imag)


class KLGrid:
    def __init__(self, csirs, k_prime, l_prime, k_bar, l_bar, cdm_j, s):
        self.csirs = csirs
        self.k_prime = k_prime
        self.l_prime = l_prime
        self.k_bar = k_bar
        self.l_bar = l_bar
        self.cdm_j = cdm_j
        self.s = s
        self.k = self.k_prime + self.k_bar
        self.l = self.l_prime + self.l_bar
        self.wf = get_wf(self.csirs.cdmType, self.s, self.k_prime)
        self.wt = get_wt(self.csirs.cdmType, self.s, self.l_prime)
        self.port_idx = self.s + self.csirs.cdm_group_size * self.cdm_j
        self.port = 3000 + self.port_idx
        

    def __str__(self):
        return f"port={self.port}, wf={self.wf}, wt={self.wt}"

    def cal_m_prime(self, crb_idx):
        return math.floor(crb_idx*self.csirs.alpha) + self.k_prime + math.floor(self.k_bar*self.density/N_sc_RB)

class CsiRs:
    def __init__(self, cfg):
        self.cfg = cfg
        cfg.copy_cfg(self)
        self.l0 = self.firstOFDMSymbolInTimeDomain
        self.l1 = self.firstOFDMSymbolInTimeDomain2
        self.init()
        self.alpha = self.density if self.nrofPorts == 1 else 2*self.density

    def init(self):
        if self.cdmType == 'noCDM':
            self.cdm_fd = 1
            self.cdm_td = 1
        elif self.cdmType == 'fd-CDM2':
            self.cdm_fd = 2
            self.cdm_td = 1
        elif self.cdmType == 'cdm4-FD2-TD2':
            self.cdm_fd = 2
            self.cdm_td = 2
        elif self.cdmType == 'cdm8-FD2-TD4':
            self.cdm_fd = 2
            self.cdm_td = 4
        self.cdm_group_size = self.cdm_fd * self.cdm_td
        getattr(self, f"init_row{self.row}")()
        self.cdm_j_list = [0, 0, 0] if self.row == 1 else list(range(len(self.k_bar_list)))
        self.klgrid_list = []
        s_idx = 0
        for l_prime in range(self.cdm_td):
            for k_prime in range(self.cdm_fd):
                for k_bar, l_bar, cdm_j in zip(self.k_bar_list, self.l_bar_list, self.cdm_j_list):
                    o = KLGrid(self, k_prime, l_prime, k_bar, l_bar, cdm_j, s_idx)
                    self.klgrid_list.append(o)
                s_idx += 1

    def __getattr__(self, name):
        if len(name) == 2 and name[0] == 'k' and name[1] in '0123456789':
            return self.k_i(int(name[1]))
        raise
        
    def k_i(self, i):
        factor = 1 if self.row in (1, 2) else 4 if self.row == 4 else 2
        f = [n for n, c in enumerate(self.frequencyDomainAllocation[::-1]) if c == '1'][i]
        return factor * f

    def init_row1(self):
        self.k_bar_list = [self.k0, self.k0+4, self.k0+8]
        self.l_bar_list = [self.l0, self.l0, self.l0]

    def init_row2(self):
        self.k_bar_list = [self.k0]
        self.l_bar_list = [self.l0]

    def init_row3(self):
        self.k_bar_list = [self.k0]
        self.l_bar_list = [self.l0]

    def init_row4(self):
        self.k_bar_list = [self.k0, self.k0+2]
        self.l_bar_list = [self.l0, self.l0]

    def init_row5(self):
        self.k_bar_list = [self.k0, self.k0]
        self.l_bar_list = [self.l0, self.l0+1]

    def init_row6(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k3]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0]

    def init_row7(self):
        self.k_bar_list = [self.k0, self.k1, self.k0, self.k1]
        self.l_bar_list = [self.l0, self.l0, self.l0+1, self.l0+1]

    def init_row8(self):
        self.k_bar_list = [self.k0, self.k1]
        self.l_bar_list = [self.l0, self.l0]

    def init_row9(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k3, self.k4, self.k5]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0, self.l0, self.l0]

    def init_row10(self):
        self.k_bar_list = [self.k0, self.k1, self.k2]
        self.l_bar_list = [self.l0, self.l0, self.l0]

    def init_row11(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k3, self.k0, self.k1, self.k2, self.k3]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0, self.l0+1, self.l0+1, self.l0+1, self.l0+1]

    def init_row12(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k3]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0]

    def init_row13(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k0,   self.k1,   self.k2,   self.k0, self.k1, self.k2, self.k0,   self.k1,   self.k2]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0+1, self.l0+1, self.l0+1, self.l1, self.l1, self.l1, self.l1+1, self.l1+1, self.l1+1]

    def init_row14(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k0, self.k1, self.k2]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l1, self.l1, self.l1]

    def init_row15(self):
        self.k_bar_list = [self.k0, self.k1, self.k2]
        self.l_bar_list = [self.l0, self.l0, self.l0]

    def init_row16(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k3, 
                           self.k0, self.k1, self.k2, self.k3,
                           self.k0, self.k1, self.k2, self.k3,
                           self.k0, self.k1, self.k2, self.k3]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0, 
                           self.l0+1, self.l0+1, self.l0+1, self.l0+1,
                           self.l1, self.l1, self.l1, self.l1, 
                           self.l1+1, self.l1+1, self.l1+1, self.l1+1]

    def init_row17(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k3, 
                           self.k0, self.k1, self.k2, self.k3]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0, 
                           self.l1, self.l1, self.l1, self.l1]

    def init_row18(self):
        self.k_bar_list = [self.k0, self.k1, self.k2, self.k3]
        self.l_bar_list = [self.l0, self.l0, self.l0, self.l0]

    def is_csirs_rb(self, rb_idx):
        if self.startingRB <= rb_idx < self.startingRB + self.nrofRBs:
            if self.density in (1, 3):
                return True
            return rb_idx % 2 == self.density_dot5
        else:
            return False

    def is_csirs_slot(self, slot):
        return slot % self.periodicity == self.offset
