from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

sup_sub_template = "<span class='word'>{word}</span><span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"

s_n_bwp_size = sup_sub_template.format(word="N", sub="BWP", sup="size")
s_n_bwp_start = sup_sub_template.format(word="N", sub="BWP", sup="start")

s_n_grid_size = sup_sub_template.format(word="N", sub="grid", sup="size")
s_n_grid_start = sup_sub_template.format(word="N", sub="grid", sup="start")

s_n_rb_offset = sup_sub_template.format(word="N", sub="RB", sup="offset")

# _scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

#############################################################################
# start add parameter
#############################################################################
t  = Sep()

t = Parameter('n_grid_start')
t.desc = f"{s_n_grid_start} <sub>38211 4.4.5</sub>"
t.range = range(2200)
t.default = 4
t.spec  = f"38331: SIB1 -> servingCellConfigCommon -> downlinkConfigCommon -> frequencyInfoDL -> scs-SpecificCarrierList -> SCS-SpecificCarrier -> offsetToCarrier<br>\
38213 12: O<sub>carrier</sub>"

t = Parameter('n_grid_size')
t.desc = f"{s_n_grid_size} <sub>38211 4.4.5</sub>"
t.range = range(1, 276)
t.default = 120
t.spec  = f"38331: SIB1 -> servingCellConfigCommon -> downlinkConfigCommon -> frequencyInfoDL -> scs-SpecificCarrierList -> SCS-SpecificCarrier -> carrierBandwidth"

t = Sep()

t = Parameter('n_bwp_size')
t.desc = f"{s_n_bwp_size} <sub>38211 4.4.5</sub>"
t.range = range(1, 276)
t.default = 100
t.spec  = f"Derived from RIV. 38213 12: L<sub>RB</sub>, 38.214 5.1.2.2.2 L<sub>RBs</sub>"

t = Parameter('rb_start')
t.desc = "RB<sub>start</sub>"
t.range = range(0, 276)
t.default = 9
t.spec  = f"Derived from RIV. 38213 12, 38.214 5.1.2.2.2"

t = ParameterDisplay('RIV')
t.default = 1
t.spec  = f'38331: BWP-Downlink -> bwp-Common -> genericParameters -> locationAndBandwidth. 38213 12, 38214 5.1.2.2.2'

t = Sep()

t = ParameterDisplay('n_bwp_start')
t.desc = f"{s_n_bwp_start} <sub>38211 4.4.5</sub>"
t.default = 0
t.spec  = f'38213 12: {s_n_bwp_start} = O<sub>carrier</sub> + RB<sub>start</sub>'

t = Sep()

t = Parameter('rb_offset')
t.range = range(-1, 6)
t.spec  = f'-1: not configured. commonControlResourceSet -> rb-Offset-r16. {s_n_rb_offset}'


#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    pass
    #############################################################################
    # start add consistency check
    #############################################################################
    def n_grid_size_change(self, e=None):
        m = self.mvalue
        self.set_range("n_bwp_size", range(1, m+1))

    def n_grid_start_change(self, e=None):
        self.update_n_bwp_start()

    def n_bwp_size_change(self, e=None):
        m = self.mvalue
        self.set_range("rb_start", range(m+1))
        # self.cal_riv()

    def rb_start_change(self, e=None):
        self.cal_riv()
        self.update_n_bwp_start()

    def cal_riv(self):
        size = 275
        L = self.n_bwp_size.value
        start = self.rb_start.value
        from math import floor
        L_1 = L - 1
        riv = size * L_1 + start if L_1 <= floor(size / 2) else size * (size - L_1) + (size - 1 - start)
        self.set_range("RIV", riv)

    def update_n_bwp_start(self):
        grid_start = self.n_grid_start.value
        rb_start = self.rb_start.value
        self.set_range("n_bwp_start", grid_start + rb_start)