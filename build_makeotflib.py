import cffi
import os
import sys
import sysconfig
import shutil

CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

sys.path.insert(0, CURR_DIR)
from setup import (
    custom_build_clib, LIBRARIES, PUBLIC_LIB, MAKEOTF_LIB, MAKEOTF_SOURCE)


ffi = cffi.FFI()

ffi.cdef("""
int main(int argc, char *argv[]);
""")

with open(os.path.join(MAKEOTF_SOURCE, "main.c"), 'r') as f:
    source = f.read()

ffi.set_source(
    'makeotflib._makeotflib_cffi',
    source,
    source_extension='.c',
    define_macros=[("MAKEOTFLIB_EXPORTS", "1")],
    sources=[
        os.path.join(MAKEOTF_SOURCE, "cb.c"),
        os.path.join(MAKEOTF_SOURCE, "cbpriv.c"),
        os.path.join(MAKEOTF_SOURCE, "fcdb.c"),
        os.path.join(MAKEOTF_SOURCE, "file.c"),
    ] + ([
        os.path.join(MAKEOTF_SOURCE, "Win32", "Win.c"),
    ] if os.name == "nt" else [
        os.path.join(MAKEOTF_SOURCE, "mac", "mac.c"),
    ]),
    include_dirs=[
        os.path.join(MAKEOTF_SOURCE, "include_files"),
        os.path.join(MAKEOTF_LIB, "api"),
        os.path.join(MAKEOTF_LIB, "resource"),
        os.path.join(PUBLIC_LIB, "api"),
    ],
)


def get_platform_build_dir(subdir_prefix='temp', base_dir=""):
    return os.path.join(
        base_dir, "build",
        "{prefix}.{platform}-{version[0]}.{version[1]}".format(
            prefix=subdir_prefix,
            platform=sysconfig.get_platform(),
            version=sys.version_info))


def build_c_libraries(tmpdir, libraries):
    from distutils.core import Distribution
    import distutils.errors
    from cffi.ffiplatform import VerificationError
    from distutils.ccompiler import new_compiler

    dist = Distribution()
    dist.parse_config_files()

    dist.cmdclass['build_clib'] = custom_build_clib

    cmd_obj = dist.get_command_obj('build_clib')
    compiler = new_compiler(cmd_obj.compiler)
    libraries = [(name, info) for name, info in libraries
                 if not os.path.exists(
                     compiler.library_filename(name, output_dir=tmpdir))]
    if not libraries:
        return

    dist.libraries = libraries

    options = dist.get_option_dict('build_clib')
    options['force'] = ('ffiplatform', True)
    options['build_clib'] = ('ffiplatform', tmpdir)
    options['build_temp'] = ('ffiplatform', tmpdir)

    try:
        dist.run_command('build_clib')
    except (distutils.errors.CompileError,
            distutils.errors.LinkError) as e:
        raise VerificationError('%s: %s' % (e.__class__.__name__, e))


if __name__ == '__main__':
    from distutils.dir_util import mkpath

    build_temp = get_platform_build_dir('temp', base_dir=CURR_DIR)
    mkpath(build_temp)

    # compile C libraries if missing from build temp
    build_c_libraries(build_temp, LIBRARIES)

    # add libraries to cffi module's build info
    module_name, source, source_extension, kwds = ffi._assigned_source
    del ffi._assigned_source
    kwds['libraries'] = [lib_name for lib_name, build_info in LIBRARIES]
    kwds['library_dirs'] = [build_temp]
    ffi.set_source(module_name, source, source_extension, **kwds)

    # compile cffi module
    ext_path = ffi.compile(build_temp)

    # copy compiled module to build_lib's package dir
    build_lib = get_platform_build_dir('lib', base_dir=CURR_DIR)
    package_lib = os.path.join(build_lib, 'makeotflib')
    mkpath(package_lib)
    dest = os.path.join(package_lib, os.path.basename(ext_path))
    if os.path.exists(dest):
        os.remove(dest)
    shutil.copy(ext_path, dest)
