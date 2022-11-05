#!/bin/bash

# pipenv 仮想環境を起動してから実行する
PROJECT_DIR=$(pwd)
SITE_PACKAGES_DIR=$(pipenv --venv)/lib/python3.9/site-packages

echo "Project Location: $PROJECT_DIR"
echo "Library Location: $SITE_PACKAGES_DIR"

# to zip site-packages
cd $SITE_PACKAGES_DIR
rm -rf __pycache__  # your option 容量節約のため．
zip -r $PROJECT_DIR/lambda.zip *

# add lambda-function script(.py)
cd $PROJECT_DIR/src
zip -g ../lambda.zip hello_world.py  # zip に Python スクリプトを追加

# display zip file
ls | grep *.zip