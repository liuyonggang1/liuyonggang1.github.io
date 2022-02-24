from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

sup_sub_template = "{word}<span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"

s_n_crb_ssb = sup_sub_template.format(word="N", sub="CRB", sup="SSB")
s_freq_ssb_gscn = sup_sub_template.format(word="FREQ", sub="SSB", sup="GSCN")
s_scs_crb_ssb = sup_sub_template.format(word="SCS", sub="CRB", sup="SSB")

# _scs_dict = {"15kHz": 15, "30kHz": 30, "60kHz": 60, "120kHz": 120, "240kHz": 240}
_scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

#############################################################################
# start add parameter
#############################################################################
t = Parameter('fr')
t.desc  = "Frequency Range"
t.range = ["FR1", "FR2"]
t.spec = "Detected by UE. FR1: 0.41-7.125, FR2: 24.25-52.6 (GHZ)"

t = Parameter('scs_ssb')
t.desc = "SCS<sub>SSB</sub>"
t.dict = _scs_dict
t.range = [15, 30, 120, 240]
t.spec  = 'SSB SubCarrierSpacing, detected by UE'

t = Sep()

t = Parameter('subCarrierSpacingCommon')
t.dict = _scs_dict
t.range = [15, 30, 60, 120]
t.spec  = 'MIB -> subCarrierSpacingCommon'

t = Parameter('kssb')
t.desc = "k<sub>SSB</sub>"
t.range = list(range(24))
# t.spec = 'MIB -> ssb-SubcarrierOffset'
t.spec = 'MIB -> ssb-SubcarrierOffset. <br>For SCS<sub>SSB</sub> and subCarrierSpacingCommon pair:<br>'
t.spec += '{15, 15}: range [0, 11]<br>'
t.spec += '{15, 30}: range [0, 23]<br>'
t.spec += '{30, 15}: range [0, 12]<br>'
t.spec += '{30, 30}: range [0, 23]<br>'
t.spec += 'FR2: range [0, 11]'

t = ParameterDisplay('scs_kssb')
# t.desc = "SCS<sub>k<span><sub>SSB</sub></span></sub>"
t.desc = "SCS<sub>kSSB</sub>"
t.dict = _scs_dict
t.spec  = 'SCS associated with k<sub>SSB</sub>. FR1: 15kHz, FR2: subCarrierSpacingCommon'

t = ParameterDisplay('scs_crb_ssb')
t.desc = s_scs_crb_ssb # "SCS<sub>crb_ssb</sub>"
t.dict = _scs_dict
# t.spec  = 'SCS associated with common resource block N<sub>CRB</sub><sup>SSB</sup>'
t.spec  = f"SCS associated with common resource block {s_n_crb_ssb}. equal to subCarrierSpacingCommon"

t = Sep()

t = ParameterInput('offsetToPointA')
# t.spec  = 'SIB1 -> offsetToPointA, number of RBs from PointA to common resource block N<sub>CRB</sub><sup>SSB</sup>. range: [0, 2199]'
t.spec  = f"SIB1 -> offsetToPointA, number of RBs from PointA to common resource block {s_n_crb_ssb}. range: [0, 2199].<br>"
t.spec += "when subCarrierSpacingCommon=30 or subCarrierSpacingCommon=120: valid value mod 2 = 0"
t.default = 2

t = ParameterDisplay('scs_offsetToPointA')
t.desc = "SCS<sub>offsetToPointA</sub>"
t.dict = _scs_dict
t.spec  = 'SCS associated with offsetToPointA. FR1: 15kHz, FR2: 60kHz'

t = Sep()

t = ParameterDisplay('ssbgscn_to_pointa')
# t.desc = "FREQ<sub>ssb<span><sub>gscn</sub></span></sub> - FREQ<sub>PointA</sub>"
t.desc = f"{s_freq_ssb_gscn} - FREQ<sub>PointA</sub>"
t.spec  = "SCS<sub>SSB</sub> * 120 + SCS<sub>kssb</sub> * kssb + SCS<sub>offsetToPointA</sub> * offsetToPointA * 12 (kHz)"

#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def fr_change(self, event):
        m = self.mvalue
        if m == "FR1":
            self.set_range('scs_ssb', [15, 30])
            self.set_range('subCarrierSpacingCommon', [15, 30])
            self.set_range('scs_kssb', 15)
            self.set_range('scs_offsetToPointA', 15)
            self.subCarrierSpacingCommon_change()
        elif m == "FR2":
            self.set_range('scs_ssb', [120, 240])
            self.set_range('subCarrierSpacingCommon', [60, 120])
            self.set_range('scs_offsetToPointA', 60)
            self.subCarrierSpacingCommon_change()
        self.scs_ssb_change()
            
    def subCarrierSpacingCommon_change(self, event=None):
        m = self.mvalue
        if self.fr.value == "FR2":
            self.set_range('scs_kssb', m)
        self.set_range('scs_crb_ssb', m)
        self.update_ssbgscn_to_pointa()

    def scs_ssb_change(self, event=None):
        m = self.mvalue
        if m == 120:
            self.set_range('kssb', [0, 2, 4, 6, 8, 10])
        elif m == 240:
            self.set_range('kssb', [0, 4, 8])
        else:
            self.set_range('kssb', list(range(24)))
        self.update_ssbgscn_to_pointa()

    def kssb_change(self, event=None):
        self.update_ssbgscn_to_pointa()

    def update_ssbgscn_to_pointa(self):
        mhz, ghz = None, None
        khz = self.scs_ssb.value * 12 * 10 + \
            self.scs_kssb.value * self.kssb.value + \
            self.scs_offsetToPointA.value * self.offsetToPointA.value * 12
        if khz >= 1000:
            mhz = khz / 1000
            if mhz >= 1000:
                ghz = mhz / 1000
        if ghz is not None:
            s = f"{ghz} GHz"
        elif mhz is not None:
            s = f"{mhz} MHz"
        else:
            s = f"{khz} KHz"
        self.ssbgscn_to_pointa.range = s