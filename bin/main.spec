import os
import glob
import sys

sys.setrecursionlimit(14000000)

from PyInstaller.utils.hooks import is_module_satisfies
import PyInstaller.compat
PyInstaller.compat.is_module_satisfies = is_module_satisfies
from PyInstaller.utils.hooks import collect_submodules

def extra_datas(mydir):
    def rec_glob(p, files):
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas


a = Analysis([r"..\src\main.py"],
             pathex=['./'],
             hiddenimports=['scipy.linalg'] + ['scipy._lib.messagestream'],
             hookspath=None,
             runtime_hooks=None,
			 excludes = ['PyQt4','wx', 'pyqtgraph' 'IPython','zmq'])

for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

a.datas += extra_datas('resources')

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SimNDT.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='resources/logo.ico')


coll = COLLECT(exe,
			   a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='SimNDT')
