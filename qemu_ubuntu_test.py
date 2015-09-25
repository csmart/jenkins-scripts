#!/usr/bin/python

import os
from qemu_simple_test import qemu_simple_test
import urllib
import hashlib


class qemu_ubuntu_test(qemu_simple_test):
    def __init__(self, qemu='qemu-system-ppc64', memory='4G', cores=1,
                 threads=1, kvm=False, virtio=False, kernel=None, initrd=None,
                 cmdline=None, image='utopic-server-cloudimg-ppc64el-disk1.img',
                 image_size='16G', image_cow=True, seed='my-seed.img',
                 seedurl='http://ozlabs.org/~anton/my-seed.img',
                 imageurl='http://cloud-images.ubuntu.com/utopic/current/utopic\
-server-cloudimg-ppc64el-disk1.img'):

        # Verify our images first
        if os.path.isfile(seed) is False \
                or hashlib.sha1(open(seed, 'ro').read()).hexdigest() != \
                "67758228a9d35927066a237f1a0e30d52e3db0f4":
            print("Downloading seed..")
            urllib.urlretrieve(seedurl, seed)
        else:
            print("Seed image looks good, continuing.")

        if os.path.isfile(image) is False \
                or hashlib.sha1(open(image, 'ro').read()).hexdigest() != \
                "f909ae37774db893637aeccd9257863f5cbf3147":
            print("Downloading image..")
            urllib.urlretrieve(imageurl, image)
        else:
            print("Backing image looks good, continuing.")

        # Now that we have our images, create our instance
        qemu_simple_test.__init__(self, qemu=qemu, memory=memory, cores=cores,
                                  threads=threads, kvm=kvm, virtio=virtio,
                                  kernel=kernel, initrd=initrd, cmdline=cmdline,
                                  image=image, image_size=image_size,
                                  image_cow=image_cow, seed=seed)

    def wait_for_login(self, timeout=300):
        self.expectcheck('ubuntu login:', timeout=timeout)

    def wait_for_prompt(self, timeout=300):
        self.child.expect('ubuntu@ubuntu', timeout=timeout)

    def boot(self, timeout=300):
        # boot it
        self.start()
        self.wait_for_login(timeout=timeout)

    def login(self, timeout=300):
        # log in
        self.child.sendline('ubuntu')
        self.child.expect('Password:', timeout=timeout)
        self.child.sendline('passw0rd')
        self.wait_for_prompt(timeout=timeout)

    def simple_test(self, timeout=300):
        self.boot(timeout=timeout)
        self.login(timeout=timeout)

        # quick network test
        self.child.sendline('ping -W 1 -c 1 10.0.2.2')
        self.child.expect('1 received', timeout=timeout)
        self.wait_for_prompt(timeout=timeout)

        # more involved network test
        self.child.sendline('wget http://ozlabs.org/~anton/datafile')
        self.wait_for_prompt(timeout=timeout)

        self.child.sendline('md5sum datafile')
        self.child.expect('2a9981457d46bf85eba3f81728159f84', timeout=timeout)
        self.wait_for_prompt(timeout=timeout)
