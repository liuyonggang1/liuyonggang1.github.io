##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable
import math

##########################################################################################################################################
def main(event=None):
    output = document['zone-output']
    output.clear()
    cfg = cfg0.get_cfg()

    a1 = None
    x = [["CRB", "BWP PRB"]]
    y = None

    nrbs = cfg.n_bwp_start + cfg.n_bwp_size
    col0 = [f"CRB {i}" for i in range(nrbs)]
    col1 = [""] * cfg.n_bwp_start + [f"{i}" for i in range(cfg.n_bwp_size)]
    dcol0 = ["" for _ in col0]
    dcol1 = ["" for _ in col1]
    start = cfg.n_bwp_start + cfg.rb_start
    for i in range(start, start + cfg.len_rbs):
        dcol1[i] = "allocated"

    data = ztable.transpose([col0, col1])[::-1]
    class_data = ztable.transpose([dcol0, dcol1])[::-1]
    caption = None
    num_merge_row = None
    num_merge_cols = None
    nrows = len(data)
    ncols = len(data[0])
    # num_merge_row = nrows
    num_merge_cols = ncols
    output <= ztable.create_htable(a1=a1, 
                                   x=x, 
                                   y=y, 
                                   data=data, 
                                   class_data=class_data, 
                                   caption=caption, 
                                   num_merge_rows=num_merge_row, 
                                   num_merge_cols=num_merge_cols)



##########################################################################################################################################
cfg0 = para.Config()
cfg0.start(main)
# main()
# document["main"].style.display = "none"