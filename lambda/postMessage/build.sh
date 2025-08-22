#!/bin/sh

poetry sync
mkdir -p dist
cp --recursive .venv/lib/python*/site-packages/* dist
cp src/postMessage/postMessage.py dist
cd dist
zip -r ../lambda.zip .
