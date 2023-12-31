import pexpect
import time
import os
import statistics
import requests


def get_minute_measure(child):
    end_time = time.time()+10
    measures = []
    while time.time() < end_time:
        child.sendline("char-write-cmd 0x25 5e")
        time.sleep(.1)

        child.expect("Notification handle.*", timeout=10)
        result = child.after.split(b'\r')[0]

        value = result.decode('ascii').split('value: ')[1]
        condensed = value.replace(' ', '')
        bytemsg = bytes.fromhex(condensed)

        # For more information, look at the file
        # p004cn/com/unitrend/ienv/android/domain/service/BluetoothLeService.java
        # From the decompiled cn-com-unitrend-ienv APK application
        assert(bytemsg[4] == 0x3b)  # Uni-T UT353BT noise meter
        assert(bytemsg[14] == 0x3d)  # dB(A) units

        value = bytemsg[5:]
        value = value.split(b'=')[0]
        assert(b'dBA' in value)
        raw_value = value.split(b'dBA')[0]

        dba_noise = float(raw_value.decode('ascii'))
        print(dba_noise)
        measures.append(dba_noise)


DEVICE = "2C:AB:33:9F:AB:39"

child = pexpect.spawn("gatttool -I")
print(f'Baglaniliyor...')
child.sendline(f'connect {DEVICE}')
child.expect("Connection successful", timeout=5)
print('Baglandi...')

time.sleep(1)

try:
    while True:
        try:
            get_minute_measure(child)
        except Exception as e:
            print("Tekrar Deneniyor...")
            time.sleep(5)
finally:
    child.sendline('disconnect')