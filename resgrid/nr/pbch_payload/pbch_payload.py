##########################################################################################################################################
from browser import document
from browser.html import *
import ztable

##########################################################################################################################################

def main(event):
    document['zone-output'].clear()
    ol = OL()
    document['zone-output'] <= ol
    ol <= LI("FR1 PBCH Payload")
    ol <= create_table1()

    ol <= BR()
    ol <= LI("FR2 PBCH Payload")
    ol <= create_table2()

    ol <= BR()
    ol <= LI("PBCH Payload Interleaver, bit position")
    ol <= create_table3()
    
def is_sfn_bit(i):
    return  1 <= i <= 6 or 24 <= i <= 27

def is_hf_bit(i):
    return i == 28

def is_issb_bit(i):
    return 29 <= i <= 31

def is_kssb_bit(i):
    return 8 <= i <= 11 or i == 29

def is_kssb_bit_fr2(i):
    return 8 <= i <= 11

def is_reserved_bit(i):
    return i in [30, 31] 

def is_controlResourceSetZero_bits(i):
    return 13 <= i <= 16

def is_searchSpaceZero_bits(i):
    return 17 <= i <= 20

def create_table1():
    nbits = 32
    x = []
    for i in range(nbits):
        if is_sfn_bit(i):
            x.append("SFN")
        elif is_hf_bit(i):
            x.append("HRF")
        elif is_kssb_bit(i):
            x.append("k<sub>SSB</sub>")
        elif is_reserved_bit(i):
            x.append("R")
        elif is_controlResourceSetZero_bits(i):
            x.append("controlResourceSetZero")
        elif is_searchSpaceZero_bits(i):
            x.append("searchSpaceZero")
        elif i == 7:
            x.append("SCS")
        elif i == 21:
            x.append("Bar")
        elif i == 22:
            x.append("I")
        elif i == 23:
            x.append("S")
        else:
            x.append("")
    data = [[i for i in range(nbits)]]
    a1 = ["IE"]
    y = ["Bit"]
    class_data = []
    for i in range(nbits):
        if i < 24:
            class_data.append("msg_bits")
        else:
            class_data.append("additional_timing_bits")
    class_data = [class_data]
    caption = None
    return ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)

def create_table2():
    nbits = 32
    x = []
    for i in range(nbits):
        if is_sfn_bit(i):
            x.append("SFN")
        elif is_hf_bit(i):
            x.append("HRF")
        elif is_kssb_bit_fr2(i):
            x.append("k<sub>SSB</sub>")
        elif is_issb_bit(i):
            x.append("i<sub>SSB</sub>")
        elif is_controlResourceSetZero_bits(i):
            x.append("controlResourceSetZero")
        elif is_searchSpaceZero_bits(i):
            x.append("searchSpaceZero")
        elif i == 7:
            x.append("SCS")
        elif i == 21:
            x.append("Bar")
        elif i == 22:
            x.append("I")
        elif i == 23:
            x.append("S")
        else:
            x.append("")
    data = [[i for i in range(nbits)]]
    a1 = ["IE"]
    y = ["Bit"]
    class_data = ["" for i in range(nbits)]
    for i in range(nbits):
        if i < 24:
            class_data[i] = "msg_bits"
        else:
            class_data[i] = "additional_timing_bits"

        if is_sfn_bit(i):
            class_data[i] = "sfn_bits"
        elif is_hf_bit(i):
            class_data[i] = "hrf_bits"
        elif is_issb_bit(i):
            class_data[i] = "issb_bits"
    class_data = [class_data]
    caption = None
    return ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)

def create_table3():
    G = {0: 16, 1: 23,  2: 18,  3:17,
         4: 8,  5: 30,  6: 10,  7: 6,
         8: 24, 9: 7,   10: 0,  11: 5,
         12: 3, 13: 2,  14: 1,  15: 4,
         16: 9, 17: 11, 18: 12, 19: 13,
         20:14, 21: 15, 22: 19, 23: 20,
         24:21, 25: 22, 26: 25, 27: 26,
         28:27, 29: 28, 30: 29, 31: 31}
    nbits = 32
    j_sfn = 0
    j_hrf = 10
    j_ssb = 11
    j_other = 14
    x = [i for i in range(nbits)]
    a = ["" for i in range(nbits)]
    class_a = ["" for i in range(nbits)]
    for i in range(nbits):
        if is_sfn_bit(i):
            g = G[j_sfn]
            a[g] = i
            class_a[g] = "sfn_bits"
            j_sfn += 1
        elif is_hf_bit(i):
            g = G[j_hrf]
            a[g] = i
            class_a[g] = "hrf_bits"
        elif is_issb_bit(i):
            g = G[j_ssb]
            a[g] = i
            class_a[g] = "issb_bits"
            j_ssb += 1
        else:
            g = G[j_other]
            a[g] = i
            j_other += 1
    data = [a]
    a1 = ["a bar"]
    y = ["a"]
    class_data = [class_a]
    caption = None
    return ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)

##########################################################################################################################################
main(None)

