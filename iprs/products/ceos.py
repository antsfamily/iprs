#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2018-11-01 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import re
import struct
import codecs
import copy
import logging
import numpy as np
from progressbar import *

from iprs.products.utils import getnumber, splitfmt
from iprs.products.record import readrcd, readrcd1item, printrcd


# B: number in binary format
# A: string
# I: char
SarDataFileFileDescriptorRecordCEOS = {
    # SAR DATA FILE - FILE DESCRIPTOR RECORD (FIXED SEGMENT)
    'Record sequence number': [(1, 4), '1B4', 0],
    'l-st record sub-type code': [(5, 5), '1B1', 0],
    'Record type code': [(6, 6), '1B1', 0],
    '2-nd record sub-type code': [(7, 7), '1B1', 0],
    '3-rd record sub-type code': [(8, 8), '1B1', 0],
    'Length of this record': [(9, 12), '1B4', 0],
    'ASCII/EBCDIC flag': [(13, 14), '1A2', 0],
    '1Blanks': [(15, 16), '1A2', 0],
    'Format control document ID': [(17, 28), '1A12', 0],
    'Format control document revision level': [(29, 30), '1A2', 0],
    'File design descriptor revision letter': [(31, 32), '1A2', 0],
    'Generating software release and revision level': [(33, 44), '1A12', 0],
    'File number': [(45, 48), '1I4', 0],
    'File name': [(49, 64), '1A16', 0],
    'Record sequence and location type flag': [(65, 68), '1A4', 0],
    'Sequence number location': [(69, 76), '1I8', 0],
    'Sequence number field length': [(77, 80), '1I4', 0],
    'Record code and location type flag': [(81, 84), '1A4', 0],
    'Record code location': [(85, 92), '1I8', 0],
    'Record code field length': [(93, 96), '1I4', 0],
    'Record length and location type flag': [(97, 100), '1A4', 0],
    'Record length location': [(101, 108), '1I8', 0],
    'Record length field length': [(109, 112), '1I4', 0],
    'Reserved1': [(113, 113), '1I1', 0],
    'Reserved2': [(114, 114), '1I1', 0],
    'Reserved3': [(115, 115), '1I1', 0],
    'Reserved4': [(116, 116), '1I1', 0],
    'Reserved segment': [(117, 180), '1A64', 0],
    # SAR DATA IMAGERY OPTIONS FILE DESCRIPTOR RECORD (VARIABLE SEGMENT)
    'Number of SAR DATA records (nominal)': [(181, 186), '1I6', 0],
    'SAR DATA record length (bytes)': [(187, 192), '1I6', 0],
    'Reserved1 (blanks)': [(193, 216), '1A4', 0],
    'Number of bits per sample': [(217, 220), '1I4', 0],
    'Number of samples per data group (or pixels)': [(221, 224), '1I4', 0],
    'Number of bytes per data group (or pixel)': [(225, 228), '1I4', 0],
    'Justification and order of samples within data group': [(229, 232), '1A4', 0],
    'Number of SAR channels in this file': [(233, 236), '1I4', 0],
    'Number of lines per data set (nominal)': [(237, 244), '1I8', 0],
    'Number of left border pixels per line': [(245, 248), '1I4', 0],
    'Total number of data groups per line per SAR channel': [(249, 256), '1I8', 0],
    'Number of right border pixels per line': [(257, 260), '1I4', 0],
    'Number of top border lines': [(261, 264), '1I4', 0],
    'Number of bottom border lines': [(265, 268), '1I4', 0],
    'Interleaving indicator': [(269, 272), '1A4', 0],
    'Number of physical records per line': [(273, 274), '1I2', 0],
    'Number of physical records per multi-channel line': [(275, 276), '1I2', 0],
    'Number of bytes of prefix data per record': [(277, 280), '1I4', 0],
    'Number of bytes of SAR data (or pixel data) per record (nominal)': [(281, 288), '1I8', 0],
    'Number of bytes of suffix data per record': [(289, 292), '1I4', 0],
    'Reserved2': [(293, 340), '1A48', 0],
    'Blanks': [(341, 368), '1A28', 0],
    'Reserved3': [(369, 400), '1A32', 0],
    'SAR Data format type identifier': [(401, 428), '1A28', 0],
    'SAR Data format type code': [(429, 432), '1A4', 0],
    'Number of left fill bits within pixel': [(433, 436), '1I4', 0],
    'Number of right fill bits within pixel': [(437, 440), '1I4', 0],
    'Maximum data range of pixel (max-min value for I and Q)': [(441, 448), '1I8', 0],
    # 'spare': [(449, 11644), '11196s', 0],
}

