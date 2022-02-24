##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable
import math


##########################################################################################################################################
def main(event=None):
    document['zone-output'].clear()
    a1 = None
    x = None
    y = None
    data = None
    class_data = None
    caption = None
    num_merge_row = None
    num_merge_cols = None

    ob = cfg.get_cfg()
    x = ["Carrier", "BWP", "IE ControlReourceSet -> frequencyDomainResources bitmap"]
    nrows = ob.n_grid_start + ob.n_grid_size
    n_bwp_end = ob.n_bwp_start + ob.n_bwp_size - 1
    data = [[""]*3 for row in range(nrows)]
    class_data = [[""]*3 for row in range(nrows)]

    for crb in range(nrows):
        data[crb][0] = f"CRB {crb}"
        class_data[crb][0] = "outcarrier" if crb < ob.n_grid_start else "incarrier"

    for i, crb in enumerate(range(ob.n_grid_start, ob.n_bwp_start)):
        data[crb][1] = f"{i}"
        class_data[crb][1] = "offset"

    for i, crb in enumerate(range(ob.n_bwp_start, n_bwp_end+1)):
        data[crb][1] = f"RB {i}"

    if ob.rb_offset == -1:
        coreset_start = 6 * math.ceil(ob.n_bwp_start / 6)
    else:
        coreset_start = ob.n_bwp_start + ob.rb_offset
    coreset_end = coreset_start + (n_bwp_end - coreset_start) // 6 * 6
    for i, crb in enumerate(range(coreset_start, coreset_end, 6)):
        for ii in range(6):
            data[crb+ii][2] = i
            class_data[crb+ii][1] = f"group{i%2}"
    
    data = data[::-1]
    class_data = class_data[::-1]
    # num_merge_row = len(data)
    num_merge_cols = len(data[0])
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=num_merge_row, num_merge_cols=num_merge_cols)



##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"