PACKAGE_NAME="vendor.zip"
OUTPUT="/mnt/c/Users/souam/Documents/Data Engineering/flights-metrics/."


function cleanup()  {
    # remove vendor folder
    rm -rfd vendor
}

function install_dependencies() {
    mkdir vendor
    mkdir vendor/python
    pipenv requirements > requirements.txt
    pip install -r requirements.txt --no-deps -t vendor/python
}

function build_zip(){
    cd vendor
    zip -r ../${PACKAGE_NAME} .
    cd ..
}

function copy_to_windows(){
    cp vendor.zip "${OUTPUT}"
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