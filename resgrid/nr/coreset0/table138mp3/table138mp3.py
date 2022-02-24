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
        kssb[0 - i] = i

    if cfg.offset.value > 0:
        start = - cfg.kssb.value - (cfg.offset.value * 12)
    else:
        start = min(kssb.keys())

    coreset0 = {}
    if cfg.offset.value > 0:
        disp_nrbs = cfg.nrbs.value + 1
    else:
        disp_nrbs = abs(cfg.offset.value) + cfg.nrbs.value
    for rb in range(disp_nrbs):
        for sc in range(12):
            i = start + rb * 12 + sc
            coreset0[i] = (rb, sc)
    top = max([max(ssb.keys()), max(kssb.keys()), max(coreset0.keys())])
    bottom = min([min(ssb.keys()), min(kssb.keys()), min(coreset0.keys())])
    overlap_rbs = overlap_coreset0_rb_set(ssb, coreset0)
    overlap_ssb_sc = overlap_ssb_set(ssb, coreset0)
    data = []
    class_data = []
    for i in  range(top, bottom - 1, -1):
        row = [""] * 4
        class_row = ["blank"] * 4
        if i in ssb:
            rb, sc = ssb[i]
            if sc in overlap_ssb_sc or sc in (0, 239):
                row[0] = sc
                class_row[0] = "ssb"
            elif sc == 238:
                row[0] = "..."
                class_row[0] = "ssb"
            else:
                continue
        if i in kssb:
            row[1] = f"kssb={kssb[i]}"
            class_row[1] = "kssb"
        if i in coreset0:
            if cfg.offset.value > 0:
                row[2] = sc = coreset0[i][1]
                row[3] = rb = coreset0[i][0]
                class_row[2] = "coreset0"
                class_row[3] = "coreset0"
                if rb not in overlap_rbs:
                    if sc != 11:
                        continue
                    else:
                        row[2] = "0..11"
                if rb >= cfg.nrbs.value:
                    class_row[2] = "dcoreset0"
                    class_row[3] = "dcoreset0"
            else:
                row[2] = sc = coreset0[i][1]
                row[3] = rb = coreset0[i][0]
                class_row[2] = "coreset0"
                class_row[3] = "coreset0"
                if rb not in overlap_rbs:
                    if sc != 11:
                        continue
                    else:
                        row[2] = "0..11"
                if rb < abs(cfg.offset.value):
                    row[3] = -rb
                    class_row[2] = "dcoreset0"
                    class_row[3] = "dcoreset0"
                else:
                    row[3] = rb - abs(cfg.offset.value)
        data.append(row)
        class_data.append(class_row)

    a1 = None
    x = [["SSB", f"kssb={cfg.kssb.value}", "CORESET#0", "CORESET#0"], 
        [f"subcarrier={cfg.scs_ssb.value}", 
         f"kssb={cfg.kssb.value}", 
         f"subcarrier={cfg.subCarrierSpacingCommon.value}", "Resource Block"]]
    y = None
    num_merge_cols=len(x[0])
    caption = f"38.213 Table 13-8 multiplexing pattern 3: RBs={cfg.nrbs.value}, Offset={cfg.offset.value}"
    table = ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=num_merge_cols)
    document['zone-output'] <= table

def overlap_coreset0_rb_set(ssb, coreset0):
    ret = set()
    for i in ssb.keys():
        if i in coreset0:
            rb = coreset0[i][0]
            ret.add(rb)
    return ret

def overlap_ssb_set(ssb, coreset0):
    ret = set()
    for i in coreset0.keys():
        if i in ssb:
            sc = ssb[i][1]
            ret.add(sc)
    return ret

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"