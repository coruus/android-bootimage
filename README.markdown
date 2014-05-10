# Correct and reversible splitting of Android boot images

A very minimal Python script to correctly split Android boot images
so that they can be modified, put back together again, and still
work.

(It also dumps some header data to a YAML file.)

It has none of the fancy features of `abootimg` at the moment. Its
sole virtue is that it is possible to put its output back together
again.

(`abootimg` doesn't parse headers correctly, and it discards anything
in portions of the boot image that are empty according to the header.
Alas, very frequently those parts of the boot image are not empty and
rather essential.)

Split an image:

    ./xbootimg.py BOOT.img

Put it back together:

    cat BOOT.img_* > BOOT2.img

Do, e.g.,

     % ls -l | colrm 1 25 | colrm 9 21

     8388608 BOOT.img
        1632 BOOT.img_00000000-00000660.header
         416 BOOT.img_00000660-00000800.pad
     4996724 BOOT.img_00000800-004c4674.kernel
         396 BOOT.img_004c4674-004c4800.pad
      449177 BOOT.img_004c4800-00532299.ramdisk
        1383 BOOT.img_00532299-00532800.pad
           0 BOOT.img_00532800-00532800.second
     2938880 BOOT.img_00532800-00800000.fin
     8388608 BOOT2.img

And then:

    % diff -s BOOT.img BOOT2.img
    Files BOOT.img and BOOT2.img are identical
