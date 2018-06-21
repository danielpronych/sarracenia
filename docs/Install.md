MetPX-Sarracenia Installation
=============================

Revision Record
---------------

version

:   @Version@

date

:   @Date@

Client Installation
-------------------

The package is built for python version 3.4 or higher. On systems where
they are available, debian packages are recommended. These can be
obtained from the launchpad repository. If you cannot use debian
packages, then consider pip packages avialable from PyPI. In both cases,
the other python packages (or dependencies) needed will be installed by
the package manager automatically.

### Ubuntu/Debian (apt/dpkg)

On Ubuntu 14.04/16.04/17.10/18.04 and derivatives of same:

    sudo add-apt-repository ppa:ssc-hpc-chp-spc/metpx
    sudo apt-get update
    sudo apt-get install python3-metpx-sarracenia  # only supports HTTP/HTTPS
    sudo apt-get install python3-paramiko   # adds SFTP support.
    sudo apt-get install sarrac # optional C client.

Currently, only the debian packages include man pages. The guides are
only available in the source repository.

### Redhat/Suse distros (rpm based)

On fedora 28:

    sudo dnf install python3-amqplib
    sudo dnf install python3-appdirs
    sudo dnf install python3-watchdog
    sudo dnf install python3-netifaces
    sudo dnf install python3-humanize
    sudo dnf install python3-psutil
    sudo dnf install python3-paramiko   # adds SFTP support.

    python3 setup.py bdist_rpm
    sudo rpm -i dist/*.noarch.rpm

The RPM´s built do not include dependency information, so these must be
manually installed with dnf. This procedured installs only the python
application (not the C one.) no man pages or other documentation are
installed.

### PIP

On windows, or other linux distributions where system packages are not
available, the above procedures are not applicable. There are also
special cases, such as if using python in virtual env, where it is more
practical to install the package using pip (python install package) from
<http://pypi.python.org/>. It is straightforward to do that:

    sudo pip install metpx-sarracenia

and to upgrade after the initial installation:

    sudo pip uninstall metpx-sarracenia
    sudo pip install metpx-sarracenia

NOTE:

    On many systems where both pythons 2 and 3 are installed, you may need to specify
    pip3 rather than pip.

### Windows

Any native python installation will do, but the dependencies in the
standard python.org installation require the installation of a
C-Compiler as well, so it gets a bit complicated. If you have an
existing python installation that works with c-modules within it, then
the complete package should install with all features.

If you do not have a python environment handy, then the easiest one to
get going with is winpython, which includes many scientifically relevant
modules, and will easily install all dependencies for Sarracenia. You
can obtain winpython from <http://winpython.github.io/> (note: select
python version \>3 ) Then one can install with pip (as above.)

### Packages

Debian packages and python wheels can be downloaded directly from:
[launchpad](https://launchpad.net/~ssc-hpc-chp-spc/+archive/ubuntu/metpx/+packages)

Source
------

Source code for each module is available <https://github.com/MetPX>:

    git clone https://github.com/MetPX/sarracenia sarracenia
    cd sarracenia

Development happens on the master branch. One probably wants real
release, so run git tag, and checkout the last one (the latest stable
release):

    blacklab% git tag

    .
    .
    .
    v2.18.04b2
    v2.18.04b3
    v2.18.04b4
    v2.18.04b5
    v2.18.05b1
    v2.18.05b2
    v2.18.05b3
    v2.18.05b4

    blacklab% git checkout v2.18.05b4
    blacklab% python3 setup.py bdist_wheel
    blacklab%  pip3 install dist/metpx_sarracenia-2.18.5b4-py3-none-any.whl

Sarrac
------

The C client is available in prebuilt binaries in the launchpad
repositories alongside the python packages:

    sudo add-apt-repository ppa:ssc-hpc-chp-spc/metpx
    sudo apt-get update
    sudo apt-get install sarrac 

For any recent ubuntu version. The librabbitmq-0.8.0 has been backported
in the PPA. sarrac's dependency. For other architectures or
distributions, one can build from source:

    git clone https://github.com/MetPX/sarrac 

on any linux system, as long as librabbitmq dependency is satisfied.
Note that the package does not build or run on non-linux systems.

Building on Old Systems
-----------------------

Sarracenia requires python3, and python themselves do not support
python3 older than 3.4. Some older Linux distributions either have no
python3 or have such an old version that it is difficult to install the
necessary dependencies.

On Ubuntu 12.04:

    apt-get install python3-dev
    apt-get install python3-setuptools
    easy_install3 pip==1.5.6
    pip3 install paramiko==1.16.0
    pip3 install metpx_sarracenia==<latest version>

Note

**Why the specific versions on older distributions?**

pip \> 1.5.6 does not support python \< 3.2 which is the python in
Ubuntu 12.04.

Later versions of paramiko require the cryptography module, which
doesn't build on python-3.2, so need to use an older version of paramiko
which uses pyCrypto, and that does build on 3.2.

Sarracenia still works python 3.2, but there might be some cosmetic
functionality missing. When having trouble installing sarracenia, one
should try building the C client (sarrac) as it has fewer dependencies
and should be easier to build on older systems.
