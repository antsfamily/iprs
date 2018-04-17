# What is IPRS?

Intelligent Processing of Radar Signal ( abbr. IPRS), is an outstanding tool for processing radar signals, which is written in python.


# Why use IPRS?

IPRS has many functions and features:

+ Simulation
    - point target
    - real scene
    - CUDA acceleration(not support yet)
+ Compression(not support yet)
+ Imaging
    - Classical 
        * Range-Doppler
        * Chirp Scaling
    - Compressed Sensing based
    - Deep Learning based
+ Detection and Tracking(not support yet)
+ Will be open source soon

# How to use?


# Getting started

## Installation

### Requirements

Python>=2.7

Install `Python` and `pip` first, then install `numpy` , `matplotlib` using the following comands:

```bash
pip install numpy matplotlib scipy Pillow h5py
```

For compressed sensing sar imaging, you need to install [pycompsense](http://pythonhosted.org/pycompsense/index.html).

```bash
sudo pip install Cython pycompsense
```

`IPython` or `jupyter` (optional) can be installed by `` pip3 install ipython`` .

### Install IPRS

The installation of IPRS is very simple, just do as follows in a terminal(Ubuntu: `bash shell` (<kbd>Ctrl+Alt+T</kbd>), Windows: `cmd` or `powershell`).

```bash
cd iprs
python setup.py install
```

If you don't want to install, you can add the root directory of "iprs" into ``PYTHONPATH`` environment variable.

In Ubuntu:

```bash
sudo gedit ~/.bashrc
export PYTHONPATH=$PYTHONPATH:/mnt/d/ws/sci/radar/iprs
```
In Windows:

```bat
:: temporary
set PYTHONPATH=yourpath_to_iprs;%PYTHONPATH%
:: permanent
setx PYTHONPATH "yourpath_to_iprs;%PYTHONPATH%"
```

<!-- ```bat
:: temporary
set PYTHONPATH=D:\ws\sci\radar\iprs;%PYTHONPATH%
:: permanent
setx PYTHONPATH "D:\ws\sci\radar\iprs;%PYTHONPATH%"
``` -->

<!--
or you can do this with GUI.

Open the ``New system variable`` dialog box by the following steps:

``Control Panel -> System -> Advanced system settings -> environment variable -> system variable -> New``

Then input the name and value of new system variable:

![setting PYTHONPATH environment variable in Windows](./PYTHONPATH.png)
-->

# Problems and Solutions

## matplotlib

For Ubuntu with Python3.5, if you get error when install:

```bash
NotImplementedError: Surface.create_for_data: Not Implemented yet.
```

Install the following packages.

```bash
sudo apt-get install python3-dev
sudo apt-get install libffi-dev
sudo pip3 install cffi
sudo pip3 install cairocffi
```


