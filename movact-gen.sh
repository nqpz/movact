#!/bin/bash
# You are free to run, copy, share and modify this script. ~Public domain.

cp -a . $HOME/movact

cd $HOME/movact/
find -name '*~' -type f -exec rm {} \;
find -name '#*#' -type f -exec rm {} \;
rm -r bak/ .bzr/
rm movact-gen.sh
clwot < README > .README.UPDATED
mv .README.UPDATED README

version=`cat VERSION`
rm VERSION

cd $HOME/
tar -czf $HOME/movact-$version.tar.gz movact

rm -r $HOME/movact/
