from browser import document, window, alert
from browser.html import TR, TD, SELECT, OPTION, DIV, SCRIPT, TABLE, OL, LI, TH, SPAN, BUTTON, HR

#############################################################################
# load css
#############################################################################
def load_css(cssname):
    link = document.select('link')[0]
    link.href = cssname

def load_js(jsname):
    return
    document.head <= SCRIPT(src=jsname)

#############################################################################
# tree
#############################################################################
col_flag = 0
col_level = 1
col_ie = 2
col_need = 3
col_udf = 4
col_vrange = 5
col_desc = 6
minus = '-'
plus = '+'

#############################################################################
# fd_div
#############################################################################
popup = True
document.body <= DIV(id='fd', style={'display':'none'})
fd_div = document['fd']

def setup_fd():
    fd_div <= DIV(id='fddivc2')
    #
    top = DIV(id='fdtop')
    top <= HR()
    b = BUTTON('copy')
    b.style.fontSize = 'xx-small'
    b.bind('click', lambda e: copy_element(document['fddivc2']))
    top <= b
    fd_div <= top
    top.style.display = 'none'
    #
    fd_div.bind('mouseleave', onmouseleave_fd)
    fd_div.bind('mouseenter', onmouseenter_fd)

def onmouseenter_fd(e):
    document['fdtop'].style.display = ''
    
def onmouseleave_fd(e):
    document['fdtop'].style.display = 'none'
    o = fd_div.getBoundingClientRect()
    if o.left < e.screenX < o.right and o.top < e.screenY < o.bottom:
        return
    fd_div.style.display = 'none'

setup_fd()
    
def button_popup(event):
    global popup
    b = event.target
    if b.html == 'Popup On':
        b.html = 'Popup Off'
        popup = False
        b.style.backgroundColor = 'red'
        fd_div.style.display = 'none'
        #fd_div.clear()
    else:
        b.html = 'Popup On'
        popup = True
        b.style.backgroundColor = 'lightgreen'
        # fd_div.style.display = ''

#############################################################################
# get
#############################################################################
def get_table():
    try:
        if document['index'].style.display != 'none':
            return document['index'].select('table')[0]
        else:
            return document['output'].select('table')[0]
    except:
        return document['output'].select('table')[0]

def get_level(tr):
    try:
        return int(tr.cells[col_level].html)
    except:
        return None

def get_flag_td(tr):
    return tr.cells[col_flag]
        
def get_flag(tr):
    return get_flag_td(tr).html

def set_flag(tr, flag):
    if get_flag(tr) != flag:
        get_flag_td(tr).html = flag

def get_treepad(tr):
    try:
        return tr.select('.iepad')[0].treepad
    except:
        return ''

def get_tablepad(tr):
    try:
        return tr.select('.iepad')[0].tablepad
    except:
        return ''
    
def get_ie(tr):
    try:
        return tr.select('.ie')[0].html
    except:
        return ''
        
def get_need(tr):
    return tr.cells[col_need].html

def get_udf(tr):
    return tr.cells[col_udf].text
    
def get_vrange(tr):
    return tr.cells[col_vrange].html

def get_desc(tr):
    return tr.cells[col_desc].html
    
#############################################################################
# flag
#############################################################################
        
def show(ele):
    if ele.style.display == 'none':
        ele.style.display = ''
    
def hide(ele):
    if ele.style.display != 'none':
        ele.style.display = 'none'

#############################################################################
# flag action
#############################################################################
def collapse(tr):
    set_flag(tr, plus)
    level = get_level(tr)
    tr = tr.nextElementSibling
    while tr and get_level(tr) > level:
        hide(tr)
        tr = tr.nextElementSibling
    
def expand(tr):
    set_flag(tr, minus)
    level = get_level(tr)
    tr = tr.nextElementSibling
    while tr:
        nlevel = get_level(tr)
        if nlevel-1 == level:
            show(tr)
            if get_flag(tr) == minus:
                expand(tr)
        elif nlevel <= level:
            break
        tr = tr.nextElementSibling
        
def click_flag(event):
    t = event.target
    while True:
        if t.tagName in ('TABLE', 'A'):
            return
        if t.tagName == 'TR':
            tr = t
            break
        else:
            t = t.parent
    if get_level(tr) is None:
        return
    flag = get_flag(tr)
    if flag == minus:
        collapse(tr)
    elif flag == plus:
        try:
            ntr = tr.nextElementSibling
            if get_level(ntr) == get_level(tr) + 1:
                expand(tr)
            else:
                window.g.append_child(tr)
        except:
            print('error 179')
            expand(tr)
            raise

