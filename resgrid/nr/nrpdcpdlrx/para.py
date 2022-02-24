from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

#############################################################################
# start add parameter
#############################################################################
t = Sep()

t = Parameter('pdcp_sn_size_dl')
t.desc  = 'pdcp-SN-SizeDL'
t.spec  = '38.331 PDCP-Config -> drb -> pdcp-SN-SizeDL. Use a small value for illustration.'
t.range = [3, 4, 5]
t.default = 4

t = Parameter('hfn_size')
t.desc  = 'HFN Size (bits)'
t.spec  = 'number of bits for HFN. Use a small value for illustration.'
t.range = [1, 2, 3, 4]
t.default = 1

t = ParameterDisplay('window_size') 
t.desc  = 'window_size'
t.spec  = '38.323 7.2. half of SN space'

t = Parameter('out_of_order_delivery')

t.desc  = 'outOfOrderDelivery'
t.range = [False, True]
# t.dict = {"False": 0, "True": 1}
t.spec  = '38.331 PDCP-Config -> drb -> outOfOrderDelivery'

t = Sep()

t = Parameter('run_mode')
t.desc  = 'run mode'
t.dict = {"auto": 0, "manual": 1}
t.range = list(t.dict.keys())
t.spec  = ''

t = Parameter('refresh_interval')
t.desc  = 'refresh interval (ms)'
t.range = [50, 100, 200, 400, 500, 1000, 2000]
t.default = 200
t.spec  = 'valid when run mode is auto'

t = Sep()


class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def pdcp_sn_size_dl_change(self, event):
        m = self.mvalue
        self.set_range('window_size', 2 ** (m-1))

    def run_mode_change(self, event):
        m = self.mvalue
        if m == 0:
            self.set_range("refresh_interval", [50, 100, 200, 400, 500, 1000, 2000])
        else:
            self.set_range("refresh_interval", [0])
