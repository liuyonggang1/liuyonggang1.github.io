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
        start = min(kssb.keys()) - 0 - (cfg.offset.value * 12) * 2
    else:
        start = min(kssb.keys()) - 1 - (cfg.offset.value * 12) * 2
    #
    coreset0 = {}
    for rb in range(cfg.nrbs.value):
        for sc in range(12):
            for half in range(2):
                i = start + rb * 12 * 2 + sc * 2 + half
                coreset0[i] = (rb, sc, half)
    
    top = max([max(ssb.keys()), max(kssb.keys()), max(coreset0.keys())])
    bottom = min([min(ssb.keys()), min(kssb.keys()), min(coreset0.keys())])
    overlap_rbs, marb, nonoverlap_subcarriers = overlap_coreset0_rb_set(ssb, coreset0)
    data = []
    class_data = []
    for i in  range(top, bottom - 1, -1):
        row = [""] * 6
        class_row = [f"blank{i}" for i in range(6)]
        if i in ssb:
            rb, sc, q = ssb[i]
            row[0] = sc
            row[1] = q
            class_row[0] = "ssbsc"
            class_row[1] = f"ssb75 q{q}"
            if sc == 120:
                row[0] = str(sc) + " <span style='font-size: small;'>SS<sub>REF</sub></span>"
                class_row[0] += " ssref"
        if i in kssb:
            k, half = kssb[i]
            row[2] = f"kssb={k}" if k == 0 else f"kssb={k}, {cfg.scs_kssb.value}kHz"
            class_row[2] = "kssb"
        if i in coreset0:
            rb, sc, half = coreset0[i]
            # row[4] = half
            # row[5] = sc
            # row[6] = rb
            # class_row[4] = f"coreset075 h{half}"
            # class_row[5] = "coreset0sc"
            # class_row[6] = "coreset0rb"
            if rb in overlap_rbs:
                row[3] = half
                row[4] = sc
                row[5] = rb
                class_row[3] = f"coreset075 h{half}"
                class_row[4] = "coreset0sc"
                class_row[5] = "coreset0rb"
            elif sc == 11 and half == 1:
                row[3] = ""
                row[4] = "0..11"
                row[5] = f"RB {rb}"
                class_row[3] = "coreset075 "
                class_row[4] = "coreset0sc"
                class_row[5] = "coreset0rb"
            else:
                continue
        data.append(row)
        class_data.append(class_row)

    a1 = None
    x = [["SSB", "SSB", f"kssb={cfg.kssb.value}", "CORESET#0", "CORESET#0", "CORESET#0"], 
         [f"subcarrier={cfg.scs_ssb.value}k", f"subcarrier={cfg.scs_ssb.value}k", 
          f"kssb={cfg.kssb.value}", 
          f"subcarrier={cfg.subCarrierSpacingCommon.value}k", f"subcarrier={cfg.subCarrierSpacingCommon.value}k", "Resource Block"]]
    y = None
    caption = f"38.213 Table 13-10 Pattern 1: RBs={cfg.nrbs.value}, Offset={cfg.offset.value}"
    table = ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=len(x[0]))
    document['zone-output'] <= table

def overlap_coreset0_rb_set(ssb, coreset0):
    ret = set()
    for i in ssb.keys():
        if i in coreset0:
            rb = coreset0[i][0]
            ret.add(rb)
    ma = max(ret)
    nonoverlap_subcarriers = []
    for i, (rb, sc, half) in coreset0.items():
        if rb == ma:
            if half == 0 and i not in ssb:
                nonoverlap_subcarriers.append(sc)
    return ret, ma, nonoverlap_subcarriers


##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"