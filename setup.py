from setuptools import setup, Extension
from distutils.command.build_ext import build_ext
from distutils.command.build_clib import build_clib
import os
from os.path import join as pjoin
from glob import glob
from distutils import log
from distutils.errors import DistutilsSetupError


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
os.chdir(CURR_DIR)

AFDKO = pjoin(CURR_DIR, 'afdko')
PUBLIC_LIB = pjoin(AFDKO, 'FDK', 'Tools', 'Programs', 'public', 'lib')
MAKEOTF_ROOT = pjoin(AFDKO, 'FDK', 'Tools', 'Programs', 'makeotf')
MAKEOTF_LIB = pjoin(MAKEOTF_ROOT, 'makeotf_lib')
MAKEOTF_SOURCE = pjoin(MAKEOTF_ROOT, 'source')

LIBRARIES = [
    ('ctutil', {
        'sources': [
            pjoin(PUBLIC_LIB, 'source', 'ctutil', 'ctutil.c'),
            ],
        'include_dirs': [
            pjoin(PUBLIC_LIB, 'api'),
            ],
        'macros': {
            'msvc': [
                ('CTL_CDECL', '__cdecl'),
                ('_CRT_SECURE_NO_DEPRECATE', '1'),
                ],
            },
        }),
    ('dynarr', {
        'sources': [
            pjoin(PUBLIC_LIB, 'source', 'dynarr', 'dynarr.c'),
            ],
        'include_dirs': [
            pjoin(PUBLIC_LIB, 'api'),
            ],
        'macros': {
            'msvc': [
                ('CTL_CDECL', '__cdecl'),
                ('_CRT_SECURE_NO_DEPRECATE', '1'),
                ],
            },
        }),
    ('hotconv', {
        'macros': {
            'any': [
                ('HOT_FEAT_SUPPORT', '1'),
                ],
            'msvc': [
                ('CDECL', '__cdecl'),
                ('_CRT_SECURE_NO_DEPRECATE', '1'),
                ],
            },
        'sources': [
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'anon.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'BASE.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'CFF_.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'cmap.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'featerr.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'featgram.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'featscan.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'fvar.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'GDEF.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'GPOS.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'GSUB.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'head.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'hhea.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'hmtx.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'hot.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'map.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'maxp.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'MMFX.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'MMSD.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'name.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'OS_2.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'otl.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'post.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'sfnt.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'vhea.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'vmtx.c'),
            pjoin(MAKEOTF_LIB, 'source', 'hotconv', 'VORG.c'),
            ],
        'include_dirs': [
            pjoin(MAKEOTF_LIB, 'api'),
            pjoin(MAKEOTF_LIB, 'resource'),
            pjoin(MAKEOTF_LIB, 'build', 'hotpccts', 'pccts', 'h'),
            pjoin(PUBLIC_LIB, 'api'),
            pjoin(PUBLIC_LIB, 'resource'),
            ],
        'extra_args': {
            # disable Microsoft language extensions incompatible with ANSI C
            'msvc': ['/Za'],
            }
        }),
    ('pstoken', {
        'macros': {
            'any': [
                ('CFF_DEBUG', '1'),
                ('CFF_T13_SUPPORT', '0'),
                ],
            'msvc': [
                ('CDECL', '__cdecl'),
                ('_CRT_SECURE_NO_DEPRECATE', '1'),
                ],
            },
        'sources': [
            pjoin(MAKEOTF_LIB, 'source', 'pstoken', 'pstoken.c'),
            ],
        'include_dirs': [
            pjoin(MAKEOTF_LIB, 'api'),
            pjoin(PUBLIC_LIB, 'api'),
            pjoin(PUBLIC_LIB, 'resource'),
            ],
        }),
    ('typecomp', {
        'macros': {
            'any': [
                ('TC_HINT_CHECK', '1'),
                ('TC_T13_SUPPORT', '0'),
                ('TC_EURO_SUPPORT', '1'),
                ('TC_SUBR_SUPPORT', '1'),
                ('TC_DEBUG', '1'),
                ],
            'msvc': [
                ('CDECL', '__cdecl'),
                ('_CRT_SECURE_NO_DEPRECATE', '1'),
                ],
            },
        'sources': [
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'charset.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'cs.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'dict.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'encoding.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'fdselect.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'parse.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'recode.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'sindex.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'subr.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 't13.c'),
            pjoin(MAKEOTF_LIB, 'source', 'typecomp', 'tc.c'),
            ],
        'include_dirs': [
            pjoin(MAKEOTF_LIB, 'api'),
            pjoin(MAKEOTF_LIB, 'resource'),
            pjoin(PUBLIC_LIB, 'api'),
            pjoin(PUBLIC_LIB, 'resource'),
            ],
        }),
    ('cffread', {
        'macros': {
            'any': [
                ('CFF_T13_SUPPORT', '0'),
                ],
            'msvc': [
                ('CDECL', '__cdecl'),
                ('_CRT_SECURE_NO_DEPRECATE', '1'),
                ],
            },
        'sources': [
            pjoin(MAKEOTF_LIB, 'source', 'cffread', 'cffread.c'),
            ],
        'include_dirs': [
            pjoin(MAKEOTF_LIB, 'api'),
            pjoin(MAKEOTF_LIB, 'resource'),
            pjoin(PUBLIC_LIB, 'api'),
            pjoin(PUBLIC_LIB, 'resource'),
            ],
        }),
    ]


