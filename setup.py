from setuptools import setup
from setuptools import find_packages


setup(name='iprs',
      version='1.0.0',
      description='Intelligent Processing for Radar Signals',
      author='Zhi Liu',
      author_email='zhiliu.mind@gmail.com',
      url='http://iridescent.ink/iprs3.0',
      download_url='https://github.com/antsfamily/iprs',
      license='MIT',
      install_requires=['numpy>=1.9.1',
                        'matplotlib',
                        'scipy>=0.14',
                        'Pillow',
                        'six>=1.9.0',
                        'pyyaml'],
      extras_require={
          'h5py': ['h5py'],
          'visualize': ['pydot>=1.2.0'],
      },
      classifiers=[
          'Development Status :: 1 - Production/Stable',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=find_packages())
