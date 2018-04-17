#!/usr/bin/env python2

#
# (c) 2018 Max Prokhorov, Lazar Obradovic
#
# Install PlatformIO and necessary frameworks, platforms and libs.


from subprocess import call
from ConfigParser import ConfigParser

import os
import re
import sys
import tempfile
import functools


def get_pio_libraries(platformio_ini="/usr/src/platformio.ini"):
    with open(platformio_ini, "r") as f:
        parser = ConfigParser()
        parser.readfp(f)

    libs = parser.get("common", "lib_deps").split('\n')[1:]

    return libs



def pio_prepare(cwd, libraries, platforms=("espressif8266@1.5.0", "espressif8266@1.6.0")):
    run_ok = lambda cmd: call(cmd, cwd=cwd) == 0
    run_fail = lambda cmd: not run_ok(cmd)

    commands = []
    for platform in platforms:
        commands.append([run_ok, ["platformio", "platform", "install", "--with-package", "framework-arduinoespressif8266", platform]])

    _install_tools_dir = tempfile.mkdtemp()
    _install_lib_dir   = os.environ["PLATFORMIO_LIBDEPS_DIR"]
    os.mkdir(_install_lib_dir)

    commands.extend([
        [run_ok, ["platformio", "init", "-d", _install_tools_dir, "-b", "esp01_1m", "-s" ]],
        [run_ok, ["cp", "/empty.ino", _install_tools_dir + "/src" ]],
        [run_ok, ["platformio", "run", "-s", "-d", _install_tools_dir ]],
    ])

    # explicitly install required libraries
    commands.extend([
        [run_ok, ["platformio", "lib", "-d", _install_lib_dir, "install"] + libraries]
    ])

    for runner, cmd in commands:
        print ('+-- INFO: Running ' + " ".join(map(str, cmd)))
        sys.stdout.flush()
        if not runner(cmd):
            return False

    return True


if __name__ == "__main__":

    root, name = os.path.split(os.path.abspath(__file__))

    base = os.path.join(root, "/usr/src")
    libs = get_pio_libraries()

    print('INFO: Preparing dependencies ...')
    if not pio_prepare(cwd=base, libraries=libs):
        sys.exit(1)

    print('INFO: Prepared dependencies')
