from __future__ import division, print_function

from construct import *

boot_img_hdr = Struct("boot_img_hdr",
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


filename = "BOOT.img"
s = open(filename, 'rb').read()

h = (boot_img_hdr.parse(s))

page_size = h.page_size

n = (h.kernel_size + page_size - 1) // page_size
m = (h.ramdisk_size + page_size - 1) // page_size
o = (h.second_size + page_size - 1) // page_size
pages = 1 + n + m + o

with open(filename + '.header', 'wb') as f:
    f.write(s[:boot_img_hdr.sizeof()])
with open(filename + '.headerpad', 'wb') as f:
    f.write(s[boot_img_hdr.sizeof():page_size])

kernelpages = s[1 * page_size:(1 + n) * page_size]
with open(filename + '.kernel', 'wb') as f:
    f.write(kernelpages[:h.kernel_size])
with open(filename + '.kernelpad', 'wb') as f:
    f.write(kernelpages[h.kernel_size:])

secondpages = s[(1 + n + m) * page_size:]
with open(filename + '.second', 'wb') as f:
    f.write(secondpages[:h.second_size])
with open(filename + '.secondpad', 'wb') as f:
    f.write(secondpages[h.second_size:])

ramdiskpages = s[(1 + n) * page_size:(1 + n + m) * page_size]
with open(filename + '.ramdisk', 'wb') as f:
    f.write(ramdiskpages[:h.ramdisk_size])
with open(filename + '.ramdiskpad', 'wb') as f:
    f.write(ramdiskpages[h.ramdisk_size:])

