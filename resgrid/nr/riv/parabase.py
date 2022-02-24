from browser import document
from browser.html import *
import sys  # sys._getframe().f_code.co_name = {File}_{Class}_{digit}_{function}_{digit}

_plist = []

##############################################################################################
# For Enumeration
##############################################################################################
class Parameter:  
    def __init__(self, pid):
        self.id = pid
        self.desc = pid        
        self._range = None
        self.dict = {}   # value: display_value
        self.spec = ""
        self.default = None
        self.desc_td = None
        self.range_td = None
        self.spec_td = None
        self._tr = None
        _plist.append(self)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, new):
        update = self._range is not None
        self._range = new
        for i in self.range:
            if i not in self.dict:
                self.dict[i] = str(i)
        if update:
            cur = self.value
            self.select = SELECT([OPTION(self.dict[i]) for i in new])
            if cur in new:
                self.select.selectedIndex = new.index(cur)
            self.range_td.clear()
            self.range_td <= self.select

    @property
    def tr(self):
        if self._tr is not None:
            return self._tr
        self.select = SELECT([OPTION(i) for i in self.range])
        if self.default is not None:
            self.select.selectedIndex = self.range.index(self.default)
        self.range_td = TD(self.select, id=self.id)
        self.desc_td = TD(self.desc)
        self.spec_td = TD(self.spec)
        self._tr = TR([self.desc_td, self.range_td, self.spec_td])
        return self._tr

    @property
    def disp_value(self):
        return self.select.options[self.select.selectedIndex].value

    @property
    def value(self):
        cur_disp = self.disp_value
        for v, disp in self.dict.items():
            if disp == cur_disp:
                return v
        # return self.dict[self.disp_value]
        
    def hide(self):
        self._tr.style.display = "none"

    def show(self):
        self._tr.style.display = ""

##############################################################################################
# For String
##############################################################################################
class ParameterInput:
    def __init__(self, pid):
        self.id = pid
        self.desc = pid        
        self.spec = ""
        self.default = ''
        self.desc_td = None
        self.range_td = None
        self.spec_td = None
        self._tr = None
        self.type = None
        _plist.append(self)

    @property
    def range(self):
        return None

    @range.setter
    def range(self, new):
        self.input.value = str(new)

    @property
    def tr(self):
        if self._tr is not None:
            return self._tr
        style = {'width':'130px'}
        self.input = INPUT(value=self.default, type='text', style=style, id=self.id)
        self.range_td = TD(self.input)
        self.desc_td = TD(self.desc)
        self.spec_td = TD(self.spec)
        self._tr = TR([self.desc_td, self.range_td, self.spec_td])
        return self._tr

    @property
    def value(self):
        if self.type is None:
            self.type = type(self.default)
        return self.type(self.input.value)

    def hide(self):
        self._tr.style.display = "none"

    def show(self):
        self._tr.style.display = ""


##############################################################################################
# For Display
##############################################################################################
class ParameterDisplay:
    def __init__(self, pid):
        self.id = pid
        self.desc = pid        
        self.dict = {}
        self.spec = ""
        self.default = ''
        self.desc_td = None
        self.range_td = None
        self.spec_td = None
        self._tr = None
        _plist.append(self)

    @property
    def range(self):
        return None

    @range.setter
    def range(self, new):
        for v, disp in self.dict.items():
            if new == v:
                self.range_td.html = disp
                return
        self.dict[new] = str(new)
        self.range_td.html = str(new)

    @property
    def tr(self):
        if self._tr is not None:
            return self._tr
        # if self.default not in self.dict:
        #     self.dict[self.default] = str(self.default)
        # self.dict[str(self.default)] = self.default
        # self.range_td = TD(self.dict[self.default])
        self.range_td = TD(self.default)
        self.desc_td = TD(self.desc)
        self.spec_td = TD(self.spec)
        self._tr = TR([self.desc_td, self.range_td, self.spec_td])
        return self._tr

    @property
    def value(self):
        cur_disp = self.range_td.html
        for v, disp in self.dict.items():
            if disp == cur_disp:
                return v
        # return self.dict[self.range_td.html]

    def hide(self):
        self._tr.style.display = "none"

    def show(self):
        self._tr.style.display = ""

##############################################################################################
# For Sep
##############################################################################################
class Sep:
    def __init__(self):
        self.id = "sep"
        self.value = None
        _plist.append(self)
        # 
        style = {'background':'lightblue'}
        td = TD(style=style)
        td.colSpan = 3
        self.tr = TR(td)


##############################################################################################
# 
##############################################################################################
class ConfigBase:
    def __init__(self):
        self.parameter_list = _plist
        for p in self.parameter_list:
            setattr(self, p.id, p)
        heads = ['Desc', 'Input', '3GPP']
        head_tds = [TD(s, Class='head-row') for s in heads]
        head_tr = [TR(head_tds)]
        caption = CAPTION('', style={'color':'red'})
        trs = [caption] + head_tr + [p.tr for p in self.parameter_list]
        self.table = TABLE(trs)

    def start(self, main):
        document['zone-input'].clear()
        document['zone-input'] <= self.table
        document['zone-input'] <= BUTTON('show result', id='main')
        self.bind_onchange()
        document['main'].bind('click', main)

    def bind_onchange(self):
        for p in self.parameter_list:
            func_name = p.id + '_change'
            if hasattr(self, func_name):
                document[p.id].bind('change', getattr(self, func_name))
        for p in self.parameter_list:
            func_name = p.id + '_change'
            if hasattr(self, func_name):
                getattr(self, func_name)(None)

    # def _get_value(self):
        # m = '_'.join(sys._getframe().f_back.f_code.co_name.split('_')[3:-2])  # m = para name. para_Config_7_n1n2_change_9
        # return getattr(getattr(self, m), 'value')

    @property
    def mvalue(self):
        # print("mvalue", sys._getframe().f_back.f_code.co_name)
        m = '_'.join(sys._getframe().f_back.f_code.co_name.split('_')[3:-2])  # m = para name. para_Config_7_n1n2_change_9
        return getattr(getattr(self, m), 'value')

    def set_range(self, name, new_range):
        getattr(self, name).range = new_range

    def copy_cfg(self, obj):
        for p in self.parameter_list:
            setattr(obj, p.id, p.value)

    def get_cfg(self):
        obj = type("", (), {})
        for p in self.parameter_list:
            setattr(obj, p.id, p.value)
        return obj

    def print_values(self):
        for p in self.parameter_list:
            print(p.id, p.value, type(p.value))

