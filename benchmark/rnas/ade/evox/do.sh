set -x

mode=simrna5x200
mkdir $mode
cd $mode
evox.py -s 200 -e -p ade
cd ..

mode=simrna5x300
mkdir $mode
cd $mode
evox.py -s 300 -e -p ade
cd ..

mode=simrna5x400
mkdir $mode
cd $mode
evox.py -s 400 -e -p ade
cd ..
