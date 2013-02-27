import subprocess
import sys

N = int(sys.argv[1])
testGen = sys.argv[2]
length = int(sys.argv[3])

for l in xrange(0, N):
    n = str(l)
    subprocess.call(["python " + testGen + " test" + n + ".c " + str(length)],
                       shell=True)
    subprocess.call(["gcc -o test" + n + " test" + n + ".c yaffs2.o -DCONFIG_YAFFS_DIRECT -DCONFIG_YAFFS_YAFFS2 -DCONFIG_YAFFS_PROVIDE_DEFS -DCONFIG_YAFFSFS_PROVIDE_VALUES -I inc -I yaffs2 -g -coverage -O2 -DVERBOSE=0"], shell=True)
    subprocess.call(["./test" + n], shell=True)
    subprocess.call(['gcov yaffs2.c | grep "Lines executed" | head -n1'], shell=True)
    subprocess.call(["rm -rf test" + n + " test" + n + ".c test" + n + ".gcda test" + n + ".gcno"], shell=True)
