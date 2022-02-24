##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable

##########################################################################################################################################

def main(event=None):
    output = document['zone-output']
    output.clear()
    output <= create_table(pci=cfg.PCI.value)


def create_table(pci):
    def set_data(lst, tag):
        for i, (k, l) in enumerate(lst):
            class_data[k][l] = tag
            if tag == "zero":
                continue
            data[k][l] = i

    x = [["l"] * 4, list(range(4))]
    y1 = list(range(240))[::-1]
    y0 = [i // 12 for i in y1]
    y = [y0, y1]

    data = [["" for l in range(4)] for k in range(240)]
    class_data = [["" for l in range(4)] for k in range(240)]

    d = {}
    d["pss"] = [(k, 0) for k in range(56, 183)]
    d["sss"] = [(k, 2) for k in range(56, 183)]
    d["zero"] = [(k, 0) for k in range(56)] + \
                [(k, 0) for k in range(183, 240)] + \
                [(k, 2) for k in range(48, 56)] + \
                [(k, 2) for k in range(183, 192)]
    v = pci % 4
    d["pbch_dmrs"] = [(k+v, 1) for k in range(0, 237, 4)] + \
                     [(k+v, 2) for k in range(0, 45, 4)] + \
                     [(k+v, 2) for k in range(192, 237, 4)] + \
                     [(k+v, 3) for k in range(0, 237, 4)]

    d["pbch_dmrs"] = [(k+v, 1) for k in range(0, 237, 4)] + \
                     [(k+v, 2) for k in range(0, 45, 4)] + \
                     [(k+v, 2) for k in range(192, 237, 4)] + \
                     [(k+v, 3) for k in range(0, 237, 4)]

    for tag, lst in d.items():
        set_data(lst, tag)

    pbch = [(k, 1) for k in range(240)] + \
           [(k, 2) for k in range(48)] + \
           [(k, 2) for k in range(192, 240)] + \
           [(k, 3) for k in range(240)]
    i = 0
    for k, l in pbch:
        if class_data[k][l] == "pbch_dmrs":
            continue
        class_data[k][l] = "pbch"
        data[k][l] = i
        i += 1

    data = data[::-1]
    class_data = class_data[::-1]
    a1 = None
    a1 = [["", ""], ["RB", "k"]]
    caption = f"PCI = {pci}"
    return ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"