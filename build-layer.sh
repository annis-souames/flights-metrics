#!/bin/bash

# this is b/c pipenv stores the virtual env in a different
# directory so we need to get the path to it
SITE_PACKAGES=$(pipenv --venv)/lib/python3.10/site-packages
OUTPUT="/mnt/c/Users/souam/Documents/Data Engineering/flights-metrics/."

echo "Library Location: $SITE_PACKAGES"
DIR=$(pwd)

# Make sure pipenv is good to go
#echo "Do fresh install to make sure everything is there"
#pipenv install

cd $SITE_PACKAGES
zip -r9 $DIR/vendor.zip *

cp $DIR/vendor.zip "${OUTPUT}"


#cd $DIR
#zip -g package.zip posts.py







# PACKAGE_NAME="vendor.zip"
# OUTPUT="/mnt/c/Users/souam/Documents/Data Engineering/flights-metrics/."


# function cleanup()  {
#     # remove vendor folder
#     rm -rfd vendor
# }

# function install_dependencies() {
#     mkdir vendor
#     mkdir vendor/python
#     cd $SITE_PACKAGES
#     zip -r9 $DIR/package.zip *
# }

# function build_zip(){
#     cd vendor
#     zip -r ../${PACKAGE_NAME} .
#     cd ..
# }

# function copy_to_windows(){
#     cp vendor.zip "${OUTPUT}"
# }

# # function copy_source_files() {
# #     # recursively copy all the source files to target/python folder
# #     cp -R emrlauncher/ target/python
# # }

# # function package() {
# #     # recursively zip contents inside target folder
# #     cd target/ && zip -r ${PACKAGE_NAME} .
# # }

# cleanup
# install_dependencies
# build_zip
# copy_to_windows
