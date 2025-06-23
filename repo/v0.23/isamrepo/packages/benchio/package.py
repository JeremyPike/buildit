
from spack.package import * 
import os
import subprocess

class Benchio(Package):
    """BenchIO: A benchmark I/O tool (example description)"""

    phases = ['build', 'install']

    homepage = "https://github.com/davidhenty/benchio"
    git = "https://github.com/davidhenty/benchio.git"

    version("master", branch="master")

    depends_on('mpi')
    depends_on("hdf5+mpi+fortran")
    depends_on("netcdf-fortran")
    depends_on("adios2")

    @property
    def build_targets(self):

        targetlist = []
        targetlist.append("COMMS_ARCH=mpi")
        targetlist.append(f"FC={self.spec['mpi'].mpifc}")

        adios2_fortran_flags = subprocess.getoutput("adios2-config --fortran-flags")
        adios2_fortran_libs = subprocess.getoutput("adios2-config --fortran-libs")

        fflags = (
                "-O3 "
                "-mcpu=neoverse-v2 "
                f"{adios2_fortran_flags}"
                )

        lflags = (
                "-lnetcdff -lnetcdf -lhdf5_fortran -lhdf5 "
                f"{adios2_fortran_libs}"
                )

        targetlist.append(f"FFLAGS={fflags}")
        targetlist.append(f"LFLAGS={lflags}")

        return targetlist

    def build(self, spec, prefix):
        make('-f', 'Makefile-archer2', *self.build_targets)

    def install(self, spec, prefix):
        # No install needed, just copy the executable to prefix.bin
        mkdirp(prefix.bin)
        install('benchio', prefix.bin)
