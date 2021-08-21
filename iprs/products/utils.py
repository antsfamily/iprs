#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-11-11 12:32:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#
from __future__ import division, print_function, absolute_import

import re


def getnumber(b):
    r"""obtain number in string or bytes

    obtain number in string/bytes, e.g. b' 123 45 ' --> [123, 45],
    b' 123, 45 ' --> [123, 45] and b'  ' --> []

    Parameters
    ----------
    b : {bytes string}
        bytes string for extracting numbers.

    Returns
    -------
    n : number list or number
        extracted number list, if there only one element, return a number.
    """
    n = [int(i) for i in re.findall(r'\d+', str(b))]
    if len(n) == 1:
        n = n[0]
    return n


def splitfmt(fmt):
    n, F, x = re.findall(r'[0-9]+|[a-z,A-Z]+|[0-9]', fmt)

    return (int(n), F, int(x))


if __name__ == '__main__':

    print(getnumber(b' 1 23'))
    print(getnumber(b' 1,23'))
    print(getnumber(b'  '))

    print(splitfmt('100IU33'))
