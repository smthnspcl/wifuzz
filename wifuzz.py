#!/usr/bin/python3

from os import geteuid
from sys import argv
from time import sleep
from terminaltables import AsciiTable

from libs import Configuration, start_thread_kbi, create_mac_table, validate_mac


def choose_targets():
    r = []
    print("enter macs you want to target")
    print("ctrl + c to start fuzzing")
    try:
        while True:
            i = input("> ")
            if not validate_mac(i):
                print(i, "is not a mac address")
            else:
                r.append(i)
    except KeyboardInterrupt:
        print()
        return r


def scan():
    if c.bt:
        from libs import BluetoothScanner
        bts = BluetoothScanner()
        print("scanning for bluetooth macs")
        start_thread_kbi(bts)
        print(AsciiTable(create_mac_table("bluetooth", bts.found, c.mac_lookup)).table)
        # todo: collect macs and add to targets
    if c.wifi:
        from libs import WiFiScanner
        if not c.iface_wl:
            print("no wifi interface found")
            exit()
        wts = WiFiScanner(c.iface_wl)
        print("scanning for wifi macs")
        start_thread_kbi(wts)
        print(AsciiTable(create_mac_table("wifi", wts.found, c.mac_lookup)).table)


def fuzz():
    from libs.adb import ADB
    adb_sessions = []
    if c.adb:
        if len(c.devices) >= 0:
            for d in c.devices:
                adb_sessions.append(ADB(d))
        else:
            adb_sessions.append(ADB())

        for s in adb_sessions:
            s.start()

        f = []
        if c.wifi:
            from libs import WiFiFuzzer
            f.append(WiFiFuzzer(c.iface_wl))
        if c.bt:
            from libs import BluetoothFuzzer
            f.append(BluetoothFuzzer(c.iface_bt))

        for _ in f:
            _.start()

        try:
            while True:
                sleep(1)  # be nice to the cpu
        except KeyboardInterrupt:
            print("stopping..")
            for s in adb_sessions:
                s.stop()
                s.join()
            for _ in f:
                _.stop()
                _.join()
            print("stopped")
    else:
        print("only adb error collection is implemented yet")
        pass  # todo server/client stuff to monitor processes on other machines


if __name__ == '__main__':
    c = Configuration.parse(argv)

    if geteuid() != 0:
        print("i need privileges")
        exit()

    if c.mac_lookup:
        create_mac_table("mac_lookup", ["ff:ff:ff:ff:ff:ff"])

    if c.wifi:
        from libs import set_monitor_mode
        c.iface_wl = set_monitor_mode(c.iface_wl)

    if c.scan:
        scan()
        c.targets = choose_targets()

    fuzz()

    if c.wifi:
        c.iface_wl = set_monitor_mode(c.iface_wl, False)

    print("done")
