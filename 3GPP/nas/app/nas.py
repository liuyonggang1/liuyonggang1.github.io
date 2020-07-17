##########################################################################################################################################
from browser import document, window
from browser.html import TABLE, TR, TD, TH, SPAN, DIV, A, SCRIPT, PRE, B, IMG, UL, LI, HR, INPUT, BR, BUTTON

g = None
name_msg_map = {}
id_ie_map = {}
name_ie_map = {}
ie_desc_array = []

def main():
    spec = window.location.href.split('/')[-1].split('#')[0].split('.')[0]
    f = open(f'../data/{spec}.json')
    s = f.read()
    global g
    g = window.JSON.parse(s)
    global name_msg_map
    name_msg_map = {m.name:m for m in g.msg_list}
    global id_ie_map
    id_ie_map = {ie.id:ie for ie in g.ie_list}
    global name_ie_map
    name_ie_map = {ie.name.strip():ie for ie in g.ie_list}
    
    window.onhashchange = body_hashchange
    body_hashchange(None)

#################################################################    
# 
#################################################################        
def get_anchor():
    if window.location.hash:
        anchor = window.location.hash[1:]
        anchor = window.decodeURI(anchor)
        return anchor
    return None
            
def body_hashchange(e):
    anchor = get_anchor()
    output_clear()
    if anchor:
        if anchor.startswith('ie'):
            create_ie(anchor)
        else:
            create_table(anchor)
    else:
        if g.release.startswith('24008'):
            create_index_24008()
        else:
            create_index()
        
def output_clear():
    document.title = ''
    document['top'].clear()
    document['title'].clear()
    document['output'].clear()
    
#################################################################################################        
# 
#################################################################################################        

def create_index():
    document.title = g.release
    document['title'] <= g.release
    document['top'] <= ''
    
    msg_list = g.msg_list
    mobility_msg_list = [m for m in msg_list if m.id.startswith('8.2')]
    session_msg_list = [m for m in msg_list if m.id.startswith('8.3')]
    d5_list = [m for m in msg_list if m.id.startswith('D.5')]
   
    table = TABLE(id='indextable')
    document['output'] <= table
    
    if g.release.startswith('24301'):
        generation = 'EPS'
    elif g.release.startswith('24501'):
        generation = '5GS'
    
    mm = '{} mobility management messages'.format(generation)
    sm = '{} session management messages'.format(generation)
    d5 = 'UE policy delivery protocol messages'
    
    table <= TR(TD(HR(), colspan='2'))
    table <= TR(TD(mm, colspan='2'))
    for m in mobility_msg_list:
        table <= TR(TD(m.id)+TD(A(f'{m.name}', href=f'#{m.name}')))

    table <= TR(TD(HR(), colspan='2'))
    table <= TR(TD(sm, colspan='2'))
    for m in session_msg_list:
        table <= TR(TD(m.id)+TD(A(f'{m.name}', href=f'#{m.name}')))

    if d5_list:
        table <= TR(TD(HR(), colspan='2'))
        table <= TR(TD(d5, colspan='2'))
        for m in d5_list:
            table <= TR(TD(m.id)+TD(A(f'{m.name}', href=f'#{m.name}')))

    table <= TR(TD(HR(), colspan='2'))
    table <= TR(TD('information elements', colspan='2'))
    for ie in g.ie_list:
        table <= TR(TD(ie.id)+TD(A(f'{ie.name}', href=f'#ie{ie.id}')))
    
def create_index_24008():
    document.title = g.release
    document['title'] <= g.release
    document['top'] <= ''
    
    msg_list = g.msg_list
    
    table = TABLE(id='indextable')
    document['output'] <= table
    
    table <= TR(TD(HR(), colspan='2'))
    table <= TR(TD('Messages', colspan='2'))
    for m in msg_list:
        table <= TR(TD(m.id)+TD(A(f'{m.name}', href=f'#{m.name}')))

    table <= TR(TD(HR(), colspan='2'))
    table <= TR(TD('information elements', colspan='2'))
    for ie in g.ie_list:
        table <= TR(TD(ie.id)+TD(A(f'{ie.name}', href=f'#ie{ie.id}')))

            
