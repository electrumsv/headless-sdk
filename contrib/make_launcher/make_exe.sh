#!/usr/bin/env bash
set -e
pyinstaller --console -F ./electrumsv-sdk.py -i ./electrum-sv.ico
