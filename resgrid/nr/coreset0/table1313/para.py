from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

sup_sub_template = "{word}<span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"

s_n_crb_ssb = sup_sub_template.format(word="N", sub="CRB", sup="SSB")
s_freq_ssb_gscn = sup_sub_template.format(word="FREQ", sub="SSB", sup="GSCN")
s_scs_crb_ssb = sup_sub_template.format(word="SCS", sub="CRB", sup="SSB")

_scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

#############################################################################
# start add parameter
#############################################################################
t  = Sep()
t = ParameterDisplay('index')
t.default = 0
t.spec  = '38.213 Table 13-13. MIB -> pdcch-ConfigSIB1 -> searchSpaceZero'

t = ParameterDisplay('num_symbols_c0')
t.desc = sup_sub_template.format(word="N", sup="CORESET", sub="symb")
t.default = 1
t.spec  = 'Number of Symbols of CORESET0. See 38.213 Table 13-7'

t = Sep()

t = ParameterDisplay('pattern')
t.default = 2
t.spec = "SS/PBCH block and CORESET multiplexing pattern"

t = ParameterDisplay('scs_ssb')
t.desc = "SCS<sub>SSB</sub>"
t.default = "120kHz"
t.dict = _scs_dict
t.spec  = ''

t = ParameterDisplay('subCarrierSpacingCommon')
t.desc = "SCS<sub>CORESET0</sub>"
t.default = "60kHz"
t.dict = _scs_dict
t.spec  = 'MIB -> subCarrierSpacingCommon'

t = ParameterDisplay('case')
t.default = "D"
t.spec  = "38.213 4.1"


#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    pass
    #############################################################################
    # start add consistency check
    #############################################################################
    # def scs_ssb_coreset0_change(self, event=None):
    #     m = self.mvalue
    #     self.set_range('scs_ssb', int(m[:2]))
    #     self.set_range('subCarrierSpacingCommon', int(m[-2:]))
    #     if m[:2] == "15":
    #         self.set_range('case', ["A1", "A2"])
    #     if m[:2] == "30":
    #         self.set_range('case', ["B1", "B2", "C1", "C2"])

    # def index_change(self, event=None):
    #     m = self.mvalue
    #     O_lst = [0, 0, 2, 2, 5, 5, 7, 7, 0, 5, 0, 0, 2, 2, 5, 5]
    #     M_lst = [1, 0.5, 1, 0.5, 1, 0.5, 1, 0.5, 2, 2, 1, 1, 1, 1, 1, 1]
    #     self.set_range('O', O_lst[m])
    #     self.set_range('M', M_lst[m])
    #     fsi_lst = [0, -1, 0, -1, 0, -1, 0, -1, 0, 0, 1, 2, 1, 2, 1, 2, 1, 2]
    #     self.set_range('first_symbol_index', fsi_lst[m])
