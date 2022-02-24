from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
# import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}

sup_sub_template = "<span class='word'>{word}</span><span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"

# s_n_crb_ssb = sup_sub_template.format(word="N", sub="CRB", sup="SSB")
# s_freq_ssb_gscn = sup_sub_template.format(word="FREQ", sub="SSB", sup="GSCN")
# s_scs_crb_ssb = sup_sub_template.format(word="SCS", sub="CRB", sup="SSB")
s_n_slot_frame = sup_sub_template.format(word="N", sub="slot", sup="frame,μ")
s_n_slot_subframe = sup_sub_template.format(word="N", sub="slot", sup="subframe,μ")

_scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

#############################################################################
# start add parameter
#############################################################################
t = Sep()

t = Parameter('subCarrierSpacingCommon')
t.range = ["15kHz", "30kHz", "60kHz", "120kHz"]
t.dict = _scs_dict
t.spec  = 'MIB -> subCarrierSpacingCommon'

t = Parameter('num_ssbs')
t.range = [4, 8, 64]
t.spec  = '38.213 4.1 L<sub>max</sub>'

t = ParameterInput('O')
t.default = 0
t.type = float
t.spec = "38.213 Table 13-11: 0, 2, 5, 7<br>\
38.213 Table 13-12: 0, 2.5, 5, 7.5"

t = ParameterInput('M')
t.default = 1
t.type = float
t.spec = "38.213 Table 13-11/12: 0.5, 1, 2"
t = Sep()

t = ParameterDisplay('mu')
t.desc = "μ"
t.spec = "38.211 Table 4.2-1. Numerology"
t.type = int

t = ParameterDisplay('nslots_frame')
t.desc = s_n_slot_frame
t.spec = "number of slots per frame. 38.211 Table 4.3.2-1, 38.213 13"
t.type = int

t = ParameterDisplay('nslots_subframe')
t.desc = s_n_slot_subframe
t.spec = "number of slots per subframe. 38.211 Table 4.3.2-1, 38.213 13"
t.type = int

#############################################################################
# end add parameter
#############################################################################

from math import log2
class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def subCarrierSpacingCommon_change(self, event=None):
        m = self.mvalue
        if m in (15, 30):
            self.set_range('num_ssbs', [4, 8])
        if m in (60, 120):
            self.set_range('num_ssbs', [64])
        mu = int(log2(m//15))
        self.set_range('mu', mu)
        self.set_range('nslots_frame', 2**mu*10)
        self.set_range('nslots_subframe', 2**mu)


