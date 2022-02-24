##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable
import math

def lcm(a, b):
    L = max(a, b)
    S = min(a, b)
    y = L
    while y % S != 0:
        y += L
    return y

def gcd(a, b):
    y = min(a, b)
    while a % y != 0 or b % y != 0:
        y -= 1
    return y

##########################################################################################################################################
def main(event=None):
    document['zone-output'].clear()
    a1 = None
    x = None
    y = None
    data = None
    class_data = None
    caption = None
    num_merge_row = None
    num_merge_cols = None

    cfg = cfg0.get_cfg()
    n_slots_frame = cfg.n_slots_frame

    a = lcm(cfg.ks, n_slots_frame)
    n_frames = max(math.ceil(2 * a / n_slots_frame), 2)
    seq = [(nf, slot) for nf in range(n_frames) for slot in range(n_slots_frame)]

    a1 = [[" "], ["slot"]]
    x0 = [f"frame {t[0]}" for t in seq]
    x1 = [t[1] for t in seq]
    x = [x0, x1]
    y = ["PDCCH Occasion"]
    row0 = list(range(len(seq)))
    data = [row0]

    class_data = [["" for col in row] for row in data]

    for i, (nf, slot) in enumerate(seq):
        if i >= cfg.os and (nf * n_slots_frame + slot - cfg.os) % cfg.ks == 0:
            class_data[0][i] = "occ0"
            for j in range(1, cfg.ts):
                if (i+j) < len(seq):
                    class_data[0][i+j] = "occ1"

    # num_merge_row = len(data)
    # num_merge_cols = len(data[0])
    caption = "Slots for PDCCH Occasions"
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=num_merge_row, num_merge_cols=num_merge_cols)
    main2()

def main2():
    pass
    output = document['zone-output']
    output <= BR()
    output <= HR()

    a1 = None
    x = None
    y = None
    data = None
    class_data = None
    caption = None
    num_merge_row = None
    num_merge_cols = None

    cfg = cfg0.get_cfg()
    x0 = [f"Symbol" for symbol in range(14)]
    x1 = [f"{symbol}" for symbol in range(14)]
    x = [x0, x1]

    cfg.monitoringSymbolsWithinSlot = cfg.monitoringSymbolsWithinSlot.replace(" ", "")
    first_symbols = [i for i, v in enumerate(cfg.monitoringSymbolsWithinSlot) if v == "1"]
    y = [f"Occasion {i}" for i, _ in enumerate(first_symbols)]

    data = [["" for col in range(14)] for row in first_symbols]
    class_data = [["" for col in row] for row in data]

    for row, first_symbol in enumerate(first_symbols):
        for i in range(cfg.n_symb_coreset):
            col = first_symbol + i
            class_data[row][col] = "occ0"
    # num_merge_row = len(data)
    # num_merge_cols = len(data[0])
    caption = "PDCCH Occasions in a slot"
    output <= ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=num_merge_row, num_merge_cols=num_merge_cols)


##########################################################################################################################################
cfg0 = para.Config()
cfg0.start(main)
# main()
# document["main"].style.display = "none"