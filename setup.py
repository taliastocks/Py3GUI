#!/usr/bin/python

import os
import sys

from distutils.core import setup
import py2exe

import glob
import matplotlib



__file__ = os.path.abspath(__file__)
os.chdir(os.path.dirname(__file__))

def purgeDir(dirname):
    sys.stderr.write('Purging directory %s\n' % dirname)
    sys.stderr.flush()
    for path, dirs, files in os.walk(dirname, topdown = False):
        for fname in files:
            try:
                fullpath = os.path.join(path, fname)
                os.remove(fullpath)
            except:
                pass
        for dir in dirs:
            try:
                fullpath = os.path.join(path, dir)
                os.rmdir(fullpath)
            except:
                pass
        try:
            os.rmdir(path)
        except:
            pass

def copy(fname, dir = '', newname = None):
    if newname == None:
        newname = os.path.basename(fname)
    targetdir = os.path.join('dist', dir)
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    from_path = fname
    to_path = os.path.join(targetdir, newname)
    sys.stderr.write('Copying file from %s to %s\n' % (from_path, to_path))
    sys.stderr.flush()
    from_file = open(from_path, 'rb')
    to_file = open(to_path, 'wb')
    data = None
    while data != '':
        data = from_file.read(4096)
        to_file.write(data)

def main(argv = []):
    purgeDir('build')
    purgeDir('dist')
    setup(
        name = 'Py3GUI',
        author = 'Collin Stocks',
        windows = [{'script': 'py3gui.py'}],
        #zipfile = None,
        options = {
            'py2exe':{
                'includes': [
                    'numpy', 'scipy', 'cvxopt', 'cvxopt.lapack', 'matplotlib',
                    'matplotlib.pyplot', 'matplotlib.figure',
                    'matplotlib.backends.backend_tkagg', 'pylab',
                ],
                'excludes': [
                    'IPython', 'OpenGL', 'pygame', 'VisionEgg', 'Image',
                    'doctest', 'pdb', 'win32com', '_ssl',
                    '_gtkagg', '_agg2', '_cairo', '_cocoaagg', '_gtk',
                    '_gtkcairo', '_qt4agg',
                ],
                'dll_excludes': [
                    'msvcm90.dll', 'msvcr90.dll', 'msvcp90.dll',
                ],
                'optimize': 1,
                'compressed': 2,
                'ascii': True,
            }
        },
        data_files = matplotlib.get_py2exe_datafiles(),
    )
    copy('logo.gif')
    winsxsdir = os.path.join(os.path.expandvars('${SystemRoot}'), 'WinSxS')
    msvc90dir = os.path.join(
        winsxsdir,
        [dirname for dirname in
            os.listdir(
                os.path.expandvars(
                    os.path.join('${SystemRoot}', 'WinSxS')
                )
            ) if 'Microsoft.VC90.CRT' in dirname
         ][0]
    )
    copy(os.path.join(msvc90dir, 'msvcm90.dll'), 'Microsoft.VC90.CRT')
    copy(os.path.join(msvc90dir, 'msvcr90.dll'), 'Microsoft.VC90.CRT')
    copy(os.path.join(msvc90dir, 'msvcp90.dll'), 'Microsoft.VC90.CRT')
    manifestsdir = os.path.join(winsxsdir, 'Manifests')
    manifest = os.path.join(
        manifestsdir,
        [fname for fname in
            os.listdir(
                manifestsdir
            ) if 'Microsoft.VC90.CRT' in fname and fname.endswith('.manifest')
        ][0]
    )
    copy(manifest, 'Microsoft.VC90.CRT',
        newname = 'Microsoft.VC90.CRT.manifest')
    from numpy.fft import fftpack_lite
    copy(fftpack_lite.__file__)
    from scipy.integrate import _quadpack
    copy(_quadpack.__file__)
    from scipy.optimize import minpack2
    copy(minpack2.__file__)
    from cvxopt import lapack
    copy(lapack.__file__)
    purgeDir('dist/tcl/tk8.4/demos')
    purgeDir('dist/tcl/tk8.4/images')
    purgeDir('dist/tcl/tcl8.4/dde1.1')
    purgeDir('dist/tcl/tcl8.4/encoding')
    purgeDir('dist/tcl/tcl8.4/http1.0')
    purgeDir('dist/tcl/tcl8.4/http2.3')
    purgeDir('dist/tcl/tcl8.4/http2.5')
    purgeDir('dist/tcl/tcl8.4/msgcat1.0')
    purgeDir('dist/tcl/tcl8.4/msgcat1.3')
    purgeDir('dist/tcl/tcl8.4/opt0.4')
    purgeDir('dist/tcl/tcl8.4/tcltest1.0')
    purgeDir('dist/tcl/tcl8.4/tcltest2.2')
    purgeDir('build')

if __name__ == '__main__':
    sys.argv.append('py2exe')
    main(sys.argv[1:])

