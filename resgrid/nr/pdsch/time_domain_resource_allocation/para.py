from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import math

sup_sub_template = "<span class='word'>{word}</span><span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"
# s_mu = "μ"

s_n_bwp_size = sup_sub_template.format(word="N", sub="BWP", sup="size")
s_n_bwp_start = sup_sub_template.format(word="N", sub="BWP", sup="start")

s_rbg_0_size = sup_sub_template.format(word="RBG", sub="0", sup="size")
s_rbg_last_size = sup_sub_template.format(word="RBG", sub="last", sup="size")

# s_n_rb_coreset = sup_sub_template.format(word="N", sub="RB", sup="CORESET")
# s_n_reg_coreset = sup_sub_template.format(word="N", sub="REG", sup="CORESET")

# scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

bar_template = "<span class='bar'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"
char_l = "&#621;"
s_l_bar = bar_template.format(sub="<i>&#621;</i>", sup="_")

#############################################################################
# start add parameter
#############################################################################
t  = Sep()

t = Parameter('pdsch_mapping_type')
t.desc = "PDSCH Mapping Type"
t.range = ["A", "B"]
t.default = "A"
t.spec = "PDSCH-TimeDomainResourceAllocation -> mappingType"

t = Parameter('CP')
t.desc = "Cyclic Prefix"
t.range = ["Normal", "Extended"]
t.default = "Normal"
t.spec = ""

t = ParameterDisplay('nsymbols')
t.desc = ""
t.default = 14
t.spec = "symbols per slot"

t = Parameter('S')
t.desc = "Start Symnbol"
t.range = [0, 1, 2, 3]
t.default = 2
t.spec = "PDSCH-TimeDomainResourceAllocation -> startSymbolAndLength"

t = Parameter('L')
t.desc = "Length"
t.range = range(3, 15)
t.default = 12
t.spec = "PDSCH-TimeDomainResourceAllocation -> startSymbolAndLength"

t = Sep()

t = Parameter('dmrs_TypeA_Position')
t.desc = "dmrs-TypeA-Position"
t.range = [2, 3]
t.default = 2
t.spec = "MIB -> dmrs-TypeA-Position"

t = Sep()

t = Parameter('dmrs_type')
t.desc = "dmrs-Type"
t.range = [1, 2]
t.default = 1
t.spec = "DMRS-DownlinkConfig -> dmrs-Type"

t = Parameter('dmrs_AdditionalPosition')
t.desc = "dmrs-AdditionalPosition"
t.range = [0, 1, 2, 3]
t.default = 0
t.spec = "DMRS-DownlinkConfig -> dmrs-AdditionalPosition"

t = ParameterDisplay('maxLength')
t.desc = "maxLength"
t.default = 1
t.spec = "DMRS-DownlinkConfig -> maxLength. The maximum number of OFDM symbols for DL front loaded DMRS"

t = Sep()

t = ParameterDisplay('l0')
t.desc = "<i>&#621;</i><sub><sub>0</sub></sub>"
t.default = 2
t.spec = "38.211 7.4.1.1.2"

t = Parameter('l1')
t.desc = "<i>&#621;</i><sub><sub>1</sub></sub>"
t.range = [11, 12]
t.default = 11
t.spec = "38.211 7.4.1.1.2, table 7.4.1.1.2-3. <i>&#621;</i><sub><sub>d</sub></sub>=(13, 14) and typeA and pos1."

t = ParameterDisplay('ld')
t.desc = "<i>&#621;</i><sub><sub>d</sub></sub>"
t.default = 0
t.spec = "38.211 7.4.1.1.2"

t = ParameterDisplay('l_bar')
t.desc = s_l_bar
t.default = ""
t.spec = "38.211 Table 7.4.1.1.2-3"

t = ParameterDisplay('l_prime')
t.desc = "<i>&#621;<sup class='lprime'>'</sup></i>"
t.default = 0
t.spec = "38.211 Table 7.4.1.1.2-1, 2, 5"

t = ParameterDisplay('ports')
t.desc = "supported antenna ports"
t.default = ""
t.spec = "38.211 Table 7.4.1.1.2-5"

t = Sep()

t = Parameter('dci11_aps')
t.desc = "DCI 1_1"
t.range = range(12)
t.default = 10
t.spec = "38.212 DCI 1_1 Antenna ports. Table 7.3.1.2.2-1/3. only show one codeword cases"

t = ParameterDisplay('dci11_dmrs_ports')
t.desc = "DMRS port(s)"
t.default = ""
t.spec = "38.212 DCI 1_1 Antenna ports. Table 7.3.1.2.2-1/3"

t = ParameterDisplay('dci11_cdm_groups')
t.desc = "CDM group(s) without data"
t.default = ""
t.spec = "38.212 DCI 1_1 Antenna ports. Table 7.3.1.2.2-1/3"

