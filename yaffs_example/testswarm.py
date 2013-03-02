import random
import sys
import subprocess
import types

gen = {}
live = {}

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

def swarm(calls):
    config = {}
    for c in calls:
        (P, res, params) = calls[c]
        if (not opts["swarm"]) or (random.random() < P):
            config[c] = (res, params)
    return config

def param(p):
    if type(p) == types.StringType:
        destructive = p[0] == "!"
        if destructive:
            p = p[1:]
        if random.random() < 0.05:
            pv = random.randint(0,gen[p])
        else:
            pv = random.choice(live[p])
        if destructive:
            try:
                live[p].remove(pv)
            except ValueError:
                pass
        return p + "[" + str(pv) + "]"
        
    else:
        return p()
    
def call(calls):
    f = random.choice(calls.keys())
    c = f + "("
    (res, params) = calls[f]
    if res != ():
        gen[res] = gen.get(res,-1) + 1
        c = res + "[" + str(gen[res]) + "] = " + c
        if res not in live:
            live[res] = []
        live[res].append(gen[res])
    return c + reduce(lambda c2,p: c2 + param(p) + ", ", params[:-1], "") + param(params[-1]) + ")"

def ref(s, refMap):
    return reduce(lambda s2,(t,r): s2.replace(t,r), refMap, s) 

def addCall(calls, refMap):
    s = call(calls)
    msg = s.replace('"','\\"')
    sRef = ref(s, refMap)
    msgRef = sRef.replace('"','\\"')
    outf.write("  test(" + s + ', "' + msg  + '");\n')
    if opts["ref"]:
        outf.write("  ref(" + sRef + ', "' + msgRef  + '");\n')
