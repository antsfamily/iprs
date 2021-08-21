#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-11-11 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import numpy as np
import re
from .utils import splitfmt


def readrcd(filepath, decfmtf, D, offset=0, endian='>'):
    """read file record

    read record information from a file. see :func:`read_ers_sar_raw` for reading ERS SAR raw data.

    Parameters
    ----------
    filepath : {string}
        file path string
    decfmtf : {function}
        format decoding function. see :func:`decfmtfers` for example.
    D : {dict}
        record descriptor dict, each value will be rewrited after reading.
    offset : {integer}, optional
        record offset, read from the offset-th Byte (the default is 0)
    endian : {str}, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    state : number
        reading status. 0 --> OK and done; 1 --> no such file; 2 --> bad record

    """

    state = 0

    try:
        f = open(filepath, 'rb')
    except FileNotFoundError as e:
        state = 1
        raise IOError("~~~File is not found!")
    else:
        try:
            for k, v in D.items():
                f.seek(v[0][0] + offset - 1, 0)
                data = f.read(int(v[0][1] - v[0][0] + 1))
                n, F, x = splitfmt(v[1])
                v[2] = decfmtf(F=F, n=n, x=x, b=data, e=endian)
        except IOError as e:
            state = 2
            print("~~~Reading record failed!")
        f.close()
    return state


def readrcd1item(filepath, decfmtf, fmt, offset=0, addr=0, endian='>'):
    """read one file record item

    read one record item information from a file. see :func:`read_ceos_sar_raw` for reading ERS SAR raw data.

    Parameters
    ----------
    filepath : {string}
        file path string
    decfmtf : {function}
        format decoding function. see :func:`decfmtfers` for example.
    fmt : {dict}
        format specification.
    offset : {integer}, optional
        record offset, read from the offset-th Byte (the default is 0)
    addr : {tuple}, optional
        record item addr. read Bytes specified by address :attr:`addr` + offset.
    endian : {str}, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    v : {}
        readed record item value.

    """

    try:
        f = open(filepath, 'rb')
    except FileNotFoundError as e:
        raise IOError("~~~File is not found!")
    else:
        try:
            f.seek(addr[0] + offset - 1, 0)
            data = f.read(int(addr[1] - addr[0] + 1))
            n, F, x = splitfmt(fmt)
            v = decfmtf(F=F, n=n, x=x, b=data, e=endian)
        except IOError as e:
            print("~~~Reading record failed!")
        f.close()
    return v


def printrcd(D):
    """print record

    print record in ascend address order.

    Parameters
    ----------
    D : {dict}
        descriptor dict
    """

    for k, v in sorted(D.items(), key=lambda item: item[1][0]):
        print(k, v)
