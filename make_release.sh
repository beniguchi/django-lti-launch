#!/bin/sh

set -e

usage ( ) {
    echo "usage: make_release.sh NEXT-VERSION"
    exit 1
}

if [ $# != 1 ]
then
    usage
fi

git checkout -B master origin/master

RELEASE_VERSION=`cat VERSION`
NEXT_VERSION=$1

if [ $RELEASE_VERSION == $NEXT_VERSION ]
then
    echo error: NEXT-VERSION should be different from current version
    exit 2
fi

git fetch --tags
EXISTING=`git tag | grep "^\(${RELEASE_VERSION}\|${NEXT_VERSION}\)$" | head -n 1`
if [ $EXISTING ]
then
    echo error: tag for version $EXISTING already exists
    exit 3
fi

git tag $RELEASE_VERSION
python3 setup.py sdist
echo ${NEXT_VERSION} > VERSION
git add VERSION
git commit -m "Set VERSION to ${NEXT_VERSION}"
git push
git push --tags
