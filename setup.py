from distutils.core import setup
setup(
  name = 'wfpdf',
  py_modules = ['wfpdf'],
  version = '0.9.0',
  description = 'convenience wrapper for fpdf with unicode support',
  install_requires = ['fpdf'],
  author = 'Mirek Zvolsky',
  author_email = 'zvolsky@seznam.cz',
  url = 'https://github.com/zvolsky/wfpdf',
  download_url = 'https://github.com/zvolsky/wfpdf/tarball/0.9.0',
  keywords = ['fpdf', 'pyfpdf', 'pdf'],
  classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Software Development',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
  ],
)
