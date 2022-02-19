# run this script to regenerate the test verification files
# visual validation of these files is then recommended

export TEST_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))
export ROOT_DIR=${TEST_DIR}/..

# generate the configuration file schema
cd ${ROOT_DIR}
pipenv run maaspower schema tests/samples/maaspower.schema.json
