# Extractor-java

Create CodeQL database directly from Java source code without compiling

## Require

1. Installed CodeQL
2. Linux / Macos

Otherwise you need to manually specify the value of variables such as codeql_home，codeql_java_home

## Usage

If there is only jar, you need to decompile it to get the java source code

```bash
unzip your.jar
python3 class2java.py dir
```

generate database for java source code

```text
usage: run.py [-h] [-l [LIB ...]] [-ld [LIBDIR ...]] db srcroot

CodeQL java extractor.

positional arguments:
  db                    codeql database name
  srcroot               java source code dir

optional arguments:
  -h, --help            show this help message and exit
  -l [LIB ...], --lib [LIB ...]
                        lib path
  -ld [LIBDIR ...], --libdir [LIBDIR ...]
                        lib dir
```

example

```bash
python3 run.py dbname srcroot
python3 run.py dbname srcroot -l lib1.jar lib2.jar
python3 run.py dbname srcroot -ld libdir1 libdir2
```