SarDataFileSignalDataRecordCEOS = {
    'Record sequence number': [(1, 4), '1B4', 0],
    'l-st record sub-type code': [(5, 5), '1B1', 0],
    'Record type code': [(6, 6), '1B1', 0],
    '2-nd record sub-type code': [(7, 7), '1B1', 0],
    '3-rd record sub-type code': [(8, 8), '1B1', 0],
    'Length of this record': [(9, 12), '1B4', 0],
    # ---PREFIX DATA - GENERAL INFORMATION
    'SAR image data line number': [(13, 16), '1B4', 0],
    'SAR image data record index (indicates the record sequence number of the image line)': [(17, 20), '1B4', 0],
    'Actual count of left-fill pixels': [(21, 24), '1B4', 0],
    'Actual count of data pixels (samples)': [(25, 28), '1B4', 0],
    'Actual count of right-fill pixels': [(29, 32), '1B4', 0],
    'Reserved1': [(33, 84), '1I52', 0],
    'Spare1': [(85, 88), '1I4', 0],
    'Spare2': [(89, 92), '1I4', 0],
    'Reserved2': [(93, 124), '1I32', 0],
    'Spare3': [(125, 128), '1I4', 0],
    # ---SAR RAW SIGNAL DATA
    # ~~~from ['Length of this record'] to 'Number of bytes of SAR data (or pixel data) per record (nominal)'
    'Raw Data': [(-1, -1), '2B1', 0]  # auto infer
}

SarDataFileProcessedDataRecordCEOS = {
    'Record sequence number': [(1, 4), '1B4', 0],
    'l-st record sub-type code': [(5, 5), '1B1', 0],
    'Record type code': [(6, 6), '1B1', 0],
    '2-nd record sub-type code': [(7, 7), '1B1', 0],
    '3-rd record sub-type code': [(8, 8), '1B1', 0],
    'Length of this record': [(9, 12), '1B4', 0],
    # SAR PROCESSED DATA
    # ~~~from ['Length of this record'] to 'Number of bytes of SAR data (or pixel data) per record (nominal)'
    # ~~~'2F2' for [real, imag], '1C4' for real+1j*imag
    # ~~~'1I1' for amplitude image
    # 'Processed Data': [(-1, -1), '2F2', 0],  # auto infer
    # 'Processed Data': [(-1, -1), '1C4', 0],  # auto infer
    'Processed Data': [(-1, -1), '1IU1', 0],  # auto infer
}


def decfmtfceos(F, n, x, b, e='<'):
    r"""decode format descriptor of CEOS

    decode format descriptor of CEOS.

    ``'nFx'`` --> decode :attr:`b` x Bytes-by-x Bytes as format :attr:`F` specified,
    and do :attr:`n` times.

    Parameters
    ----------
    F : {string}
        formation string, ``C`` --> Complex(real, imag), ``F`` --> float, ``B`` --> Bytes, ``A`` --> String, ``I`` --> asicc
    n : {integer}
        amount of elements with formation :attr:`F`
    x : {integer}
        number of Bytes
    b : {bytes}
        bytes to be decoded
    e : {str}, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    list
        decoded result list.
    """
    return {
        'F': lambda: [float(b[i * x:(i + 1) * x]) for i in range(n)],
        'f': lambda: struct.unpack(e + str(n) + 'f', b),
        'C': lambda: [float(b[i * int(x / 2.):(i + 1) * int(x / 2)]) + 1j * float(b[i * x:(i + 1) * x]) for i in range(n)],
        'B': lambda: [int.from_bytes(b[i * x:(i + 1) * x], byteorder=('big' if e is '>' else 'little'), signed=False) for i in range(n)],
        'A': lambda: [struct.unpack(e + str(x) + 's', b[i * x:(i + 1) * x])[0].decode() for i in range(n)],
        'I': lambda: [getnumber(b[i * x:(i + 1) * x]) for i in range(n)],
        # 'I': lambda: [struct.unpack(e + str(x) + 's', b[i * x:(i + 1) * x])[0] for i in range(n)],
        'IU': lambda: [int.from_bytes(b[i * x:(i + 1) * x], byteorder=('big' if e is '>' else 'little'), signed=False) for i in range(n)],
        # 'IU': lambda: [int(codecs.encode(b[i * x:(i + 1) * x], 'hex'), 16) for i in range(n)],
        'IS': lambda: [int.from_bytes(b[i * x:(i + 1) * x], byteorder=('big' if e is '>' else 'little'), signed=True) for i in range(n)],
        # 'IS': lambda: [b2i(b[i * x:(i + 1) * x]) for i in range(n)],
    }.get(F, None)()


