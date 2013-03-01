import subprocess
import sys

N = int(sys.argv[1])
testGen = sys.argv[2]
args = sys.argv[3]
runOpts = sys.argv[4]

for l in xrange(0, N):
    n = str(l)
    subprocess.call(["python " + testGen + " test" + n + ".c " + args], shell=True)
    subprocess.call(["gcc -o test" + n + " test" + n + ".c yaffs2.o -DCONFIG_YAFFS_DIRECT -DCONFIG_YAFFS_YAFFS2 -DCONFIG_YAFFS_PROVIDE_DEFS -DCONFIG_YAFFSFS_PROVIDE_VALUES -I inc -I yaffs2 -g -coverage -O2 " + runOpts + " >& /dev/null"], shell=True)
    rv = subprocess.call(["./test" + n], shell=True)
    if rv == 0:
        subprocess.call(["rm -rf test" + n + " test" + n + ".c test" + n + ".gcda test" + n + ".gcno"], shell=True)
