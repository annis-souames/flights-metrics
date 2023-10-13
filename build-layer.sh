#!/bin/bash

PACKAGE_NAME="vendor.zip"

function cleanup()  {
    # remove target folder
    rm -rfd target
}

function install_dependencies() {
    mkdir target
    mkdir target/python
    # install the project dependencies inside target/python folder
    pip3 install --target=target/python -r requirements.txt
}

function build_zip(){
    cd vendor

    zip -r ../${PACKAGE_NAME} .
    cd ..
}

function copy_to_windows(){
    cp vendor.zip /mnt/c/Users/souam/Documents/.
}

# function copy_source_files() {
#     # recursively copy all the source files to target/python folder
#     cp -R emrlauncher/ target/python
# }

# function package() {
#     # recursively zip contents inside target folder
#     cd target/ && zip -r ${PACKAGE_NAME} .
# }

cleanup
install_dependencies
build_zip
copy_to_windows
