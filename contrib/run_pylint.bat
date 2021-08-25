@echo off
@rem "to specify default python version to 3.9 create/edit ~/AppData/Local/py.ini with [default] set
@rem to python3=3.9"
set REPO_DIR=%~dp0..\headless-python
py -3.9 -m pip install pylint -U
py -3.9 -m pylint --rcfile ../.pylintrc %REPO_DIR%
