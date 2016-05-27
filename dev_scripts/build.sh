#!/usr/bin/env bash

TEMP_DIR=$(mktemp -d)
BUILD_DIR="${TEMP_DIR}/django-lti-launch"

mkdir -p "${BUILD_DIR}"
cp -r django_lti_launch/ltilaunch LICENSE README.md MANIFEST.in setup.py \
    requirements/ "${BUILD_DIR}"
pushd .
cd "${BUILD_DIR}"
python3 setup.py sdist
popd
cp -r "${BUILD_DIR}"/dist .
rm -r "${TEMP_DIR}"