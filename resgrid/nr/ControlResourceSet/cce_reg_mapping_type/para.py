from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
# import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
# import itertools

sup_sub_template = "<span class='word'>{word}</span><span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"

s_n_symb_coreset = sup_sub_template.format(word="N", sub="symb", sup="CORESET")
s_n_rb_coreset = sup_sub_template.format(word="N", sub="RB", sup="CORESET")
s_n_reg_coreset = sup_sub_template.format(word="N", sub="REG", sup="CORESET")

# _scs_dict = {15: "15kHz", 30: "30kHz", 60: "60kHz", 120: "120kHz", 240: "240kHz"}

_cce_reg_mapping_type_dict = {0: "interleaved", 1: "nonInterleaved"}

#############################################################################
# start add parameter
#############################################################################
t  = Sep()

t = Parameter('n_rb_coreset')
t.desc = f"{s_n_rb_coreset} <sub>38211 7.3.2.2</sub>"
t.range = [24, 48, 96] + [i*6 for i in range(1, 17) if i not in [24//6, 48//6, 96//6]]
t.default = 24
t.spec  = f"resource block in frequency domain. Derived from IE ControlResourceSet -> frequencyDomainResources. 38211 7.3.2.2"


t = Parameter('n_symb_coreset')
t.desc = f"{s_n_symb_coreset} <sub>38211 7.3.2.2</sub>"
t.range = [1, 2, 3]
t.default = 2
t.spec  = f"IE ControlResourceSet -> duration. number of consecutive symbols for CORESET. 38211 7.3.2.2"

t = ParameterDisplay('n_reg_coreset')
t.desc = f"{s_n_reg_coreset} <sub>38211 7.3.2.2</sub>"
t.default = 0
t.spec  = f"the number of REGs in CORESET. 38211 7.3.2.2"

t = Sep()

t = Parameter('cce_reg_mapping_type')
t.desc = "cce-REG-MappingType"
t.dict = _cce_reg_mapping_type_dict
t.range = list(t.dict.values())
t.spec  = f"IE ControlResourceSet -> cce-REG-MappingType. 38211 7.3.2.2"

t = Parameter('reg_bundle_size')
t.desc = "reg-BundleSize (L)"
t.range = [2, 3, 6]
t.spec  = f"IE ControlResourceSet -> interleaved -> reg-BundleSize. 38211 7.3.2.2"

t = Parameter('interleaver_size')
t.desc = "interleaverSize (R)"
t.range = [2, 3, 6]
t.spec  = f"IE ControlResourceSet -> interleaved -> interleaverSize. 38211 7.3.2.2"

t = ParameterDisplay('C')
t.default = 0
t.spec  = f"{s_n_reg_coreset}/(LR). 38211 7.3.2.2"


t = Parameter('shift_index')
t.desc = "shiftIndex (n<sub>shift</sub>)"
t.range = range(274)
t.spec  = f"IE ControlResourceSet -> interleaved -> shiftIndex. 38211 7.3.2.2<br>\
the effective range can be reduced to <b>n<sub>shift</sub> mod ({s_n_reg_coreset} / L)</b>"

t = Sep()

t = ParameterDisplay('n_bundles_coreset')
t.default = 0
t.spec  = f"the number of REG bundles in CORESET = {s_n_reg_coreset} / L"


t = ParameterDisplay('n_bundles_per_cce')
t.default = 0
t.spec  = f"the number of REG bundles per CCE = 6 / L"

t = ParameterDisplay('n_cces_coreset')
t.default = 0
t.spec  = f"the number of CCEs in CORESET"


#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    pass
    #############################################################################
    # start add consistency check
    #############################################################################
    def cc(self):
        nrbs = self.n_rb_coreset.value
        nsymbs = self.n_symb_coreset.value
        self.set_range("n_reg_coreset", nrbs * nsymbs)
        #
        mapping = self.cce_reg_mapping_type.value
        if mapping == 0: # interleaved
            new_bundle_size_range = [2, 6] if nsymbs == 1 else [nsymbs, 6]
            self.set_range("reg_bundle_size", new_bundle_size_range)
            #
            self.interleaver_size.show()
            nregs = self.n_reg_coreset.value
            L = self.reg_bundle_size.value
            new_r_range = []
            for R in [2, 3, 6]:
                if nregs % L == 0 and (nregs // L) % R == 0:
                    if R not in new_r_range:
                        new_r_range.append(R)
            self.set_range("interleaver_size", sorted(new_r_range))
            #
            R = self.interleaver_size.value
            self.set_range("C", nregs // (L*R))
            #
            self.shift_index.show()
            self.set_range("shift_index", range(nregs // L))
        else:
            self.set_range("reg_bundle_size", [6])
            self.interleaver_size.hide()
            self.C.hide()
            self.shift_index.hide()
        self.set_range("n_bundles_coreset", self.n_reg_coreset.value // self.reg_bundle_size.value)
        self.set_range("n_bundles_per_cce", 6 // self.reg_bundle_size.value)
        self.set_range("n_cces_coreset", self.n_bundles_coreset.value // self.n_bundles_per_cce.value)
        self.cal_reg_to_cce_map()

    def cce_reg_mapping_type_change(self, e=None):
        self.cc()

    def reg_bundle_size_change(self, e=None):
        self.cc()

    def interleaver_size_change(self, e=None):
        self.cc()

    def shift_index_change(self, e=None):
        self.cc()

    def n_rb_coreset_change(self, e=None):
        self.cc()

    def n_symb_coreset_change(self, e=None):
        self.cc()

    def cal_reg_to_cce_map(self):
        mapping = self.cce_reg_mapping_type.value
        n_cces_coreset = self.n_cces_coreset.value
        L = self.reg_bundle_size.value
        R = self.interleaver_size.value
        nshift = self.shift_index.value
        n_reg_coreset = self.n_reg_coreset.value
        C = n_reg_coreset // (L * R)

        cce_to_x = dict()
        x_to_cce = dict()
        x_to_bundle = x_to_fx = dict()  # x to bundle
        self.cce_to_bundle = cce_to_bundle = dict()
        self.bundle_to_cce = bundle_to_cce = dict()

        for j in range(n_cces_coreset):
            cce_to_x[j] = []
            for i in range(6//L):
                x = 6 * j // L + i
                x_to_cce[x] = j
                cce_to_x[j].append(x)
        if mapping == 0:
            for x in x_to_cce.keys():
                c, r = divmod(x, R)
                fx = (r * C + c + nshift) % (n_reg_coreset // L)
                x_to_fx[x] = fx
        else:
            for x in x_to_cce.keys():
                x_to_fx[x] = x
        for x in x_to_cce.keys():
            bundle = x_to_bundle[x]
            cce = x_to_cce[x]
            bundle_to_cce[bundle] = cce
        for cce, k in cce_to_x.items():
            cce_to_bundle[cce] = [x_to_bundle[x] for x in k]
    
    def reg_to_cce(self, reg):
        bundle = reg // self.reg_bundle_size.value
        return self.bundle_to_cce[bundle]
