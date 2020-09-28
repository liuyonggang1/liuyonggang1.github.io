##########################################################################################################################################
from browser import document, alert, window
from browser.html import *
import para
import ztable
import codebook

##########################################################################################################################################
def main(event):
    document['zone-output'].clear()
    a1, x, y = None, None, None
    x, result = codebook.Codebook(cfg).get_table()
    x = x[:-2]+x[-1:]
    result = [row[:-2]+row[-1:] for row in result]
    y = list(range(len(result)))
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=result, class_data=None, caption='', num_merge_rows=None, num_merge_cols=None)
    window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub])
    

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
