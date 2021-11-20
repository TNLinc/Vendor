#!/bin/bash


# script dir
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
TEST_DIR="$( cd -P "$( dirname "$DIR" )" >/dev/null 2>&1 && pwd )"

# load
export $(grep -v '^#' $TEST_DIR/.env.test | xargs -0)

# Start server
docker run -d -p"$TEST_DB_PORT":5432 -e POSTGRES_PASSWORD="$TEST_DB_PASSWORD" -e POSTGRES_DB="$TEST_DB_NAME" tnlinc/db:latest