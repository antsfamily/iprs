#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-12-25 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import os
import re
import struct
import logging
import numpy as np
from iprs.products.ceos import decfmtfceos, read_ceos_sar_raw, read_ceos_sar_slc
from iprs.products.record import readrcd1item


# B: number in binary format
# A: string
# I: char
SarDataFileFileDescriptorRecordERS = {
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

SarDataFileSignalDataRecordERS = {
    'Record sequence number': [(1, 4), '1B4', 0],
    'l-st record sub-type code': [(5, 5), '1B1', 0],
    'Record type code': [(6, 6), '1B1', 0],
    '2-nd record sub-type code': [(7, 7), '1B1', 0],
    '3-rd record sub-type code': [(8, 8), '1B1', 0],
    'Length of this record': [(9, 12), '1B4', 0],
    # PREFIX DATA - GENERAL INFORMATION
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
    # PREFIX DATA PLATFORM REFERENCE INFORMATION
    'Platform information': [(129, 192), '1B64', 0],
    # PREFIX DATA - SENSOR/FACILITY SPECIFIC, AUXILIARY DATA
    'Fixed code = AA in Hexadecimal notation': [(193, 193), '1B1', 0],
    'OGRC/OBRC flag (1 or 0)': [(194, 194), '1B1', 0],
    'ICU on board time': [(195, 198), '1B4', 0],
    'Activity task': [(199, 200), '1B2', 0],
    'Image format counter': [(201, 204), '1B4', 0],
    'Sampling window start time': [(205, 206), '1B2', 0],
    'Pulse repetition interval': [(207, 208), '1B2', 0],
    'Calibration attenuation setting': [(209, 209), '1B1', 0],
    'Receiver gain attenuation setting': [(210, 210), '1B1', 0],
    'Spare4': [(211, 340), '130B1', 0],
    '36 calibration pulses as (4bit spare 6bit Q 6bit I from MSB down to LSB)': [(341, 412), '36B2', 0],
    # SAR RAW SIGNAL DATA
    'Raw Data': [(413, 414), '2B1', 0]  # [I, Q]
}

SarDataFileProcessedDataRecordERS = {
    'Record sequence number': [(1, 4), '1B4', 0],
    'l-st record sub-type code': [(5, 5), '1B1', 0],
    'Record type code': [(6, 6), '1B1', 0],
    '2-nd record sub-type code': [(7, 7), '1B1', 0],
    '3-rd record sub-type code': [(8, 8), '1B1', 0],
    'Length of this record': [(9, 12), '1B4', 0],
    # SAR PROCESSED DATA
    # 'Processed Data': [(13, 16), '2F2', 0],  # '2F2' for [real, imag], or '1C4' for real + 1j*imag
    'Processed Data': [(13, 16), '1I1', 0],  # '1I1' for amplitude image
}


def read_uavsar_csm(filepath, sl=1, el=-1, rmbp=False):
    r"""read UAVSAR raw data

    read UAVSAR SAR raw data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly and do some post-process.


    Parameters
    ----------
    filepath : {string}
        UAVSAR raw data file path string, for UAVSAR --> ``*.raw``
    sl : {number}, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : {number}, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : {bool}, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : {numpy 2d-array}
       SAR raw signal data matrix.

    """

    logging.info("===In read_ers_sar_raw...")

    raise TypeError("Not opened yet!")

    logging.info("===Out read_ers_sar_raw.")

    return S


def read_uavsar_mlc(filepath, dshape=None, dtype='complex'):
    r"""read UAVSAR MLC data

    read UAVSAR SAR MLC data.


    Parameters
    ----------
    filepath : {string}
        UAVSAR MLC data file path string, for UAVSAR --> ``*.mlc``
    dshape : {tuple}, optional
        MLC data shape (:math:`N_a\times N_r`), where, :math:`N_a, N_r` equal
        to ``mlc_mag.set_rows``, ``mlc_mag.set_cols`` which can be obtained
        from the ``.ann`` file (the default is 1, which means the first line)
    dshape : {string}
        MLC data type: ``'complex'`` for complex-valued floating point data,
        ``'real'`` for real-valued floating point data.

    Returns
    -------
    S : {numpy 2d-array}
       SAR MLC data matrix.

    """

    logging.info("===In read_uavsar_mlc...")

    endian = '<'
    n = dshape[0] * dshape[1]
    if dtype == 'complex':
        n = n + n
    try:
        f = open(filepath, 'rb')
    except FileNotFoundError as e:
        raise IOError("~~~File is not found!")
    else:
        try:
            f.seek(0, 0)
            b = f.read(int(n * 4))
            S = np.array(struct.unpack(endian + str(n) + 'f', b))
            if dtype == 'complex':
                S = np.array([np.reshape(np.array(S[0::2]), (dshape[1], dshape[0])).transpose(),
                              np.reshape(np.array(S[1::2]), (dshape[1], dshape[0])).transpose()]
                             ).transpose(1, 2, 0)
        except IOError as e:
            print("~~~Reading file failed!")
        f.close()

    logging.info("===Out read_uavsar_mlc.")
    return S
