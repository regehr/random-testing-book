import random
import sys
import subprocess

outFile = sys.argv[1]
length = int(sys.argv[2])

assert (subprocess.call(["cp headerv1.c " + outFile], shell=True) == 0)

outf = open(outFile,'a')

pathElements = ["alpha","beta","gamma","delta","epsilon"]
def pathname():
    path = "\"/yaffs2"
    while random.randint(0,1) != 0:
        path += "/" + random.choice(pathElements)
    path += "\""
    return path

modes = ["S_IREAD","S_IWRITE"]
def mode():
    mode = random.choice(modes)
    while random.randint(0,1) != 0:
        mode += " | " + random.choice(modes)
    return mode

calls = {"yaffs_freespace" : [pathname],
         "yaffs_mkdir" : [pathname, mode],
         "yaffs_rmdir" : [pathname],
         "yaffs_rename" : [pathname, pathname]}
def call():
    f = random.choice(calls.keys())
    c = f+"("
    for p in calls[f]:
        c += p() + ", "
    cp = c.rfind(", ")
    if (cp != -1):
        c = c[0:cp]
    return c + ")"

def addCall(s):
    outf.write("  callFunc(" + s + ', "' + s.replace('"', '\\"') + '");\n')

for s in xrange(0,length):
    addCall(call())

outf.write("}\n")
outf.close()