#############################################################################
# click level
#############################################################################
def create_level_div(table):
    lst = sorted({get_level(tr) for tr in table.rows if get_level(tr) is not None})
    if table.previousElementSibling is not None:
        div = table.previousElementSibling
        table.parent.removeChild(div)
    div = DIV()
    div.style.position = 'sticky'
    div.style.top = 21
    div.style.backgroundColor = 'RGB(230,230,230)'
    span = SPAN('Level:')
    div <= span
    for i in lst:
        span = SPAN(i)
        span.style.color = 'blue'
        span.style.textDecoration = 'underline'
        span.style.padding = '5px 5px 5px 5px'
        span.style.cursor = 'pointer'
        span.style.borderRightStyle = 'none'
        span.onclick = click_level
        div <= span
    table.parent.insertBefore(div, table)
    if table.className == 'toctable':
        collapse_to_level(table, lst[0])
    
def click_level(event):
    level = int(event.target.html)
    table = event.target.parent.nextElementSibling
    collapse_to_level(table, level)

def collapse_to_level(table, level):
    for tr in table.rows:
        if get_level(tr) is None:
            continue
        l = get_level(tr)
        td = get_flag_td(tr)
        if l < level:
            show(tr)
            if get_flag(tr) == plus:
                set_flag(tr, minus)
        elif l == level:
            show(tr)
            if get_flag(tr) == minus:
                set_flag(tr, plus)            
        elif l > level:
            hide(tr)
            if get_flag(tr) == minus:
                set_flag(tr, plus)            
    
#############################################################################
# auto size clip
#############################################################################
def set_width_for_asn1_table(table=None):
    if table is None:
        table = document.select('asn1tree')[0]
    if table.tview == 'tree':
        set_width_for_vrange_col(table)
    else:
        set_width_for_vrange_desc_col(table)
    
def set_width_for_vrange_col(table):
    col_clip = table.select('.vrange')[0].cellIndex
    #
    stylesheet = document.styleSheets[0]
    for i, rule in enumerate(stylesheet.cssRules):
        if rule.cssText.startswith("table.asn1tree[tview=tree] td.vrange") and "max-width" in rule.cssText:
            stylesheet.deleteRule(i)
    #
    if document.body.scrollWidth <= window.innerWidth: return
    width = window.innerWidth - (table.scrollWidth - table.rows[1].cells[col_clip].scrollWidth) - len(table.rows[1].cells)*4
    width = min(width, int(window.innerWidth*0.3))
    stylesheet = document.styleSheets[0]
    rule = "table.asn1tree[tview=tree] td.vrange { max-width: " + str(width) + "px;}"
    stylesheet.insertRule(rule, stylesheet.cssRules.length)
    #
    for td in table.select('.vrange'):
        if td.clientWidth < td.scrollWidth:
            td.desc = 'hasdesc'

def set_width_for_vrange_desc_col(table):
    col_clip = table.select('.vrange')[0].cellIndex
    col_desc = table.select('.desc')[0].cellIndex
    #
    stylesheet = document.styleSheets[0]
    for i, rule in enumerate(stylesheet.cssRules):
        if rule.cssText.startswith("table.asn1tree[tview=table] td.vrange") and "max-width" in rule.cssText:
            stylesheet.deleteRule(i)
        if rule.cssText.startswith("table.asn1tree[tview=table] td.desc") and "max-width" in rule.cssText:
            stylesheet.deleteRule(i)
    #
    width_clip = table.rows[1].cells[col_clip].scrollWidth
    width_desc = table.rows[1].cells[col_desc].scrollWidth
    sum = width_desc + width_clip
    if width_desc > width_clip:
        return
    else:
        width_clip = int(sum*0.4)
        width_desc = sum - width_clip
    stylesheet = document.styleSheets[0]
    rule = "table.asn1tree[tview=table] td.vrange { max-width: " + str(width_clip) + "px;}"
    stylesheet.insertRule(rule, stylesheet.cssRules.length)
    rule = "table.asn1tree[tview=table] td.desc { max-width: " + str(width_desc) + "px;}"
    stylesheet.insertRule(rule, stylesheet.cssRules.length)
    #
            
# def remove_clip_width_css():
    # stylesheet = document.styleSheets[0]
    # for i, rule in enumerate(stylesheet.cssRules):
        # if rule.cssText.startswith("table.asn1tree[tview=tree] td.clip") and "max-width" in rule.cssText:
            # stylesheet.deleteRule(i)
            
#############################################################################
# mouse move
#############################################################################
def onmouseover_table(e):
    try:
        tr = e.target
        while tr.tagName != 'TR':
            tr = tr.parent
        flag = get_flag(tr)
        if flag:
            tr.clickable = flag
    except:
        pass
    if not popup: return
    t = e.target
    if t.tagName == 'SPAN' and t.className == 'ie':
        td = t.parent
        s = get_tip_for_ie(td)
        display_tip(s, e)
    elif t.tagName == 'TD' and t.cellIndex == col_vrange and (t.hasAttribute('desc') or t.html.strip().startswith('ENUMERATED')):
        s = get_tip_for_type(t)
        display_tip(s, e)
    elif fd_div.style.display != 'none':
        fd_div.style.display = 'none'

