#!/bin/bash

set -e
if [[ -x /usr/src/espurna/code/build.sh ]]; then
  cd /usr/src/espurna/code
  ./build.sh $@
fi
