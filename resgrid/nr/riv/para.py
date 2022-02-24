from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

sup_sub_template = "{word}<span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"

s_n_bwp_size = sup_sub_template.format(word="N", sub="BWP", sup="size")

# _scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

#############################################################################
# start add parameter
#############################################################################
t  = Sep()

t = ParameterInput('n_bwp_size')
t.desc = s_n_bwp_size
t.default = 13
t.spec  = f'{s_n_bwp_size} [38.214 5.1.2.2.2]'

t = ParameterInput('RIV')
t.default = 1
t.spec  = f'38.214 5.1.2.2.2. example: BWP -> locationAndBandwidth'

t = ParameterDisplay('LRBs')
t.desc = "L<sub>RBs</sub>"
t.default = 1
t.spec  = f'38.214 5.1.2.2.2'

t = ParameterDisplay('RBstart')
t.desc = "RB<sub>start</sub>"
t.default = 0
t.spec  = f'38.214 5.1.2.2.2'


#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    # pass
    #############################################################################
    # start add consistency check
    #############################################################################
    def n_bwp_size_change(self, e=None):
        self.decode_riv()

    def RIV_change(self, e=None):
        self.decode_riv()

    def decode_riv(self):
        size = self.n_bwp_size.value
        riv = self.RIV.value
        L_1, start = divmod(riv, size)
        L = L_1 + 1
        if (L + start) > size:
            L = size + 1 - L_1
            start = size - 1 - start
        self.set_range("LRBs", L)
        self.set_range("RBstart", start)



