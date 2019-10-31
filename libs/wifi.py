from .fuzzer import Fuzzer
from .scanner import Scanner

from os import system
from time import sleep
from scapy.layers.dot11 import *
from scapy.all import AsyncSniffer
from netifaces import interfaces


def get_interface():
    for i in interfaces():
        if i.startswith("wl"):
            return i
    return None


def set_monitor_mode(interface, enable=True):
    system("ip link set dev %s down" % interface)
    if enable:
        system("iwconfig %s mode monitor" % interface)
    else:
        system("iwconfig %s mode managed" % interface)  # managed or auto for normal
    system("ip link set dev %s up" % interface)


class WiFiFuzzer(Fuzzer):
    targets = ["dc:0b:34:c4:8c:06"]
    frame_combos = [
        [Dot11Beacon, Dot11Elt],
        [Dot11Beacon],
        [Dot11AssoReq, Dot11Elt, Dot11EltRates]
    ]


class WiFiScanner(Scanner):
    daemon = False
    do_run = True

    def callback(self, pdu):
        a = pdu.addr1
        print(a)
        if a not in self.found:
            self.found.append(a)

    def run(self):
        a = AsyncSniffer(iface=self.iface, prn=self.callback)
        while self.do_run:
            sleep(1)  # be nice to the cpu
        a.stop()
