#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


from __future__ import division, print_function, absolute_import
import os


def listxfile(listdir=None, exts=None, issubdir=None):
    r"""
    listdir: lists of string
    exts: list of string, such as ['.png', 'jpg']

    """

    filelists = []

    if listdir is None:
        raise ValueError("'listdir' should not be None!")
        return filelists

    for s in os.listdir(listdir):
        newDir = os.path.join(listdir, s)
        if os.path.isfile(newDir):
            if exts is not None:
                if newDir and(os.path.splitext(newDir)[1] in exts):
                    filelists.append(newDir)
            else:
                filelists.append(newDir)
    return filelists


def pathjoin(*kwargs):
    filesep = os.path.sep
    filepath = ''
    for k in kwargs:
        filepath += filesep + k
    return filepath


def fileparts(file):
    r"""Filename parts

    Returns the path, file name, and file name extension for the specified :attr:`file`.
    The :attr:`file` input is the name of a file or folder, and can include a path and
    file name extension.

    Parameters
    ----------
    file : {str}
        The name of a file or folder.

    Returns
    -------
    filepath : {str}
        The path of a file or folder.
    name : {str}
        The name of a file or folder.
    ext : {str}
        The ext of a file.

    """

    filepath, filename = os.path.split(file)
    name, ext = os.path.splitext(filename)
    return filepath, name, ext


if __name__ == '__main__':

    filepath = '/mnt/d/DataSets/sar/ALOSPALSAR/mat/ALPSRP273680670/ALPSRP273680670-L1.0/ALOS_PALSAR_RAW=IMG-HH-ALPSRP273680670-H1(sl=1el=35345).mat'

    filepath = pathjoin('a', 'b', 'c', '.d')
    print(filepath)
