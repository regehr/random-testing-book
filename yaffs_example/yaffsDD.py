# $Id: GCCDD.py,v 1.1 2001/11/05 19:53:33 zeller Exp $
# Using delta debugging on GCC input

import DD
import subprocess
import string
import sys

class MyDD(DD.DD):
    def __init__(self):
        DD.DD.__init__(self)
        
    def _test(self, deltas):
        print "TESTING"
        # Build input
        input = ""
        for (index, line) in deltas:
            input = input + line

        # Write input to `testDD.c'
        out = open('testDD.c', 'w')
        out.write(input)
        out.close()

        print self.coerce(deltas)

        rv = subprocess.call(["gcc -o testDD testDD.c yaffs2.o -DCONFIG_YAFFS_DIRECT -DCONFIG_YAFFS_YAFFS2 -DCONFIG_YAFFS_PROVIDE_DEFS -DCONFIG_YAFFSFS_PROVIDE_VALUES -I inc -I yaffs2 -g -coverage -O2 -DFAIL_VERBOSE >& /dev/null"], shell=True)

        if rv != 0:
            return self.PASS
        
        rv = subprocess.call(["./testDD"], shell=True)

        if rv == 0:
            return self.PASS

        return self.FAIL

    def coerce(self, deltas):
        # Pretty-print the configuration
        input = ""
        for (index, character) in deltas:
            input = input + character
        return input


if __name__ == '__main__':
    deltas = []
    f = open(sys.argv[1])
    fc = f.read()
    f.close()
    fcs = fc.split("  test(")
    deltas.append((1, fcs[0]))
    index = 2
    for chunk in fcs[1:]:
        deltas.append((index, "  test(" + chunk))
        index += 1

    mydd = MyDD()
    
    print "Simplifying failure-inducing input..."
    c = mydd.ddmin(deltas)              # Invoke DDMIN
    print "The 1-minimal failure-inducing input is", mydd.coerce(c)
    print "Removing any element will make the failure go away."


    f = open(sys.argv[2],'w')
    f.write(mydd.coerce(c))
    f.close()
    # print
    
    # print "Isolating the failure-inducing difference..."
    # (c, c1, c2) = mydd.dd(deltas)	# Invoke DD
    # print "The 1-minimal failure-inducing difference is", c
    # print mydd.coerce(c1), "passes,", mydd.coerce(c2), "fails"




# Local Variables:
# mode: python
# End:
