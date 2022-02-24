##########################################################################################################################################
from browser import document, alert, timer
from browser.html import *
import para
import ztable
import random

##########################################################################################################################################
class RlcSdu:
    def __init__(self, rlc_entity, sn):
        self.sn = sn
        self.segments = []
        self.reassembled_and_delivered = False
        self.discarded = False
        self.rlc = rlc_entity
        self._no_missing_segment = True

    def add_segment(self, segment):
        self.segments.append(segment)
        self._no_missing_segment = self.determine_no_missing_segment()
    
    def is_all_received(self):
        return sum(self.segments) >= 1

    def is_partial_received(self):
        return 0 < sum(self.segments) < 1

    def reassemble_and_delivere(self):
        self.reassembled_and_delivered = True

    def discard(self):
        self.segments.clear()
        self.discarded = True
        self._no_missing_segment = True
    
    def clear(self):
        if self.segments:
            self.segments.clear()
            self.discarded = True
            self._no_missing_segment = True

    def clear_discard_flag(self):
        self.discarded = False

    def reset(self):
        self.segments.clear()
        self.reassembled_and_delivered = False
        self.discarded = False
        self._no_missing_segment = True

    def percent(self):
        return int(sum(self.segments) * 100)

    def determine_no_missing_segment(self):
        return self.is_all_received() or random.randrange(10) < self.rlc.possibility
        
    def no_missing_segment(self):
        return self._no_missing_segment

