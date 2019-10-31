## wifuzz
### why?
wanted my own wireless fuzzer

### whats inside?
scapy for packet generation / sending<br>
netifaces to automatically get a wifi interface if none supplied

### how to ...
#### ... get started
```shell script
pip install -r requirements.txt
```
#### ... to use it
```shell script
usage: ./wifuzz.py {arguments}
	{arguments}		{example/hint}
	-h	--help		this
	-t	--target	fe:ed:de:ad:be:ef
		--targets	de:ad:be:ef:b0:ff,c0:33:b3:ff:ee:33
	-s	--scan		scan for mac addresses
	-w	--wifi		use wifi
	-b	--bt		use bluetooth
	-i	--interface	call supply after -w/-b
	-a	--adb		use adb
	-d	--device	adb transport id
		--devices	tid1,tid2,tid5
```
