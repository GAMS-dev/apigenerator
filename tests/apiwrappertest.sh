#!/bin/bash

set e

SRCDIR=$(pwd)
TESTDIR=$(pwd)/wrptest

set -x
if [ ${WSYS} = unix ] ; then
   export LD_LIBRARY_PATH=${TESTDIR}
fi

fails=0

${SRCDIR}/wrptest.run ${TESTDIR}/wrpccctest || (( fails=fails+${?} ))

if [ ${WSYS} = windows ] ; then
   ${TESTDIR}/testercs.exe || (( fails=fails+${?} ))
   ${TESTDIR}/testervbnet.exe || (( fails=fails+${?} ))
fi

if which java > /dev/null ; then
   java -classpath ${TESTDIR} -Djava.library.path=${TESTDIR} com.gams.tester.testerjava || (( fails=fails+${?} ))
else
   echo "java not found in PATH variable, skipped testerjava"
   fails=$((fails+1))
fi

if which python > /dev/null ; then
   python ${TESTDIR}/testerpy.py || (( fails=fails+${?} ))
else
   echo "python not found, skipped testerpy"
   fails=$((fails+1))
fi
set +x

echo "Finished all apiwrapper tests: ${fails} fails"
exit $fails
