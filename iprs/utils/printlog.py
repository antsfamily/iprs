#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-12-24 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import sys
import time


class ProgressBar:

    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width
        sys.stdout.write('\r\n')

    def move(self):
        self.count += 1

    def log(self):
        # sys.stdout.write(' ' * (self.width + 9))
        sys.stdout.flush()
        progress = int(self.width * self.count / self.total)
        progressstr = '.' * progress + '-' * (self.width - progress)
        progressstr = '.' * progress
        sys.stdout.write(
            '{0:3}/{1:3}: '.format(self.count, self.total) + progressstr + '\r')
        # sys.stdout.write()
        # if progress == self.width:
        #     sys.stdout.write('\n')
        # sys.stdout.flush()


if __name__ == '__main__':

    bar = ProgressBar(total=100)

    for i in range(100):
        bar.move()
        bar.log()
        time.sleep(0.5)
