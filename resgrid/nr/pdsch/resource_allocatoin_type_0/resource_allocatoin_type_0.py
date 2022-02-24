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

    nrbs = cfg.n_bwp_start + cfg.n_bwp_size
    col0 = [f"CRB {i}" for i in range(nrbs)]
    a = [0] * cfg.rbg_0_size
    b = [rbg for rbg in range(1, cfg.n_rgb - 1) for _ in range(cfg.p)]
    c = [cfg.n_rgb - 1] * cfg.rbg_last_size
    col1 = [""] * cfg.n_bwp_start + [f"RBG {i}" for i in a + b + c]
    data = ztable.transpose([col0, col1])[::-1]
    a1 = None
    x = [["CRB", "BWP RGB"]]
    y = None
    class_data = None
    caption = None
    num_merge_row = None
    num_merge_cols = None
    nrows = len(data)
    ncols = len(data[0])
    # num_merge_row = nrows
    num_merge_cols = ncols
    output <= DIV("resource allocation type 0 uses bitmap to mark RBGs to be allocated")
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