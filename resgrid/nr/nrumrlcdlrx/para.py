from parabase import Parameter, ConfigBase, ParameterDisplay, ParameterInput, Sep
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

#############################################################################
# start add parameter
#############################################################################
t = Sep()

t = Parameter('rlc_sn_size_dl')
t.desc  = 'sn-FieldLength'
t.spec  = '38.331 RLC-Config -> um-Bi-Directional -> dl-UM-RLC -> sn-FieldLength. Use a small value for illustration.'
t.range = [4, 5, 6]
t.default = 6

t = ParameterDisplay('window_size') 
t.desc  = 'window_size'
t.spec  = '38.322 7.2. half of SN space'

t = Parameter('possibility')
t.desc  = 'possibility'
t.range = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
t.default = 5
t.spec  = """For determining the result of no missing byte segment of the RLC SDU associated with SN = RX_Next_Reassembly before the last byte of all received segments of this RLC SDU.
<br>Randomly generate an int in [0, 9]. result = random < this value. 0: always False, 9: always True. 5: half-to-half.
<br>This is related to t_reassemebly."""

t = Sep()

t = Parameter('refresh_interval')
t.desc  = 'refresh interval (ms)'
t.range = [50, 100, 200, 500, 1000, 2000, 3000]
t.default = 1000
t.spec  = 'valid when run mode is auto'

t = Sep()


class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def rlc_sn_size_dl_change(self, event):
        m = self.mvalue
        self.set_range('window_size', 2 ** (m-1))

    def run_mode_change(self, event):
        m = self.mvalue
        if m == 0:
            self.set_range("refresh_interval", [50, 100, 200, 400, 500, 1000, 2000])
        else:
            self.set_range("refresh_interval", [0])
