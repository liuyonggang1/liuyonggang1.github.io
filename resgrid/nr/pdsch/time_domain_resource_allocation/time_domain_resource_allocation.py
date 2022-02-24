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

    mp = f"PDSCH Mapping Type {cfg.pdsch_mapping_type}"
    cp = f"{cfg.CP} Cyclic Prefix"
    
    nsymbols = cfg.nsymbols
    S = cfg.S
    L = cfg.L
    title = f"{mp} {cp} \n S={S} L={L}"
    str_k = '<i class="itatic_kl">k</i>'
    str_l = '<i class="itatic_kl">&#621;</i>'
    x0 = [str_l for i in range(nsymbols)]
    x1 = [i for i in range(nsymbols)]
    x = [x0, x1]
    y0 = [str_k for i in range(12)][::-1]
    y1 = [i for i in range(12)][::-1]
    y = [y0, y1]
    data = [["" for col in range(nsymbols)] for row in range(12)]
    class_data = [["" for col in range(nsymbols)] for row in range(12)]
    for row in range(12):
        for col in range(S, S+L):
            class_data[row][col] = "pdsch"
    
    if cfg.dmrs_type == 1:
        ports = range(1000, 1004)
        # table 7.4.1.1.2-1
        paras = [[0, 0, 1, 1, 1, 1],
                 [0, 0, 1,-1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1,-1, 1, 1]]
        n_list = [0, 1, 2]
        n_factor = 4
        kp_factor = 2
    if cfg.dmrs_type == 2:
        ports = range(1000, 1006)
        paras = [[0, 0, 1, 1, 1, 1],
                 [0, 0, 1,-1, 1, 1],
                 [1, 2, 1, 1, 1, 1],
                 [1, 2, 1,-1, 1, 1],
                 [2, 4, 1, 1, 1, 1],
                 [2, 4, 1,-1, 1, 1]]
        n_list = [0, 1]
        n_factor = 6
        kp_factor = 1
    l_bar_list = [int(i.strip()) for i in cfg.l_bar.split(",")]

    seq = []
    for i in range(len(ports)):
        port = ports[i]
        cdm_group, tri = paras[i][:2]
        wfks = paras[i][2:4]
        wtls = paras[i][4:]
        for n in n_list:
            for k_prime in [0, 1]:
                for l_prime in [0]:
                    for l_bar in l_bar_list:
                        l = l_bar + l_prime
                        k = n_factor * n + kp_factor * k_prime + tri
                        wf = wfks[k_prime]
                        wt = wtls[l_prime]
                        w = "+" if wf * wt == 1 else "-"
                        seq.append([port, cdm_group, k, l, w])
    tt = TABLE()
    tr = TR()
    tt <= tr
    output <= tt

    dci11_cdm_groups = cfg0.dci11_cdm_groups.list_value
    dci11_dmrs_ports = cfg0.dci11_dmrs_ports.list_value

    for p in dci11_dmrs_ports:
        data = [["" for col in range(nsymbols)] for row in range(12)]
        class_data = [["" for col in range(nsymbols)] for row in range(12)]
        for row in range(12):
            for col in range(S, S+L):
                class_data[row][col] = "pdsch"
        cdm = None
        for port, cdm_group, k, l, w in seq:
            if cdm_group in dci11_cdm_groups:
                class_data[k][l] = f"black"
        for port, cdm_group, k, l, w in seq:
            if p == port:
                data[k][l] = w
                class_data[k][l] = f"dmrs cdm{cdm_group}"
                if w == "-":
                    class_data[k][l] += " w-1"
                cdm = cdm_group
        a1 = None
        caption = f"{title}, port={p}, CDM group={cdm}"
        num_merge_row = None
        num_merge_cols = None
        nrows = len(data)
        ncols = len(data[0])
        # num_merge_row = nrows
        # num_merge_cols = ncols
        td = TD()
        # td.class_name = "out-td"
        tr <= td
        td <= ztable.create_htable(a1=a1, 
                                    x=x, 
                                    y=y, 
                                    data=data, 
                                    class_data=class_data, 
                                    caption=caption, 
                                    num_merge_rows=num_merge_row, 
                                    num_merge_cols=num_merge_cols)
        # output <= BR()                            



##########################################################################################################################################
cfg0 = para.Config()
cfg0.start(main)
# main()
# document["main"].style.display = "none"