def _getdtype_component(fmtrcd, fmtuser):

    if fmtrcd in ['CIS', 'CI']:
        if fmtuser in ['C', 'CI']:
            dtype = 'complex'
            nComponentPerPixel = 1  # [I+1j*Q] or [real+1j*imag]
        else:
            dtype = 'uint'
            nComponentPerPixel = 2  # [I Q] or [real imag]
    if fmtrcd in ['CS', 'C']:
        dtype = 'float'
        if fmtuser in ['C', 'CI']:
            dtype = 'complex'
            nComponentPerPixel = 1  # [I+1j*Q] or [real+1j*imag]
        else:
            dtype = 'float'
            nComponentPerPixel = 2  # [I Q] or [real imag]
    if fmtrcd in ['IU']:
        dtype = 'uint'
        nComponentPerPixel = 1  # amplitude
    if fmtrcd in ['I']:
        dtype = 'int'
        nComponentPerPixel = 1  # amplitude

    return dtype, nComponentPerPixel


def read_ceos_sar_raw(filepath, sl=1, el=-1, rmbp=False):
    r"""read CEOS SAR raw data

    read CEOS SAR raw data pulse from line :attr:`sl` to line :attr:`el`.

    Parameters
    ----------
    filepath : {string}
        SAR raw data file path string, for ERS1/2 --> ``*.raw`` for RADARSAT --> ``DAT_01.001``
    sl : {number}, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : {number}, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : {bool}, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : {numpy 2d-array}


    """

    logging.info("===In read_ceos_sar_raw...")

    raise TypeError("Not opened yet!")
    logging.info("===Out read_ceos_sar_raw.")

    return S


def read_ceos_sar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read CEOS SAR slc data

    read CEOS SAR slc data from line :attr:`sl` to line :attr:`el`.

    Parameters
    ----------
    filepath : {string}
        SAR slc data file path string, for ERS1/2 --> ``*.D`` for RADARSAT --> ``DAT_01.001``
    sl : {number}, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : {number}, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : {bool}, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : {numpy 2d-array}
       Processed SLC SAR data matrix.

    """

    logging.info("===In read_ceos_sar_slc...")

    raise TypeError("Not opened yet!")

    logging.info("===Out read_ceos_sar_slc.")

    return S


if __name__ == '__main__':

    disk = '/mnt/d/'
    filename = 'E2_84686_STD_L0_F203'
    # filename = 'E2_84699_STD_L0_F303'
    # filepath = disk + 'DataSets/sar/ERS/data/' + filename + '/' + filename + '.000.ldr'
    filepath = disk + 'DataSets/sar/ERS/data/' + \
        filename + '/' + filename + '.000.raw'

    endian = '>'

    D = copy.deepcopy(SarDataFileFileDescriptorRecordCEOS)
    # D = copy.deepcopy(SarDataFileSignalDataRecordERS)

    offset = 0
    # offset = 11644

    readrcd(filepath, decfmtfers, D, offset=offset, endian='>')

    print("===============")
    printrcd(D)
