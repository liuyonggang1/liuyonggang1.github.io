from parabase import Parameter, ConfigBase, ParameterDisplay
# import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}

#############################################################################
# start add parameter
#############################################################################
t = Parameter("codebookMode")
t.range = [1, 2]
t.spec  = '38331: CodebookConfig->codebookType->type1->codebookMode'

t = Parameter('pcsirs')
t.desc  = 'P<sub>CSI-RS</sub>'
t.range = [4, 8, 12, 16, 24, 32]
t.spec  = '38.214 Table 5.2.2.2.1-2. The number of CSI-RS ports.'

t = Parameter('n1n2')
t.desc  = 'N<sub>1</sub>,N<sub>2</sub>'
t.range = [""]
t.spec  = '38331: CodebookConfig->codebookType->type1->subType->typeI-SinglePanel->nrOfAntennaPorts->moreThanTwo->n1-n2'

t = ParameterDisplay('o1o2')
t.desc  = 'O<sub>1</sub>,O<sub>2</sub>'
t.spec  = '38.214 Table 5.2.2.2.1-2'

t = Parameter('nlayers')
t.desc  = 'layers'
t.range = [1,2,3,4,5,6,7,8]
t.spec  = 'number of layers'

#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def pcsirs_change(self, event):
        m = self.mvalue
        if m == 4:
            new_range = ["2,1"]
        elif m == 8:
            new_range = ["2,2", "4,1"]
        elif m == 12:
            new_range = ["3,2", "6,1"]
        elif m == 16:
            new_range = ["4,2", "8,1"]
        elif m == 24:
            new_range = ["4,3", "6,2", "12,1"]
        elif m == 32:
            new_range = ["4,4", "8,2", "16,1"]
        self.set_range('n1n2', new_range)
        self.n1n2_change(None)
        if m == 4:
            new_range = range(1, 5)
        else:
            new_range = range(1, 9)
        self.set_range('nlayers', new_range)

    def n1n2_change(self, event):
        m = self.mvalue
        new_range = "4,1" if m.endswith(",1") else "4,4"
        self.set_range('o1o2', new_range)
