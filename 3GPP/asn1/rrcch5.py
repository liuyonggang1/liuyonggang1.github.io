##########################################################################################################################################
from browser import document, window, load
from browser.html import TABLE, TR, TD, SPAN, DIV, A, B, H3, SELECT, OPTION, BR, HR, INPUT
import ready

col_flag = 0
col_level = 1
col_text = 2
dtop = document['top']
doutput = document['output']
document.body <= DIV(id='dindex')
dindex = document['dindex']


def load_json():
    stem = window.location.pathname.split('/')[-1].replace('.html', '')
    json = f'{stem}.json'
    with open(json, encoding='utf-8') as f:
        s = f.read()
    o = window.JSON.parse(s)
    return o

class Data:
    def __init__(self):
        self.o = load_json()
        self.release = self.o.release + ' CH5'
        self.section_list = self.o.section_list
        self.ies = self.o.ies
        self._map = {s.id:s for s in self.section_list}
        self._map2 = [s.id for s in self.section_list if s.aoa]
        self.toc = self.get_toc()
        self.chars = sorted({ie[0].upper() for ie in self.ies})
        
    def body_hashchange(self, e=None):
        anchor = self.anchor
        if anchor == '':
            self.create_index()
        elif anchor ==  "search":
            self.create_search()
        elif anchor in self._map2:
            self.create_table()
        else:
            self.create_search_result()
    
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
        dtop <= SPAN(A('Search', href=f'#search'))
        dindex.style.display = ''
        if dindex.html:
            return        
        #
        table = TABLE(Class='toctable')
        for i, row in enumerate(self.toc):
            flag, level, sid, width, sname = row
            tr = TR()
            tr <= TD(flag, Class='flag')
            tr <= TD(level, Class='level')
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

    def create_table(self, aoa=None, key=''):
        dindex.style.display = 'none'    
        dtop.clear()
        doutput.clear()
        title = 'LTE' if self.release.startswith('36') else 'NR'
        if aoa is None:
            section = self.get_section()
            aoa = section.aoa
            #
            document.title = f'{title} {section.id}'
            dtop <= SPAN(f'{self.release}')
            dtop <= SPAN(A('Index', href='#'))
            dtop <= SPAN(A('Search', href='#search'))
            dtop <= SPAN(f'{section.id} {section.name}')
            self.create_prev_next()
        else:
            document.title = f'{title}5 {key}'
            dtop <= SPAN(f'{self.release}')
            dtop <= SPAN(A('Index', href='#'))
            dtop <= SPAN(A('Search', href='#search'))
        #
        table = TABLE(Class='ch5content')
        for r, row in enumerate(aoa):
            level = row[col_level]
            tr = TR()
            table <= tr
            for c, v in enumerate(row):
                if c == col_text:
                    v = v.replace('\t', '&emsp;')
                    if level == -1:
                        v = '<br>'.join(v.split('\n')[1:])
                        tr <= TD(B(v))
                    else:
                        v = v.replace('\n', '<br>'*2)
                        td = TD(v)
                        set_indent(td, level)
                        tr <= td
                elif c == col_flag:
                    tr <= TD(v, Class='flag')
                else:
                    tr <= TD(v)
        doutput <= table
        ready.ready_table(table)

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
        #
        chars = sorted({item[0].upper() for item in self.ies})
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
        for ie in self.ies:
            if ie[0].upper() == c:
                dout <= A(ie, href=f'#{ie}')
                dout <= BR()
        
    def input_change(self, event):
        dout = document['searchresult']
        dout.clear()
        text = event.target.value
        if len(text) <= 1:
            return
        else:
            result = [ie for ie in self.ies if text.lower() in ie.lower()]
            if result:
                for ie in result:
                    dout <= A(ie, href=f'#{ie}')
                    dout <= BR()
            else:
                doutput <= B('No match')
                
    def create_search_result(self):
        text = remove_ie_suffix(self.anchor)
        if text in self.ies:
            result = []
            num = 0
            for i in self.ies[text]:
                s = self.section_list[i]
                for row in s.aoa:
                    if text in row[col_text]:
                        result.append(copy_row(row, text, num, s.headline))
                        num += 1
                    else:
                        result.append(row)
            self.create_table(aoa=result, key=text)
            dtop <= SPAN(f'Search result for {text}, {num} matches')
            window.find(text)
        else:
            output <= B('no match')

def set_indent(td, level):
    indent = int(level)
    if indent:
        indent = f'{indent*2}em'
        td.style.paddingLeft = indent

def create_head_td(text):
    '<br>'.join(text.split('\n')[1:]).replace('\t', '&emsp;')
    ele = TD()
    lines = text.split('\n')
    for l in lines[1:]:
        sid, sname = l.split('\t')
        ele <= create_a(l, sid)
    sid, sname = lines[-1].split('\t')
    ele <= BR()
    ele <= B(create_a(lines[-1], sid))
    return ele

def remove_ie_suffix(text):
    lst = text.split('-')
    if lst[-1][0] in 'rv' and lst[-1][1:].isdigit():
        return '-'.join(lst[:-1])
    else:
        return text

def copy_row(row, text, num, headline):
    lst = row[::]
    title = f'{num+1}: {headline}'.replace('\t', ' ')
    lst[2] = lst[2].replace(text, f'<span style="font-weight: bolder; font-size: large;">{text}</span><sub style="color:red;">{title}</sub>')
    return lst

    
#################################################################################
# 
#################################################################################       
g = Data()
window.onhashchange = g.body_hashchange
g.body_hashchange()
