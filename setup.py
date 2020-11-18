# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# setuptools loads some plugins necessary for use here.
from setuptools import find_packages  # noqa: F401
from distutils.core import setup

# Use the readme as the long description.
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="servicex-cli",
      version='1.0.0',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      scripts=[],
      entry_points={
          'console_scripts': ['servicex=servicex_cli.servicex:main'],
      },
      description="CLI for the ServiceX Data Server",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Ben Galewsky (IRIS-HEP/NCSA/University of Illinois)",
      author_email="bengal1@illinois.edu",
      maintainer="Ben Galewsky (IRIS-HEP/NCSA/University of Illinois)",
      maintainer_email="bengal1@illinois.edu",
      url="https://github.com/ssl-hep/servicex_cli",
      license='bsd 3 clause',
      python_requires='>=3.6',
      test_suite="tests",
      install_requires=[
          "oauthlib==3.1.0",
          "kubernetes",
          "pyopenssl==19.1.0"
      ],
      extras_require={
          'test': ['flake8==3.5',
                   'pytest',
                   'pytest-mock',
                   'coverage==4.5.2',
                   'codecov==2.0.15'],
      },
      classifiers=[
          "Development Status :: 3 - Alpha",
          # "Development Status :: 4 - Beta",
          # "Development Status :: 5 - Production/Stable",
          # "Development Status :: 6 - Mature",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Programming Language :: Python",
          "Topic :: Software Development",
          "Topic :: Utilities",
      ],
      platforms="Any",
      )
