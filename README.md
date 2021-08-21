# What is IPRS?

Intelligent Processing of Radar Signal ( ab. IPRS), is an outstanding tool for processing radar signals, which is written in python.


# Why use IPRS?

IPRS has many functions and features:

+ Simulation
    - point target
    - real scene
<!-- + Compression -->
+ Compression(Not Supported yet)
+ Imaging
    - Classical
        * Range-Doppler
        * Chirp Scaling
    - Compressed Sensing based
    - Deep Learning based
<!-- + Detection and Tracking -->
+ Detection and Tracking(Not Supported yet)

# How to use?


# Getting started

## Installation

### Requirements

Python>=2.7

Install `Python` and `pip` first, then install `numpy` , `matplotlib` using the following comands:

```bash
	# Python3
	pip3 install -r requirements.txt

	# Python2
	pip2 install -r requirements.txt


```

`IPython` or `jupyter` (optional) can be installed by `` pip3 install ipython``.


### Install IPRS


Now you can install ``iprs`` by command: ``pip install iprs``! 

You can install it manually, the installation of ``iprs`` is very simple, just do as follows in a terminal(Ubuntu: `bash shell` (<kbd>Ctrl+Alt+T</kbd>), Windows: `cmd` or `powershell`).

```bash
cd iprs
python setup.py install
```

Otherwise, you can just run ``install.sh`` (Ubuntu) or ``install.bat`` （Windows）to install iprs automatically.

If you don't want to install, you can add the root directory of "iprs" into ``PYTHONPATH`` environment variable.

In Ubuntu:

```bash
sudo gedit ~/.bashrc
export PYTHONPATH=$PYTHONPATH:yourpath_to_iprs
```
In Windows:

```bat
:: temporary
set PYTHONPATH=yourpath_to_iprs;%PYTHONPATH%
:: permanent
setx PYTHONPATH "yourpath_to_iprs;%PYTHONPATH%"
```

## Uninstallation

- If you install IPRS by running ``install.sh`` or ``install.bat``, Just run ``uninstall.sh`` (Ubuntu) or ``uninstall.bat`` （Windows）to uninstall iprs automatically.
- If you install IPRS by ``python setup.py install``, try ``pip uninstall iprs``.
- If you install IPRS by adding a ``PYTHONPATH`` environment, just remove that path.


# Todo

- if ``Ab`` is not small, the both sides along range footprint of the Central Point is not equal. The accuracy of calculation (Rnear, Rfar) is inaccurate, and will cause the target far from the actual value.

- along range footprint: ``ar_footprint(Wl, H, Lr, Ad)``

# Problems and Solutions

## matplotlib

For Ubuntu with Python3.5, if you get error when install it:

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


