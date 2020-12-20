#!/bin/sh
set -ex

pip install -Ur dev-requirements.txt
pre-commit install
pre-commit run -a
tox
