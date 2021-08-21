#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
#

from lxml import etree
# from lxml import html
import logging.handlers
import logging
import os
import sys
import iprs


class logger:
    # 先读取XML文件中的配置数据
    # 由于config.xml放置在与当前文件相同的目录下，因此通过 __file__ 来获取XML文件的目录，然后再拼接成绝对路径
    # 这里利用了lxml库来解析XML
    root = etree.parse(os.path.join(
        os.path.dirname(__file__), 'logconfig.xml')).getroot()
    # 读取日志文件保存路径
    logpath = root.find('logpath').text
    # 读取日志文件容量，转换为字节
    logsize = 1024 * 1024 * int(root.find('logsize').text)
    # 读取日志文件保存个数
    lognum = int(root.find('lognum').text)

    if logpath is None:
        # logpath = iprs.__file__
        logpath, _ = os.path.split(iprs.__file__)

        # pos = [i.start() for i in re.finditer(os.sep, logpath)]
        # logpath = logpath[0:pos[-2]]
    logpath = logpath + '/logs/'
    # print(logpath)

    if not os.path.exists(logpath):
        os.mkdir(logpath)

    # 日志文件名：由用例脚本的名称，结合日志保存路径，得到日志文件的绝对路径
    logname = os.path.join(logpath, sys.argv[0].split('/')[-1].split('.')[0])

    if logname == logpath:
        logname = logpath + '/temp'

    # 初始化logger
    log = logging.getLogger()
    # 日志格式，可以根据需要设置
    fmt = logging.Formatter(
        '[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

    # 日志输出到文件，这里用到了上面获取的日志名称，大小，保存个数
    handle1 = logging.handlers.RotatingFileHandler(
        logname, maxBytes=logsize, backupCount=lognum)
    handle1.setFormatter(fmt)
    # 同时输出到屏幕，便于实施观察
    handle2 = logging.StreamHandler(stream=sys.stdout)
    handle2.setFormatter(fmt)
    log.addHandler(handle1)
    log.addHandler(handle2)

    # 设置日志基本，这里设置为INFO，表示只有INFO级别及以上的会打印
    log.setLevel(logging.INFO)

    # 日志接口，用户只需调用这里的接口即可，这里只定位了INFO, WARNING, ERROR三个级别的日志，可根据需要定义更多接口
    @classmethod
    def info(cls, msg):
        cls.log.info(msg)
        return

    @classmethod
    def warning(cls, msg):
        cls.log.warning(msg)
        return

    @classmethod
    def error(cls, msg):
        cls.log.error(msg)
        return
