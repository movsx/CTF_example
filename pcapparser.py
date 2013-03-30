# -*- coding: utf-8 -*-
import binascii
import dpkt
import struct
import sys

### Пример разбора PCAP с использованием dpkt
pcap = dpkt.pcap.Reader(open("ppp.pcap", 'rb'))

# Create a partial mapping from keycodes to ASCII chars
keys = {}
keys.update({
i + 0x4: chr(i + ord('a'))
for i in range(26)
})
keys.update({
i + 0x1e: chr(i + ord('1'))
for i in range(9)
})
keys[0x27] = '0'
keys.update({
    0x28: '\n',
    0x2c: ' ',
    0x2d: '-',

    0x2e: '+',
    0x2f: '[',
    0x30: ']',
    })

# Then iterate over each USB frame
for ts, buf in pcap:
    # We are interested only in packets that has the expected URB id, and
    # packets carrying keycodes embed exactly 8 bytes.
    urb_id = ''.join(reversed(buf[:8]))
    if binascii.hexlify(urb_id) != 'ffff88003b7d8fc0':
        continue
    data_length, = struct.unpack('<I', buf[0x24:0x28])
    if data_length != 8:
        continue
    key_code = ord(buf[0x42])
    if not key_code:
        continue
    sys.stdout.write(keys[key_code])