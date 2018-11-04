rem tested with 32 bit gcc/mingw 7.2.0/5.0.3 and 32 bit python 2.7
rem your paths to python and mingw may vary
set PATH=C:\Program Files (x86)\mingw-w64\i686-8.1.0-posix-dwarf-rt_v6-rev0\mingw32\bin;%PATH%
call C:\Python27-32\python.exe -m nuitka --follow-imports --standalone killthealiens.py