##########################################################################################################################################
class NrRlcDlRx:
    def __init__(self, cfg):
        self.cfg = cfg
        cfg.copy_cfg(self)
        self.num_sn = 1 << self.rlc_sn_size_dl
        self.max_sn = self.num_sn - 1
        self.rx_next_reassembly = 0
        self.rx_timer_trigger = 0
        self.rx_next_highest = 0
        self.table, self.tds, self.out_tds = self.create_table()
        self.in_first_window = True
        self.buffer = [RlcSdu(self, sn) for sn in range(self.num_sn)]
        self.t_reassemebly_running = False
        self.t_reassemebly_expired = False
        self.use_manual_input = False
        # self.rx_next_reassembly_no_missing_segment = True

    @property
    def _window_size(self):
        return self.rx_next_highest if self.in_first_window else self.window_size
    
    @property
    def modulus_base(self):
        return self.rx_next_highest - self._window_size

    def mod_base(self, v):
        return (v - self.modulus_base) % self.num_sn
    
    def larger_than(self, a, b):
        a0 = self.mod_base(a)
        b0 = self.mod_base(b)
        return a0 > b0
    
    def larger_equal(self, a, b):
        a0 = self.mod_base(a)
        b0 = self.mod_base(b)
        return a0 >= b0

    def less_than(self, a, b):
        a0 = self.mod_base(a)
        b0 = self.mod_base(b)
        return a0 < b0

    def less_equal(self, a, b):
        a0 = self.mod_base(a)
        b0 = self.mod_base(b)
        return a0 <= b0

    def add(self, a, b):
        return (a+b) % self.num_sn

    def create_table(self):
        tds, tds_info, out_tds, out_tds_info = [], [], [], []
        n = self.num_sn // 4
        nrows = ncols = n + 2 + 2
        data = [["" for col in range(ncols)] for row in range(nrows)]
        i = 0
        row = 1
        for col in range(2, ncols-2):
            data[row][col] = str(i)
            tds_info.append([i, row, col, "top_row"])
            out_tds_info.append([i, row-1, col])
            i += 1
        col = ncols - 2
        for row in range(2, nrows-2):
            data[row][col] = str(i)
            tds_info.append([i, row, col, "right_col"])
            out_tds_info.append([i, row, col+1])
            i += 1
        row = nrows - 2
        for col in range(2, ncols-2)[::-1]:
            data[row][col] = str(i)
            tds_info.append([i, row, col, "bottom_row"])
            out_tds_info.append([i, row+1, col])
            i += 1
        col = 1
        for row in range(2, nrows-2)[::-1]:
            data[row][col] = str(i)
            tds_info.append([i, row, col, "left_col"])
            out_tds_info.append([i, row, col-1])
            i += 1
        caption = "SN Ring"
        table = ztable.create_htable(data=data, caption=caption)
        for (i, row, col, pos) in tds_info:
            td = table.rows[row].cells[col]
            td.attrs["ring"] = ""
            td.attrs["pos"] = pos
            td.attrs["idx"] = str(i)
            td.attrs["row"] = str(row)
            td.attrs["col"] = str(col)
            a, b = divmod(i, n)
            if (a == 0 and b == (n-1)) or (a == 2 and b == 0):
                td.attrs["right_border"] = ""
            if (a == 1 and b == (n-1)) or (a == 3 and b == 0):
                td.attrs["bottom_border"] = ""
            tds.append(td)
        for (i, row, col) in out_tds_info:
            td = table.rows[row].cells[col]
            td.attrs["out_ring"] = ""
            td.attrs["out_idx"] = str(i)
            td.attrs["out_row"] = str(row)
            td.attrs["out_col"] = str(col)
            out_tds.append(td)
        return table, tds, out_tds

    def simulate(self):
        # self.end_flag = False
        self.use_manual_input = False
        self.sim_timer = timer.set_interval(self.recv, self.refresh_interval)
        #
        output = document['zone-output']
        #
        output <= BR()
        self.btn_t_reassemebly = BUTTON("trigger t_reassemebly expire")
        self.btn_t_reassemebly.bind("click", self.click_btn_t_reassemebly)
        output <= self.btn_t_reassemebly
        #
        output <= BR()
        self.btn_auto_control = BUTTON("pause")
        self.btn_auto_control.bind("click", self.click_btn_auto_control)
        output <= self.btn_auto_control
        #
        self.span_manual_input = SPAN(Class="span_manual_input")
        output <= self.span_manual_input
        self.span_manual_input.style.display = "none"
        self.span_manual_input <= SPAN("manually input SN and segement", Class="span_manual_inpit")
        self.select_manaul_sn = SELECT([OPTION(i) for i in range(self.num_sn)], title="SN")
        self.span_manual_input <= self.select_manaul_sn
        self.select_manaul_segment = SELECT([OPTION(i) for i in range(101)], title="segment")
        self.span_manual_input <= self.select_manaul_segment

    def set_manaul_input_random(self):
        sn = self.generate_random_sn()
        self.select_manaul_sn.selectedIndex = sn
        seg = random.randrange(101)
        self.select_manaul_segment.selectedIndex = seg
    
    def get_manaul_input(self):
        sn = self.select_manaul_sn.selectedIndex
        seg = (self.select_manaul_segment.selectedIndex) / 100
        return sn, seg

    def click_btn_auto_control(self, event):
        if self.btn_auto_control.text == "pause":
            timer.clear_interval(self.sim_timer)
            # self.end_flag = True
            self.btn_auto_control.text = "resume"
            self.span_manual_input.style.display = ""
            self.set_manaul_input_random()
        else:
            # self.end_flag = False
            self.use_manual_input = True
            self.btn_auto_control.text = "pause"
            self.span_manual_input.style.display = "none"
            self.sim_timer = timer.set_interval(self.recv, self.refresh_interval)

    def click_btn_t_reassemebly(self, event):
        if self.t_reassemebly_expired:
            return
        self.t_reassemebly_expired = True
        self.btn_t_reassemebly.style.color = "red"

    def generate_random_sn(self):
        lst = []
        for sn in range(self.num_sn):
            if self.in_reassembly_window(sn):
                lst.append(sn)
        for i in range(1, 1+2):
            sn = (self.rx_next_highest + i) % self.num_sn
            lst.append(sn)
        return random.choice(lst)

    def recv(self):        
        # if self.end_flag:
        #     timer.clear_interval(self.sim_timer)
        #     # alert("end")
        #     return
        if self.t_reassemebly_expired:
            self.handle_t_reassemebly_expire()
            self.t_reassemebly_expired = False
            self.btn_t_reassemebly.style.color = "black"
            self.plot(None)
            return
        pdu = type("", (), {})
        if self.use_manual_input:
            self.use_manual_input = False
            pdu.sn, pdu.segment = self.get_manaul_input()
        else:
            pdu.sn = self.generate_random_sn()
            pdu.segment = random.random()
        if pdu.sn >= self.window_size:
            self.in_first_window = False
        for sn in range(self.num_sn):
            if not self.in_reassembly_window(sn):
                self.get_sdu(sn).reset()
        for sn in range(self.num_sn):
            self.get_sdu(sn).clear_discard_flag()
        self.recv_pdu_from_lower(pdu)
        self.plot(pdu)

    def discard(self, rcvd_sn):
        self.get_sdu(rcvd_sn).discard()

    def in_reassembly_window(self, sn):
        window_size = self._window_size
        a = (sn - (self.rx_next_highest - window_size)) % self.num_sn
        return 0 <= a < window_size

    def in_discard_area(self, sn):
        window_size = self._window_size
        a = (sn - (self.rx_next_highest - window_size)) % self.num_sn
        b = (self.rx_next_reassembly - (self.rx_next_highest - window_size)) % self.num_sn
        return 0 <= a < b

    def get_sdu(self, sn):
        return self.buffer[sn]

    def recv_pdu_from_lower(self, pdu):
        rcvd_sn = pdu.sn
        segment = pdu.segment
        if self.in_discard_area(rcvd_sn):
            self.discard(rcvd_sn)
            return
        rcvd_sdu = self.get_sdu(rcvd_sn)
        if rcvd_sdu.reassembled_and_delivered:
            self.discard(rcvd_sn)
            return
        rcvd_sdu.add_segment(segment)
        if rcvd_sdu.is_all_received():
            rcvd_sdu.reassemble_and_delivere()
            if rcvd_sn == self.rx_next_reassembly:
                for i in range(1, self.num_sn):
                    sn = (rcvd_sn + i) % self.num_sn
                    sdu = self.get_sdu(sn)
                    if not sdu.reassembled_and_delivered:
                        self.rx_next_reassembly = sn
                        break
        elif not self.in_reassembly_window(rcvd_sn):
            self.rx_next_highest = (rcvd_sn + 1) % self.num_sn
            for sn in range(self.num_sn):
                if not self.in_reassembly_window(sn):
                    self.get_sdu(sn).clear()
            if not self.in_reassembly_window(self.rx_next_reassembly):
                start_sn = (self.rx_next_highest - self._window_size) % self.num_sn
                for i in range(self.num_sn):
                    sn = (start_sn + i) % self.num_sn
                    if not self.get_sdu(sn).reassembled_and_delivered:
                        self.rx_next_reassembly = sn
                        break
        # t_reassemebly
        if self.t_reassemebly_running:
            c1 = self.less_equal(self.rx_timer_trigger, self.rx_next_reassembly)
            c2 = not self.in_reassembly_window(self.rx_timer_trigger) and self.rx_timer_trigger != self.rx_next_highest
            c31 = self.rx_next_highest == self.add(self.rx_next_reassembly, 1)
            c32 = self.get_sdu(self.rx_next_reassembly).no_missing_segment()
            c3 = c31 and c32
            if c1 or c2 or c3:
                self.t_reassemebly_running = False
        if not self.t_reassemebly_running:
            d1 = self.larger_than(self.rx_next_highest, self.add(self.rx_next_reassembly, 1))
            d21 = self.rx_next_highest == self.add(self.rx_next_reassembly, 1)
            d22 = not self.get_sdu(self.rx_next_reassembly).no_missing_segment()
            d2 = d21 and d22
            if d1 or d2:
                self.t_reassemebly_running = True
                self.rx_timer_trigger = self.rx_next_highest

    def handle_t_reassemebly_expire(self):
        for _sn in range(self.num_sn):
            sn = self.add(self.rx_timer_trigger, _sn)
            if not self.get_sdu(sn).reassembled_and_delivered:
                self.rx_next_reassembly = sn
                break
        for sn in range(self.num_sn):
            if self.in_discard_area(sn):
                self.get_sdu(sn).clear()
        c1 = self.larger_than(self.rx_next_highest, self.add(self.rx_next_reassembly, 1))
        c21 = self.rx_next_highest == self.add(self.rx_next_reassembly, 1)
        c22 = not self.get_sdu(self.rx_next_reassembly).no_missing_segment()
        c2 = c21 and c22
        if c1 or c2:
            self.t_reassemebly_running = True
            self.rx_timer_trigger = self.rx_next_highest

    def plot(self, pdu):
        for sn in range(self.num_sn):
            sdu = self.get_sdu(sn)
            self.tds[sn].attrs["rcvd_sn"] = "no"
            self.out_tds[sn].attrs["out_rcvd_sn"] = "no"
            self.out_tds[sn].attrs["out_rcvd_no_missing_seg"] = ""
            if self.in_reassembly_window(sn):
                if self.in_discard_area(sn):
                    self.tds[sn].attrs["area"] = "in_window_discard"
                else:
                    self.tds[sn].attrs["area"] = "in_window_reassemble"
                    self.out_tds[sn].attrs["out_rcvd_no_missing_seg"] = "yes" if sdu.no_missing_segment() else "no"
            else:
                self.tds[sn].attrs["area"] = "out_of_window"
            self.tds[sn].attrs["discarded"] = "yes" if sdu.discarded else "no"
            if sdu.reassembled_and_delivered:
                self.tds[sn].attrs["status"] = "reassembled_and_delivered"
                self.tds[sn].text = str(sn)
            elif sdu.is_partial_received():
                self.tds[sn].attrs["status"] = "partial_received"
                self.tds[sn].html = f"{sn}<sub>{sdu.percent()}</sub>"
            else:
                self.tds[sn].attrs["status"] = "no_segments"
                self.tds[sn].text = str(sn)
            self.out_tds[sn].text = ""

        td = self.out_tds[self.rx_next_highest]
        td.text = "H"
        td = self.out_tds[self.rx_next_reassembly]
        td.text += "R"
        td = self.out_tds[self.rx_timer_trigger]
        td.text += "T"
        if pdu is not None:
            rcvd_sn, segment = pdu.sn, pdu.segment
            self.tds[rcvd_sn].attrs["rcvd_sn"] = "yes"            
            td = self.out_tds[rcvd_sn]
            if td.text == "" and not self.get_sdu(rcvd_sn).discarded:
                td.text = str(int(segment * 100))
                td.attrs["out_rcvd_sn"] = "yes"


##########################################################################################################################################
def main(event):
    rlc = NrRlcDlRx(cfg)
    document['zone-output'].clear()
    document['zone-output'] <= rlc.table
    rlc.simulate()

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
