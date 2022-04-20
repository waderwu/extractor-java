# Extractor-java

Create CodeQL database directly from Java source code without compiling

## Usage

If there is only Jar package, you need to decompile to get the java source code

```bash
unzip your.jar
python3 class2java.py dir
```

generate database for java source code

```bash
python3 run.py dbname javaSourceDir
```
