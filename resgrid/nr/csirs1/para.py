from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

#############################################################################
# start add parameter
#############################################################################
t = Parameter('row')
t.range = range(1, 19)
t.spec  = "38.211 table 7.4.1.5.3-1"

t = Sep()

t = ParameterDisplay('nrofPorts') # t.range = [1, 2, 4, 8, 12, 16, 24, 32]
t.spec  = 'CSI-RS-ResourceMapping->nrofPorts. X in 38.211 7.4.1.5.3'

t = ParameterDisplay('cdmType') # t.range = ['noCDM', 'fd-CDM2', 'cdm4-FD2-TD2', 'cdm8-FD2-TD4']
t.desc  = 'cdm-Type'
t.spec  = 'CSI-RS-ResourceMapping->cdm-Type'

t = Parameter('density')
t.range = [0.5, 1, 3]
t.spec  = 'CSI-RS-ResourceMapping->density. &rho; in 38.211 7.4.1.5.3'

t = Parameter('density_dot5')
t.desc  = 'density.dot5'
t.range = ["evenPRBs", "oddPRBs"]
t.dict = {"evenPRBs": 0, "oddPRBs": 1}
t.spec  = 'CSI-RS-ResourceMapping->density->dot5.'

t = Parameter('frequencyDomainAllocation')
t.range = ['']
t.spec  = "CSI-RS-ResourceMapping->frequencyDomainAllocation"

t = Parameter('firstOFDMSymbolInTimeDomain')
t.range = range(14)
t.spec  = 'CSI-RS-ResourceMapping->firstOFDMSymbolInTimeDomain. l<sub>0</sub> in 38.211 7.4.1.5.3'

t = Parameter('firstOFDMSymbolInTimeDomain2')
t.range = range(2, 13)
t.spec  = 'CSI-RS-ResourceMapping->firstOFDMSymbolInTimeDomain2. l<sub>1</sub> in 38.211 7.4.1.5.3'

t = Sep()

t = Parameter('fr')
t.desc  = "Frequency Range"
t.range = ["FR1", "FR2"]
t.spec = "38.104 5.3.2 Transmission bandwidth configuration"

t = Parameter('scs')
t.desc  = 'SCS (kHz)'
t.range = [15, 30, 60, 120]
t.spec = "38.104 5.3.2"

t = Parameter('bandwidth')
t.desc  = 'Bandwidth (MHz)'
t.range = [5, 10, 15, 20, 25, 30, 40, 60, 60, 70, 80, 90, 100, 200, 400]
t.default = 20
t.spec = "38.104 5.3.2"

t = ParameterDisplay('nrb')
t.desc = "N<sub>RB</sub>"
t.spec = "38.104 5.3.2"

t = Sep()

t = Parameter('startingRB')
t.range = range(0, 275, 4)
t.spec  = 'CSI-RS-ResourceMapping->freqBand->startingRB'

t = Parameter('nrofRBs')
t.range = range(24, 277, 4)
t.spec  = 'CSI-RS-ResourceMapping->freqBand->nrofRBs'

t = Sep()

t = Parameter('periodicity')
t.range = [4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 160, 320, 640]
t.spec  = 'derived from NZP-CSI-RS-Resource->periodicityAndOffset. unit slots'

t = Parameter('offset')
t.range = ['']
t.spec  = 'derived from NZP-CSI-RS-Resource->periodicityAndOffset.'


#############################################################################
# end add parameter
#############################################################################


# 38.104 table 5.3.2-1 and -2
bw_dct = {
    "FR1": {
        15: {5:25, 10:52, 15:79, 20:106, 25:133, 30:160, 40:216, 50:270},
        30: {5:11, 10:24, 15:38, 20:51, 25:65, 30:78, 40:106, 50:133, 60:162, 70:189, 80:217, 90:245, 100:273},
        60: {10:11, 15:18, 20:24, 25:31, 30:38, 40:51, 50:65, 60:79, 70:93, 80:107, 90:121, 100:135},
    },
    "FR2": {
        60: {50:66, 100:132, 200:264},
        120: {50:32, 100:66, 200:132, 400:264},
    },
}


