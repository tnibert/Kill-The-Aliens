rem tested with 32 bit gcc/mingw 7.2.0/5.0.3 and 32 bit python 2.7 on Windows 10
rem your paths to python and mingw may vary

set OLDPATH=%PATH%
set PATH=C:\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\bin;%PATH%

rem create a temp pyw file so we don't get a console when we launch the game
copy killthealiens.py killthealiens.pyw

call C:\Python27-32\python.exe -m nuitka --show-progress --windows-disable-console --follow-imports --standalone killthealiens.pyw

del killthealiens.pyw

rem copy file resources to build directory
xcopy *.png killthealiens.dist\
xcopy *.mp3 killthealiens.dist\

ren killthealiens.dist killthealiens-win32

rem create zip file of build
mkdir winbuild
move killthealiens-win32 winbuild
copy README-Windows.txt winbuild
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('winbuild', 'killthealiens.zip'); }"

rem clean up
set PATH=%OLDPATH%
rmdir winbuild /S /Q
rmdir killthealiens.build /S /Q