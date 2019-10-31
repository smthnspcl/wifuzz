#!/usr/bin/python3

from os import geteuid
from sys import argv

from libs import Configuration


if __name__ == '__main__':
    c = Configuration.parse(argv)

    if geteuid() != 0:
        print("i need privileges")
        exit()

    if c.scan:
        if c.bt:
            from libs import BluetoothScanner
            bts = BluetoothScanner()
            bts.start()
            # todo: collect macs and add to targets
        if c.wifi:
            from libs import WiFiScanner, set_monitor_mode
            set_monitor_mode("")
            wts = WiFiScanner()
            wts.start()
