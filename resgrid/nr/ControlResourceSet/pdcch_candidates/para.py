from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep

sup_sub_template = "<span class='word'>{word}</span><span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"
s_mu = "μ"

# s_n_symb_coreset = sup_sub_template.format(word="N", sub="symb", sup="CORESET")
# s_n_rb_coreset = sup_sub_template.format(word="N", sub="RB", sup="CORESET")
# s_n_reg_coreset = sup_sub_template.format(word="N", sub="REG", sup="CORESET")
s_n_slot_frame_mu = sup_sub_template.format(word="N", sub="s,f", sup=s_mu)
s_n_candidates_1 = sup_sub_template.format(word="M", sub="s", sup="1")
s_n_candidates_2 = sup_sub_template.format(word="M", sub="s", sup="2")
s_n_candidates_4 = sup_sub_template.format(word="M", sub="s", sup="4")
s_n_candidates_8 = sup_sub_template.format(word="M", sub="s", sup="8")
s_n_candidates_16 = sup_sub_template.format(word="M", sub="s", sup="16")

# scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

#############################################################################
# start add parameter
#############################################################################
t  = Sep()

t = Parameter('uss')
t.desc = ""
t.range = ["CSS", "USS"]
t.default = "USS"

t = Sep()
# t = Parameter('mu')
# t.desc = s_mu
# t.range = range(4)
# t.default = 1
# t.spec = "numerologies. 0: 15kHz, 1: 30kHz, 2: 60kHz, 3: 120kHz"

# t = ParameterDisplay('scs_coreset')
# t.desc = "SCS"
# t.default = "30kHz"
# t.spec  = f"IE BWP-Downlink -> bwp-Common -> genericParameters -> subcarrierSpacing"

t = Parameter('nsf')
t.desc = f"{s_n_slot_frame_mu} <sub></sub>"
t.range = range(80)
t.spec  = f"the slot index in a frame. 15kHz: 0..9, 30kHz: 0..19, 60kHz: 0..39, 120kHz: 0..79"

t = ParameterInput('rnti')
t.desc = "n<sub><sub>RNTI</sub></sub>"
t.default = 2
t.spec = "C-RNTI"

t = Parameter('p')
t.desc = "p mod 3"
t.range = range(3)
t.spec  = f"p is IE SearchSpace -> controlResourceSetId, SearchSpaceExt-r16 -> controlResourceSetId-r16"

t = ParameterDisplay('A')
t.desc = "A<sub>p</sub>"
t.default = 0
t.spec = "38213 10.1"

t = ParameterDisplay('D')
t.default = 65537
t.spec = "38213 10.1"

t = ParameterDisplay('Y')
t.default = 0
t.spec = f"CSS: fixed to 0. USS: determined by {s_n_slot_frame_mu}, n<sub><sub>RNTI</sub></sub> and p. 38213 10.1"

t = Parameter('nci')
t.desc = "n<sub><sub>CI</sub></sub>"
t.range = range(8)
# t.range = range(1)
t.default = 0
t.spec  = f"For USS: 0 or IE ServingCellConfig -> crossCarrierSchedulingConfig -> schedulingCellInfo -> other -> cif-InSchedulingCell"

t = ParameterDisplay('nci2')
t.desc = "n<sub><sub>CI</sub></sub>"
t.default = 0
t.spec  = f"fixed to 0 for CSS"

t = Sep()

t = Parameter('n_cces')
t.desc = "N<sub><sub>CCE</sub></sub>"
t.range = [24, 48, 96] +  [i for i in range(1, 97) if (i % 4 == 0 or i % 6 == 0) and i not in [24, 48, 96] ]
t.default = 24
t.spec  = f"the number of CCEs in the CORESET"

# t = Sep()

t = Parameter('n_candidates_1')
t.desc = f"{s_n_candidates_1} <sub></sub>"
t.range = [0, 1, 2, 3, 4, 5, 6, 8]
t.default = 8
t.spec  = f"IE SearchSpace -> nrofCandidates -> aggregationLevel1. the number of PDCCH candidates the UE is configured to monitor for the aggregation level1"

t = Parameter('n_candidates_2')
t.desc = f"{s_n_candidates_2} <sub></sub>"
t.range = [0, 1, 2, 3, 4, 5, 6, 8]
t.default = 8
t.spec  = f"IE SearchSpace -> nrofCandidates -> aggregationLevel2. the number of PDCCH candidates the UE is configured to monitor for the aggregation level2"

t = Parameter('n_candidates_4')
t.desc = f"{s_n_candidates_4} <sub></sub>"
t.range = [0, 1, 2, 3, 4, 5, 6, 8]
t.default = 8
t.spec  = f"IE SearchSpace -> nrofCandidates -> aggregationLevel4. the number of PDCCH candidates the UE is configured to monitor for the aggregation level4"

t = Parameter('n_candidates_8')
t.desc = f"{s_n_candidates_8} <sub></sub>"
t.range = [0, 1, 2, 3, 4, 5, 6, 8]
t.default = 8
t.spec  = f"IE SearchSpace -> nrofCandidates -> aggregationLevel8. the number of PDCCH candidates the UE is configured to monitor for the aggregation level8"

t = Parameter('n_candidates_16')
t.desc = f"{s_n_candidates_16} <sub></sub>"
t.range = [0, 1, 2, 3, 4, 5, 6, 8]
t.default = 8
t.spec  = f"IE SearchSpace -> nrofCandidates -> aggregationLevel16. the number of PDCCH candidates the UE is configured to monitor for the aggregation level16"

t = Sep()

#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    def __init__(self):
        super().__init__()
        self._cc = ["uss", "nsf", "rnti", "p"]
    #############################################################################
    # start add consistency check
    #############################################################################
    def cc(self, ev=None):
        # mu = self.mu.value
        # # self.set_range("scs_coreset", scs_dict[2**mu*15])
        # self.set_range("nsf", range(2**mu*10))
        #
        self.set_range("nci2", 0)

        uss = self.uss.value
        if uss == "CSS":
            self.rnti.hide()
            self.p.hide()
            self.A.hide()
            self.D.hide()
            self.set_range("Y", 0)
            self.nsf.hide()
            # self.Y.hide()
            self.nci.hide()
            self.nci2.show()
            self.set_range("nci", range(1))
            self.set_range("n_candidates_1", [0])
            self.set_range("n_candidates_2", [0])
            self.set_range("n_candidates_4", [4])
            self.set_range("n_candidates_8", [2])
            self.set_range("n_candidates_16", [1])
        else:
            self.rnti.show()
            self.p.show()
            self.A.show()
            self.D.show()
            self.nsf.show()
            # self.Y.show()
            self.nci.show()
            self.nci2.hide()
            self.set_range("nci", range(8))
            #
            self.set_range("A", {0: 39827, 1:39829, 2:39839}[self.p.value % 3])
            self.set_range("D", self.D.default)
            Y = self.rnti.value
            for _ in range(self.nsf.value+1):
                Y = (self.A.value * Y) % self.D.value
            self.set_range("Y", Y)
            self.set_range("n_candidates_1", [0, 1, 2, 3, 4, 5, 6, 8])
            self.set_range("n_candidates_2", [0, 1, 2, 3, 4, 5, 6, 8])
            self.set_range("n_candidates_4", [0, 1, 2, 3, 4, 5, 6, 8])
            self.set_range("n_candidates_8", [0, 1, 2, 3, 4, 5, 6, 8])
            self.set_range("n_candidates_16", [0, 1, 2, 3, 4, 5, 6, 8])
