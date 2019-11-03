## wifuzz
### why?
wanted my own wireless fuzzer

### whats inside?
[scapy](https://scapy.net/) for packet generation / sending<br>
[netifaces](https://pypi.org/project/netifaces/) to automatically get a wifi interface if none supplied<br>
[mac_vendor_lookup](https://pypi.org/project/mac-vendor-lookup/) for ...<br>
[terminaltables](https://pypi.org/project/terminaltables/) to make stuff look fancy<br>
[progressbar2](https://pypi.org/project/progressbar2/) for fanciness<br>
[pybluez](https://github.com/pybluez/pybluez) for bluetooth stuff<br>
[gattlib](https://bitbucket.org/OscarAcena/pygattlib) for pybluez[ble]<br>

### how to ...
#### ... get started
```shell script
sudo apt install aircrack-ng libbluetooth-dev pkg-config libboost-python-dev \
                 libboost-thread-dev libglib2.0-dev python-dev

# https://stackoverflow.com/questions/41463847/got-error-while-download-gattlib-via-pip3
pip3 download gattlib
tar xvzf ./gattlib-0.20150805.tar.gz
cd gattlib-0.20150805/
sed -ie 's/boost_python-py34/boost_python37/' setup.py
pip3 install .

pip3 install -r requirements.txt
```
#### ... to use it
```shell script
usage: ./wifuzz.py {arguments}
	{arguments}		{example/hint}
	-h	--help		this
	-t	--target	fe:ed:de:ad:be:ef
		--targets	de:ad:be:ef:b0:ff,c0:33:b3:ff:ee:33
	-s	--scan		scan for mac addresses/targets
	-w	--wifi		use wifi
	-b	--bt		use bluetooth
	-i	--interface	call supply after -w/-b
	-a	--adb		use adb
	-d	--device	adb transport id
		--devices	tid1,tid2,tid5
	-m	--mac-lookup	lookup macs
ex:
sudo ./wifuzz.py -s -w -i wlp13s0
```