class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def row_change(self, event):
        m = self.mvalue
        if m == 1:
            self.set_range('nrofPorts', 1)
            self.set_range('density', [3])
            self.set_range('cdmType', 'noCDM')
        elif m == 2:
            self.set_range('nrofPorts', 1)
            self.set_range('density', [1, 0.5])            
            self.set_range('cdmType', 'noCDM')
        elif m == 3:
            self.set_range('nrofPorts', 2)
            self.set_range('density', [1, 0.5])            
            self.set_range('cdmType', 'fd-CDM2')
        elif m == 3:
            self.set_range('nrofPorts', 2)
            self.set_range('density', [1, 0.5])            
            self.set_range('cdmType', 'fd-CDM2')
        elif m in (4, 5):
            self.set_range('nrofPorts', 4)
            self.set_range('density', [1])
            self.set_range('cdmType', 'fd-CDM2')
        elif m in (6, 7):
            self.set_range('nrofPorts', 8)
            self.set_range('density', [1])
            self.set_range('cdmType', 'fd-CDM2')
        elif m == 8:
            self.set_range('nrofPorts', 8)
            self.set_range('density', [1])
            self.set_range('cdmType', 'cdm4-FD2-TD2')
        elif m == 9:
            self.set_range('nrofPorts', 12)
            self.set_range('density', [1])
            self.set_range('cdmType', 'fd-CDM2')
        elif m == 10:
            self.set_range('nrofPorts', 12)
            self.set_range('density', [1])
            self.set_range('cdmType', 'cdm4-FD2-TD2')
        elif m == 11:
            self.set_range('nrofPorts', 16)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'fd-CDM2')
        elif m == 12:
            self.set_range('nrofPorts', 16)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'cdm4-FD2-TD2')
        elif m == 13:
            self.set_range('nrofPorts', 24)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'fd-CDM2')
        elif m == 14:
            self.set_range('nrofPorts', 24)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'cdm4-FD2-TD2')
        elif m == 15:
            self.set_range('nrofPorts', 24)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'cdm8-FD2-TD4')
        elif m == 16:
            self.set_range('nrofPorts', 32)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'fd-CDM2')
        elif m == 17:
            self.set_range('nrofPorts', 32)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'cdm4-FD2-TD2')
        elif m == 18:
            self.set_range('nrofPorts', 32)
            self.set_range('density', [1, 0.5])
            self.set_range('cdmType', 'cdm8-FD2-TD4')
        
        t = list(range(2, 13)) if m in (13, 14, 16, 17) else ['']
        self.set_range('firstOFDMSymbolInTimeDomain2', t)
        bitstring_length = {1:4, 2:12, 4:3}.get(m, 6)
        num = 1
        if m in (7, 8,):  # k1
            num = 2
        elif m in (10, 13, 14, 15): # k2
            num = 3
        elif m in (6, 11, 12, 16, 17, 18): # k3
            num = 4
        elif m in (9,): # k5
            num = 6
        k_list = [''.join(i) for i in itertools.product('01', repeat=bitstring_length) if i.count('1') == num]
        self.set_range('frequencyDomainAllocation', k_list)
            
    def density_change(self, event):
        m = self.mvalue
        new_range = [''] if m in (1, 3) else ["evenPRBs", "oddPRBs"]
        self.set_range('density_dot5', new_range)

    def periodicity_change(self, event):
        m = self.mvalue
        new_range = list(range(m))
        self.set_range('offset', new_range)

    def fr_change(self, event):
        new_range = sorted(bw_dct[self.fr.value].keys())
        self.set_range('scs', new_range)
        self.scs_change()

    def scs_change(self, event=None):
        new_range = sorted(bw_dct[self.fr.value][self.scs.value].keys())
        self.set_range('bandwidth', new_range)
        self.bandwidth_change()

    def bandwidth_change(self, event=None):
        nrb = bw_dct[self.fr.value][self.scs.value][self.bandwidth.value]
        self.set_range('nrb', nrb)
        new_range = range(0, nrb-24, 4)
        self.set_range('startingRB', new_range)
        self.startingRB_change()

    def startingRB_change(self, event=None):
        m = self.mvalue
        nrb = self.nrb.value
        new_range = range(24, nrb-m+4, 4)
        self.set_range('nrofRBs', new_range)
        
