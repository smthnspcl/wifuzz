from .fuzzer import Fuzzer
from .scanner import Scanner

from subprocess import check_output
from scapy.layers.dot11 import *
from netifaces import interfaces


def get_interface():
    for i in interfaces():
        if i.startswith("wl"):
            return i
    return None


def set_monitor_mode(interface, enable=True):
    print(check_output(["ip", "link", "set", "dev", interface, "down"]))
    if enable:
        print(check_output(["iwconfig", interface, "mode", "monitor"]))
    else:
        print(check_output(["iwconfig", interface, "mode", "managed"]))  # or auto
    print(check_output(["ip", "link", "set", "dev", interface, "up"]))


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
