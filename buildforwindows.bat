@echo off
set WORKSPACE=%~dp0
pushd "%WORKSPACE%"

set output_folder=%WORKSPACE%\build\

call python -m PyInstaller killthealiens.py -y --onefile --log-level ERROR --clean --distpath %output_folder%

popd
