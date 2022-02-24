##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable

sup_sub_template = "{word}<span class='supsub'><sup class='superscript'>{sup}</sup><sub class='subscript'>{sub}</sub></span>"
s00 = sup_sub_template.format(word="slot", sup="Frame", sub="SSB")
s01 = sup_sub_template.format(word="symbol", sup="", sub="SSB")
# s02 = sup_sub_template.format(word="symbol", sup="HF", sub="SSB_SCS")

s10 = sup_sub_template.format(word="slot", sup="Frame", sub="C0")
s11 = sup_sub_template.format(word="symbol", sup="", sub="C0")

##########################################################################################################################################
def main(event=None):
    document['zone-output'].clear()

    max_scs = max(cfg.scs_ssb.value, cfg.subCarrierSpacingCommon.value)
    ssb = TimeSequence(cfg.scs_ssb.value, max_scs)

    sf_row = [g.sf for g in ssb.grids]
    ssb_slot_row = [g.sf * ssb.num_slots + g.slot for g in ssb.grids]
    ssb_symb_row = [g.symbol for g in ssb.grids]
    ssb_symb_class_row = mask_ssb(ssb_symb_row)

    c0 = TimeSequence(cfg.subCarrierSpacingCommon.value, max_scs)

    c0_slot_row = [g.sf * c0.num_slots + g.slot for g in c0.grids]
    c0_symb_row = [g.symbol for g in c0.grids]
    c0_symb_class_row = mask_c0_symbol(ssb_symb_row, c0_symb_row)

    x = ["Subframe", s00, s01, s11, s10]
    data = [sf_row, 
            ssb_slot_row, 
            ssb_symb_row, 
            c0_symb_row, 
            c0_slot_row]
    sf_class_row = [f"sf{g.sf % 2}" for g in ssb.grids]
    ssb_slot_class_row = [f"ssbslot{slot % 2}" for slot in ssb_slot_row]
    c0_slot_class_row = [f"c0slot{slot % 2}" for slot in c0_slot_row]
    # c0_symb_class_row = ["" for _ in c0_symb_row]
    class_data = [  sf_class_row, 
                    ssb_slot_class_row, 
                    ssb_symb_class_row, 
                    c0_symb_class_row, 
                    c0_slot_class_row]


    data = ztable.transpose(data)
    class_data = ztable.transpose(class_data)
    y = None
    a1 = None
    caption = "38.213 Table 13-14, pattern 2, {240, 120} kHz<br>illustrated with 1st, 2nd, 3rd subframe"
    num_merge_row = len(data)
    num_merge_row = None
    num_merge_cols = None
    num_merge_cols = len(data[0])
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=num_merge_row, num_merge_cols=num_merge_cols)
    # alert("done")


class TimeSequence:
    def __init__(self, scs, max_scs):
        from math import log2
        mu = int(log2(scs // 15))
        sfs = 3
        slots = 2 ** mu
        symbols = 14
        cells = max_scs // scs
        from collections import namedtuple
        Grid = namedtuple('Grid', ["sf", "slot", "symbol", "cell"])
        grids = [Grid(sf, slot, symbol, cell) for sf in range(sfs) for slot in range(slots) for symbol in range(symbols) for cell in range(cells)]
        self.scs, self.mu, self.num_sfs, self.num_slots, self.num_symbols, self.num_cells = scs, mu, sfs, slots, symbols, cells
        self.grids = grids

def mask_ssb(ssb_symb_row):
    i_lst = [8, 12, 16, 20, 32, 36, 40, 44]
    n_lst = [0, 1, 2, 3] + [5, 6, 7, 8]
    factor = 56
    s2i = {}  # symbol to ssb index
    s2i_start = {}  # symbol to ssb index
    i_ssb = 0
    for n in n_lst:
        for i in i_lst:
            start = i + factor * n
            s2i_start[start] = i_ssb
            for j in range(4):
                s2i[start + j] = i_ssb
            i_ssb += 1
    for i, s in enumerate(ssb_symb_row):
        i_ssb = s2i_start.get(i, "")
        if i_ssb != "":
            ssb_symb_row[i] = f"{s} i<sub>ssb</sub>={i_ssb}"

    ssb_symb_class_row = ["" for _ in ssb_symb_row]
    for i, s in enumerate(ssb_symb_row):
        i_ssb = s2i.get(i, "")
        if i_ssb != "":
            ssb_symb_class_row[i] = f"issb{i_ssb % 2}"
    return ssb_symb_class_row

def mask_c0_symbol(ssb_symb_row, c0_symb_row):
    c0_symb_class_row = ["" for _ in c0_symb_row]
    for i, s in enumerate(ssb_symb_row):
        if isinstance(s, str) and "ssb" in s:
            i_ssb = int(s.split("=")[-1].strip())
            first = [0, 1, 2, 3, 12, 13, 0, 1][i_ssb % 8]
            i_symb0 = i - c0_symb_row[i] * 2 + first * 2
            if (i_ssb % 8) in (4, 5):
                i_symb0 -= 28
            t = f"{c0_symb_row[i_symb0]} i<sub>ssb</sub>={i_ssb}"
            c0_symb_row[i_symb0] = t
            c0_symb_row[i_symb0+1] = t
            c0_symb_class_row[i_symb0] = f"issb{i_ssb % 2}" 
            c0_symb_class_row[i_symb0+1] = f"issb{i_ssb % 2}" 

    return c0_symb_class_row

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
# main()
# document["main"].style.display = "none"