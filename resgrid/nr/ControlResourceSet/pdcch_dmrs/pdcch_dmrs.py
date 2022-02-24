##########################################################################################################################################
from browser import document, alert
from browser.html import *
# import para
import ztable
# import math

##########################################################################################################################################
def main(event=None):
    output = document['zone-output']
    output.clear()
    n = 0
    tt = TABLE()
    tr = TR()
    tt <= tr
    output <= tt
    for nsymbs in [1, 2, 3]:
        x = [[f"l<sub>{i}</sub>" for i in range(nsymbs)]]
        y0 = ["k"] * 12
        y1 = list(range(12))[::-1]
        y = [y0, y1]
        class_data = [["" for _ in range(nsymbs)] for k in range(12)]
        for k_prime in [0, 1, 2]:
            k = n * 12 + 4 * k_prime + 1
            class_data[k] = ["dmrs"] * nsymbs
        class_data = class_data[::-1]
        caption = f"{nsymbs} symbol CORESET"
        td = TD()
        div = DIV()
        div.class_name = "out_div"
        td <= div
        div <= ztable.create_htable(x=x, y=y, 
                                   class_data=class_data, 
                                   caption=caption)
        tr <= td


##########################################################################################################################################
# cfg0 = para.Config()
# cfg0.start(main)
main()
# document["main"].style.display = "none"