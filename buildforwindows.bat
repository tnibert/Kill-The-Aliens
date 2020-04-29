rem Must compile with python 3.6 or you will get a libvorbisfile.dll error at run time
rem This has been used with mingw64 and python 3.6, both 64 bit, on Windows 10
rem You must adjust your paths as they will differ

set OLDPATH=%PATH%

set PATH=C:\mingw64\mingw64\bin;%PATH%
set CC=C:\mingw64\mingw64\bin\gcc.exe

set PYTHON=C:\Users\Tim\AppData\Local\Programs\Python\Python36\python.exe

rem --windows-disable-console will hide errors unfortunately
call %PYTHON% -m nuitka --show-progress --windows-disable-console --follow-imports --standalone killthealiens.py

rem copy file resources to build directory
cd killthealiens.dist
mkdir assets
cd ..
robocopy assets\ killthealiens.dist\assets\ /MIR

ren killthealiens.dist killthealiens-windows

rem create zip file of build
mkdir winbuild
move killthealiens-windows winbuild
copy README-Windows.txt winbuild
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('winbuild', 'killthealiens.zip'); }"

rem clean up
set PATH=%OLDPATH%
rem rmdir winbuild /S /Q
rmdir killthealiens.build /S /Q