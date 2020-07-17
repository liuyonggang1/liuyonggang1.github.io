##########################################################################################################################################
from browser import document, window, load
from browser.html import TABLE, TR, TD, SPAN, DIV, A, B, H3, SELECT, OPTION, BR, HR, INPUT, TH, BUTTON
import ready

col_flag = 0
col_pad = 1
col_level = 2
col_ie = 3
col_udf = 4
col_vrange = 5
col_need = 6
col_desc = 7
col_ch5link = 8

dtop = document['top']
doutput = document['output']
document.body <= DIV(id='dindex')
dindex = document['dindex']

need_str = """D: Default
C: Cond
O: OPTIONAL
ON: No action
OR/R: Release
OP/S: Specified
M: Maintain
N: No action (one-shot)
"""

def load_json():
    stem = get_stem()
    json = f'{stem}.json'
    with open(json, encoding='utf-8') as f:
        s = f.read()
    o = window.JSON.parse(s)
    return o

def get_stem():
    return window.location.pathname.split('/')[-1].replace('.html', '')
    
def get_protocol_name():
    stem = get_stem()
    d = {'36331':'', '36413':'S1', '36423': 'X2', '36443':'M2', '36444':'M3', '36455': 'LP',
         '38331':'NR',  '38413':'NG', '38423': 'Xn', '38463':'E1', '38473':'F1'}
    return d[stem]

   
