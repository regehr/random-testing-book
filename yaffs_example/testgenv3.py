import random
import sys
import subprocess
import types

outFile = sys.argv[1]
length = int(sys.argv[2])
genRef = not("--noRef" in sys.argv)

assert (subprocess.call(["cp headerv3.c " + outFile],shell=True) == 0)

outf = open(outFile,'a')

gen = {}

pathElements = ["alpha","beta","gamma","delta","epsilon"]
def pathname():
    path = '"/yaffs2'
    while random.randint(0,1) != 0:
        path += "/" + random.choice(pathElements)
    path += '"'
    return path

def concatProb(opts,P,c):
    m = filter(lambda opt: random.random() < P, opts)
    if m == []:
        return random.choice(opts)
    else:
        return reduce(lambda s,o: s + c + o, m[0:-1], m[-1])

def mode():
    return concatProb(["S_IREAD", "S_IWRITE"], 0.5, "|")

def flag():
    return concatProb(["O_CREAT","O_APPEND","O_RDWR","O_RDONLY","O_WRONLY"], 0.5, "|")

NUM_BUFFERS = 4
def buffer():
    return "rw[" + str(random.randint(0,NUM_BUFFERS)) + "]"

MAX_BYTES = 2048*3
def bytes():
    return str(random.randint(0,MAX_BYTES))
def offset():
    return str(random.randint(0,MAX_BYTES))

def whence():
    return random.choice(["SEEK_SET","SEEK_CUR","SEEK_END"])

calls = {
    "yaffs_mkdir" : ((), [pathname, mode]),
    "yaffs_rmdir" : ((), [pathname]),
    "yaffs_rename" : ((), [pathname, pathname]),
    "yaffs_open" : ("h", [pathname, flag, mode]),
    "yaffs_close" : ((), ["h"]),
    "yaffs_read" : ((), ["h", buffer, bytes]),
    "yaffs_write" : ((), ["h", buffer, bytes]),
    "yaffs_unlink" : ((), [pathname]),
    "yaffs_truncate" : ((), [pathname, offset]),
    "yaffs_ftruncate" : ((), ["h", offset]),
    "yaffs_lseek" : ((), ["h", offset, whence])
    }
def param(p):
    if type(p) == types.StringType:
        return p + "[" + str(random.randint(0,gen[p])) + "]"
    else:
        return p()
def call():
    f = random.choice(calls.keys())
    c = f + "("
    (res,params) = calls[f]
    if res != ():
        gen[res] = gen.get(res,-1) + 1
        c = res + "[" + str(gen[res]) + "] = " + c
    return c + reduce(lambda c2,p: c2 + param(p) + ", ", params[:-1], "") + param(params[-1]) + ")"

refMap = [('"/yaffs2', '"/dev/shm'),
          ("yaffs_", ""),
          ("h[", "fd["),
          ("rw[", "rwRef[")]
def ref(s):
    return reduce(lambda s2,(t,r): s2.replace(t,r), refMap, s) 

def addCall(s):
    msg = s.replace('"','\\"')
    outf.write("  test(" + s + ', "' + msg  + '");\n')
    if genRef:
        outf.write("  ref(" + ref(s) + ', "' + msg  + '");\n')

for s in xrange(0,length):
    try:
        addCall(call())
    except KeyError:
        pass

outf.write('  printf("TEST SUCCESSFULLY COMPLETED.\\n");\n')
outf.write('  exit(0);\n')
outf.write("}\n")
outf.close()
