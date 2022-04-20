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

```bash
python3 run.py dbname javaSourceDir
```
