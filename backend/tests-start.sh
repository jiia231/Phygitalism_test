#! /usr/bin/env bash
set -e

coverage run -m pytest

coverage report --fail-under 80
