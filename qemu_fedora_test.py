#!/usr/bin/python

import os
from qemu_simple_test import qemu_simple_test
import urllib
import hashlib

env_http_proxy = os.getenv('http_proxy', '')
env_https_proxy = os.getenv('https_proxy', '')


class qemu_fedora_test(qemu_simple_test):
    def __init__(self, qemu='qemu-system-ppc64', memory='4G', cores=1,
                 threads=1, kvm=False, virtio=False, kernel=None, initrd=None,
                 cmdline=None, image='Fedora-Cloud-Base-22-20150521-1.ppc64le.qcow2',
                 image_size='16G', image_cow=True, seed='my-seed-fedora.img',
                 seedurl='http://ozlabs.org/~anton/my-seed.img',
                 imageurl='https://dl.fedoraproject.org/pub/fedora-secondary/\
releases/22/Cloud_Images/ppc64le/Images/\
Fedora-Cloud-Base-22-20150521-1.ppc64le.qcow2'):

        # Make sure we have a valid seed file
        if os.path.isfile(seed) is False \
                or hashlib.sha1(open(seed, 'ro').read()).hexdigest() != \
                "adcffcc80124760e550f8fca6e46499436dc8c40":
            print("Downloading seed..")
            urllib.urlretrieve(seedurl, seed)
        else:
            print("Seed image looks good, continuing.")

        # Make sure we have a valid base image to work from
        if os.path.isfile(image) is False \
                or hashlib.sha1(open(image, 'ro').read()).hexdigest() != \
                "ec7554dfb4ca7b1456436d93062b6978d476f3b8":
            print("Downloading image..")
            urllib.urlretrieve(imageurl, image)
        else:
            print("Backing image looks good, continuing.")

        # Let's initialise our test VM, now that we have valid images
        qemu_simple_test.__init__(self, qemu=qemu, memory=memory, cores=cores,
                                  threads=threads, kvm=kvm, virtio=virtio,
                                  kernel=kernel, initrd=initrd, cmdline=cmdline,
                                  image=image, image_size=image_size,
                                  image_cow=image_cow, seed=seed)

    def wait_for_login(self, timeout=600):
        self.expectcheck('SYSTEM READY TO LOG IN', timeout=timeout)

    def wait_for_prompt(self, timeout=600):
        self.child.expect('fedora@localhost', timeout=timeout)

    def boot(self, timeout=600):
        # boot it
        self.start()
        self.wait_for_login(timeout=timeout)

    def login(self, timeout=600):
        # log in
        self.child.sendline('fedora')
        self.child.expect('Password:', timeout=timeout)
        self.child.sendline('passw0rd')
        self.wait_for_prompt(timeout=timeout)

    def simple_test(self, timeout=600):
        self.boot(timeout=timeout)
        self.login(timeout=timeout)

        # quick network test
        self.child.sendline('ping -W 1 -c 1 10.0.2.2')
        self.child.expect('1 received', timeout=timeout)
        self.wait_for_prompt(timeout=timeout)

        # more involved network test
        self.child.sendline('curl --proxy "%s"\
                            http://ozlabs.org/~anton/datafile > datafile' % (env_http_proxy))
        self.wait_for_prompt(timeout=timeout)

        self.child.sendline('md5sum datafile')
        self.child.expect('2a9981457d46bf85eba3f81728159f84', timeout=timeout)
        self.wait_for_prompt(timeout=timeout)
