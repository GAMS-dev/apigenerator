#!/bin/bash

set e

echo $WSYS
TESTDIR=$(pwd)

fails=0

${TESTDIR}/wrptest.run ./wrpccctest || (( fails=fails+${?} ))

if [ ${WSYS} = unix ] ; then
   export LD_LIBRARY_PATH=${TESTDIR}
   echo $LD_LIBRARY_PATH
fi

if which java > /dev/null ; then
   java -classpath . -Djava.library.path=. com.gams.tester.testerjava || (( fails=fails+${?} ))
else
   echo "java not found in PATH variable, skipped testerjava"
   fails=$((fails+1))
fi

if which python3 > /dev/null ; then
   python testerpy.py || (( fails=fails+${?} ))
else
   echo "python not found, skipped testerpy"
   fails=$((fails+1))
fi

echo "Finished all apiwrapper tests: ${fails} fails"
exit $fails
