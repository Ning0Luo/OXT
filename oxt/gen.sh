#!/bin/sh
pyinstaller  --workpath /tmp/build --distpath  ../exe server.py
pyinstaller  --workpath /tmp/build --distpath ../exe client.py
