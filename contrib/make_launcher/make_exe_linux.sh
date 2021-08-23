#!/usr/bin/env bash
set -e

SCRIPT=$(readlink -f "$0")
SCRIPTDIR=$(dirname "$SCRIPT")

pushd "$SCRIPTDIR"
pyinstaller --console -F "$SCRIPTDIR/electrumsv-sdk.py" -i electrum-sv.ico
POPD

cp "$SCRIPTDIR"/.env "$SCRIPTDIR"/dist/.env
