#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################
#
#   OfusPy 1.0
#   Pacheco, Matias W. <mwpacheco@outlook.es>
#   Copyright (c) 2020 Wehaa Portal Soft.
#   License MIT
#
#################################################

from __future__ import unicode_literals
from __future__ import print_function

import sys, os, zlib, base64

_header = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
##################################################################
#
#   OfusPy 1.0
#   Pacheco, Matias W. <mwpacheco@outlook.es>
#   Copyright (c) 2020 Wehaa Portal Soft.
#   License MIT
#
# Created by: Compress PY code generator
#
# WARNING! All changes made in this file will be lost!
#
##################################################################
import zlib, base64
exec(zlib.decompress(base64.b64decode('%s')))
'''

def compilePyFiles():
    def compilePyDir(dir, recurse=False, map=None, **compilePy_args):
        def compile_py(pi_dir, pi_file):
            if pi_file.endswith('.py'):
                py_dir = pi_dir
                py_file = pi_file[:-3] + '.py'

                if map is not None:
                    py_dir, py_file = list(map(py_dir, py_file))

                try:
                    os.makedirs(py_dir)
                except:
                    pass
                
                pi_path = os.path.join(pi_dir, pi_file)
                py_path = os.path.join(py_dir, py_file)

                pi_file = open(pi_path, 'rb')
                py_file = open(py_path, 'w')

                try:
                    compilePi(pi_file, py_file, **compilePy_args)
                finally:
                    pi_file.close()
                    py_file.close()
        if recurse:
            for root, _, files in os.walk(dir):
                for pi in files:
                    compile_py(root, pi)
        else:
            for pi in os.listdir(dir):
                if os.path.isfile(os.path.join(dir, pi)):
                    compile_py(dir, pi)
        
    def pyName(py_dir, py_file):
        return py_dir, "c_{0}".format(py_file)

    compilePyDir(".", True, pyName)

def compilePi(pifile, pyfile, execute=False):
    try:
        pifname = pifile.name
    except AttributeError:
        pifname = pifile

    original_data = pifile.read()    
    compressed_data = zlib.compress(original_data, zlib.Z_BEST_COMPRESSION)
    gzipped_data = base64.b64encode(compressed_data).decode()

    pyfile.write(_header % (gzipped_data))

def main(argv):
    print("Compiling .py files...")
    compilePyFiles()

if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit:
        raise
