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
t.spec  = '38.213 Table 13-14. MIB -> pdcch-ConfigSIB1 -> searchSpaceZero'

t = ParameterDisplay('num_symbols_c0')
t.desc = sup_sub_template.format(word="N", sup="CORESET", sub="symb")
t.default = 1
t.spec  = 'Number of Symbols of CORESET0. See 38.213 Table 13-10'

t = Sep()

t = ParameterDisplay('pattern')
t.default = 2
t.spec = "SS/PBCH block and CORESET multiplexing pattern"

t = ParameterDisplay('scs_ssb')
t.desc = "SCS<sub>SSB</sub>"
t.default = "240kHz"
t.dict = _scs_dict
t.spec  = ''

t = ParameterDisplay('subCarrierSpacingCommon')
t.desc = "SCS<sub>CORESET0</sub>"
t.default = "120kHz"
t.dict = _scs_dict
t.spec  = 'MIB -> subCarrierSpacingCommon'

t = ParameterDisplay('case')
t.default = "E"
t.spec  = "38.213 4.1"


#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    pass
    #############################################################################
    # start add consistency check
    #############################################################################

