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
t.default = 50
t.spec = "38214 5.1.2.2.1. the number of PRBs for the BWP"

t = Parameter('n_bwp_start')
t.desc = s_n_bwp_start
t.range = range(1, 276)
t.default = 5
t.spec = "38214 5.1.2.2.1. the starting CRB for the BWP"

t = Parameter('rgb_size_config')
t.desc = ""
t.range = ["config1", "config2"]
t.spec = "PDSCH-Config -> rbg-Size. 38214 Table 5.1.2.2.1-1"

t = ParameterDisplay('p')
t.desc = "P"
t.default = 0
t.spec = "38214 Table 5.1.2.2.1-1. the number of PRBs per RGB"

t = ParameterDisplay('n_rgb')
t.desc = "N<sub>RBG</sub>"
t.default = 0
t.spec = "38214 5.1.2.2.1. the number of RBGs for the BWP"

t = ParameterDisplay('rbg_0_size')
t.desc = s_rbg_0_size
t.default = 0
t.spec = "38214 5.1.2.2.1. the number of PRBs for the first RGB"

t = ParameterDisplay('rbg_last_size')
t.desc = s_rbg_last_size
t.default = 0
t.spec = "38214 5.1.2.2.1. the number of PRBs for the last RGB"



#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    def __init__(self):
        super().__init__()
        self._cc = ["n_bwp_size", "n_bwp_start", "rgb_size_config"]
    #############################################################################
    # start add consistency check
    #############################################################################
    def cc(self, ev=None):
        aoa = [[1, 36, 2, 4],
               [37, 72, 4, 8],
               [73, 144, 8, 16],
               [145, 275, 16, 16]]
        config = self.rgb_size_config.value
        bwp_size = self.n_bwp_size.value
        bwp_start = self.n_bwp_start.value
        for (a, b, c, d) in aoa:
            if a <= bwp_size <= b:
                p = c if config == "config1" else d
                break
        self.set_range("p", p)
        n_rgb = math.ceil( (bwp_size  + (bwp_start % p))  / p)
        self.set_range("n_rgb", n_rgb)
        p0 = p - bwp_start % p
        self.set_range("rbg_0_size", p0)
        p1 = (bwp_start + bwp_size) % p
        if p1 == 0:
            p1 = p
        self.set_range("rbg_last_size", p1) 

