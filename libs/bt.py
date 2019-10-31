from .fuzzer import Fuzzer
from .scanner import Scanner

from scapy.layers.bluetooth import *


class BluetoothFuzzer(Fuzzer):

    sock = None
    targets = []
    frame_combos = [
        [None, HCI_Hdr, HCI_Command_Hdr]
    ]

    def run(self) -> None:
        self.sock = BluetoothHCISocket()
        self.f_send = self.sock.send
        for t in self.targets:
            self.fuzz(t)

    def stop(self):
        self.do_run = False
        self.sock.close()


class BluetoothScanner(Scanner):
    def __init__(self, iface=0):
        Scanner.__init__(self, iface)

    def callback(self, pdu):
        print(pdu.summary())

    def run(self):
        s = BluetoothHCISocket(self.iface)
        d = s.sr(HCI_Hdr() / HCI_Command_Hdr() / HCI_Cmd_LE_Set_Scan_Enable(enable=False), verbose=False)
        print(d)
