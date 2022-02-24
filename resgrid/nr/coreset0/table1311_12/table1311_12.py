##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable

##########################################################################################################################################
def main(event=None):
    document['zone-output'].clear()
    ob = cfg.get_cfg()
    a1 = [["subframe"],["slot"]]
    nframes = 20
    nsubframes = 10
    x0 = [sf for sf in range(nsubframes) for _ in range(ob.nslots_subframe)]
    x1 = [slot for slot in range(ob.nslots_frame)]
    x = [x0, x1]
    y = [f"SFN {sfn}" for sfn in range(nframes)]
    caption = f"38.213 Table 13-11, 12 <br>i<sub>SSB</sub> and associated n<sub>0</sub>"
    data = [["" for slot in range(ob.nslots_frame)] for sfn in range(nframes)]
    class_data = None

    result = {}
    for i in range(ob.num_ssbs):
        mframe, n0 = cal_mframe(ob, i)
        result[i] = []
        for sfn in range(nframes):
            if (sfn % 2 == 0 and mframe == 0) or \
               (sfn % 2 == 1 and mframe == 1):
                result[i].append((sfn, n0))
    for i, v in result.items():
        for (sfn, n0) in v:
            s = data[sfn][n0]
            data[sfn][n0] = f"{i}" if s == "" else f"{s},{i}"
    num_merge_rows = None
    num_merge_cols = None
    table = ztable.create_htable(a1=a1, 
                                 x=x, 
                                 y=y, 
                                 data=data, 
                                 class_data=class_data, 
                                 caption=caption, 
                                 num_merge_rows=num_merge_rows, 
                                 num_merge_cols=num_merge_cols)
    document['zone-output'] <= table


def cal_mframe(ob, i):
    from math import floor
    a = ob.O * ob.nslots_subframe
    b = floor(i * ob.M)
    c = a + b
    d = c / ob.nslots_frame
    e = floor(d)
    f = e % 2
    n0 = int(c) % ob.nslots_frame 
    # print(f"i={i}", a, b, c, d, e, f, f"n0={n0}")
    return f, n0


##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"