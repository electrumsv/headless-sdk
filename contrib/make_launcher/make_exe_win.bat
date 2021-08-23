@echo off
set BATCH_DIR=%~dp0

PUSHD %BATCH_DIR%
pyinstaller --console -F %BATCH_DIR%\electrumsv-sdk.py -i electrum-sv.ico
POPD

copy %BATCH_DIR%\.env %BATCH_DIR%\dist\.env
