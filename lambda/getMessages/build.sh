#!/bin/sh

poetry sync
mkdir -p dist
cp -R .venv/lib/python*/site-packages/* dist
cp src/getmessage/getMessage.py dist
cd dist
zip -r ../lambda.zip .
