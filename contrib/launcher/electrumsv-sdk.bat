@echo off
set BATCH_DIR=%~dp0

%BATCH_DIR%\python\python.exe %BATCH_DIR%\python\Scripts\electrumsv-sdk.py %*
