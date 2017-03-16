import sys
from distutils.core import Extension, setup
from Cython.Distutils import build_ext

include_dirs = []
lib_suffix = ""
if 'win' in sys.platform:
    import os
    import numpy
    include_dirs = [numpy.get_include()]

    lib_suffix = "_vs2010"

    # def is_python64_windows():
    #     return "PROGRAMFILES(X86)" in os.environ

    # # Note: I had issues builidng 64bit version of bullet dlls.
    # if is_python64_windows():
    #     lib_suffix += "_x64"
    lib_suffix += "_x64"

    lib_suffix += "_debug"
    # lib_suffix += "_release"
    libraries = []
else:
    import os
    import numpy

    libraries=[
        "BulletSoftBody" + lib_suffix,
        "BulletDynamics" + lib_suffix,
        "BulletCollision" + lib_suffix,
        "LinearMath" + lib_suffix,
    ]

base_bullet_src_dir = "/Users/micro/src_external/bullet3-2.83.7/src"
source_dir_names = ["LinearMath", "BulletCollision", "BulletDynamics",
                    "BulletSoftBody"]
source_files = []
for source_dir_name in source_dir_names:
    src_path = base_bullet_src_dir + "/" + source_dir_name
    for root, dirs, files in os.walk(src_path):
        for filename in files:
            if filename.endswith(".cpp"):
                source_files.append(root + "/" + filename)

print("sources:", source_files)

setup(
    name="bullet",
    packages=["bullet"],
    ext_modules=[Extension(
        "bullet.bullet",
        ["bullet/bullet.pyx"] + source_files,
        libraries=libraries,
        # libraries=[
        #         "BulletSoftBody" + lib_suffix,
        #         "BulletDynamics" + lib_suffix,
        #         "BulletCollision" + lib_suffix,
        #         "LinearMath" + lib_suffix,
        #         ],
        include_dirs=include_dirs,
        language="c++")],
    cmdclass={'build_ext': build_ext},
    )
