import random
import sys
import subprocess
import types

outFile = sys.argv[1]
length = int(sys.argv[2])

assert (subprocess.call(["cp headerv2.c " + outFile], shell=True) == 0)

outf = open(outFile,'a')

gen = {}

pathElements = ["alpha","beta","gamma","delta","epsilon"]
def pathname():
    path = '"/yaffs2'
    while random.randint(0,1) != 0:
        path += "/" + random.choice(pathElements)
    path += '"'
    return path

modes = ["S_IREAD","S_IWRITE"]
def mode():
    m = random.choice(modes)
    while random.randint(0,1) != 0:
        m += " | " + random.choice(modes)
    return m

flags = ["O_CREAT","O_APPEND", "O_RDWR", "O_RDONLY", "O_WRONLY"]
def flag():
    f = random.choice(flags)
    while random.randint(0,1) != 0:
        f += " | " + random.choice(flags)
    return f

NUM_BUFFERS = 4
def buffer():
    return "rwBuf[" + str(random.randint(0, NUM_BUFFERS)) + "]"

MAX_BYTES = 10000
def bytes():
    return str(random.randint(0, MAX_BYTES))

calls = {"yaffs_freespace" : ((), [pathname]),
         "yaffs_mkdir" : ((), [pathname, mode]),
         "yaffs_rmdir" : ((), [pathname]),
         "yaffs_rename" : ((), [pathname, pathname]),
         "yaffs_open" : ("h", [pathname, flag, mode]),
         "yaffs_close" : ((), ["h"]),
         "yaffs_read" : ((), ["h", buffer, bytes]),
         "yaffs_write" : ((), ["h", buffer, bytes])}
def call():
    f = random.choice(calls.keys())
    c = f+"("
    (res, params) = calls[f]
    if res != ():
        if res not in gen:
            gen[res] = 0
        else:
            gen[res] += 1
        c = res + "[" + str(gen[res]) + "] = " + c
    for p in params:
        if type(p) == types.StringType:
            c += p + "[" + str(random.randint(0,gen[p])) + "], "
        else:
            c += p() + ", "
    cp = c.rfind(", ")
    if (cp != -1):
        c = c[0:cp]
    return c + ")"

def addCall(s):
    outf.write("  callFunc(" + s + ', "' + s.replace('"', '\\"') + '");\n')

for s in xrange(0,length):
    try:
        addCall(call())
    except KeyError:
        pass

outf.write('  printf("TEST SUCCESSFULLY COMPLETED.\\n");\n')
outf.write('  exit(0);\n')
outf.write("}\n")
outf.close()
