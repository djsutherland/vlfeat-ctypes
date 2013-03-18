#!/usr/bin/env python
from __future__ import print_function

import os
import platform
import shutil
import sys
import tarfile
import tempfile
import urllib2

DEFAULT_VERSION = '0.9.16'

# TODO: could probably be faster by opening the stream with TarFile and only
#       going until we hit the file we need...
def download_lib(version=DEFAULT_VERSION, tgz_filename=None):
    url = 'http://www.vlfeat.org/download/vlfeat-{}-bin.tar.gz'.format(version)

    # download file if we don't already have it
    if tgz_filename is None or not os.path.exists(tgz_filename):
        if tgz_filename is None:
            f = tempfile.NamedTemporaryFile(delete=False)
            tgz_filename = f.name
        else:
            f = open(tgz_filename, 'w+b')

        print('Downloading {} to {}'.format(url, tgz_filename), file=sys.stderr)

        try:
            r = urllib2.urlopen(urllib2.Request(url))
            try:
                shutil.copyfileobj(r, f)
            finally:
                r.close()
        finally:
            f.close()

    return tgz_filename


def pick_platform():
    plat = {
        'Linux': ('glnx', '86', 'a64', 'libvl.so'),
        'Darwin': ('maci', '', '64', 'libvl.dylib'),
        'Windows': ('win', '32', '64', 'vl.dll'),
    }
    base, s32, s64, fname = plat[platform.system()]
    return base + (s64 if platform.machine() == 'x86_64' else s32), fname


def extract_so(version, tgz_filename, out_dir):
    platform, fname = pick_platform()

    with tarfile.open(tgz_filename) as f:
        path = 'vlfeat-{}/bin/{}/{}'.format(version, platform, fname)
        so_f = f.extractfile(f.getmember(path))

        with open(os.path.join(out_dir, fname), 'wb') as outf:
            shutil.copyfileobj(so_f, outf)


def ensure_so(version, out_dir, tgz_filename=None):
    _, fname = pick_platform()

    if not os.path.exists(os.path.join(out_dir, fname)):
        tgz_filename = download_lib(version=version, tgz_filename=tgz_filename)
        extract_so(version=version, tgz_filename=tgz_filename, out_dir=out_dir)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', default=DEFAULT_VERSION)
    parser.add_argument('--tgz-filename')
    parser.add_argument('--out-dir',
            default=os.path.dirname(os.path.abspath(__file__)))
    args = parser.parse_args()

    ensure_so(**vars(args))

if __name__ == '__main__':
    main()