#############################################################################
# retrieve field description
#############################################################################
def get_tip_for_ie(td):
    tr = td.parent
    lst = []
    lst.append(f'<b>{get_ie(tr)}:</b> {get_ie_path(td.parent)}')
    if document.select('.asn1tree')[0].tview == 'tree':
        desc = get_desc(td.parent)
        if desc:
            lst.append(desc)
    # t = get_type(tr)
    # if t and t not in ('SEQUENCE', 'ExtGroup', 'CHOICE'):
        # lst.append(f'<b>Type:</b> {get_type(tr)}')
    lst = [i for i in lst]
    return '<br><hr>'.join(lst)

def get_tip_for_type(td):
    if document.select('.asn1tree')[0].tview == 'table':
        return ''
    if td.html.startswith('ENUMERATED'):
        v = td.html.replace('ENUMERATED', '').strip()[1:-1]
        lst = [i.strip() for i in v.split(',')]
        if len(lst) <= 1: return
        lst = [f'{i}. {s}' for i, s in enumerate(lst)]
        return ',<br>'.join(lst)
    else:
        return td.html
        
def display_tip(text, e):
    fddiv = fd_div
    if text:
        o = e.target.getBoundingClientRect()
        eleleft = int(o.left + window.scrollX)
        eletop = int(o.top + window.scrollY)
        eleright = int(o.right + window.scrollX)
        elebottom = int(o.bottom + window.scrollY)
        if e.target.className == 'ie':
            fddiv.style.left = eleright - 5
            # fddiv.style.left = e.pageX + 1
        else:
            fddiv.style.left = e.pageX + 1
        fddiv.style.top = elebottom - 2
        fddiv.style.display = ''
        #
        fddivc2 = document['fddivc2']
        fddivc2.clear()
        fddivc2 <= DIV(text)
        #
    else:
        fddiv.style.display = 'none'
        
def get_ie3(tr):
    ie = get_ie(tr)
    s = get_udf(tr)
    if ie in ('nonCriticalExtension', 'lateNonCriticalExtension') and s:
        return s
    else:
        return ie

def get_ie_path(tr):
    a = [get_ie3(tr)] 
    level = get_level(tr)
    while level:
        tr = tr.previousElementSibling
        tmp = get_level(tr)
        if level == tmp + 1:
            a.append(get_ie3(tr))
            level =  tmp
    return ' -> '.join(a[::-1])
        
#############################################################################
# ready table
#############################################################################
def ready_table(table):
    table.onclick = click_flag
    create_level_div(table)
    window.scroll(0,0)
    if table.className == 'asn1tree':
        table.bind('mouseover', onmouseover_table)
        set_width_for_asn1_table(table)
    else:
        for tr in table.rows:
            tr.clickable  = get_flag(tr)
        
#############################################################################
# copy
#############################################################################
def copy_tree(event):
    table = document['output'].getElementsByTagName('table')[0]
    
    treefmt = [get_treepad(tr)+get_ie(tr) for tr in table.rows if tr.style.display != 'none'][1:]
    tablefmt = [get_tablepad(tr)+get_ie(tr) for tr in table.rows if tr.style.display != 'none'][1:]
    #
    f2 = [l.replace('├', '+').replace('─', '-').replace('└', '+').replace('│', '|') for l in treefmt]
    #
    text = '\n'.join(treefmt + ['', ''] + f2 + ['', ''] + tablefmt)
    copy_text(text)

def copy_text(text):
    style = {'font-family': "'Segoe UI'", 
             'font-size':   'small',
             'position':    'absolute', 
             'left':        '-1000px', 
             'top':         '-1000px', 
             'white-space': 'pre'}
    d = DIV(text, style=style)
    document.body <=  d
    copy_element(d)
    document.body.removeChild(d)
    
def copy_element(e):
    window.getSelection().empty()
    range = document.createRange()
    range.selectNode(e)
    window.getSelection().addRange(range)
    document.execCommand('copy')
    window.getSelection().empty()

#############################################################################
# export_xlsx
#############################################################################
def export_xlsx(aoa, xlsx_name, sheet_name):
    ws = window.XLSX.utils.aoa_to_sheet(aoa)
    wb = window.XLSX.utils.book_new()
    window.XLSX.utils.book_append_sheet(wb, ws, sheet_name)
    window.XLSX.writeFile(wb, xlsx_name)
