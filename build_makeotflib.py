import cffi
import os


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(CURR_DIR, "_makeotflib.c"), 'r') as f:
    source = f.read()

AFDKO = os.path.join(CURR_DIR, 'afdko')

PUBLIC_LIB = os.path.join(AFDKO, 'FDK', 'Tools', 'Programs', 'public', 'lib')

MAKEOTF_ROOT = os.path.join(AFDKO, 'FDK', 'Tools', 'Programs', 'makeotf')
MAKEOTF_LIB = os.path.join(MAKEOTF_ROOT, 'makeotf_lib')
MAKEOTF_SOURCE = os.path.join(MAKEOTF_ROOT, 'source')

ffi = cffi.FFI()

ffi.cdef("""
int run(void);
""")

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
        os.path.join(MAKEOTF_SOURCE, "main.c"),
    ],
    include_dirs=[
        os.path.join(MAKEOTF_SOURCE, "include_files"),
        os.path.join(MAKEOTF_LIB, "api"),
        os.path.join(MAKEOTF_LIB, "resource"),
        os.path.join(PUBLIC_LIB, "api"),
    ],
    extra_objects=[
        os.path.join(CURR_DIR, 'lib', "ctutil.a"),
        os.path.join(CURR_DIR, 'lib', "dynarr.a"),
        os.path.join(CURR_DIR, 'lib', "hotconv.a"),
        os.path.join(CURR_DIR, 'lib', "pstoken.a"),
        os.path.join(CURR_DIR, 'lib', "typecomp.a"),
        os.path.join(CURR_DIR, 'lib', "cffread.a"),
    ],
)


if __name__ == '__main__':
    ffi.compile()
