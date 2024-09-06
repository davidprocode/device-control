from distutils.core import setup
from glob import glob
import py2exe

data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]

setup(
    data_files=data_files,
    console=[
        {'script': 'host.py', 'dest_base': 'host'},
        {'script': 'client.py', 'dest_base': 'client'}
    ],
    options={
        'py2exe': {
            'bundle_files': 1,  # Agrupa tudo em um único arquivo
            'compressed': True,  # Comprime o arquivo de biblioteca
            'dist_dir': 'dist',  # Define o diretório de saída
        }
    },
    zipfile=None,  # Não cria um arquivo zip separado
    py_modules=['host', 'client']  # Define explicitamente os módulos
)
