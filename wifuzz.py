#!/usr/bin/python3

from os import geteuid
from sys import argv
from time import sleep
from terminaltables import AsciiTable

from libs import Configuration, start_thread_kbi, create_mac_table, validate_mac
from libs.runnable import Runnable


class ADBFuzzer(Runnable):
    adb_devices = None
    fuzzers = []

    def __init__(self, adb_devices, fuzzers):
        Runnable.__init__(self)
        self.adb_devices = adb_devices
        self.fuzzers = fuzzers

    def run(self) -> None:
        for f in self.fuzzers:
            f.start()
        while self.do_run:
            for ad in self.adb_devices.devices:
                ad.start_logcat()
                ad.crashes.show()
            sleep(1)

    def stop(self):
        self.do_run = False
        for ad in self.adb_devices.devices:
            ad.stop_logcat()


class Main(object):
    @staticmethod
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

    @staticmethod
    def scan():
        if c.bt:
            from libs import BluetoothScanner
            if not c.iface_bt:
                print("no bluetooth interface found")
                exit()
            bts = BluetoothScanner(c.iface_bt)
            print("scanning for bluetooth macs")
            start_thread_kbi(bts)
            print(AsciiTable(create_mac_table("bluetooth", bts.found, c.mac_lookup)).table)
        if c.wifi:
            from libs import WiFiScanner
            if not c.iface_wl:
                print("no wifi interface found")
                exit()
            wts = WiFiScanner(c.iface_wl)
            print("scanning for wifi macs")
            start_thread_kbi(wts)
            print(AsciiTable(create_mac_table("wifi", wts.found, c.mac_lookup)).table)

    @staticmethod
    def fuzz():
        if c.adb:
            f = ADBFuzzer(c.adb_devices, [])
            if c.wifi:
                print("creating wifi fuzzer with interface", c.iface_wl)
                from libs import WiFiFuzzer
                _ = WiFiFuzzer(c.iface_wl)
                _.targets = c.targets_wifi
                f.fuzzers.append(_)
            if c.bt:
                print("creating bluetooth fuzzer with interface", c.iface_bt)
                from libs import BluetoothFuzzer
                _ = BluetoothFuzzer(c.iface_bt)
                _.targets.append(c.targets_bt)
                f.fuzzers.append(_)

            try:
                print("running")
                f.start()
                f.join()
            except KeyboardInterrupt:
                print("stopping..")
                f.stop()
                print("stopped")
        else:
            print("only adb error collection is implemented yet")
            pass  # todo server/client stuff to monitor processes on other machines

    @staticmethod
    def test():
        exit()


if __name__ == '__main__':
    # Main.test()

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
        Main.scan()
        c.targets = Main.choose_targets()

    Main.fuzz()

    if c.wifi:
        c.iface_wl = set_monitor_mode(c.iface_wl, False)

    print("done")
