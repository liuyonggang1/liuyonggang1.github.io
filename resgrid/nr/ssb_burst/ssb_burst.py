##########################################################################################################################################
from browser import document
from browser.html import *
import ztable

##########################################################################################################################################

def main(event):
    document['zone-output'].clear()
    ol = OL()
    document['zone-output'] <= ol
    ol <= LI("Case A: 15 kHz SCS, FR1 <= 3GHz")
    ol <= create_table2(num_slot_per_sf=1, max_n=1, ilst=[2, 8], factor=14)
    
    ol <= LI("Case A: 15 kHz SCS, FR1 > 3GHz")
    ol <= create_table2(num_slot_per_sf=1, max_n=3, ilst=[2, 8], factor=14)
    
    ol <= LI("Case B: 30 kHz SCS, FR1 <= 3GHz")
    ol <= create_table2(num_slot_per_sf=2, max_n=0, ilst=[4, 8, 16, 20], factor=28)
    
    ol <= LI("Case B: 30 kHz SCS, FR1 > 3GHz")
    ol <= create_table2(num_slot_per_sf=2, max_n=1, ilst=[4, 8, 16, 20], factor=28)
    
    ol <= LI("Case C: 30 kHz SCS, paired FR1 <= 3GHz OR unpaired FR1 <= 2.3GHz")
    ol <= create_table2(num_slot_per_sf=2, max_n=1, ilst=[2, 8], factor=14)
    
    ol <= LI("Case C: 30 kHz SCS, paired FR1 > 3GHz OR unpaired FR1 > 2.3GHz")
    ol <= create_table2(num_slot_per_sf=2, max_n=3, ilst=[2, 8], factor=14)

    ol <= LI("Case D: 120 kHz SCS, FR2")
    ol <= create_table2(num_slot_per_sf=8, max_n=18, ilst=[4, 8, 16, 20], factor=28)
    
    ol <= LI("Case E: 240 kHz SCS, FR2")
    ol <= create_table2(num_slot_per_sf=16, max_n=8, ilst=[8, 12, 16, 20, 32, 36, 40, 44], factor=56)


def set_class(lst, idx):
    lst[idx] = "start"
    for i in (1,2,3):
        lst[idx+i] = "ssb"

def create_table(num_slot_per_sf=None, max_n=None, ilst=None, factor=None):
    num_symb_per_slot = 14
    num_symb_per_sf = num_symb_per_slot * num_slot_per_sf    
    total_sf = 5
    total_symb = total_sf * num_slot_per_sf * num_symb_per_slot
    num_symb = total_symb
    
    row_hf = ["half frame" for i in range(num_symb)]
    row_sf = [f"subframe {i//num_symb_per_sf}" for i in range(num_symb)]
    row_slot = [f"slot {i//num_symb_per_slot}" for i in range(num_symb)]
    row_symb = [i%num_symb_per_slot for i in range(num_symb)]
    
    data = [[i for i in range(num_symb)]]
    class_data = ["" for i in range(num_symb)]
    for n in range(max_n+1):
        for i in ilst:
            idx = i + factor*n
            set_class(class_data, idx)
    class_data = [class_data]
    a1 = None
    x = [row_hf, row_sf, row_slot, row_symb]
    x = [row_sf, row_slot]
    x = [row_sf]
    y = None
    caption = None
    return ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)

def set_class(lst, idx):
    lst[idx] = "start"
    for i in (1,2,3):
        lst[idx+i] = "ssb"

def create_table2(num_slot_per_sf=None, max_n=None, ilst=None, factor=None):
    num_symb_per_slot = 14
    num_symb_per_sf = num_symb_per_slot * num_slot_per_sf    
    total_sf = 5
    # total_symb = total_sf * num_slot_per_sf * num_symb_per_slot
    # num_symb = total_symb
    
    data = [[row*num_symb_per_slot+i for i in range(num_symb_per_slot)] for row in range(total_sf*num_slot_per_sf)]
    class_data = [["" for i in range(num_symb_per_slot)] for row in range(total_sf*num_slot_per_sf)]
    for n in range(max_n+1):
        for i in ilst:
            idx = i + factor*n
            r, c = divmod(idx, num_symb_per_slot)
            class_data[r][c] = "start"
            for j in (1,2,3):
                r, c = divmod(idx+j, num_symb_per_slot)
                class_data[r][c] = "ssb"
    
    a1 = [["subframe", "slot"]]
    x = [["symbol"]*num_symb_per_slot]
    y0 = [sf for sf in range(total_sf) for slot in range(num_slot_per_sf)]
    y1 = [slot for sf in range(total_sf) for slot in range(num_slot_per_sf)]
    y = [y0, y1]
    if num_slot_per_sf == 1:
        a1 = [["subframe"]]
        y = [y0]
     
    caption = "SSB Burst half frame"
    return ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)



##########################################################################################################################################
main(None)

