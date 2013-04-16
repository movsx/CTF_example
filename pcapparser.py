# -*- coding: utf-8 -*-
import binascii
import dpkt
import struct
import sys

### Пример разбора PCAP с использованием dpkt
def dpkt_parser():
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

### Задача на разбор кусков торрента
# Решение tshark плюс скрипт на питоне для сшивки сессий
###
# We’re given a pcap file containing BitTorrent traffic, among which lots of packets containing BitTorrent ‘piece’ data.
# Let’s use some tshark magic to extract only the relevant data (piece index and data):
###
# tshark -r torrent.pcap -R 'bittorrent.piece.data' -Tfields -e bittorrent.piece.index -e bittorrent.piece.data > pieces
#
# Finally we use a few lines of python to stitch together the pieces
def stitch_pieces():
    pieces = {}

    for line in open('pieces'):
        line = line.strip()

        idx, data = line.split('\t')
        data = data.replace(':','').decode('hex')

        try:
            pieces[idx] += data
        except KeyError:
            pieces[idx] = data
    
    pieces = sorted([(int(p[0], 16), p[1]) for p in pieces.items()])

    data = ''.join([p[1] for p in pieces])
    open('torrent.out', 'w').write(data)

# The resulting file turns out to be a bzip2-compressed tar archive.
# $ tar xf torrent.out
# $ cat key.txt
# t0renz0_v0n_m4tt3rh0rn