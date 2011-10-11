#usage: python setup.py py2exe
#note requires installation of py2exe. see \\ilstore.il.nds.com\STB-Integration\Tools\LinkedTools\PythonInstall

# py2exe can't work with eggs.
# I had to remove simple-json by:
# - easy_install -m simplejson
# - go to C:\Python26\Lib\site-packages and delete the egg of simplejson
# then I have re-installed correctly: easy_install --always-unzip simplejson
#
# same for py_dom_xpath
#
#for instructions, see http://ndpedia/index.php/CMDCS_Simulator_release

from distutils.core import setup
import py2exe
import sys



includes = []
excludes = []
packages = []
dll_excludes = ['w9xpopen.exe'] #only required for win 95/98
extra_files = [("resources", ["resources\\acc.png", "resources\\acc.ico"])#,
    #"winDist\\msvcr90.dll", "winDist\\Microsoft.VC90.CRT.manifest"
]

setup(
    name='PowerOnOff',
    author='Ilan Finci',
    data_files=extra_files ,
    zipfile=None,
    options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": "WinDist\\PowerOnOff",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": ''
                         }
              },
    windows=[
        {
        "script" : 'powerOnOff.py',
        "icon_resources": [(0x004, "resources\\acc.ico")]
        }
    ]
)    
