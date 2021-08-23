#!/usr/bin/env bash
set -e

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SCRIPT=$(readlink -f "$0")
    SCRIPTDIR=$(dirname "$SCRIPT")
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install coreutils
    SCRIPT=$(greadlink -f "$0")
    SCRIPTDIR=$(dirname "$SCRIPT")
else
    echo "this platform is not supported"
    exit 0
fi

$SCRIPTDIR/python/python.exe "$SCRIPTDIR"/python/install/bin/electrumsv-sdk.py "$@"
