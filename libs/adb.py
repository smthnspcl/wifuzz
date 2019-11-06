from .runnable import Runnable

from subprocess import Popen, PIPE


class ADB(Runnable):
    device = None
    crash_callback = None

    mac_bt = None
    mac_wifi = None

    def __init__(self, device=None, crash_callback=None):
        Runnable.__init__(self)
        self.device = device
        self.crash_callback = crash_callback

    class Line(object):
        date = None
        time = None
        pid = None
        priority = None
        name = None
        text = None

        def __init__(self, line):
            self.text = line
            line = line.split()
            self.date = line[0]
            self.time = line[1]
            self.pid = line[2]
            self.priority = line[4]
            self.name = line[5]
            if self.name.endswith(b":"):
                self.name = self.name[0:-1]

    def get_wifi_mac(self):
        cmd = ["adb", "shell", "iwconfig"]
        if self.device is not None:
            cmd.append("-d")
            cmd.append(self.device)
        print(cmd)
        adbp = Popen(cmd, stdout=PIPE, stderr=PIPE)
        print(adbp.stdout.read())
        for m in adbp.stdout.readlines():
            m = m.strip()
            print(m)


    def get_macs(self):
        self.get_wifi_mac()

    def run(self) -> None:
        cmd = ["adb", "logcat"]
        if self.device is not None:
            cmd.append("-d")
            cmd.append(self.device)
        adbp = Popen(cmd, stdout=PIPE, stderr=PIPE)
        while self.do_run:
            for l in adbp.stdout:
                if l.startswith(b"---"):
                    continue
                line = ADB.Line(l)
                if line.priority in [b'W', b'E']:
                    if self.crash_callback is not None:
                        self.crash_callback(line)
                    print(line.text)
                # if b'System.err:' in l.text:
                #     print(l.text)

# interesting names
# bt_sdp, bt_btif_sock_rfcomm, bt_btif, bt_vendor, bt_osi_thread
# BluetoothHealthServiceJni, BluetoothPanServiceJni, BluetoothHidServiceJni
# BluetoothSdpJni
# wificond, QCNEJ, WifiAPDataHandler
# WCNSS_FILTER
# ip
