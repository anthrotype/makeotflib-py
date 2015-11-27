import cffi
import os
import sys
import sysconfig
import shutil
import errno


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

AFDKO = os.path.join(CURR_DIR, 'afdko')

PUBLIC_LIB = os.path.join(AFDKO, 'FDK', 'Tools', 'Programs', 'public', 'lib')

MAKEOTF_ROOT = os.path.join(AFDKO, 'FDK', 'Tools', 'Programs', 'makeotf')
MAKEOTF_LIB = os.path.join(MAKEOTF_ROOT, 'makeotf_lib')
MAKEOTF_SOURCE = os.path.join(MAKEOTF_ROOT, 'source')

BUILD_TEMP = os.path.join(
    CURR_DIR, "build", "temp.{platform}-{version[0]}.{version[1]}".format(
        platform=sysconfig.get_platform(),
        version=sys.version_info))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


ffi = cffi.FFI()

ffi.cdef("""
int main(int argc, char *argv[]);
""")

with open(os.path.join(MAKEOTF_SOURCE, "main.c"), 'r') as f:
    source = f.read()

ffi.set_source(
    '_makeotflib_cffi',
    source,
    source_extension='.c',
    define_macros=[("MAKEOTFLIB_EXPORTS", "1")],
    sources=[
        os.path.join(MAKEOTF_SOURCE, "cb.c"),
        os.path.join(MAKEOTF_SOURCE, "cbpriv.c"),
        os.path.join(MAKEOTF_SOURCE, "fcdb.c"),
        os.path.join(MAKEOTF_SOURCE, "file.c"),
        os.path.join(MAKEOTF_SOURCE, "mac", "mac.c"),
    ],
    include_dirs=[
        os.path.join(MAKEOTF_SOURCE, "include_files"),
        os.path.join(MAKEOTF_LIB, "api"),
        os.path.join(MAKEOTF_LIB, "resource"),
        os.path.join(PUBLIC_LIB, "api"),
    ],
    extra_objects=[
        os.path.join(BUILD_TEMP, "libctutil.a"),
        os.path.join(BUILD_TEMP, "libdynarr.a"),
        os.path.join(BUILD_TEMP, "libhotconv.a"),
        os.path.join(BUILD_TEMP, "libpstoken.a"),
        os.path.join(BUILD_TEMP, "libtypecomp.a"),
        os.path.join(BUILD_TEMP, "libcffread.a"),
    ],
)


if __name__ == '__main__':
    # compile extension module to build/temp-* folder
    mkdir_p(BUILD_TEMP)
    ext_path = ffi.compile(BUILD_TEMP)

    # copy compiled module inside package dir
    dest = os.path.join(CURR_DIR, 'makeotflib', os.path.basename(ext_path))
    if os.path.exists(dest):
        os.remove(dest)
    shutil.copy(ext_path, dest)
