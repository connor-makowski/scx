from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'scx',
  packages = ['scx'],
  version = '1.0.7',
  license='MIT',
  description = 'MIT Supply Chain Python Package',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Connor Makowski',
  author_email = 'conmak@mit.edu',
  url = 'https://github.com/connor-makowski/scx',
  download_url = 'https://github.com/connor-makowski/scx/dist/scx-1.0.7.tar.gz',
  keywords = [],
  install_requires=["PuLP==2.6.0", "type_enforced==0.0.14"],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
