#!/usr/bin/python

import sys
from qemu_fedora_test import qemu_fedora_test


if len(sys.argv) != 2:
    print "Usage: qemu_fedora_quick_test.py kernel"
    sys.exit(1)

kernel = sys.argv[1]

print "Testing PAPR virtual IO"
q = qemu_fedora_test(kvm=False, kernel=kernel, cmdline='root=/dev/sda2 rw')
q.simple_test(timeout=1200)
q.close()
