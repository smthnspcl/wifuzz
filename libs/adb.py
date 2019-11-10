from .runnable import Runnable

from subprocess import Popen, PIPE
from datetime import datetime


class Crash(object):
    timestamp = None
    line = None

    def __init__(self, line):
        self.line = line
        self.timestamp = datetime.now()


class Device(object):
    name = None
    id = None
    mac_bt = None
    mac_wifi = None
    lc_session = None

    crashes = []

    def __init__(self, device_id, name=None):
        self.id = str(device_id)
        self.name = str(name)
        self.lc_session = Logcat(self.id, self.crash_callback)

    def get_wifi_mac(self):
        cmd = ["adb", "shell", "ip", "link"]
        if self.id is not None:
            cmd.append("-d")
            cmd.append(self.id)
        adbp = Popen(cmd, stdout=PIPE, stderr=PIPE)
        i = 0
        lns = adbp.stdout.readlines()
        while i < len(lns):
            m = str(lns[i].strip()).split(": ")
            if len(m) > 2 and m[1].startswith("wl"):
                self.mac_wifi = str(lns[i + 1].strip().split()[1])
            i += 1

    def crash_callback(self, line):
        print(line.date, line.time, line.name)
        print("\t", line.text)
        self.crashes.append(line)

    def get_bt_mac(self):
        raise NotImplemented  # todo

    def get_macs(self):
        self.get_wifi_mac()
        # device.get_bt_mac()

    def start_logcat(self):
        self.lc_session.start()

    def stop_logcat(self):
        self.lc_session.stop()


class Devices(object):
    devices = []

    def __init__(self):
        pass

    def get_macs(self):
        for d in self.devices:
            d.get_macs()

    def size(self):
        return len(self.devices)

    def add(self, device):
        for d in self.devices:
            if d.id == device.id:
                return False
        self.devices.append(device)
        return True

    def add_by_id(self, device_id):
        self.add(Device(device_id))

    def add_by_ids(self, device_ids):
        for did in device_ids:
            self.add_by_id(did)

    def get(self):
        cmd = ["adb", "devices"]
        adbp = Popen(cmd, stdout=PIPE, stderr=PIPE)
        self.devices = []
        i = 0
        for l in adbp.stdout:
            if i == 0:
                i += 1
                continue
            if l.startswith(b"*"):
                continue
            dt = l.split()
            if len(dt) == 0:
                continue
            d = Device(dt[0], dt[1])
            self.devices.append(d)
        return self.devices


class Logcat(Runnable):
    device = None
    crash_callback = None

    def __init__(self, device, crash_callback=None):
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
                line = Logcat.Line(l)
                if line.priority in [b'W', b'E']:
                    if self.crash_callback is not None:
                        self.crash_callback(line)
                # if b'System.err:' in l.text:
                #     print(l.text)

# interesting names
# bt_sdp, bt_btif_sock_rfcomm, bt_btif, bt_vendor, bt_osi_thread
# BluetoothHealthServiceJni, BluetoothPanServiceJni, BluetoothHidServiceJni
# BluetoothSdpJni
# wificond, QCNEJ, WifiAPDataHandler
# WCNSS_FILTER
# ip
