from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep

sup_sub_template = "<span class='word'>{word}</span><span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"

s_n_symb_coreset = sup_sub_template.format(word="N", sub="symb", sup="CORESET")
s_n_slot_frame = sup_sub_template.format(word="N", sub="slot", sup="frame")


_scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

#############################################################################
# start add parameter
#############################################################################
t  = Sep()

t = Parameter('scs_coreset')
t.desc = "SCS<sub>CORESET</sub>"
t.range = list(_scs_dict.values())
t.dict = _scs_dict
t.default = "30kHz"
t.spec  = f"IE BWP-Downlink -> bwp-Common -> genericParameters -> subcarrierSpacing"

t = ParameterDisplay('n_slots_frame')
t.desc = s_n_slot_frame
t.type = int
t.spec  = f"number slots per frame"

t = Sep()

ks_range = [1, 2, 4, 5, 8, 10, 16, 20, 40, 80, 160] 
t = Parameter('ks')
t.desc = "periodicity. k<sub>s</sub> <sub>38211 10.1</sub>"
t.range = ks_range
t.default = 2
t.spec  = f"IE SearchSpace -> monitoringSlotPeriodicityAndOffset. PDCCH monitoring periodicity of k<sub>s</sub> slots"

t = Parameter('os')
t.desc = "offset. o<sub>s</sub> <sub>38211 10.1</sub>"
t.range = [0]
t.spec  = f"IE SearchSpace -> monitoringSlotPeriodicityAndOffset. PDCCH monitoring offset of o<sub>s</sub> slots"

t = Parameter('ts')
t.desc = "T<sub>s</sub> <sub>38211 10.1</sub>"
t.range = [1]
t.spec  = f"IE SearchSpace -> duration. Number of consecutive slots that a SearchSpace lasts in every occasion"

t = Sep()

t = Parameter('n_symb_coreset')
t.desc = f"{s_n_symb_coreset} <sub>38211 7.3.2.2</sub>"
t.range = [1, 2, 3]
t.default = 2
t.spec  = f"IE ControlResourceSet -> duration. number of consecutive symbols for CORESET"

t = ParameterInput('monitoringSymbolsWithinSlot')
t.default = "1000 0001 0000 00"
t.spec  = f"IE SearchSpace -> monitoringSymbolsWithinSlot. bitmap for position of first symbols(s)."



#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    pass
    #############################################################################
    # start add consistency check
    #############################################################################
    def scs_coreset_change(self, e=None):
        m = self.mvalue
        import math
        mu = int(math.log2(m // 15))
        n_slots_frame = 2 ** mu * 10
        # result = [ks for ks in ks_range if ks % n_slots_frame == 0 or n_slots_frame % ks == 0]
        # self.set_range("ks", result)
        self.set_range("n_slots_frame", n_slots_frame)

    def ks_change(self, e=None):
        m = self.mvalue
        self.set_range("os", range(m))
        self.set_range("ts", range(1, m+1))

    # def os_change(self, e=None):
    #     m = self.mvalue
    #     ks = self.ks.value
    #     self.set_range("ts", range(1, ks+1))

