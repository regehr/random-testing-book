import random
import sys
import time
import testfeedback as T

T.processOpts({"seed"   : time.time(),
               "ref"    : False,
               "length" : 100})
random.seed(int(T.opts["seed"]))
T.setupTestFile()

pathHistory = ['"/yaffs2"']
pathComps = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]
Rpathname = lambda: '"/yaffs2' + T.any(pathComps, 0.5, "/") + '"'

def pathname():
    if random.random() < 0.05:
        return Rpathname()
    else:
        path = random.choice(pathHistory)
        if random.random() < 0.5:
            path = path[0:-1] + "/" + random.choice(pathComps) + '"'
        return path
    
def Cpathname():
    path = pathname()
    if path not in pathHistory:
        pathHistory.append(path)
    return path

mode = lambda: T.someOf(["S_IREAD", "S_IWRITE"], 0.5, "|")
flag = lambda: T.someOf(["O_CREAT", "O_APPEND", "O_RDWR", "O_RDONLY", "O_WRONLY"], 0.5, "|")

NUM_BUFFERS = 4
buffer = lambda: "rw[" + str(random.randint(0,NUM_BUFFERS-1)) + "]"

MAX_BYTES = 2048*3
bytes = lambda: str(random.randint(0,MAX_BYTES-1))
offset = lambda: str(random.randint(0,MAX_BYTES-1))

whence = lambda: random.choice(["SEEK_SET", "SEEK_CUR", "SEEK_END"])

calls = {
    "yaffs_mkdir" : ((), [Cpathname, mode]),
    "yaffs_rmdir" : ((), [pathname]),
    "yaffs_rename" : ((), [pathname, Cpathname]),
    "yaffs_open" : ("h", [Cpathname, flag, mode]),
    "yaffs_close" : ((), ["!h"]),
    "yaffs_read" : ((), ["h", buffer, bytes]),
    "yaffs_write" : ((), ["h", buffer, bytes]),
    "yaffs_unlink" : ((), [pathname]),
    "yaffs_truncate" : ((), [pathname, offset]),
    "yaffs_ftruncate" : ((), ["h", offset]),
    "yaffs_lseek" : ((), ["h", offset, whence])
    }

refMap = [('"/yaffs2', 'REFPATH "'),
          ("yaffs_", ""),
          ("h[", "fd["),
          ("rw[", "rwRef[")]

s = 0
while s < int(T.opts["length"]):
    try:
        T.addCall(calls, refMap)
        s += 1
    except (KeyError, IndexError):
        pass

T.finishTest()
