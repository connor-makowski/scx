from distutils.core import setup
setup(
  name = 'scx',
  packages = ['scx'],
  version = '0.0.3',
  license='MIT',
  description = 'MIT Supply Chain Python Package',
  author = 'Connor Makowski',
  author_email = 'conmak@mit.edu',
  url = 'https://github.com/connor-makowski/scx',
  download_url = 'https://github.com/connor-makowski/scx/dist/scx-0.0.3.tar.gz',
  keywords = [],
  install_requires=["PuLP==2.6.0", "type_enforced==0.0.5"],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
