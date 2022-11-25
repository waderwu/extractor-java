#!/usr/bin/env python3
import os
import sys
import subprocess
import glob
import argparse
import platform

class Extract:
    def __init__(self, db, srcroot, lib, libdir):
        self.dbname = db
        self.srcroot = srcroot
        if lib:
            self.libs = lib
        else:
            self.libs = []
        if libdir:
            for _dir in libdir:
                for lib in glob.glob(f"{_dir}/**/*.jar", recursive=True):
                    self.libs.append(lib)

    def init_database(self):
        p = subprocess.run(["codeql", "database", "init", self.dbname, "-l", "java", "--source-root", self.srcroot])
        if p.returncode == 0:
            self.dbpath = os.path.realpath(self.dbname)
            print(f"[*extract_log*] dbpath : {self.dbpath}")
        else:
            sys.exit(1)

    def init_env(self):
        codeql_path = subprocess.check_output(["which", "codeql"]).decode()
        codeql_home = os.path.dirname(codeql_path)
        self.codeql_home = codeql_home
        print(f"[*extract_log*] codeql_home : {codeql_home}")
        s = platform.system().lower()
        MAPPING = {'darwin': 'osx',
                   'windows': 'win',
                   'linux': 'linux'
                   }
        if s in MAPPING:
            s = MAPPING.get(s)
        # print(f"{codeql_home}/tools/{s}*/java")
        codeql_java_home = glob.glob(f"{codeql_home}/tools/{s}*/java")[0]
        self.codeql_java_home = codeql_java_home
        print(f"[*extract_log*] codeql_java_home : {codeql_java_home}")
        env = {
            "CODEQL_DIST": codeql_home,
            "CODEQL_EXTRACTOR_JAVA_LOG_DIR": f"{self.dbpath}/log",
            "CODEQL_EXTRACTOR_JAVA_ROOT": f"{codeql_home}/java",
            "CODEQL_EXTRACTOR_JAVA_SOURCE_ARCHIVE_DIR": f"{self.dbpath}/src",
            "CODEQL_EXTRACTOR_JAVA_TRAP_DIR": f"{self.dbpath}/trap/java",
            "CODEQL_EXTRACTOR_JAVA_WIP_DATABASE": self.dbpath,
            "CODEQL_JAVA_HOME": codeql_java_home
        }
        for key in env:
            print(f"{key}={env[key]}")
        return env

    def generate_javacargs(self):
        javafiles = glob.glob(f"{self.srcroot}/**/*.java", recursive=True)
        print(len(javafiles))
        with open(f"{self.dbpath}/log/javac.args", "w") as f:
            f.write("-Xprefer:source" + "\n")
            if len(self.libs) > 0:
                f.write("-classpath\n")
                libstr = ""
                for lib in self.libs:
                    libstr = libstr + lib + ":"
                f.write(libstr + "\n")

            for javafile in javafiles:
                # if "test" not in javafile:
                f.write(javafile + "\n")

    def generate_trap(self):
        env = self.init_env()
        p = subprocess.run([f"{self.codeql_java_home}/bin/java", "-Xmx1024M", "-Xms256M", "-cp",
                            f"{self.codeql_home}/java/tools/semmle-extractor-java.jar",
                            "com.semmle.extractor.java.JavaExtractor", "--javac-args",
                            f"@@@{self.dbpath}/log/javac.args"], env=env)

    def import_trap(self):
        p = subprocess.run(["codeql", "dataset", "import", f"{self.dbpath}/db-java", f"{self.dbpath}/trap", "-S",
                            f"{self.codeql_home}/java/semmlecode.dbscheme"])

    def finalize(self):
        p = subprocess.run(["codeql", "database", "finalize", self.dbpath])

    def run(self):
        self.init_database()
        self.generate_javacargs()
        self.generate_trap()
        # self.import_trap()
        self.finalize()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CodeQL java extractor.')
    parser.add_argument('db', help='codeql database name')
    parser.add_argument('srcroot', help='java source code dir')
    parser.add_argument('-l', '--lib', nargs='*', help='lib path')
    parser.add_argument('-ld', '--libdir', nargs='*', help='lib dir')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    print(args)
    print(args.db)
    print(args.srcroot)
    print(args.lib)
    print(args.libdir)
    extractor = Extract(args.db, args.srcroot, args.lib, args.libdir)
    extractor.run()
