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
import copy
import numpy as np
from progressbar import *

import logging
from iprs.products.ceos import decfmtfceos
from iprs.products.utils import splitfmt
from iprs.products.record import readrcd, readrcd1item, printrcd


LeaderFileImportantImagingParametersRecordERS = {
    'Radar frequency (GHz)': [(720 + 493, 720 + 500), '1F8', 0],
    'Radar wavelength (meters)': [(720 + 501, 720 + 516), '1F16', 0],
    'Sampling rate (MHz)': [(720 + 711, 720 + 726), '1F16', 0],
    'Range pulse length (usec)': [(720 + 743, 720 + 758), '1F16', 0],
    'Range compressed flag': [(720 + 763, 720 + 766), '1A4', 0],
    'DC Bias for I-component': [(720 + 819, 720 + 834), '1F16', 0],
    'DC Bias for Q-component': [(720 + 835, 720 + 850), '1F16', 0],
    'Gain imbalance for I & Q': [(720 + 851, 720 + 866), '1F16', 0],
    'Nominal PRF (Hz)': [(720 + 935, 720 + 950), '1F16', 0],
    'Zero-doppler range time of first range pixel (msec)': [(720 + 1767, 720 + 1782), '1F16', 0],
    'Zero-doppler range time of centre range pixel (msec)': [(720 + 1783, 720 + 1798), '1F16', 0],
    'Zero-doppler range time of last range pixel (msec)': [(720 + 1799, 720 + 1814), '1F16', 0],
    'Zero-doppler range time of last range pixel (msec)': [(720 + 1799, 720 + 1814), '1F16', 0],
}


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
    'Raw Data': [(-1, -1), '2B1', 0]  # auto infer, (413, )
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
    'Processed Data': [(-1, -1), '1IU1', 0],  # auto infer, (13, )
}


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


def read_ers_sar_ldr_iip(filepath, verbose=False):
    r"""Read important imaging parameters from leader file

    Read important imaging parameters from leader file.

    Parameters
    ----------
    filepath : {str}
        Leader file path string.
    """

    logging.info("===In read_ers_sar_ldr_iip...")

    LFIIPR = copy.deepcopy(LeaderFileImportantImagingParametersRecordERS)

    offsLFIIPR = 0
    readrcd(filepath, decfmtfceos, LFIIPR, offset=offsLFIIPR, endian='>')
    if verbose:
        printrcd(LFIIPR)
    logging.info("---Done.")
    logging.info("===Out read_ers_sar_ldr_iip.")
    return LFIIPR


def read_ers_sar_raw(filepath, sl=1, el=-1, rmbp=False):
    r"""read ERS SAR raw data

    read ERS1/2 SAR raw data pulse from line :attr:`sl` to line :attr:`el`.


    Parameters
    ----------
    filepath : {string}
        ERS SAR raw data file path string, for ERS1/2 --> ``*.raw``
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


def read_ers_sar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read ERS SAR SLC data

    read ERS1/2 SAR SLC data pulse from line :attr:`sl` to line :attr:`el`.


    Parameters
    ----------
    filepath : {string}
        ERS SAR raw data file path string, for ERS1/2 --> ``*.raw``
    sl : {number}, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : {number}, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : {bool}, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : {numpy 2d-array}
       SAR SLC data matrix.

    """

    logging.info("===In read_ers_sar_slc...")

    raise TypeError("Not opened yet!")

    logging.info("===Out read_ers_sar_slc.")

    return S
