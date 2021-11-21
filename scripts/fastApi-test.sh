#!/bin/bash


# Get dirs
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="$( cd -P "$( dirname "$DIR" )" >/dev/null 2>&1 && pwd )"

# Load .env.test
echo "Load .env.test"
set -a
source $BASE_DIR/tests/.env.test
set +a

# Start DB
echo "Start DB"
CONTAINER_ID=$(docker run -d -p"$TEST_DB_PORT":5432 \
-e POSTGRES_PASSWORD="$TEST_DB_PASSWORD" \
-e POSTGRES_DB="$TEST_DB_NAME" --rm tnlinc/db:latest)


# Go to the root project dir
cd "$BASE_DIR" || exit

# Wait DB
python tests_pre_start.py

# Run tests
echo "Run tests"
pytest . -v -s

# Stop docker
echo "Stop DB"
docker stop "$CONTAINER_ID"