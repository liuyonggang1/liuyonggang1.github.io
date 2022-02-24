##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable
import math

##########################################################################################################################################
def main(event=None):
    output = document['zone-output']
    output.clear()
    cfg = cfg0.get_cfg()
    main1(output, cfg)
    main2(output, cfg)

def main1(output, cfg):
    a1 = None
    x0 = ["CCE"] * cfg.n_cces
    x1 = [cce for cce in range(cfg.n_cces)]
    x = [x0, x1]
    y = ["AL1", " ", "AL2", " ", "AL4", " ", "AL8", " ", "AL16"]
    data = []
    class_data = []
    for AL in [1, 2, 4, 8, 16]:
        data_row = []
        for cce in range(cfg.n_cces):
            n = cce // AL
            data_row.append(" "*n)
        data.append(data_row)
        class_data.append([""]*cfg.n_cces)
    #
    candidates = cal_candidates(cfg)
    total = 0
    for row, AL in enumerate([1, 2, 4, 8, 16]):
        for m, first_cce in candidates[AL]:
            for ci in range(AL):
                col = first_cce + ci
                data[row][col] = f"{m}<sub><sub>{total}</sub></sub>"
            total += 1
    #
    sep_row = [""]*cfg.n_cces
    sep_class_row = ["sep_row"]*cfg.n_cces
    nd = [data[0]]
    for row in data[1:]:
        nd.append(sep_row)
        nd.append(row)
    nc = [class_data[0]]
    for row in class_data[1:]:
        nc.append(sep_class_row)
        nc.append(row)
    data = nd
    class_data = nc
    #
    caption = "PDCCH Candidates within one search space (IndexInAL<sub><sub>IndexInSS</sub></sub>)"
    num_merge_row = None
    num_merge_cols = None
    nrows = len(data) + len(x)
    ncols = len(data[0]) + len(y)
    num_merge_row = nrows
    # num_merge_cols = ncols
    output <= ztable.create_htable(a1=a1, 
                                   x=x, 
                                   y=y, 
                                   data=data, 
                                   class_data=class_data, 
                                   caption=caption, 
                                   num_merge_rows=num_merge_row, 
                                   num_merge_cols=num_merge_cols)

def cal_candidates(cfg):
    d = {}
    ret = {}
    for L in [1, 2, 4, 8, 16]:
        if cfg.n_cces < L:
            break
        M = getattr(cfg, f"n_candidates_{L}")
        d[L] = []
        ret[L] = []
        for m in range(M):
            first_cce_index = L * ( (cfg.Y + math.floor(m * cfg.n_cces / (L * M)) + cfg.nci) % math.floor(cfg.n_cces / L) )
            if (first_cce_index + L) <= cfg.n_cces:
                if no_overlap(L, d[L], first_cce_index):
                    d[L].append(first_cce_index)
                    ret[L].append([m, first_cce_index])
    return ret

def no_overlap(L, lst, first):
    set0 = {first+i for i in range(L)}
    for good_first in lst:
        set1 = {good_first+i for i in range(L)}
        if len(set0 & set1) > 0:
            return False
    return True



def cal_candidates2(cfg):
    ret = {}
    for L in [1, 2, 4, 8, 16]:
        if cfg.n_cces < L:
            break
        M = getattr(cfg, f"n_candidates_{L}")
        ret[L] = []
        for m in range(M):
            first_cce_index = L * ( (cfg.Y + math.floor(m * cfg.n_cces / (L * M)) + cfg.nci) % math.floor(cfg.n_cces / L) )
            ret[L].append([m, first_cce_index])
    return ret

def main2(output, cfg):
    output <= BR()
    output <= HR()
    good_candidates = cal_candidates(cfg) 
    candidates = cal_candidates2(cfg)
    a1 = [[" ", f"m<sub>s,n<sub>CI</sub></sub>"], [" ", f"m<sub>s,n<sub>CI</sub></sub>"]]
    y0 = []
    y1 = []
    max_cce = cfg.n_cces - 1
    for AL in [1, 2, 4, 8, 16]:
        lst = candidates[AL]
        for m, first_cce in lst:
            y0.append(f"AL{AL}")
            y1.append(f" {m}")
            max_cce = max(max_cce, first_cce)
        y0.append("")
        y1.append("")
    y = [y0, y1]
    n_cces = max_cce + 1
    x0 = ["CCE"] * n_cces
    x1 = [cce for cce in range(n_cces)]
    x = [x0, x1]
    sep_row = [""] * n_cces
    sep_row = list(range(n_cces))
    sep_class_row = ["sep_row"] * n_cces
    data = []
    class_data = []
    for AL in [1, 2, 4, 8, 16]:
        lst = candidates[AL]
        for m, first_cce in lst:
            data_row = []
            for cce in range(n_cces):
                n = cce // AL
                data_row.append(" "*n)
            class_data_row = [""] * n_cces
            ov = is_overlap(good_candidates[AL], m)
            for i in range(AL):
                col = first_cce + i
                data_row[col] = m
                if col >= cfg.n_cces or ov:
                    class_data_row[col] = "overlap"
            data.append(data_row)
            class_data.append(class_data_row)
        data.append(sep_row)
        class_data.append(sep_class_row)
    #
    caption = "All candidates (including overlapped)"
    num_merge_row = None
    num_merge_cols = None
    nrows = len(data) + len(x)
    ncols = len(data[0]) + len(y)
    num_merge_row = nrows
    # num_merge_cols = ncols
    output <= ztable.create_htable(a1=a1, 
                                   x=x, 
                                   y=y, 
                                   data=data, 
                                   class_data=class_data, 
                                   caption=caption, 
                                   num_merge_rows=num_merge_row, 
                                   num_merge_cols=num_merge_cols)


def is_overlap(lst, m):
    for m0, _ in lst:
        if m0 == m:
            return False
    return True

##########################################################################################################################################
cfg0 = para.Config()
cfg0.start(main)
# main()
# document["main"].style.display = "none"