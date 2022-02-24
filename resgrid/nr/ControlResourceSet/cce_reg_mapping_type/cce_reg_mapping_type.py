##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable
# import math
# import collections
# from fractions import gcd

def lcm(a, b):
    return (a*b) // gcd(a, b)

##########################################################################################################################################
def main(event=None):
    output = document['zone-output']
    output.clear()
    cfg = cfg0.get_cfg()
    main1(output, cfg)
    main2(output, cfg)

def main1(output, cfg):
    a1 = None
    x0 = [f"REG" for symbol in range(cfg.n_symb_coreset)]
    x1 = [f"symbol<sub>{symbol}</sub>" for symbol in range(cfg.n_symb_coreset)]
    x_sep0 = [" "]
    x_sep1 = [" "]
    x2 = [f"REG Bundle" for symbol in range(cfg.n_symb_coreset)]
    x3 = [f"symbol<sub>{symbol}</sub>" for symbol in range(cfg.n_symb_coreset)]

    x4 = [f"CCE" for symbol in range(cfg.n_symb_coreset)]
    x5 = [f"symbol<sub>{symbol}</sub>" for symbol in range(cfg.n_symb_coreset)]
    x = [x0 + x_sep0 + x2 + x_sep0 + x4, x1 + x_sep1 + x3 + x_sep1 + x5]

    y0 = [f"RB<sub>{rb}</sub>" for rb in range(cfg.n_rb_coreset)][::-1]
    y = [y0]
    data_reg = [[rb * cfg.n_symb_coreset + symbol for symbol in range(cfg.n_symb_coreset)] for rb in range(cfg.n_rb_coreset)][::-1]
    data_sep = [[" "] for rb in range(cfg.n_rb_coreset)][::-1]
    data_reg_bundle = [[reg // cfg.reg_bundle_size for reg in row] for row in data_reg]
    #
    data_cce = [[cfg0.reg_to_cce(reg) for reg in row] for row in data_reg]
    #
    data = []
    for a, b, c, d in zip(data_reg, data_sep, data_reg_bundle, data_cce):
        data.append(a+b+c+b+d)
    class_data = None
    caption = None
    num_merge_row = None
    num_merge_cols = None
    nrows = len(data) + len(x)
    ncols = len(data[0]) + len(y)
    num_merge_row = nrows
    num_merge_cols = ncols
    output <= ztable.create_htable(a1=a1, 
                                   x=x, 
                                   y=y, 
                                   data=data, 
                                   class_data=class_data, 
                                   caption=caption, 
                                   num_merge_rows=num_merge_row, 
                                   num_merge_cols=num_merge_cols)

def main2(output, cfg):
    output <= BR()
    output <= HR()
    nrows = cfg.interleaver_size
    nbundles = cfg.n_bundles_coreset
    ncols = nbundles // nrows
    x = ["REG_Bundle<sub>cce</sub>" for _ in range(ncols)]
    data = []
    class_data = []
    for row in range(nrows):
        one = []
        class_one = []
        for col in range(ncols):
            b = row * ncols + col
            cce = cfg0.bundle_to_cce[b]
            s = f"{b}<sub>{cce}</sub>"
            one.append(s)
            cl = f"cce{cce%4}"
            class_one.append(cl)
            # one.append(b)
            # one.append(cce)
        data.append(one)
        class_data.append(class_one)
    output <= ztable.create_htable(a1=None, 
                                   x=x, 
                                   y=None, 
                                   data=data, 
                                   class_data=class_data, 
                                   caption=None, 
                                   num_merge_rows=None, 
                                   num_merge_cols=None)
    




##########################################################################################################################################
cfg0 = para.Config()
cfg0.start(main)
# main()
# document["main"].style.display = "none"