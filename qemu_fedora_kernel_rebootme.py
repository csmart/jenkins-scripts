#!/usr/bin/python

import sys
from qemu_fedora_test import qemu_fedora_test


if len(sys.argv) != 3:
    print "Usage: qemu_fedora_kernel_rebootme.py kernel iterations"
    sys.exit(1)

kernel = sys.argv[1]
iterations = int(sys.argv[2])

q = qemu_fedora_test(kvm=True, cores=8, threads=8, kernel=kernel,
                     cmdline='root=/dev/sda2 rw', virtio=True)
q.boot()

for i in range(iterations):
    q.login()
    q.child.sendline('shutdown -r now')
    q.wait_for_login()
