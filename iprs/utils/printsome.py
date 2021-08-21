#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-12-01 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#


def printb2h(bytes):
    """print bytes in hex mode

    The default :func:`print` function print bytes with ascii convertion

    Parameters
    ----------
    bytes : {bytes}
        bytes to be printed.
    """

    h = [hex(int(b)) for b in bytes]
    print(r"\x ".join(h))
