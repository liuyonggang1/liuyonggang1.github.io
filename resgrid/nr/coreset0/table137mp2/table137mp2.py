##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable

##########################################################################################################################################
def main(event=None):
    document['zone-output'].clear()
    ssb = {sc * 4 + q: (sc//12, sc, q) for sc in range(240)[::-1] for q in range(4)[::-1]}
    #
    kssb = {}
    if cfg.kssb.value == 0:
        kssb[2] = (0, 1)
        kssb[1] = (0, 0)
    else:
        start_row = 1
        kssb_row = 0
        for sc in range(1, cfg.kssb.value + 1):
            for half in (1, 0):
                # i = sc * 2 + half
                kssb[start_row - kssb_row] = (sc, half)
                kssb_row += 1
    if cfg.kssb.value == 0:
        if cfg.offset.value > 0:
            start = min(kssb.keys()) - 0 - (cfg.offset.value * 12) * 2
        else:
            start = min(kssb.keys()) - 0 - (0 * 12) * 2
    else:
        if cfg.offset.value > 0:
            start = min(kssb.keys()) - 1 - (cfg.offset.value * 12) * 2
        else:
            start = min(kssb.keys()) - 1 - (0 * 12) * 2
    #
    coreset0 = {}
    if cfg.offset.value > 0:
        disp_nrbs = cfg.nrbs.value+2
    else:
        disp_nrbs = abs(cfg.offset.value) + cfg.nrbs.value
    for rb in range(disp_nrbs):
        for sc in range(12):
            for half in range(2):
                i = start + rb * 12 * 2 + sc * 2 + half
                coreset0[i] = (rb, sc, half)
    
    top = max([max(ssb.keys()), max(kssb.keys()), max(coreset0.keys())])
    bottom = min([min(ssb.keys()), min(kssb.keys()), min(coreset0.keys())])
    overlap_rbs = overlap_coreset0_rb_set(ssb, coreset0)
    data = []
    class_data = []
    for i in  range(top, bottom - 1, -1):
        row = [""] * 7
        class_row = [f"blank{i}" for i in range(7)]
        if i in ssb:
            rb, sc, q = ssb[i]
            row[0] = rb
            row[1] = str(sc)
            if sc == 120:
                row[1] += " <span style='font-size: small;'>SS<sub>REF</sub></span>"
            row[2] = q
            class_row[0] = "ssbrb"
            class_row[1] = "ssbsc"
            if sc == 120:
                class_row[1] += " ssref"
            class_row[2] = f"ssb75 q{q}"
        if i in kssb:
            k, half = kssb[i]
            if k == 0:
                row[3] = f"kssb={k}"
            else:
                row[3] = f"kssb={k}, {cfg.scs_kssb.value}kHz"
            class_row[3] = "kssb"
        if i in coreset0:
            rb, sc, half = coreset0[i]
            # row[4] = half
            # row[5] = sc
            # row[6] = rb
            # class_row[4] = f"coreset075 h{half}"
            # class_row[5] = "coreset0sc"
            # class_row[6] = "coreset0rb"
            if cfg.offset.value > 0:
                if rb in overlap_rbs or rb >= cfg.nrbs.value:
                    row[4] = half
                    row[5] = sc
                    row[6] = rb
                    class_row[4] = f"coreset075 h{half}"
                    class_row[5] = "coreset0sc"
                    class_row[6] = "coreset0rb"
                    if rb >= cfg.nrbs.value:
                        class_row[4] = f"dcoreset075 h{half}"
                        class_row[5] = "dcoreset0sc"
                        class_row[6] = "dcoreset0rb"
                elif sc == 11 and half == 1:
                    row[4] = ""
                    row[5] = "0..11"
                    row[6] = rb
                    class_row[4] = "coreset075 "
                    class_row[5] = "coreset0sc"
                    class_row[6] = "coreset0rb"
                else:
                    continue
            if cfg.offset.value < 0:
                if rb in overlap_rbs or rb < abs(cfg.offset.value):
                    row[4] = half
                    row[5] = sc
                    row[6] = rb
                    class_row[4] = f"coreset075 h{half}"
                    class_row[5] = "coreset0sc"
                    class_row[6] = "coreset0rb"
                    if rb < abs(cfg.offset.value):
                        row[6] = -rb
                        class_row[4] = f"dcoreset075 h{half}"
                        class_row[5] = "dcoreset0sc"
                        class_row[6] = "dcoreset0rb"
                elif sc == 11 and half == 1:
                    row[4] = ""
                    row[5] = "0..11"
                    row[6] = rb - abs(cfg.offset.value)
                    class_row[4] = "coreset075 "
                    class_row[5] = "coreset0sc"
                    class_row[6] = "coreset0rb"
                else:
                    continue
        data.append(row)
        class_data.append(class_row)

    a1 = None
    x = [["SSB", "SSB", "SSB", f"kssb={cfg.kssb.value}", "CORESET#0", "CORESET#0", "CORESET#0"], 
         [f"subcarrier={cfg.scs_ssb.value}k", f"subcarrier={cfg.scs_ssb.value}k", f"subcarrier={cfg.scs_ssb.value}k", 
          f"kssb={cfg.kssb.value}", 
          f"subcarrier={cfg.subCarrierSpacingCommon.value}k", f"subcarrier={cfg.subCarrierSpacingCommon.value}k", "Resource Block"]]
    y = None
    caption = f"38.213 Table 13-7 Pattern 1: RBs={cfg.nrbs.value}, Offset={cfg.offset.value}"
    table = ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=len(x[0]))
    document['zone-output'] <= table

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