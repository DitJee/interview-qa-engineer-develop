#!/usr/bin/env bash
set -e

psql -U postgres airline -a -f /home/scripts/$1
