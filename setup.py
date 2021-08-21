from setuptools import setup
from setuptools import find_packages


setup(name='iprs',
      version='1.0.4',
      description='Intelligent Processing for Radar Signals',
      author='Zhi Liu',
      author_email='zhiliu.mind@gmail.com',
      url='http://iridescent.ink/iprs3.0',
      download_url='https://github.com/antsfamily/iprs',
      license=None,
      install_requires=['numpy>=1.9.1',
                        'matplotlib',
                        'scipy>=0.14',
                        'scikit-image',
                        'h5py',
                        'Pillow',
                        'six>=1.9.0',
                        'progressbar2',
                        'scikit-learn',
                        'lxml',
                        'pyyaml'],
       classifiers=['Programming Language :: Python :: 3',
                    'Operating System :: OS Independent',],
      packages=find_packages(),
      include_package_data=True,
      )
