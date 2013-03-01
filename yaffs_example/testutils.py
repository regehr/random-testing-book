import random
import sys
import subprocess
import types

gen = {}

def processOpts(defaults):
    global opts
    opts = defaults
    for o in sys.argv:
        if o.find("--") == 0:
            if "=" in o:
                es = o.split("=")
                opts[es[0].split("--")[1]] = es[1]
            else:
                opts[o.split("--")[1]] = True

def setupTestFile():
    global outf
    outFile = sys.argv[1]
    assert (subprocess.call(["cp headerv3.c " + outFile],shell=True) == 0)
    outf = open(outFile,'a')

def finishTest():
    outf.write('  printf("TEST SUCCESSFULLY COMPLETED.\\n");\n')
    outf.write('  exit(0);\n')
    outf.write("}\n")
    outf.close()

def someOf(choices, P, c):
    m = filter(lambda c: random.random() < P, choices)
    if m == []:
        return random.choice(choices)
    else:
        return reduce(lambda s, o: s + c + o, m[0:-1], m[-1])

def any(choices, P, c):
    r = ""
    while random.random() < P:
        r += c + random.choice(choices)
    return r

def param(p):
    if type(p) == types.StringType:
        return p + "[" + str(random.randint(0,gen[p])) + "]"
    else:
        return p()
    
def call(calls):
    f = random.choice(calls.keys())
    c = f + "("
    (res, params) = calls[f]
    if res != ():
        gen[res] = gen.get(res,-1) + 1
        c = res + "[" + str(gen[res]) + "] = " + c
    return c + reduce(lambda c2,p: c2 + param(p) + ", ", params[:-1], "") + param(params[-1]) + ")"

def ref(s, refMap):
    return reduce(lambda s2,(t,r): s2.replace(t,r), refMap, s) 

def addCall(calls, refMap):
    s = call(calls)
    msg = s.replace('"','\\"')
    outf.write("  test(" + s + ', "' + msg  + '");\n')
    if opts["ref"]:
        outf.write("  ref(" + ref(s, refMap) + ', "' + msg  + '");\n')
