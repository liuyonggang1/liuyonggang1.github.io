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

#############################################################################
# start add parameter
#############################################################################
t  = Sep()

t = Parameter('n_bwp_size')
t.desc = s_n_bwp_size
t.range = range(1, 276)
t.default = 20
t.spec = "38214 5.1.2.2.2. the number of PRBs for the BWP"

t = Parameter('n_bwp_start')
t.desc = s_n_bwp_start
t.range = range(1, 276)
t.default = 5
t.spec = "38214 5.1.2.2.2. the starting CRB for the BWP"

t = Parameter('rb_start')
t.desc = "RB<sub>start</sub>"
t.range = [7]
t.spec = "38214 5.1.2.2.2. the starting RB in BWP"

t = Parameter('len_rbs')
t.desc = "L<sub>RBs</sub>"
t.range = [9]
t.spec = "38214 5.1.2.2.2. the number of RBs"



#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    def __init__(self):
        super().__init__()
        self._cc = ["n_bwp_size", "rb_start"]
    #############################################################################
    # start add consistency check
    #############################################################################
    def cc(self, ev=None):
        bwp_size = self.n_bwp_size.value
        self.set_range("rb_start", range(bwp_size))
        rb_start = self.rb_start.value
        self.set_range("len_rbs", range(1, bwp_size-rb_start))

