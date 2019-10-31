#!/usr/bin/python3

from os import geteuid
from sys import argv
from time import sleep

from libs import Configuration


def scan():
    if c.bt:
        from libs import BluetoothScanner
        bts = BluetoothScanner()
        bts.start()
        # todo: collect macs and add to targets
    if c.wifi:
        from libs import WiFiScanner, set_monitor_mode
        if not c.iface_wl:
            print("no wifi interface found")
            exit()
        print("setting monitor mode")
        # set_monitor_mode(c.iface_wl)
        wts = WiFiScanner(c.iface_wl)
        try:
            print("wifi: sniffing for macs")
            wts.start()
        except KeyboardInterrupt:
            wts.stop()
            print("\nresults:")
            print(wts.found)


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


if __name__ == '__main__':
    c = Configuration.parse(argv)

    if geteuid() != 0:
        print("i need privileges")
        exit()

    if c.scan:
        scan()

    fuzz()
    print("done")
