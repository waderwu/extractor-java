#!/usr/bin/env python3

import os
import sys

def decompiler(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    cmd = f"cd {path};java -cp {curdir}/java-decompiler.jar org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -hdc=0 -dgs=1 -rsy=1 -rbr=1 -lit=1 -nls=1 -mpm=60 . ."
    # print(cmd)
    os.system(cmd)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[Usage:] python3 class2java.py directory")
    else:
        decompiler(sys.argv[1])