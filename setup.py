from distutils.core import setup
setup(
  name = 'cumulocitypython',
  packages = ['cumulocitypython'],
  version = '0.1.1',
  license='MIT',
  description = 'Purpose of this package is to easily request historical data from your cumulocity tenant and return it as a pandas dataframe.',
  author = 'Silver Laius',
  author_email = 'silver.laius@gmail.com',
  url = 'https://github.com/SilverLaius/cumulocity-python',
  download_url = 'https://github.com/SilverLaius/cumulocity-python/archive/v_01.tar.gz',
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