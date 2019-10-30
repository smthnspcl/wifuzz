from .runnable import Runnable

from scapy.all import fuzz, send


class Fuzzer(Runnable):
    targets = []
    '''
    frame_combos = [
        [BasePacket, FuzzPacket, FuzzPacket],
        ...
    ]
    '''
    frame_combos = []

    f_send = send

    def fuzz(self, target):
        for fc in self.frame_combos:
            p = fc[0]  # base packet
            if p is not None:
                p = p(addr1=target)  # dot11 packet
            for fp in fc[1:]:
                p /= fuzz(fp())
            self.f_send(p)

    def run(self) -> None:
        while self.do_run:
            for t in self.targets:
                self.fuzz(t)