#################################################################################################        
# 
#################################################################################################        
def create_table(name):
    global ie_desc_array
    ie_desc_array = []
    #
    m = name_msg_map[name]
    document.title = f'{g.release}: {m.id} {m.name}'
    document['title'] <= document.title
    #
    button = BUTTON('show IE description')
    document['top'] <= button
    button.bind('click', toggle_ie_desc)
    #
    document['top'] <= SPAN(' ')
    document['top'] <= A('Index', href='')
    document['output'] <= PRE(m.id + ' ' + m.name + '\n' + m.definition, Class='definition')
    table = TABLE(id='msgtable')
    document['output'] <= table
    for r, row in enumerate(m.aoa):
        tr = TR(Class=f'r{r}')
        table <= tr
        for c, v in enumerate(row):
            title = ''
            if r == 0 and c in (2, 3, 4, 5):
                title, v = v, ''
            elif c == 2:
                lst = v.replace('\n', ' ').split(' ')
                lst2 = [ie for ieid, ie in id_ie_map.items() if ieid in lst]
                if len(lst2) == 1:
                    ie = lst2[0]
                    title = f'{ie.id} {ie.name}\n{ie.definition}'
                    v = A(f'{ie.id}', href=f'#ie{ie.id}')
                ie_desc_array.append(title)
            elif r != 0 and c == 6:
                if v:
                    v = DIV(v) + DIV('', Class='iedescdiv', needsep='y')
                else:
                    v = DIV('', Class='iedescdiv', needsep='n')
            tr <= TD(v, title=title, Class=f'c{c}')

#################################################################################################
def toggle_ie_desc(event):
    button = event.target
    text = button.text
    if text == 'show IE description':
        button.text = 'hide IE description'
        for s, div in zip(ie_desc_array, document.select('.iedescdiv')):
            if div.needsep == 'y':
                div <= BR()
            div <= sniff_24008_link(s)
    else:
        button.text = 'show IE description'
        for div in document.select('.iedescdiv'):
            div.clear()

def sniff_24008_link(ie_text):
    result = ie_text
    try:
        line1 = ie_text.split('\n')[0]
        line2 = ie_text.split('\n')[1]
        lst = [s for s in line2.split(' ') if s]
        try:
            if lst[0] == 'See' and lst[1] == 'subclause' and lst[3] == 'in' and lst[4] == '3GPP' and lst[5] == 'TS' and lst[6] == '24.008':
                lst[2] = A(f'{lst[2]}', href=f'24008.html#ie{lst[2]}')
                lst[6] = A(f'{lst[6]}', href='24008.html')
                result = SPAN()
                result <= SPAN(line1+'\n')
                for i in lst:
                    result <= SPAN(i) + SPAN(' ')
        except:
            return ie_text
    except:
        return ie_text
    return result
            

def create_ie(name):
    ie = id_ie_map[name[2:]]
    document.title = f'{g.release}: {ie.id} {ie.name}'
    document['title'] <= document.title
    document['top'] <= A('Index', href='')
    document['output'].html = ie.html_text
    sniff_24008_ie()
    
def sniff_24008_ie():
    for p in document['output'].select('p'):
        lst = [s for s in p.text.split(' ') if s]
        try:
            if lst[0] == 'See' and lst[1] == 'subclause' and lst[3] == 'in' and lst[4] == '3GPP' and lst[5] == 'TS' and lst[6] == '24.008':
                lst[2] = A(f'{lst[2]}', href=f'24008.html#ie{lst[2]}')
                lst[6] = A(f'{lst[6]}', href='24008.html')
                p.clear()
                for i in lst:
                    p <= SPAN(i) + SPAN(' ')
        except:
            pass

main()