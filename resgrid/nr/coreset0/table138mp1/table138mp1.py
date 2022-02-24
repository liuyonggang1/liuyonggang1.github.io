##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable

##########################################################################################################################################

def main(event=None):
    document['zone-output'].clear()
    ssb = {sc: (sc//12, sc) for sc in range(240)}
    kssb = {}
    for i in range(cfg.kssb.value + 1):
        kssb[0 - i] = f"kssb = {i}"
    start = - cfg.kssb.value - (cfg.offset.value * 12)
    coreset0 = {}
    for rb in range(cfg.nrbs.value):
        for sc in range(12):
            i = start + rb * 12 + sc
            coreset0[i] = (rb, sc)
    top = max([max(ssb.keys()), max(kssb.keys()), max(coreset0.keys())])
    bottom = min([min(ssb.keys()), min(kssb.keys()), min(coreset0.keys())])
    overlap_rbs = overlap_coreset0_rb_set(ssb, coreset0)
    data = []
    class_data = []
    for i in  range(top, bottom - 1, -1):
        row = [""] * 5
        class_row = ["blank"] * 5
        if i in ssb:
            rb = row[0] = ssb[i][0]
            if cfg.kssb.value == 0:
                row[1] = ssb[i][1] if rb == 0 else ""
            else:
                row[1] = ssb[i][1]
            class_row[0] = "ssb"
            class_row[1] = "ssb"
        if i in kssb:
            row[2] = kssb[i]
            class_row[2] = "kssb"
        if i in coreset0:
            rb = row[4] = coreset0[i][0]
            sc = coreset0[i][1]
            if rb not in overlap_rbs and sc != 11:
                continue
            if cfg.kssb.value == 0:
                row[3] = coreset0[i][1] if in_kssb_area(rb, kssb, coreset0) else ""
            else:
                row[3] = coreset0[i][1] if rb in overlap_rbs and i not in ssb else ""
            class_row[3] = "coreset0"
            class_row[4] = "coreset0"
        data.append(row)
        class_data.append(class_row)

    a1 = None
    x = [["SSB", "SSB", f"kssb={cfg.kssb.value}", "CORESET#0", "CORESET#0"], 
        [" ", f"subcarrier={cfg.scs_ssb.value}", 
         f"kssb={cfg.kssb.value}", 
         f"subcarrier={cfg.subCarrierSpacingCommon.value}", "Resource Block"]]
    y = None
    caption = f"38.213 Table 13-8 multiplexing pattern 1: RBs={cfg.nrbs.value}, Offset={cfg.offset.value}"
    table = ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=5)
    document['zone-output'] <= table

def in_kssb_area(rb, kssb, coreset0):
    mi = min(kssb.keys())
    ma = max(kssb.keys())
    mi_rb = coreset0[mi][0]
    ma_rb = coreset0[ma][0]
    return mi_rb <= rb <= ma_rb

def overlap_coreset0_rb_set(ssb, coreset0):
    ret = set()
    for i in ssb.keys():
        if i in coreset0:
            rb = coreset0[i][0]
            ret.add(rb)
    return ret

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"