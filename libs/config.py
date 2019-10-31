from .wifi import get_interface as get_wifi_interface


class Configuration(object):
    targets = []
    wifi = False
    bt = False
    scan = False
    adb = False
    devices = []

    iface_bt = 0
    iface_wl = "wlan0"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def help():
        print("usage: ./wifuzz.py {arguments}")
        print("\t{arguments}\t\t{example/hint}")
        print("\t-h\t--help\t\tthis")
        print("\t-t\t--target\tfe:ed:de:ad:be:ef")
        print("\t\t--targets\tde:ad:be:ef:b0:ff,c0:33:b3:ff:ee:33")
        print("\t-s\t--scan\t\tscan for mac addresses")
        print("\t-w\t--wifi\t\tuse wifi")
        print("\t-b\t--bt\t\tuse bluetooth")
        print("\t-i\t--interface\tcall supply after -w/-b")
        print("\t-a\t--adb\t\tuse adb")
        print("\t-d\t--device\tadb transport id")
        print("\t\t--devices\ttid1,tid2,tid5")
        exit()

    @staticmethod
    def filter_duplicates(lst):
        _t = []
        for i in lst:
            if i not in _t:
                _t.append(i)
        return _t

    def check(self):
        if not self.wifi and not self.bt:
            self.help()
        if len(self.targets) == 0 and not self.scan:
            self.help()
        self.targets = self.filter_duplicates(self.targets)
        self.devices = self.filter_duplicates(self.devices)
        if self.iface_wl is None:
            self.iface_wl = get_wifi_interface()

    @staticmethod
    def parse(args):
        i = 0
        _c = Configuration()
        while i < len(args):
            a = args[i]
            if a in ["-t", "--target"]:
                _c.targets.append(args[i + 1])
            elif a in ["--targets"]:
                _c += args[i + 1].split(",")
            elif a in ["-s", "--scan"]:
                _c.scan = True
            elif a in ["-w", "--wifi"]:
                _c.wifi = True
            elif a in ["-b", "--bt"]:
                _c.bt = True
            elif a in ["-a", "--adb"]:
                _c.adb = True
            elif a in ["-d", "--device"]:
                _c.devices.append(args[i + 1])
            elif a in ["--devices"]:
                _c.devices += args[i + 1].split(",")
            elif a in ["-i", "--interface"]:
                if args[i - 1] in ["-b", "--bt"]:
                    _c.iface_bt = args[i + 1]
                elif args[i - 1] in ["-w", "--wifi"]:
                    _c.iface_wl = args[i + 1]
            elif a in ["-h", "--help"]:
                Configuration.help()
            i += 1
        _c.check()
        return _c


if __name__ == '__main__':
    Configuration.help()
