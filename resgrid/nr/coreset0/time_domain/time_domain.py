##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable

sup_sub_template = "{word}<span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"
s00 = sup_sub_template.format(word="slot", sup="Frame", sub="SSB_SCS")
s01 = sup_sub_template.format(word="symbol", sup="Slot", sub="SSB")
s02 = sup_sub_template.format(word="symbol", sup="HF", sub="SSB_SCS")

s10 = sup_sub_template.format(word="slot", sup="Frame", sub="C0_SCS")
s11 = sup_sub_template.format(word="symbol", sup="Slot", sub="C0")

##########################################################################################################################################
def main(event=None):
    document['zone-output'].clear()
    max_scs = max(cfg.scs_ssb.value, cfg.subCarrierSpacingCommon.value)
    ssb = TimeSequence(cfg.scs_ssb.value, max_scs)

    sfn_row = [g.sfn for g in ssb.grids]
    sf_row = [g.sf for g in ssb.grids]
    ssb_slot_row = [g.sf * ssb.num_slots + g.slot for g in ssb.grids]
    ssb_symb_row = [g.symbol for g in ssb.grids]
    ssb_symb_hf_row = [g.sf % 5 * ssb.num_slots * ssb.num_symbols + g.slot * ssb.num_symbols + g.symbol for g in ssb.grids]
    ssb_index_row = cal_ssb_index_ssb_row(cfg.case.value, ssb_symb_hf_row)

    c0 = TimeSequence(cfg.subCarrierSpacingCommon.value, max_scs)

    c0_slot_row = cal_c0_slot_row(c0) #[g.sf * c0.num_slots + g.slot for g in c0.grids]
    c0_symb_row = [g.symbol for g in c0.grids]

    x = ["SFN", "Subframe", s00, s01, s02, "i<sub>SSB</sub>", s10, s11]
    data = [sfn_row, 
            sf_row, 
            ssb_slot_row, 
            ssb_symb_row, 
            ssb_symb_hf_row, 
            ssb_index_row,
            c0_slot_row, 
            c0_symb_row]
    sfn_class_row = [f"sfn sfn{g.sfn % 2}" for g in ssb.grids]
    sf_class_row = [f"sf hf{g.sf // 5}" for g in ssb.grids]
    ssb_slot_class_row = ["" for _ in ssb_slot_row]
    ssb_symb_class_row = ["" for _ in ssb_symb_row]
    ssb_symb_hf_class_row = ["" for _ in ssb_symb_hf_row]
    ssb_index_class_row = ["" for _ in ssb_index_row]
    c0_slot_class_row = ["" for _ in c0_slot_row]
    c0_symb_class_row = ["" for _ in c0_symb_row]
    class_data = [sfn_class_row, 
                    sf_class_row, 
                    ssb_slot_class_row, 
                    ssb_symb_class_row, 
                    ssb_symb_hf_class_row, 
                    ssb_index_class_row,
                    c0_slot_class_row, 
                    c0_symb_class_row]


    data = ztable.transpose(data)
    class_data = ztable.transpose(class_data)
    # class_data = None
    y = None
    a1 = None
    caption = None
    num_merge_row = len(data)
    num_merge_row = None
    num_merge_cols = None
    num_merge_cols = len(data[0])
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=num_merge_row, num_merge_cols=num_merge_cols)
    alert("done")


class TimeSequence:
    def __init__(self, scs, max_scs):
        mu = scs // 15 - 1
        sfns = 10
        sfs = 10
        slots = 2 ** mu
        symbols = 14
        cells = max_scs // scs
        from collections import namedtuple
        Grid = namedtuple('Grid', ["sfn", "sf", "slot", "symbol", "cell"])
        grids = [Grid(sfn, sf, slot, symbol, cell) for sfn in range(sfns) for sf in range(sfs) for slot in range(slots) for symbol in range(symbols) for cell in range(cells)]
        self.scs, self.mu, self.num_sfns, self.num_sfs, self.num_slots, self.num_symbols, self.num_cells = scs, mu, sfns, sfs, slots, symbols, cells
        self.grids = grids
        self.num_slots_per_frame = self.num_sfs * self.num_slots

def cal_ssb_index_ssb_row(case, ssb_symb_hf_row):
    if case in ("A1", "C1"):
        i_lst = [2, 8]
        n_lst = range(2)
        factor = 14
    if case in ("A2", "C2"):
        i_lst = [2, 8]
        n_lst = range(4)
        factor = 14
    if case == "B1":
        i_lst = [4, 8, 16, 20]
        n_lst = range(1)
        factor = 28
    if case == "B2":
        i_lst = [4, 8, 16, 20]
        n_lst = range(2)
        factor = 28

    s2i = {}  # symbol to ssb index
    index = 0
    for n in n_lst:
        for i in i_lst:
            start = i + factor * n
            for s in range(4):
                sy = start + s
                s2i[sy] = index
            index += 1
    ret = [s2i.get(sy, "") for sy in ssb_symb_hf_row]
    return ret

def cal_n0(c0):
    import math
    num_ssbs = 4 if cfg.case.value[-1] == "1" else 8
    d = {}
    print(cfg.O.value, cfg.M.value, c0.num_slots, c0.num_slots_per_frame)
    for i in range(num_ssbs):
        cond0 = (cfg.O.value * c0.num_slots + math.floor(i * cfg.M.value)) / c0.num_slots_per_frame
        print("cond0", i, cond0)
        cond0 = math.floor(cond0)
        cond0 = cond0 % 2 == 0
        cond1 = (cfg.O.value * c0.num_slots + i * cfg.M.value) / c0.num_slots_per_frame
        print("cond1", i, cond1)
        cond1 = math.floor(cond1)
        cond1 = cond1 % 2 == 1
        for sfn in range(c0.num_sfns):
            if (cond0 and sfn % 2 == 0) or (cond1 and sfn % 2 == 1):
                n0 = (cfg.O.value * c0.num_slots + math.floor(i * cfg.M.value)) % c0.num_slots_per_frame
                d[(sfn, n0)] = i
    return d

def cal_c0_slot_row(c0):
    d = cal_n0(c0)
    ret = []
    for g in c0.grids:
        slot = g.sf * c0.num_slots + g.slot
        if (g.sfn, slot) in d:
            i = d[(g.sfn, slot)]
            s = f"{slot}<br>n<sub>0</sub><br>i<sub>SSB</sub>={i}"
            ret.append(s)
        else:
            ret.append(slot)
    return ret

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"