#############################################################################
# end add parameter
#############################################################################
class Config(ConfigBase):
    def __init__(self):
        super().__init__()
        self._cc = ["pdsch_mapping_type", "CP", "S", "L", "dmrs_TypeA_Position", "dmrs_AdditionalPosition", "dmrs_type", "l1", "dci11_aps"]
    #############################################################################
    # start add consistency check
    #############################################################################
    def cc(self, ev=None):
        mp = self.pdsch_mapping_type.value
        cp = self.CP.value
        n = 14 if cp == "Normal" else 12
        self.set_range("nsymbols", n)

        if mp == "A":
            self.set_range("S", range(4))
            S = self.S.value
            self.set_range("L", range(3, n-S+1))
            self.dmrs_TypeA_Position.show()
            l0 = self.dmrs_TypeA_Position.value
            self.set_range("l0", l0)
            ld = self.S.value + self.L.value
            self.set_range("ld", ld)
            self.set_range("dmrs_AdditionalPosition", [0,1,2,3])
            if ld in (13, 14) and self.dmrs_AdditionalPosition.value == 1:
                self.l1.show()
            else:
                self.l1.hide()
            if ld in [3,4,5,6,7]:
                l_bar = [l0]
            elif ld in [8, 9]:
                if self.dmrs_AdditionalPosition.value == 0:
                    l_bar = [l0]
                else:
                    l_bar = [l0, 7]
            elif ld in [10, 11]:
                if self.dmrs_AdditionalPosition.value == 0:
                    l_bar = [l0]
                elif self.dmrs_AdditionalPosition.value == 1:
                    l_bar = [l0, 9]
                else:
                    l_bar = [l0, 6, 9]
            elif ld in [12]:
                if self.dmrs_AdditionalPosition.value == 0:
                    l_bar = [l0]
                elif self.dmrs_AdditionalPosition.value == 1:
                    l_bar = [l0, 9]
                elif self.dmrs_AdditionalPosition.value == 2:
                    l_bar = [l0, 6, 9]
                elif self.dmrs_AdditionalPosition.value == 3:
                    l_bar = [l0, 5, 8, 11]
            elif ld in [13, 14]:
                if self.dmrs_AdditionalPosition.value == 0:
                    l_bar = [l0]
                elif self.dmrs_AdditionalPosition.value == 1:
                    l_bar = [l0, self.l1.value]
                elif self.dmrs_AdditionalPosition.value == 2:
                    l_bar = [l0, 7, 11]
                elif self.dmrs_AdditionalPosition.value == 3:
                    l_bar = [l0, 5, 8, 11]
            else:
                l_bar = ["error"]
        if mp == "B":
            self.set_range("S", range(n-2+1))
            S = self.S.value
            a = [i for i in [2, 4, n//2] if S+i <= n]
            if self.L.value not in a:
                self.set_range("L", [a[-1]])
            self.set_range("L", a)
            self.dmrs_TypeA_Position.hide()
            l0 = 0
            self.set_range("l0", l0)
            ld = self.L.value
            self.set_range("ld", ld)
            self.set_range("dmrs_AdditionalPosition", [0,1])
            self.l1.hide()
            if ld in [2, 4]:
                l_bar = [l0]
            elif ld in [6, 7]:
                if self.dmrs_AdditionalPosition.value == 0:
                    l_bar = [l0]
                else:
                    l_bar = [l0, 4]
            else:
                l_bar = ["error"]
        l_bar = ",".join([str(_)  for _ in l_bar])
        self.set_range("l_bar", l_bar)
        if self.dmrs_type.value == 1:
            self.set_range("ports", "1000 - 1003")
        if self.dmrs_type.value == 2:
            self.set_range("ports", "1000 - 1005")
        
        # 38212 Table 7.3.1.2.2-1
        aps1 = [
            [1, 0],
            [1, 1],
            [1, 0, 1],
            [2, 0],
            [2, 1],
            [2, 2],
            [2, 3],
            [2, 0, 1],
            [2, 2, 3],
            [2, 0, 1, 2],
            [2, 0, 1, 2, 3],
            [2, 0, 2]]
        # 38212 Table 7.3.1.2.2-3
        aps2 = [
            [1, 0],
            [1, 1],
            [1, 0, 1],
            [2, 0],
            [2, 1],
            [2, 2],
            [2, 3],
            [2, 0, 1],
            [2, 2, 3],
            [2, 0, 1, 2],
            [2, 0, 1, 2, 3],
            [3, 0],
            [3, 1],
            [3, 2],
            [3, 3],
            [3, 4],
            [3, 5],
            [3, 0, 1],
            [3, 2, 3],
            [3, 4, 5],
            [3, 0, 1, 2],
            [3, 3, 4, 5],
            [3, 0, 1, 2, 3],
            [2, 0, 2],
            [3, 0, 1]]
        if self.dmrs_type.value == 1:
            self.set_range("dci11_aps", range(12))
            aps = aps1[self.dci11_aps.value]
        if self.dmrs_type.value == 2:
            self.set_range("dci11_aps", range(24))
            aps = aps2[self.dci11_aps.value]
        self.dci11_cdm_groups.list_value = list(range(aps[0]))
        self.set_range("dci11_cdm_groups", str(self.dci11_cdm_groups.list_value))
        self.dci11_dmrs_ports.list_value = [1000+i for i in aps[1:]]
        self.set_range("dci11_dmrs_ports", str(self.dci11_dmrs_ports.list_value))





