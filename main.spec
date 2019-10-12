# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( '.\Resource\\add-icon.png', 'Resource' ),
         ( '.\Resource\\about-icon.png', 'Resource' ),
         ( '.\Resource\\close-icon.png', 'Resource' ),
         ( '.\Resource\\steam-icon.png', 'Resource' ),
         ( '.\Resource\\delete-icon.png', 'Resource' )
         ]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\nath\\PycharmProjects\\SteamAccountManager'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Steam Account Manager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='C:\\Users\\nath\\PycharmProjects\\SteamAccountManager\\resource\\SAM.ico')
