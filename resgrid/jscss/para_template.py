from parabase import Parameter, ConfigBase, ParameterDisplay
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}
import itertools

#############################################################################
# start add parameter
#############################################################################
t = Parameter('row')
t.range = list(range(1, 19))
t.spec  = "38.211 table 7.4.1.5.3-1"

#############################################################################
# end add parameter
#############################################################################


class Config(ConfigBase):
    #############################################################################
    # start add consistency check
    #############################################################################
    def density_change(self, event):
        # m = '_'.join(sys._getframe().f_code.co_name.split('_')[3:-2])  # m = para name
        # m = getattr(getattr(self, m), 'value')
        m = self._get_value()
        new_range = [''] if m in (1, 3) else ["evenPRBs", "oddPRBs"]
        self.set_range('density_dot5', new_range)
