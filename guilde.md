## 1. List devices

```bash
adb devices -l
```

output: List of devices attached
2285d50b40047ece device product:starlteks model:SM_G960N device:starlteks transport_id:1

👉 First column (2285d50b40047ece) is serial/ID.

## 2. Send request for special device

```bash
adb -s <serial/ID> shell monkey -p org.mozilla.firefox -c android.intent.category.LAUNCHER 1
```

## 3. Connect wireless

##### Android < 11 or not use Wireless debugging

```bash
adb tcpip 5555
# Unplugin cable to connect via wifi
adb connect 192.168.1.43:5555
```

##### Android > 11

1. On Android: Settings → Developer options → Wireless debugging → ON

- (a) Pair device with pairing code

  - Bấm vào đó → nó hiện:
  - IP:PAIR_PORT (ví dụ 192.168.1.50:47123)
  - Pairing code

- (b) IP address & port
  - At Wireless debugging has line:
  - IP address & port (ví dụ 192.168.1.50:37099)

2. On PC:

- (a) Pair (use PAIR_PORT)

```bash
adb pair 192.168.1.50:47123 #Replace pairing code on android
```

- (b) Connect (use IP address & port)

```bash
adb connect 192.168.1.50:37099
adb devices
```

- If right, will have:

```bash
192.168.1.50:37099 device
scrcpy -s 192.168.1.50:37099
```
