##########################################################################################################################################
from browser import document, window, load
from browser.html import TABLE, TR, TD, SPAN, DIV, A, B, H3, SELECT, OPTION, BR, HR, INPUT, TH, BUTTON
import ready

col_flag = 0
col_level = 1
col_ie = 2
col_desc = 6
dtop = document['top']
doutput = document['output']
document.body <= DIV(id='dindex')
dindex = document['dindex']

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
    d = {'36331':'LTE', '36413':'S1', '36423': 'X2', '36443':'M2', '36444':'M3', '36455': 'LP',
         '38331':'NR',  '38413':'NG', '38423': 'Xn', '38463':'E1', '38473':'F1'}
    try:
        return d[stem]
    except:
        return stem     #'E2AP': 'E2AP', 'E2SM_gNB_X2':'E2SM_gNB_X2'
    
class Data:
    def __init__(self):
        self.o = load_json()
        self.release = self.o.release
        self.section_list = self.o.section_list
        self._map = {s.id:s for s in self.section_list}
        self._map2 = [s.id for s in self.section_list if s.aoa]
        self.toc = self.get_toc()
        
    def body_hashchange(self, e=None):
        anchor = self.anchor
        if anchor == '':
            self.create_index()
        elif anchor in self._map2:
            self.create_table()
    
    @property
    def anchor(self):
        anchor = window.location.hash.replace('#', '')
        anchor = window.decodeURI(anchor)
        return anchor
        
    def create_prev_next(self):
        sid = self.anchor
        try:
            i = self._map2.index(sid)
            if i-1 >= 0:
                prev = self._map2[i-1]
                dtop <= SPAN(A(f'Prev {prev}', href=f'#{prev}', title=self.get_section(prev).name))
            if i+1 < len(self._map2):
                next = self._map2[i+1]
                dtop <= SPAN(A(f'Next {next}', href=f'#{next}', title=self.get_section(next).name))
        except:
            return
        
    def get_toc(self):
        #
        result1 = dict()
        for s in self.section_list:
            level = s.id.count('.')+1
            try:
                result1[level] = max(result1[level], len(s.id))
            except:
                result1[level] = len(s.id)
        for k, v in result1.items():
            result1[k] = v + 2
        result = []
        for s in self.section_list:
            level = s.id.count('.')+1
            width = result1[level]
            result.append(['', level, s.id, width, s.name])
        for p, n in zip(result[:-1], result[1:]):
            pl = p[1]
            nl = n[1]
            if pl == nl - 1:
                p[0] = '-'
        return result
    
    def get_section(self, sid=None):
        if sid is None:
            sid = self.anchor
        return self._map[sid]
        
    def create_index(self):
        dtop.clear()
        doutput.clear()
        #
        document.title = f'{self.release}'
        dtop <= SPAN(f'{self.release}')
        #
        dindex.style.display = ''
        if dindex.html:
            return
        table = TABLE(Class='toctable')
        for i, row in enumerate(self.toc):
            flag, level, sid, width, sname = row
            tr = TR()
            tr <= TD(flag, Class='flag')
            tr <= TD(level)
            span = SPAN(sid)
            span.style.width = f"{width}ch"
            span.style.display = 'inline-block'
            if self.get_section(sid).aoa:
                td = TD(span+A(sname, href=f'#{sid}'))
            else:
                td = TD(span+sname)
            tr <= td
            set_indent(td, level-2)
            tr <= TD(i)
            table <= tr
        dindex <= table
        ready.ready_table(table)

    def create_table(self):
        dindex.style.display = 'none'
        dtop.clear()
        doutput.clear()
        section = self.get_section()
        aoa = section.aoa
        #
        document.title = f'{get_protocol_name()} {section.name}'
        dtop <= SPAN(self.release)
        dtop <= SPAN(A('Index', href='#'))
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
        dtop <= SPAN(f'{section.id} {section.name}')
        self.create_prev_next()
        #
        table = TABLE(Class='asn1tree', tview='tree', core='')
        head = ["", "", 'IE', 'Need', 'Refer', 'Type', 'Description', 'Crit', 'Assign']
        table <= TR([TD(B(v)) for v in head])
        table.rows[0].cells[6].className = 'desc'
        #
        for row in aoa:
            flag, level, ie, need, udf, vrange, desc, crit, assign = row
            pad, ie = get_pad_and_ie(ie)
            tr = TR()
            tr <= TD(flag, Class='flag')
            tr <= TD(level)
            hasdesc = 'hasdesc' if desc else ''
            tr <= TD(SPAN(pad, Class='iepad', treepad=pad, tablepad='>'*level+' ')+SPAN(ie, Class='ie', desc=hasdesc))
            tr <= TD(need)
            if udf:
                tr <= TD(A(udf, href=f'#{udf}'))
            else:
                tr <= TD()
            tr <= TD(vrange, Class='vrange')
            tr <= TD(desc, Class='desc')
            tr <= TD(crit)
            tr <= TD(assign)
            table <= tr
        for tr in table.rows:
            tr <= TD(tr.rowIndex)
        doutput <= table
        ready.ready_table(table)

    def change_view(self, event):
        b = event.target
        table = document.select('.asn1tree')[0]
        if table.tview == 'tree':
            # change to table view
            table.tview = 'table'
            b.html = 'tree view'
            for span in document.select('.iepad'):
                span.html = span.tablepad
            document.select('.iepad')[0].html = ''
        else:
            # change to tree view
            table.tview = 'tree'
            b.html = 'table view'
            for span in document.select('.iepad'):
                span.html = span.treepad
        ready.set_width_for_asn1_table(table)
        
    def export_xlsx(self, event):
        section = self.get_section()
        aoa = section.aoa
        head = ['', '', 'IE', 'Need', 'Refer', 'Type', 'Description', 'Criticality', 'Assigned']
        t =[head]
        for row in aoa:
            flag, level, ie, need, refer, vrange, desc, crit, assign = row
            ie = '>'* level + ' ' + ie.replace('├', '').replace('─', '').replace('└', '').replace('│', '').strip()
            desc = desc.replace('<b>', '').replace('</b>', '').replace('<br>', '\n').strip()
            t.append([flag, level, ie.strip(), need, refer, vrange, desc, crit, assign])
        xlsx_name = f'{section.id}-{section.name}.xlsx'
        sheet_name = section.name[:31]
        ready.export_xlsx(t, xlsx_name, sheet_name)
        
def set_indent(td, level):
    indent = int(level)
    if indent:
        indent = f'{indent*2}em'
        td.style.paddingLeft = indent

def get_pad_and_ie(text):
    for i, c in enumerate(text):
        if c.lower() in 'abcdefghijklmnopqrstuvwxyz':
            break
    pad, ie = text[:i], text[i:]
    a = r" └─"  # last
    b = r" ├─"  # middle    
    c = r" │ "  # up
    d = r"   "  # down    
    
    a1 = r"└─"  # last
    b1 = r"├─"  # middle    
    c1 = r"│ "  # up
    d1 = r"  "  # down    
    pad = pad.replace(a, a1).replace(b, b1).replace(c, c1).replace(d, d1)
    return pad, ie
        
#################################################################################
# main
#################################################################################       
ready.load_js('xlsx.full.min.js')
g = Data()
window.onhashchange = g.body_hashchange
g.body_hashchange()
