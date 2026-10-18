#!/bin/sh
set -eu

export PGADMIN_DEFAULT_EMAIL="$(cat /run/secrets/pgadmin_email)"
export PGADMIN_DEFAULT_PASSWORD="$(cat /run/secrets/pgadmin_password)"

exec /entrypoint.sh