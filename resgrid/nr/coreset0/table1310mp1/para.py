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
t = Sep()

t = ParameterDisplay('mpattern')
t.default = 1
t.spec = "SS/PBCH block and CORESET multiplexing pattern"

t = ParameterDisplay('scs_ssb')
t.default = "240kHz"
t.dict = _scs_dict
t.spec  = ''

t = ParameterDisplay('subCarrierSpacingCommon')
t.default = "120kHz"
t.dict = _scs_dict
t.spec  = 'MIB -> subCarrierSpacingCommon'

t = Sep()

t = Parameter('nrbs')
t.range = [48]
t.spec = "number of RBs"

t = Parameter('offset')
t.range = [0, 8]
t.spec = "Offset (RBs)"

t = Sep()

t = Parameter('kssb')
t.desc = "k<sub>SSB</sub>"
t.range = list(range(12))
t.spec = 'MIB -> ssb-SubcarrierOffset<br>\
    <span style="color:red;">0 and 1 may be invalid if not the lowest RB overlap with SSB</span>'

t = ParameterDisplay('scs_kssb')
t.default = "120kHz"
t.dict = _scs_dict
t.spec  = ''

#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def cc(self):
        if self.nrbs.value == 48:
            self.set_range('offset', [0, 8])
        if self.nrbs.value == 96:
            self.set_range('offset', [28])

    def nrbs_change(self, event=None):
        m = self.mvalue
        if m == 48:
            self.set_range('offset', [0, 8])
        if m == 96:
            self.set_range('offset', [28])
