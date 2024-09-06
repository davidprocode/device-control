from distutils.core import setup
from glob import glob
import py2exe

data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]

setup(
    data_files=data_files,
    console=['host.py'],
    console=['client.py'],
    options={
        'py2exe': {
            'bundle_files': 1,  # Bundle everything into a single file
            'compressed': True,  # Compress the library archive
        }
    },
    zipfile=None  # Do not create a separate zip file
)
