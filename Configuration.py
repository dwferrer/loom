#!/usr/bin/python
#Configure and store the compiler and libraries to use
import sys
import os
import ConfigParser

import scipy.weave

loompath = os.path.dirname(__file__)
cfgfilename = loompath + "/config.ini"

Compiler = ''
Headers = []
IncludePaths = []
Libraries = []
LibraryPaths = []
Defines = []
CompileArgs = []

def autoconfigure():
    global Compiler
    global Headers
    global IncludePaths
    global Libraries
    global LibraryPaths
    global Defines
    global CompileArgs

    print("Autoconfiguring loom:")
    if testIntel():
        print("\tChose Intel Compiler with TBB")
        Compiler = 'intelem'
        Headers = ["<algorithm>","\"tbb/parallel_sort.h\"","<omp.h>"]
        Libraries = ["tbb","iomp5"]
        Defines = [("HAS_TBB",None)]
        CompileArgs = ["-openmp"]
    else:
        print("\tFalling back to g++. NOTE: This uses the slower, singlethreaded std::sort")
        Compiler = 'g++'
        Headers = ["<algorithm>","<omp.h>"]
        libraries = ["gomp"]
        CompileArgs = ["-fopenmp"]
    return


def testIntel():
    print("\tChecking for scipy.weave intel support")
    testcode = "printf(\"\\ticc Compilation Success\\n\");"
    try:
        scipy.weave.inline(testcode,[],
                compiler="intelem",
                headers=["\"tbb/parallel_sort.h\"","<omp.h>"],
                libraries=["tbb","iomp5"],
                verbose=2)
        return 1
    except Exception as e:
        print("\t icc Compilation Failed")
        print(e.args)
        return 0



def save():
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    config.add_section("Compilation")
    config.set("Compilation","Compiler",Compiler)
    config.set("Compilation","Headers",toTSV(Headers))
    config.set("Compilation","IncludePaths",toTSV(IncludePaths))
    config.set("Compilation","Libraries",toTSV(Libraries))
    config.set("Compilation","LibraryPaths",toTSV(LibraryPaths))
    config.set("Compilation","Defines",defToTSV(Defines))
    config.set("Compilation","CompileArgs",toTSV(CompileArgs))
    with open(cfgfilename,"wb") as configfile:
        config.write(configfile)



def read():
    global Compiler
    global Headers
    global IncludePaths
    global Libraries
    global LibraryPaths
    global Defines
    global CompileArgs

    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    config.read(cfgfilename)
    Compiler = config.get("Compilation","Compiler")
    Headers = config.get("Compilation","Headers").split()
    IncludePaths = config.get("Compilation","IncludePaths").split()
    Libraries = config.get("Compilation","Libraries").split()
    LibraryPaths = config.get("Compilation","LibraryPaths").split()
    Defines = [(d,None) for d in config.get("Compilation","Defines").split()]
    CompileArgs = config.get("Compilation","CompileArgs").split()

    if(__name__=="__main__"):
        print (config.items("Compilation"))
        print Compiler
        print Headers
        print IncludePaths
        print Libraries
        print LibraryPaths
        print Defines
    return


def toTSV(l):
    s = ""
    for i in l:
        s+= i + "\t"
    return s

def defToTSV(l):
    s = ""
    for i in l:
        s+= i[0] + "\t"
    return s


if not os.path.exists(cfgfilename):
    autoconfigure()
    save()
else:
    read()


def weave(code,args,local_dict,support_code=None,add_head=[],add_lib=[]):
    scipy.weave.inline(code,args,
            local_dict=local_dict,
            compiler=Compiler,
            headers=Headers+add_head,
            include_dirs=IncludePaths,
            libraries=Libraries+add_lib,
            library_dirs=LibraryPaths,
            support_code=support_code,
            extra_compile_args=CompileArgs,
            verbose=2)


