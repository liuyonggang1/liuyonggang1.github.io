##########################################################################################################################################
from browser import document, alert
from browser.html import *
import ztable

##########################################################################################################################################

def main(event):
    document['zone-output'].clear()
    create_table(0, 14)
    create_table(1, 14)
    create_table(2, 14)
    create_table(2, 12)
    create_table(3, 14)
    create_table(4, 14)

def create_table(mu, num_symb=14):
    num_sf = 1
    num_slot = 2**mu
    scs = 15 * num_slot
    ms_per_slot = 1/num_slot
    ms_per_symb = ms_per_slot/num_symb
    ms_per_symb = int(ms_per_symb * 1000 * 1000)
    ms_per_symb = f"{ms_per_symb}ns"
    rb_khz = scs*12
    

    a1 = [['subcarrier']]*3
    a1 = None
    sf_row_x = [f"subframe" for sf in range(num_sf) for slot in range(num_slot) for symb in range(num_symb)]
    slot_row_x = [f"slot{slot}" for sf in range(num_sf) for slot in range(num_slot) for symb in range(num_symb)]
    symb_row_x = [hex(symb)[-1] for sf in range(num_sf) for slot in range(num_slot) for symb in range(num_symb)]
    # x = [sf_row_x, slot_row_x, symb_row_x]
    x = [slot_row_x, symb_row_x]
    x = [slot_row_x]
    
    sc_col_rb = [f"{scs}kHz<br>*<br>12" for sc in reversed(range(12))]
    sc_col_rb = [f"{rb_khz}<br>kHz<br>" for sc in reversed(range(12))]
    # sc_col_y = [f"{sc}" for sc in reversed(range(12))]
    # y = [sc_col_rb, sc_col_y]
    y = [sc_col_rb]
    
    class_data = [[f'mu{mu}-{num_symb} slot{col//num_symb%10%2}' for col in range(num_sf*num_slot*num_symb)] for row in range(12)]
    caption = f"&mu;={mu}, scs={scs}kHz, 1sf=(1ms, {num_slot}slot, {num_symb*num_slot}symbol), 1slot={ms_per_slot}ms, 1symbol={ms_per_symb}"
    
    document['zone-output'] <= ztable.create_htable(a1=a1, x=x, y=y, data=None, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)
    
    
##########################################################################################################################################
main(None)

