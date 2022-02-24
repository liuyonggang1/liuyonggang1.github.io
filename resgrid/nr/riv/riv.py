##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable


sup_sub_template = "{word}<span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"
s_rb_start ="RB<sub>start</sub>"
s_l_rb ="L<sub>RB</sub>"
s_n_start_bwp = sup_sub_template.format(word="N", sup="start", sub="BWP")
s_n_size_bwp = sup_sub_template.format(word="N", sup="size", sub="BWP")

##########################################################################################################################################
def main(event=None):
    from math import floor
    document['zone-output'].clear()
    a1 = None
    data = []
    size = cfg.n_bwp_size.value
    x0 = ["RB<sub>start</sub>" for start in range(size)]
    x1 = [f"{start}" for start in range(size)]
    x = [x0, x1]
    y0 = ["L<sub>RB</sub> - 1" for L_1 in range(size)]
    y1 = [f"{L_1}" for L_1 in range(size)]
    y = [y0, y1]
    data = [["" for start in range(size)] for L_1 in range(size)]
    class_data = [["" for start in range(size)] for L_1 in range(size)]

    rivs = []

    for L_1 in range(size):
        L = L_1 + 1
        for start in range(size):
            if (L + start) > size:
                continue
            riv, flag = cal_riv(size, L, start)
            data[L_1][start] = riv
            class_data[L_1][start] = f"riv{flag}"
            rivs.append(riv)
            
    caption = f"encode RIV for {s_n_size_bwp}={size}"
    # num_merge_row = len(data)
    # num_merge_cols = len(data[0])
    num_merge_row = None
    num_merge_cols = None
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=num_merge_row, num_merge_cols=num_merge_cols)
    # alert("done")
    main2(rivs, size)

def main2(rivs, size):
    document['zone-output'] <= HR()
    a1 = None
    data = []
    x0 = ["RB<sub>start</sub>" for start in range(size)]
    x1 = [f"{start}" for start in range(size)]
    x = [x0, x1]
    y0 = ["L<sub>RB</sub> - 1" for L_1 in range(size)]
    y1 = [f"{L_1}" for L_1 in range(size)]
    y = [y0, y1]
    data = [["" for start in range(size)] for L_1 in range(size)]
    class_data = [["" for start in range(size)] for L_1 in range(size)]

    for riv in rivs:
        L_1, start = divmod(riv, size)
        L = L_1 + 1
        data[L_1][start] = riv
        if (L + start) > size:
            flag = 2
        else:
            flag = 0
        class_data[L_1][start] = f"riv{flag}"

        if flag == 2:
            L_1 = size - L_1
            start = size - 1 - start
            data[L_1][start] = riv
            class_data[L_1][start] = f"riv{flag - 1}"
            
    caption = f"decode RIV for {s_n_size_bwp}={size}"
    # num_merge_row = len(data)
    # num_merge_cols = len(data[0])
    num_merge_row = None
    num_merge_cols = None
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=num_merge_row, num_merge_cols=num_merge_cols)
    # alert("done")

    document['zone-output'] <= HR()
    document['zone-output'] <= IMG(src="decode_riv.png")



def cal_riv(size, L, start):
    from math import floor
    L_1 = L - 1
    if L_1 <= floor(size / 2):
        riv = size * L_1 + start
        return riv, 0
    else:
        riv = size * (size - L_1) + (size - 1 - start)
        return riv, 1

def decode_riv(riv, size):
    L_1, start = divmod(riv, size)
    L = L_1 + 1
    if (L + start) > size:
        L = size + 1 - L_1
        start = size - 1 - start
    return L, start


##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"