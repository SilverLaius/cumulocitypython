from distutils.core import setup
setup(
  name = 'cumulocitypython',
  packages = ['cumulocitypython'],
  version = '0.1.5',
  license='MIT',
  description = 'Purpose of this package is to easily request historical data from your cumulocity tenant and return it as a pandas dataframe.',
  long_description = 'Purpose of this package is to easily request historical data from your cumulocity tenant and return it as a pandas dataframe. More detailed description and documentation is available at https://github.com/SilverLaius/cumulocitypython',
  author = 'Silver Laius',
  author_email = 'silver.laius@gmail.com',
  url = 'https://github.com/SilverLaius/cumulocitypython',
  download_url = 'https://github.com/SilverLaius/cumulocitypython/archive/1.1.5.tar.gz',
  keywords = ['Python', 'Cumulocity', 'Pandas'],
  install_requires=[
          'python-dateutil',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)