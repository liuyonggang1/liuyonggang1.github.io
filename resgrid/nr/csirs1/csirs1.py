##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable
import csirs

##########################################################################################################################################

def main(event):
    document['zone-output'].clear()
    main1()
    main2()

def main1():
    csi = csirs.CsiRs(cfg)
    x = [['symbol'] * 14, [i for i in range(14)]]
    a1 = [['subcarrier']]*2
    y = list(range(12))[::-1]
    result = [['' for sym in range(14)] for sc in y]
    for i, o in enumerate(csi.klgrid_list):
        result[o.k][o.l] = str(o.port_idx)
    result = result[::-1]
    document['zone-output'] <= DIV("0: port3000, 1: port3001, ...")
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=result, class_data=result, caption='CSI-RS in one PRB/slot', num_merge_rows=None, num_merge_cols=None)

def main2():
    csi = csirs.CsiRs(cfg)
    nrb = cfg.nrb.value
    period = cfg.periodicity.value
    nslot = 40 if period*2 < 40 else period
    a1 = [["PRB"], ["PRB"]]
    x = [["Slot" for slot in range(nslot)], [slot for slot in range(nslot)]]
    y = [prb for prb in range(nrb)][::-1]
    result = [["" for slot in range(nslot)] for prb in range(nrb)]
    for prb in range(nrb):
        for slot in range(nslot):
            if csi.is_csirs_rb(prb) and csi.is_csirs_slot(slot):
                result[prb][slot] = "csirs"
    result = result[::-1]
    document['zone-output'] <= BR()
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=None, class_data=result, caption='CSI-RS Grid', num_merge_rows=None, num_merge_cols=None)
    

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
