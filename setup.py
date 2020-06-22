from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools

from pathlib import Path

from os import listdir
from os.path import isfile, join, abspath, dirname

__version__ = '0.1.2'


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


extensions = [
    Extension(
        'pyclothoids._clothoids_cpp',
        [join('pyclothoids' , *i) for i in (('src','main.cpp'),('src','Submodules','Clothoids','src','Fresnel.cc'),('src','Submodules','Clothoids','src','Clothoid.cc'),
        ('src','Submodules','Clothoids','src','G2lib.cc'),('src','Submodules','Clothoids','src','AABBtree.cc'),('src','Submodules','Clothoids','src','Biarc.cc'),('src','Submodules','Clothoids','src','BiarcList.cc'),
        ('src','Submodules','Clothoids','src','Circle.cc'),
        ('src','Submodules','Clothoids','src','ClothoidDistance.cc'),('src','Submodules','Clothoids','src','ClothoidG2.cc'),('src','Submodules','Clothoids','src','ClothoidList.cc'),
        ('src','Submodules','Clothoids','src','G2lib_intersect.cc'),('src','Submodules','Clothoids','src','Line.cc'),('src','Submodules','Clothoids','src','PolyLine.cc'),
        ('src','Submodules','Clothoids','src','Triangle2D.cc'),
        ('src','Submodules','Clothoids','submodules','quarticRootsFlocke','src','PolynomialRoots-1-Quadratic.cc'),('src','Submodules','Clothoids','submodules','quarticRootsFlocke','src','PolynomialRoots-2-Cubic.cc'),
        ('src','Submodules','Clothoids','submodules','quarticRootsFlocke','src','PolynomialRoots-3-Quartic.cc'),('src','Submodules','Clothoids','submodules','quarticRootsFlocke','src','PolynomialRoots-Jenkins-Traub.cc'),
        ('src','Submodules','Clothoids','submodules','quarticRootsFlocke','src','PolynomialRoots-Utils.cc'))],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            join('pyclothoids','src','Submodules','Clothoids','src'),
            join('pyclothoids','src','Submodules','Clothoids','submodules','quarticRootsFlocke','src')
        ],
        language='c++'
    ),
]


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.

    The newer version is prefered over c++11 (when it is available).
    """
    flags = ['-std=c++11'] #'-std=c++17', '-std=c++14', 

    for flag in flags:
        if has_flag(compiler, flag): return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)
        
# read the contents of your README file
this_directory = abspath(dirname(__file__))
with open(join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyclothoids',
    version=__version__,
    author='Phillip Dix',
    author_email='phildix11@gmail.com',
    url='https://github.com/phillipd94/PyClothoids',
    description='A library for clothoid curves in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages = ['pyclothoids'],
    ext_modules=extensions,
    install_requires=['pybind11>=2.4','numpy'],
    setup_requires=['pybind11>=2.4'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