class Data:
    def __init__(self):
        self.o = load_json()
        self.asn1html = f'{get_stem()}_asn1.html'
        self.ch5html = f'{get_stem()}_ch5.html'
        self.release = self.o.release
        self.udf_list = self.o.udf_list
        self.dct = self.o.dct
        self.nrows = self.o.nrows
        self._map2 = self.o.dct
        self.toc = self.get_toc()
        self._expand_aoa_dct = dict()
        
    def body_hashchange(self, e=None):
        anchor = self.anchor
        if anchor == '':
            self.create_index()
        elif anchor == 'search':
            self.create_search()
        elif anchor in self._map2:
            t0 = window.Date.now()
            self.create_tree()
            t1 = window.Date.now()
            print(self.anchor, t1-t0, 'ms')
    
    @property
    def anchor(self):
        anchor = window.location.hash.replace('#', '')
        anchor = window.decodeURI(anchor)
        return anchor
        
    def get_toc(self):
        width = max([len(row[0].split('\t')[0]) for row in self.o.toc if row[1] == 0])
        result = []
        for row in self.o.toc:
            name, level = row
            if level == 0:
                sid, sname = name.split('\t')
                span = SPAN(sid.strip())
                span.style.width = f"{width}ch"
                span.style.display = 'inline-block'
                span2 = SPAN(sname.strip())
                result.append(['', level, span+span2])
            else:
                result.append(['', level, name])
        for p, n in zip(result[:-1], result[1:]):
            pl = p[1]
            nl = n[1]
            if pl == nl - 1:
                p[0] = '-'
        return result

    def get_short_title(self):
        names = [row[0] for row in self.o.toc if row[1]]
        if self.anchor in names:
            name = self.anchor
            lst = name.split('-')
            if len(lst) > 1 and lst[-1][0] == 'r' and lst[-1][1:].isdigit():
                name = '-'.join(lst[:-1])
            if name.startswith('SystemInformationBlockType'):
                name = name.replace('SystemInformationBlockType', 'SIB')
            if name.startswith('RRCConnection'):
                name = name[len('RRCConnection'):]
            return name
        else:
            return self.anchor
    
        
    def get_aoa(self, udf=None):
        if udf is None:
            udf = self.anchor
        return self._map2[udf]

    def get_expand_aoa(self, udf=None):
        if udf is None:
            udf = self.anchor
        return self._expand_aoa_dct.get(udf, None)
        
    def get_nrows(self, udf=None):
        if udf is None:
            udf = self.anchor
        return self.nrows[udf]
        
    def create_index(self):
        dtop.clear()
        doutput.clear()
        #
        document.title = f'{self.release}'
        dtop <= SPAN(f'{self.release}')
        dtop <= SPAN(A('Search', href=f'#search'))
        dtop <= SPAN(A('ASN1', href=self.asn1html))
        #
        dindex.style.display = ''
        if dindex.html:
            return
        table = TABLE(Class='toctable')
        for i, row in enumerate(self.toc):
            flag, level, name = row
            tr = TR()
            tr <= TD(flag, Class='flag')
            tr <= TD(level)
            if level:
                td = TD(A(name, href=f'#{name}'))
            else:
                td = TD(name)
            tr <= td
            set_indent(td, level)
            tr <= TD(i)
            table <= tr
        dindex <= table
        ready.ready_table(table)

    def creat_head_row(self, table):
        head = ["", "", 'IE', 'Need', 'Define', 'Range', 'Description', '']
        table <= TR([TD(B(v)) for v in head])
        table.rows[0].cells[3].title = need_str
        table.rows[0].cells[3].style.color = 'blue'
        table.rows[0].cells[6].className = 'desc'
        
    def create_tree(self):
        dindex.style.display = 'none'
        dtop.clear()
        doutput.clear()
        aoa = self.get_aoa()
        #
        document.title = f'{get_protocol_name()} {self.anchor}'
        document.title = f'{get_protocol_name()} {self.get_short_title()}'.strip()
        dtop <= SPAN(self.release)
        dtop <= SPAN(A('Index', href='#'))
        dtop <= SPAN(A('Search', href=f'#search'))
        dtop <= SPAN(A('ASN1', href=f'{self.asn1html}#{self.anchor}'))
        #
        b = BUTTON('copy tree')
        b.bind('click', ready.copy_tree)
        dtop <= SPAN(b)
        #
        b = BUTTON('export xlsx')
        b.bind('click', self.export_xlsx)
        dtop <= SPAN(b)
        #
        b = BUTTON('table view')
        b.bind('click', self.change_view)
        dtop <= SPAN(b)
        #
        b = BUTTON('Popup On')
        b.bind('click', ready.button_popup)
        dtop <= SPAN(b)
        b.style.backgroundColor = 'lightgreen'
        #
        t = int((self.get_nrows()/1000) * 2 + 1 )
        t = f'{t}s'
        b = BUTTON(f'expand all ({self.get_nrows()} rows, need {t})')
        b.bind('click', self.click_expand_all)
        dtop <= SPAN(b)
        #
        b = BUTTON('Hidden Prefix')
        b.bind('click', self.click_hidden_prefix)
        dtop <= SPAN(b)
        #
        dtop <= SPAN(f'{self.anchor}')
        #
        table = TABLE(Class='asn1tree', tview='tree')
        self.creat_head_row(table)
        for row in aoa:
            table <= self.create_tree_tr(row)
        doutput <= table
        for tr in table.rows:
            tr.cells[-1].html = tr.rowIndex
        ready.ready_table(table)

    def click_expand_all(self, event):
        b = event.target
        table = ready.get_table()
        if b.html.startswith('expand all'):
            b.html = 'init view'
            t0 = window.Date.now()
            table.html = ''
            self.creat_head_row(table)
            result = self.get_expand_aoa()
            if result is None:
                t2 = window.Date.now()
                result = self.create_expand_aoa()
                t3 = window.Date.now()
                print(f'create_expand_aoa {t3-t2}ms to expand {self.anchor}')
            for row in result:
                table <= self.create_tree_tr(row)
            if table.tview == 'table':
                for span in table.select('.iepad'):
                    span.html = span.tablepad
                table.select('.iepad')[0].html = ''
            t1 = window.Date.now()            
            print(f'create_expand_table {t1-t0}ms to expand {self.anchor}')
            for tr in table.rows:
                tr.cells[-1].html = tr.rowIndex
            ready.create_level_div(table)
            ready.set_width_for_asn1_table(table)            
        else:
            self.create_tree()

    def create_expand_aoa(self):
        result = self.get_aoa()[::]
        i = 1
        while i < len(result):
            row = result[i]        
            udf = row[col_udf]
            if udf != 'RRCReconfiguration' and row[col_flag] == '+':
                aoa = self.get_remain(udf)
                pad = row[col_pad].replace(r"└", r" ").replace(r"├", r"│").replace(r"─", r" ")
                level = row[col_level]
                idx = i+1
                for ra in aoa[::-1]:
                    tmp = ra[::]
                    tmp[col_pad] = pad + tmp[col_pad]
                    tmp[col_level] = level + tmp[col_level]
                    result.insert(idx, tmp)
            i += 1
        #
        for i in range(len(result)-1):
            if row[col_udf] == 'RRCReconfiguration':
                continue
            if result[i][col_level] == result[i+1][col_level] - 1:
                result[i][col_flag] = '-'
            else:
                result[i][col_flag] = ''
        result[-1][col_flag] = ''
        self._expand_aoa_dct[self.anchor] = result
        return result

    # def expand_all(self, table):
        # tr = table.rows[1]
        # while tr is not None:
            # flag = tr.cells[0].html
            # if flag == '+' and tr.udf:
                # self.append_child(tr, refresh_level_list=False)
            # tr = tr.nextElementSibling

    def append_child(self, tr):
        aoa = self.get_remain(ready.get_udf(tr))
        table = tr.parent
        if aoa:
            start_level = ready.get_level(tr)
            pad_prefix = ready.get_treepad(tr)
            pad_prefix = pad_prefix.replace(r"└", r" ").replace(r"├", r"│").replace(r"─", r" ")
            cur = tr
            for row in aoa:
                new = self.create_tree_tr(row, pad_prefix, start_level)
                if table.tview == 'table':
                    span = new.select('.iepad')[0]
                    span.html = span.tablepad
                cur.insertAdjacentElement("afterend", new)
                cur = new
            ready.set_flag(tr, '-')
            ready.create_level_div(table)
            for tr in table.rows:
                tr.cells[-1].html = tr.rowIndex
            ready.create_level_div(table)
            # ready.set_width_for_clip_col(table)
            ready.set_width_for_asn1_table(table)
        else:
            ready.set_flag(tr, '')
            
    def get_remain(self, udf):
        aoa = self.get_aoa(udf)
        next_udf = aoa[0][col_udf]  # col_udf
        if next_udf:
            return self.get_remain(next_udf)
        else:
            return aoa[1:]
        
    def create_tree_tr(self, row, pad_prefix='', start_level=0):
        flag, pad, level, ie, udf, vrange, need, desc, ch5link = row
        pad = pad_prefix + pad
        level += start_level
        tr = TR()
        tr <= TD(flag, Class='flag')
        tr <= TD(level)
        tr <= TD(SPAN(pad, Class='iepad', treepad=pad, tablepad='>'*level+' ')+SPAN(ie, Class='ie', desc=ch5link))
        tr <= TD(need)
        if udf:
            tr <= TD(A(udf, href=f'#{udf}'))
        else:
            tr <= TD()
        tr <= TD(vrange, Class='vrange')
        tr <= TD(desc, Class='desc')
        tr <= TD()
        return tr

    def change_view(self, event):
        b = event.target
        table = ready.get_table()
        if table.tview == 'tree':   # change to table view
            table.tview = 'table'
            b.html = 'tree view'
            for span in document.select('.iepad'):
                span.html = span.tablepad
            document.select('.iepad')[0].html = ''
        else:                       # change to tree view
            table.tview = 'tree'
            b.html = 'table view'
            for span in document.select('.iepad'):
                span.html = span.treepad
        ready.set_width_for_asn1_table(table)
        
    def create_search(self):
        dindex.style.display = 'none'
        dtop.clear()
        doutput.clear()
        #
        document.title = f'{self.release} Search'
        dtop <= SPAN(f'{self.release}')
        dtop <= SPAN(A('Index', href='#'))
        #
        dsearch = DIV()
        doutput <= dsearch
        dsearch.style.paddingLeft = '20px'
        chars = sorted({item[0].upper() for item in self.udf_list})
        div = DIV()
        div.style.marginBottom = '10px'
        dsearch <= div
        for c in chars:
            span = SPAN(c)
            span.style.color = 'blue'
            span.style.textDecoration = 'underline'
            span.style.padding = '2px 5px 10px 5px'
            span.style.cursor = 'pointer'
            span.onclick = self.click_one
            div <= span
        #
        input = INPUT(type="text")
        input.title = 'Search'
        input.style.width = '40ch'
        input.style.marginBottom = '10px'
        dsearch <= input
        input.bind('input', self.input_change)
        #
        dsearch <= DIV(id='searchresult')
    
    def click_one(self, event):
        dout = document['searchresult']
        dout.clear()
        c = event.target.html
        for item in self.udf_list:
            if item[0].upper() == c:
                dout <= A(item, href=f'#{item}')
                dout <= BR()
        
    def input_change(self, event):
        dout = document['searchresult']
        dout.clear()
        text = event.target.value
        if len(text) <= 1:
            return
        else:
            result = [udf for udf in self.udf_list if text.lower() in udf.lower()]
            if result:
                for udf in result:
                    dout <= A(udf, href=f'#{udf}')
                    dout <= BR()
            else:
                dout <= B('No match')

    def click_hidden_prefix(self, e):
        table = document.select('.asn1tree')[0]
        b = e.target
        if b.html == 'Hidden Prefix':
            b.html = 'Show Prefix'
            table.hiddeniepad = 'y'
        else:
            b.html = 'Hidden Prefix'
            table.removeAttribute('hiddeniepad')
            
                
    def export_xlsx(self, event):
        aoa = self.get_expand_aoa()
        if aoa is None:
            aoa = self.create_expand_aoa()
        head = ['', '', 'IE', 'Need', 'Type', 'Range', 'Description', '']
        t =[head]
        for row in aoa:
            flag, pad, level, ie, udf, vrange, need, desc, ch5link = row
            desc = desc.replace('<b>', '').replace('</b>', '').replace('<br>', '\n')
            try:
                desc = desc[:desc.index('<a ')]
            except:
                pass
            t.append([flag, level, '>'*level+' '+ie, need, udf, vrange, desc.strip(), ' '])
        xlsx_name = f'{self.anchor}.xlsx'
        sheet_name = self.anchor[:31]
        ready.export_xlsx(t, xlsx_name, sheet_name)
        
def set_indent(td, level):
    indent = int(level)
    if indent:
        indent = f'{indent*2}em'
        td.style.paddingLeft = indent

        
#################################################################################
# main
#################################################################################       
ready.load_js('xlsx.js')
g = Data()
window.onhashchange = g.body_hashchange
g.body_hashchange()
window.g = g

