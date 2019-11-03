from mac_vendor_lookup import MacLookup
import re

REGEX_MAC = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")


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
    except Exception as e:
        print(e)
        pass
    return td


def validate_mac(addr):
    return REGEX_MAC.match(addr)