class custom_build_clib(build_clib):
    """ Custom build_clib command which allows to pass compiler-specific
    'macros' and 'extra_args' when compiling C libraries.
    """

    def build_libraries(self, libraries):
        for (lib_name, build_info) in libraries:
            sources = build_info.get('sources')
            if sources is None or not isinstance(sources, (list, tuple)):
                raise DistutilsSetupError(
                       "in 'libraries' option (library '%s'), "
                       "'sources' must be present and must be "
                       "a list of source filenames" % lib_name)
            sources = list(sources)

            log.info("building '%s' library", lib_name)

            compiler_type = self.compiler.compiler_type
            # get list of preprocessor definitions from 'macros' dict
            macros_dict = build_info.get('macros', {})
            macros = macros_dict.get('any', [])
            macros.extend(macros_dict.get(compiler_type, []))

            include_dirs = build_info.get('include_dirs')
            # get list of compiler extra arguments from 'extra_args' dict
            extra_args_dict = build_info.get('extra_args', {})
            extra_args = extra_args_dict.get('any', [])
            extra_args.extend(extra_args_dict.get(compiler_type, []))
            # compile the source code to object files
            objects = self.compiler.compile(sources,
                                            output_dir=self.build_temp,
                                            macros=macros,
                                            include_dirs=include_dirs,
                                            extra_postargs=extra_args,
                                            debug=self.debug)

            # Now "link" the object files together into a static library.
            # (On Unix at least, this isn't really linking -- it just
            # builds an archive.  Whatever.)
            self.compiler.create_static_lib(objects, lib_name,
                                            output_dir=self.build_clib,
                                            debug=self.debug)


class custom_build_ext(build_ext):

    def get_source_files(self):
        filenames = build_ext.get_source_files(self)
        for ext in self.extensions:
            filenames.extend(ext.depends)
        return filenames


makeotflib = Extension(
    "makeotflib._makeotflib",
    sources=[
        "_makeotflib.c",
        pjoin(MAKEOTF_SOURCE, "cb.c"),
        pjoin(MAKEOTF_SOURCE, "cbpriv.c"),
        pjoin(MAKEOTF_SOURCE, "fcdb.c"),
        pjoin(MAKEOTF_SOURCE, "file.c"),
        pjoin(MAKEOTF_SOURCE, "main.c"),
    ] + ([
        pjoin(MAKEOTF_SOURCE, "Win32", "Win.c"),
    ] if os.name == "nt" else [
        pjoin(MAKEOTF_SOURCE, "mac", "mac.c"),
    ]),
    define_macros=[("MAKEOTFLIB_EXPORTS", "1")],
    depends=(
        [pjoin(MAKEOTF_SOURCE, "makeotflib.h")] +
        glob(pjoin(MAKEOTF_SOURCE, "include_files", "*.h")) +
        glob(pjoin(MAKEOTF_LIB, "api", "*.h")) +
        glob(pjoin(MAKEOTF_LIB, "resource", "*.h")) +
        glob(pjoin(PUBLIC_LIB, "api", "*.h")) +
        glob(pjoin(MAKEOTF_LIB, 'source', 'hotconv', "*.[hc]")) +
        glob(pjoin(MAKEOTF_LIB, 'build', 'hotpccts', 'pccts', 'h', "*.h")) +
        glob(pjoin(PUBLIC_LIB, "resource", "*.h")) +
        glob(pjoin(MAKEOTF_LIB, 'source', 'typecomp', "*.[hc]")) +
        glob(pjoin(MAKEOTF_LIB, 'source', 'typecomp', "*.cs")) +
        glob(pjoin(MAKEOTF_LIB, 'source', 'cffread', "*.c"))
        ),
    include_dirs=[
        pjoin(MAKEOTF_SOURCE, "include_files"),
        pjoin(MAKEOTF_LIB, "api"),
        pjoin(MAKEOTF_LIB, "resource"),
        pjoin(PUBLIC_LIB, "api"),
    ],
    language="c",
    )


if __name__ == "__main__":
    setup(
        name='makeotflib',
        version="0.1",
        url="https://www.daltonmaag.com/",
        description="Python bindings for makeotf",
        author="Cosimo Lupo",
        author_email="cosimo.lupo@daltonmaag.com",
        license="Apache 2.0",
        packages=['makeotflib'],
        ext_modules=[makeotflib],
        cmdclass={
            'build_ext': custom_build_ext,
            'build_clib': custom_build_clib,
            },
        entry_points={
            'console_scripts': [
                'pymakeotf=makeotflib:main'
                ],
            },
        libraries=LIBRARIES,
    )
