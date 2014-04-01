"""Splits an Android boot.img into its various parts.

   You can put it back together using `cat`.
"""
from __future__ import division, print_function

import sys

from construct import Array, Bytes, ULInt32, Struct

_BOOTIMGHDR = Struct("boot_img_hdr",
                      Bytes("magic", 8),
                      ULInt32("kernel_size"),
                      ULInt32("kernel_addr"),
                      ULInt32("ramdisk_size"),
                      ULInt32("ramdisk_addr"),
                      ULInt32("second_size"),
                      ULInt32("second_addr"),
                      ULInt32("tags_addr"),
                      ULInt32("page_size"),
                      Array(2, ULInt32("unused")),
                      Bytes("name", 16),
                      Bytes("cmdline", 512),
                      Array(8, ULInt32("id")),
                      Bytes("extra_cmdline", 1024))

_HEADERLEN = _BOOTIMGHDR.sizeof()

_OUT = "{filename}_{start:08x}-{end:08x}.{name}"


def extract_bootimg(filename):
    """Extract an Android boot image."""
    s = open(filename, 'rb').read()
    h = (_BOOTIMGHDR.parse(s))

    page_size = h.page_size

    n = (h.kernel_size + page_size - 1) // page_size
    m = (h.ramdisk_size + page_size - 1) // page_size
    o = (h.second_size + page_size - 1) // page_size
    #pages = 1 + n + m + o

    PARTS = [('header', (0, _HEADERLEN)),
             ('kernel', (1, h.kernel_size)),
             ('ramdisk', (1 + n, h.ramdisk_size)),
             ('second', (1 + n + m, h.second_size))]

    end = 0
    for name, (page, size) in PARTS:
        start = page * page_size
        if start > end:
            outname = _OUT.format(start=end, end=start, filename=filename, name='pad')
            with open(outname, 'wb') as f:
                f.write(s[end:start])
        end = start + size
        outname = _OUT.format(start=start, end=end, filename=filename, name=name)
        with open(outname, 'wb') as f:
            f.write(s[start:end])

if __name__ == '__main__':
    extract_bootimg(sys.argv[1])
