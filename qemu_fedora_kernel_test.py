#!/usr/bin/python

import sys
from qemu_fedora_test import qemu_fedora_test


if len(sys.argv) != 2:
    print "Usage: qemu_fedora_kernel_test.py kernel"
    sys.exit(1)

kernel = sys.argv[1]

print "Testing PAPR virtual IO"
q = qemu_fedora_test(kvm=True, kernel=kernel, cmdline='root=/dev/sda2 rw')
q.simple_test(timeout=30)
q.close()

print "Testing virtio virtual IO"
q = qemu_fedora_test(kvm=True, kernel=kernel, cmdline='root=/dev/vda2 rw',
                     virtio=True)
q.simple_test(timeout=30)
q.close()

print "Testing SMP"
q = qemu_fedora_test(kvm=True, cores=8, threads=8, kernel=kernel,
                     cmdline='root=/dev/sda2 rw')
q.simple_test(timeout=30)
q.close()

print "Testing QEMU full emulation"
q = qemu_fedora_test(kvm=False, kernel=kernel, cmdline='root=/dev/sda2 rw')
q.simple_test()
q.close()
