##########################################################################################################################################
from browser import document, alert, timer
from browser.html import *
import para
import ztable
import random

##########################################################################################################################################
class NrPdcpDlRx:
    def __init__(self, cfg):
        self.cfg = cfg
        cfg.copy_cfg(self)
        self.num_sn = 1 << self.pdcp_sn_size_dl
        self.num_hfn = 1 << self.hfn_size
        self.max_count = 2 ** (self.hfn_size + self.pdcp_sn_size_dl) - 1
        self.rx_next = 0
        self.rx_deliv = 0
        self.rx_reord = 0
        self.window_size = 2 ** (self.pdcp_sn_size_dl - 1)
        self.inbox = {}  # self.inbox[count] = pdu, buffered at PDCP
        # self.outbox = {} # self.outbox[count] = pdu, sent to upper layer
        self.skip_by_reorder = []
        self.table = self.create_table()
        self.tds = [[self.table.rows[row].cells[col] for col in range(1, 1 + self.num_sn)] for row in range(2, 2 + self.num_hfn)]
        self.t_reordering_running = False

    def create_table(self):
        data = [["" for col in range(self.num_sn)] for row in range(self.num_hfn)]
        # class_data = [["" for col in range(self.num_sn)] for row in range(self.num_hfn)]
        class_data = None
        a1 = [["HFN"], ["HFN"]]
        x = [["PDCP SN"]*self.num_sn, [i for i in range(self.num_sn)]]
        y = [i for i in range(self.num_hfn)]
        caption = None
        return ztable.create_htable(a1=a1, x=x, y=y, data=data, class_data=class_data, caption=caption, num_merge_rows=None, num_merge_cols=None)

    def simulate(self):
        if self.run_mode == 0:
            self.simulate_auto()
        if self.run_mode == 1:
            self.simulate_manual()

    def simulate_auto(self):
        self.end_flag = False
        self.sim_timer = timer.set_interval(self.recv, self.refresh_interval)
        output = document['zone-output']
        output <= BR()
        output <= SPAN("received SN: ")
        self.span_sn = SPAN()
        output <= self.span_sn

    def recv(self):
        if self.end_flag:
            timer.clear_interval(self.sim_timer)
            alert("end")
            return
        pdu = type("", (), {})
        pdu.sn = random.randrange(self.num_sn)
        self.span_sn.text = str(pdu.sn)
        self.recv_pdu_from_lower(pdu)

    def get_hfn_sn(self, count):
        return divmod(count, 1 << self.pdcp_sn_size_dl)

    def _cal_rcvd_hfn(self, rcvd_sn):
        win = self.window_size
        deliv_hfn, deliv_sn = self.get_hfn_sn(self.rx_deliv)
        if deliv_sn > win and rcvd_sn < deliv_sn - win:
            rcvd_hfn = deliv_hfn + 1
        elif deliv_sn == win:
            rcvd_hfn = deliv_hfn
        elif deliv_sn < win and rcvd_sn >= deliv_sn + win:
            rcvd_hfn = deliv_hfn - 1
        else:
            rcvd_hfn = deliv_hfn
        return rcvd_hfn

    def discard(self, rcvd_count=None):
        if rcvd_count is not None:
            hfn, sn = divmod(rcvd_count, self.num_sn)
            v = self.tds[hfn][sn].text
            v = 0 if v == "" else int(v)
            v += 1
            self.tds[hfn][sn].text = str(v)

    def update_td(self, count, **kw):
        if count > self.max_count:
            return
        hfn, sn = divmod(count, self.num_sn)
        td = self.tds[hfn][sn]
        for k, v in kw.items():
            setattr(td, k, v)

    def update_td_reorder(self):
        count = self.rx_reorder
        if count > self.max_count:
            return
        hfn, sn = divmod(count, self.num_sn)
        td = self.tds[hfn][sn]
        td.class_name += " rx_reorder"
        td.class_name = td.class_name.strip()

    def recv_pdu_from_lower(self, pdu):
        # R2-1706869 push window
        rcvd_sn = pdu.sn
        rcvd_hfn = self._cal_rcvd_hfn(rcvd_sn)
        if rcvd_hfn < 0 or rcvd_hfn > self.num_hfn - 1:
            self.discard()
            return
        rcvd_count = rcvd_hfn * self.num_sn + rcvd_sn
        if rcvd_count < 0 or rcvd_count > self.max_count:
            self.discard()
            return
        if rcvd_count < self.rx_deliv or rcvd_count in self.inbox:
            self.discard(rcvd_count)
            return
        else:
            self.update_td(rcvd_count, text="1")
            # outbox = []
            prev_rx_deliv = self.rx_deliv
            prev_rx_next = self.rx_next
            self.inbox[rcvd_count] = pdu
            if rcvd_count >= self.rx_next:
                self.rx_next = rcvd_count + 1
            if rcvd_count == self.rx_deliv:
                count = self.rx_deliv
                while True:
                    if count in self.inbox:
                        del self.inbox[count]  # send to upper layer
                        # outbox.append(count)
                        count += 1
                    else:
                        break
                self.rx_deliv = count

            if self.t_reordering_running and self.rx_deliv >= self.rx_reorder:
                self.t_reordering_running = False

            if not self.t_reordering_running and self.rx_deliv < self.rx_next:
                self.rx_reorder = self.rx_next
                self.t_reordering_running = True
            self.plot(prev_rx_deliv, prev_rx_next)

    def plot(self, prev_rx_deliv, prev_rx_next):
        self.end_flag = self.rx_deliv > self.max_count
        for count in range(self.max_count+1):
            if count < self.rx_deliv - self.window_size:
                self.update_td(count, class_name="older", text="")
            elif self.rx_deliv - self.window_size <= count < self.rx_deliv:
                self.update_td(count, class_name="old")
            elif self.rx_deliv <= count < self.rx_deliv + self.window_size:
                self.update_td(count, class_name="win")
            else:
                self.update_td(count, class_name="future")
        
        self.update_td(prev_rx_next, text="")
        self.update_td(prev_rx_deliv, text="")
        if prev_rx_deliv != self.rx_deliv:
            self.update_td(prev_rx_deliv, text="1")
        if prev_rx_next != self.rx_next:
            self.update_td(prev_rx_next, text="1")
        if self.rx_next == self.rx_deliv:
            if self.rx_next <= self.max_count:
                self.update_td(self.rx_next, text="D,N")
        else:
            if self.rx_next <= self.max_count:
                self.update_td(self.rx_next, text="N")
            if self.rx_deliv <= self.max_count:
                self.update_td(self.rx_deliv, text="D")

        if self.t_reordering_running:
            self.update_td_reorder()


    #  manual
    def simulate_manual(self):
        self.end_flag = False
        self.btn_reorder = BUTTON("Reorder")
        self.btn_play = BUTTON("Receive SN")
        self.sel_sn = SELECT([OPTION(i) for i in range(self.num_sn)])
        # if cur in new:
        #     self.select.selectedIndex = new.index(cur)
        output = document['zone-output']
        output <= self.btn_play
        output <= self.sel_sn
        output <= BR()
        output <= self.btn_reorder
        self.set_random_sn()
        self.btn_play.bind('click', self.click_btn_play)
        self.btn_reorder.bind('click', self.click_btn_reorder)

    def set_random_sn(self):
        sn = random.randrange(self.num_sn)
        self.sel_sn.selectedIndex = sn
    
    def get_sel_sn(self):
        return self.sel_sn.selectedIndex

    def click_btn_play(self, event):
        if self.end_flag:
            self.reset()
            return
        pdu = type("", (), {})
        pdu.sn = self.get_sel_sn()
        self.recv_pdu_from_lower(pdu)
        self.set_random_sn()

    def click_btn_reorder(self, event):
        prev_rx_deliv = self.rx_deliv
        prev_rx_next = self.rx_next

        for count in range(self.rx_deliv, self.rx_reorder):
            if count in self.inbox:
                del self.inbox[count]  # send to upper layer
            else:
                self.skip_by_reorder.append(count)

        count = self.rx_reorder
        while count < min(self.max_count+1, self.rx_next):
            if count in self.inbox:
                del self.inbox[count]  # send to upper layer
                # outbox.append(count)
                count += 1
            else:
                break
        self.rx_deliv = count
        if self.rx_deliv < self.rx_next:
            self.rx_reorder = self.rx_next
            self.t_reordering_running = True
        self.plot(prev_rx_deliv, prev_rx_next)

    def reset(self):
        pass

##########################################################################################################################################
def main(event):
    pdcp = NrPdcpDlRx(cfg)
    document['zone-output'].clear()
    document['zone-output'] <= pdcp.table
    pdcp.simulate()

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
