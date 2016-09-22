# -*- mode: python -*-
a = Analysis(['MetGeomi.py'],
             pathex=['C:\\Users\\Aly\\Downloads\\NIC'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MetGeomi.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='crawl.ico')
