from .fuzzer import Fuzzer
from .scanner import Scanner

from subprocess import check_output
from scapy.layers.dot11 import *


def set_monitor_mode(interface, enable=True, channel=1):
    o = check_output(["ifconfig", interface, "down"])
    print(o)


class WiFiFuzzer(Fuzzer):
    # iface = "wlp13s0"
    targets = ["dc:0b:34:c4:8c:06"]
    frame_combos = [
        [Dot11Beacon, Dot11Elt],
        [Dot11Beacon],
        [Dot11AssoReq, Dot11Elt, Dot11EltRates]
    ]


class WiFiScanner(Scanner):
    iface = "wlan0"

    def callback(self, pdu):
        print(pdu.summary())

    def run(self):
        sniff(iface=self.iface, prn=self.callback)
