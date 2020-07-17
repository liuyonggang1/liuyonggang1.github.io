from browser import window

def main():
    stem = window.location.pathname.split('/')[-1].replace('.html', '')
    if stem[:5] in ('36331', '38331'):
        if stem.endswith('ch5'):
            import rrcch5
        else:
            import rrc
    else:
        import core
    # elif stem[:5] in ('36413', '36423', '36443', '36444', '36455', '38413', '38423', '38463','38473'):
        # import core
    # elif stem in ('E2AP', 'E2SM_gNB_X2'):
        # import core
    # else:
        # raise
main()