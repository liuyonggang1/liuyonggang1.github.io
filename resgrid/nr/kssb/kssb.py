##########################################################################################################################################
from browser import document, alert
from browser.html import *
import para
import ztable

##########################################################################################################################################

def main(event=None):
    document['zone-output'].clear()
    update_ssbgscn_to_pointa(cfg)

    ol = OL()
    document['zone-output'] <= ol
    # FR1
    for scs_ssb in [15, 30]:
        for subCarrierSpacingCommon in [15, 30]:
            s = f"SCS<sub>SSB</sub>={scs_ssb}k, subCarrierSpacingCommon={subCarrierSpacingCommon}k"
            if scs_ssb == 30 and subCarrierSpacingCommon == 15:
                s += ". <b>0 is invalid because not the lowest RB overlap with SSB.</b>"
            li = LI(s)
            ol <= li
            ol <= BR()
            ol <= IMG(src=f"{scs_ssb}_{subCarrierSpacingCommon}.png")
            ol <= HR()
    # FR2
    for scs_ssb in [120, 240]:
        for subCarrierSpacingCommon in [60, 120]:
            s = f"SCS<sub>SSB</sub>={scs_ssb}k, subCarrierSpacingCommon={subCarrierSpacingCommon}k"
            if scs_ssb == 120 and subCarrierSpacingCommon == 60:
                s += ". <b>0 is invalid because not the lowest RB overlap with SSB.</b>"
            if scs_ssb == 240 and subCarrierSpacingCommon == 120:
                s += ". <b>0 is invalid because not the lowest RB overlap with SSB.</b>"
            if scs_ssb == 240 and subCarrierSpacingCommon == 60:
                s += ". <b>0 and 1 are invalid because not the lowest RB overlap with SSB.</b>"
            li = LI(s)
            ol <= li
            ol <= BR()
            ol <= IMG(src=f"{scs_ssb}_{subCarrierSpacingCommon}.png")
            ol <= HR()


def update_ssbgscn_to_pointa(cfg):
    mhz, ghz = None, None
    khz = cfg.scs_ssb.value * 12 * 10 + \
        cfg.scs_kssb.value * cfg.kssb.value + \
        cfg.scs_offsetToPointA.value * cfg.offsetToPointA.value * 12
    if khz >= 1000:
        mhz = khz / 1000
        if mhz >= 1000:
            ghz = mhz / 1000
    if ghz is not None:
        s = f"{ghz} GHz"
    elif mhz is not None:
        s = f"{mhz} MHz"
    else:
        s = f"{khz} KHz"
    cfg.ssbgscn_to_pointa.range = s
    return 

##########################################################################################################################################
cfg = para.Config()
cfg.start(main)
main()
document["main"].style.display = "none"