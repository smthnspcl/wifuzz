from mac_vendor_lookup import MacLookup


def start_thread_kbi(tc):
    try:
        tc.start()
    except KeyboardInterrupt:
        print("\ncaught ctrl + c")
        tc.stop()


def create_mac_table(key, lst, lookup=False):
    td = [[key]]
    if lookup:
        td[0].append("vendor")
        m = MacLookup()
    try:
        for i in lst:
            if lookup:
                td.append([i, m.lookup(i)])
            else:
                td.append([i])
    except KeyError:
        pass
    return td
