#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


from __future__ import division, print_function, absolute_import
import re


def str2list(s):

    left = [i.start() for i in re.finditer('\[', s)]
    print(left)
    right = [i.start() for i in re.finditer('\]', s)]
    print(right)

    nlevel = -1
    for l in left:
        nlevel += 1
        if l > right[0]:
            break
    right[0:nlevel - 1] = right[0:nlevel - 1][::-1]
    right.insert(0, right.pop())
    print(right)


def str2num(s, tfunc=None):

    numstr = re.findall(r'-?\d+\.?\d*e*E?-?\d*', s)
    if tfunc is None:
        return numstr
    else:
        if tfunc == 'auto':
            numlist = []
            for num in numstr:
                if num.find('.') > -1 or num.find('e') > -1:
                    numlist.append(float(num))
                else:
                    numlist.append(int(num))
            return numlist
        else:
            return [tfunc(i) for i in numstr]


if __name__ == '__main__':

    s = '[0, [[[[1], 2.], 33], 4], [5, [6, 2.E-3]], 7, [8]], 1e-3'

    str2list(s)

    # print(str2num(s, int))
    print(str2num(s, float))
    print(str2num(s, 'auto'))


    print(2**(str2num('int8', int)[0]))

