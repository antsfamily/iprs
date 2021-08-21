#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-12-25 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import re
import copy
import logging
import numpy as np
from progressbar import *

from iprs.products.ceos import decfmtfceos
from iprs.products.utils import splitfmt
from iprs.products.record import readrcd, readrcd1item


LeaderFileImportantImagingParametersRecordALOS = {
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
SarDataFileFileDescriptorRecordALOSPALSAR = {
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
    'Record sequence and location type flag': [(69, 76), '1I8', 0],
    'Sequence number location': [(77, 80), '1I4', 0],
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
    'Number of SAR DATA records': [(181, 186), '1I6', 0],
    'SAR DATA record length (bytes)': [(187, 192), '1I6', 0],
    'Reserved1 (blanks)': [(193, 216), '1A24', 0],
    # SAMPLE GROUP DATA
    'Number of bits per sample': [(217, 220), '1I4', 0],
    'Number of samples per data group (or pixels)': [(221, 224), '1I4', 0],
    'Number of bytes per data group (or pixel)': [(225, 228), '1I4', 0],
    'Justification and order of samples within data group': [(229, 232), '1A4', 0],
    # SAR RELATED DATA IN THE RECORD
    'Number of SAR channels in this file': [(233, 236), '1I4', 0],
    'Number of lines per data set (nominal)': [(237, 244), '1I8', 0],
    'Number of left border pixels per line': [(245, 248), '1I4', 0],
    'Total number of data groups per line per SAR channel': [(249, 256), '1I8', 0],
    'Number of right border pixels per line': [(257, 260), '1I4', 0],
    'Number of top border lines': [(261, 264), '1I4', 0],
    'Number of bottom border lines': [(265, 268), '1I4', 0],
    'Interleaving indicator': [(269, 272), '1A4', 0],
    # RECORD DATA IN THE FILE
    'Number of physical records per line': [(273, 274), '1I2', 0],
    'Number of physical records per multi-channel line': [(275, 276), '1I2', 0],
    'Number of bytes of prefix data per record': [(277, 280), '1I4', 0],
    'Number of bytes of SAR data (or pixel data) per record (nominal)': [(281, 288), '1I8', 0],
    'Number of bytes of suffix data per record': [(289, 292), '1I4', 0],
    'Prefix/suffix repeat flag': [(293, 296), '1A4', 0],
    # PREFIX/SUFFIX DATA LOCATORS
    'Sample data line number locator ': [(297, 304), '1A8', 0],
    'SAR channel number locator': [(305, 312), '1A8', 0],
    'Time of SAR data line locator': [(313, 320), '1A8', 0],
    'Left-fill count locator': [(321, 328), '1A8', 0],
    'Right-fill count locator': [(329, 336), '1A8', 0],
    'Pad pixels present indicator': [(337, 340), '1A4', 0],
    'Always blank filled': [(341, 368), '1A28', 0],
    'SAR data line quality code locator': [(369, 376), '1A8', 0],
    'Calibration information field locator': [(377, 384), '1A8', 0],
    'Gain values field locator': [(385, 392), '1A8', 0],
    'Bias values filed locator': [(393, 400), '1A8', 0],
    'SAR Data format type identifier': [(401, 428), '1A28', 0],
    'SAR Data format type code': [(429, 432), '1A4', 0],
    'Number of left fill bits within pixel': [(433, 436), '1I4', 0],
    'Number of right fill bits within pixel': [(437, 440), '1I4', 0],
    'Maximum data range of pixel (starting form 0)': [(441, 448), '1I8', 0],
    # 'spare': [(449, 11644), '11196s', 0],
}

SarDataFileSignalDataRecordALOSPALSAR = {  # level1.0
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
    'Actual count of data pixels': [(25, 28), '1B4', 0],
    'Actual count of right-fill pixels': [(29, 32), '1B4', 0],
    # PREFIX DATA-SENSOR PARAMETERS
    'Sensor parameters update flag (1=data in this section is an update 0=data is a repeat)': [(33, 36), '1B4', 0],

    'Sensor acquisition year (UT)': [(37, 40), '1B4', 0],
    'Sensor acquisition day of year (UT) ': [(41, 44), '1B4', 0],
    'Sensor acquisition msecs of day (UT)': [(45, 48), '1B4', 0],
    'SAR channel indicator (sequence number in multi-channel SAR data, polarization)': [(49, 50), '1B2', 0],
    'SAR channel code (0 = L, 1 = 5, 2 = C, 3 = X, 4 = KU and 5 = KA channel)': [(51, 52), '1B2', 0],
    'Transmitted polarization': [(53, 54), '1B2', 0],
    'Received polarization': [(55, 56), '1B2', 0],
    'PRF [mHz]': [(57, 60), '1B4', 0],
    'Scan ID for SCAN SAR mode ( 1 - 5 ) except Wide Observation mode = always 0': [(61, 64), '1B4', 0],
    'Onboard Range compressed flag (0 = no/1 = yes) = always 0': [(65, 66), '1B2', 0],
    'Pulse (chirp) type designator (0 = "LINEARbFMbCHIRPb",1 = "PHASEbMODULATORS") = always 0': [(67, 68), '1B2', 0],
    'Chirp length (nano-secs)': [(69, 72), '1B4', 0],
    'Chirp constant coefficient (Hz) (nominal value)': [(73, 76), '1B4', 0],
    'Chirp linear coefficient (Hz/usec) (nominal value)': [(77, 80), '1B4', 0],
    'Chirp quadratic coefficient (Hz/Wsec,)': [(81, 84), '1B4', 0],
    'spare Always blank(0) filled1': [(85, 88), '1B4', 0],
    'spare Always blank(0) filled2': [(89, 92), '1B4', 0],
    'Receiver gain (dB) nominal value': [(93, 96), '1B4', 0],
    'Nought line flag (0 = no(Right Line)/1 = yes(Loss Line))': [(97, 100), '1B4', 0],
    'Electronic antenna squint angle (millionths of degrees)= always blank (0) filled': [(101, 104), '1B4', 0],
    'Antenna mechanical elevation angle from nadir (millionths of degrees)= always blank (0) filled': [(105, 108), '1B4', 0],
    'Electronic antenna squint angle (millionths of degrees)': [(109, 112), '1B4', 0],
    'Mechanical antenna squint angle (millionths of degrees)= always blank (0) filled': [(113, 116), '1B4', 0],
    'Slant range to 1st data sample (m)': [(117, 120), '1B4', 0],
    'Data record window position (i.e.. sample delay) (nano-secs)': [(121, 124), '1B4', 0],
    'spare Always blank(0) filled3': [(125, 128), '1B4', 0],
    # PREFIX DATA-PLATFORM REFERENCE INFORMATION
    'Platform information': [(129, 192), '1B64', 0],
    # PREFIX DATA - SENSOR/FACILITY SPECIFIC, AUXILIARY DATA
    'Always blank (0) filled1': [(193, 284), '1B92', 0],
    'Counter of PALSAR frame': [(285, 288), '1B4', 0],
    'PALSAR auxiliary data': [(289, 388), '1B100', 0],
    'Always blank (0) filled2': [(389, 412), '1B24', 0],
    # SAR RAW SIGNAL DATA
    'Raw Data': [(413, 414), '2B1', 0]  # [I, Q]
}


# B: number in binary format
# A: string
# I: char
SarImageFileFileDescriptorRecordALOSPALSAR = {
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
    'Referenced file name': [(49, 64), '1A16', 0],
    'Record sequence and location type flag': [(65, 68), '1A4', 0],
    'Record sequence and location type flag': [(69, 76), '1I8', 0],
    'Sequence number location': [(77, 80), '1I4', 0],
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
    'Number of SAR DATA records': [(181, 186), '1I6', 0],
    'SAR DATA record length (bytes)': [(187, 192), '1I6', 0],
    'Reserved1 (blanks)': [(193, 216), '1A24', 0],
    # SAMPLE GROUP DATA
    'Number of bits per sample': [(217, 220), '1I4', 0],
    'Number of samples per data group (or pixels)': [(221, 224), '1I4', 0],
    'Number of bytes per data group (or pixel)': [(225, 228), '1I4', 0],
    'Justification and order of samples within data group': [(229, 232), '1A4', 0],
    # SAR RELATED DATA IN THE RECORD
    'Number of SAR channels in this file': [(233, 236), '1I4', 0],
    'Number of lines per data set (nominal)': [(237, 244), '1I8', 0],
    'Number of left border pixels per line': [(245, 248), '1I4', 0],
    'Total number of data groups per line per SAR channel': [(249, 256), '1I8', 0],
    'Number of right border pixels per line': [(257, 260), '1I4', 0],
    'Number of top border lines': [(261, 264), '1I4', 0],
    'Number of bottom border lines': [(265, 268), '1I4', 0],
    'Interleaving indicator': [(269, 272), '1A4', 0],
    # RECORD DATA IN THE FILE
    'Number of physical records per line': [(273, 274), '1I2', 0],
    'Number of physical records per multi-channel line': [(275, 276), '1I2', 0],
    'Number of bytes of prefix data per record': [(277, 280), '1I4', 0],
    'Number of bytes of SAR data (or pixel data) per record (nominal)': [(281, 288), '1I8', 0],
    'Number of bytes of suffix data per record': [(289, 292), '1I4', 0],
    'Prefix/suffix repeat flag': [(293, 296), '1A4', 0],
    # PREFIX/SUFFIX DATA LOCATORS
    'Sample data line number locator ': [(297, 304), '1A8', 0],
    'SAR channel number locator': [(305, 312), '1A8', 0],
    'Time of SAR data line locator': [(313, 320), '1A8', 0],
    'Left-fill count locator': [(321, 328), '1A8', 0],
    'Right-fill count locator': [(329, 336), '1A8', 0],
    'Pad pixels present indicator': [(337, 340), '1A4', 0],
    'Always blank filled': [(341, 368), '1A28', 0],
    'SAR data line quality code locator': [(369, 376), '1A8', 0],
    'Calibration information field locator': [(377, 384), '1A8', 0],
    'Gain values field locator': [(385, 392), '1A8', 0],
    'Bias values filed locator': [(393, 400), '1A8', 0],
    'SAR Data format type': [(401, 428), '1A28', 0],
    'SAR Data format type code': [(429, 432), '1A4', 0],
    'Number of left fill bits within pixel': [(433, 436), '1I4', 0],
    'Number of right fill bits within pixel': [(437, 440), '1I4', 0],
    'Maximum data range of pixel (starting form 0)': [(441, 448), '1I8', 0],
    # 'Always blank filled': [(449, 720), '1A272', 0],
}

SarImageFileSignalDataRecordALOSPALSAR = {  # level1.1
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
    'Actual count of data pixels': [(25, 28), '1B4', 0],
    'Actual count of right-fill pixels': [(29, 32), '1B4', 0],
    # PREFIX DATA-SENSOR PARAMETERS
    'Sensor parameters update flag (1=data in this section is an update 0=data is a repeat)': [(33, 36), '1B4', 0],

    'Sensor acquisition year (UT)': [(37, 40), '1B4', 0],
    'Sensor acquisition day of year (UT) ': [(41, 44), '1B4', 0],
    'Sensor acquisition msecs of day (UT)': [(45, 48), '1B4', 0],
    'SAR channel indicator (sequence number in multi-channel SAR data, polarization)': [(49, 50), '1B2', 0],
    'SAR channel code (0 = L, 1 = 5, 2 = C, 3 = X, 4 = KU and 5 = KA channel)': [(51, 52), '1B2', 0],
    'Transmitted polarization': [(53, 54), '1B2', 0],
    'Received polarization': [(55, 56), '1B2', 0],
    'PRF [mHz]': [(57, 60), '1B4', 0],
    'Scan ID for SCAN SAR mode ( 1 - 5 ) except Wide Observation mode = always 0': [(61, 64), '1B4', 0],
    'Onboard Range compressed flag (0 = no/1 = yes) = always 0': [(65, 66), '1B2', 0],
    'Pulse (chirp) type designator (0 = "LINEARbFMbCHIRPb",1 = "PHASEbMODULATORS") = always 0': [(67, 68), '1B2', 0],
    'Chirp length (nano-secs)': [(69, 72), '1B4', 0],
    'Chirp constant coefficient (Hz) (nominal value)': [(73, 76), '1B4', 0],
    'Chirp linear coefficient (Hz/usec) (nominal value)': [(77, 80), '1B4', 0],
    'Chirp quadratic coefficient (Hz/Wsec,)': [(81, 84), '1B4', 0],
    'Always blank(0) filled1': [(85, 92), '1B8', 0],
    'Receiver gain (dB) nominal value': [(93, 96), '1B4', 0],
    'Nought line flag (Effective line = 0, Invalid line (loss line) = 1)': [(97, 100), '1B4', 0],
    'Electronic antenna squint angle (millionths of degrees)= always blank (0) filled': [(101, 104), '1B4', 0],
    'Antenna mechanical elevation angle from nadir (millionths of degrees)= always blank (0) filled': [(105, 108), '1B4', 0],
    'Electronic antenna squint angle (millionths of degrees)': [(109, 112), '1B4', 0],
    'Mechanical antenna squint angle (millionths of degrees)= always blank (0) filled': [(113, 116), '1B4', 0],
    'Slant range to 1st data sample (m)': [(117, 120), '1B4', 0],
    'Data record window position (i.e.. sample delay) (nano-secs)': [(121, 124), '1B4', 0],
    'Always blank(0) filled2': [(125, 128), '1B4', 0],
    # PREFIX DATA-PLATFORM REFERENCE INFORMATION
    'Platform information': [(129, 192), '1B64', 0],
    # PREFIX DATA - SENSOR/FACILITY SPECIFIC, AUXILIARY DATA
    'Latitude of 1st pixel (millionths of degrees)': [(193, 196), '1B4', 0],
    'Latitude of middle-pixel (millionths of degrees)': [(197, 200), '1B4', 0],
    'Latitude of last pixel (millionths of degrees)': [(201, 204), '1B4', 0],
    'Longitude of 1st pixel (millionths of degrees)': [(205, 208), '1B4', 0],
    'Longitude of middle-pixel (millionths of degrees)': [(209, 212), '1B4', 0],
    'Longitude of last pixel (millionths of degrees)': [(213, 216), '1B4', 0],
    'Always blank (0) filled3': [(217, 284), '1B68', 0],
    'Counter of PALSAR frame': [(285, 288), '1B4', 0],
    'PALSAR auxiliary data': [(289, 388), '1B100', 0],
    'Always blank (0) filled4': [(389, 412), '1B24', 0],
    # SAR RAW SIGNAL DATA
    # 'Raw Data': [(-1, -1), '2B4', 0]  # [I, Q]
    'Raw Data': [(413, 420), '2f1', 0]  # [I, Q]
}

SarImageFileProcessedDataRecordALOSPALSAR = {  # level1.5
    'Record sequence number': [(1, 4), '1B4', 0],
    'l-st record sub-type code': [(5, 5), '1B1', 0],
    'Record type code': [(6, 6), '1B1', 0],
    '2-nd record sub-type code': [(7, 7), '1B1', 0],
    '3-rd record sub-type code': [(8, 8), '1B1', 0],
    'Length of this record': [(9, 12), '1B4', 0],
    # PREFIX DATA-GENERAL INFORMATION
    'SAR image data line number': [(13, 16), '1B4', 0],
    'SAR image data record index': [(17, 20), '1B4', 0],
    'Actual count of left-fill pixels': [(21, 24), '1B4', 0],
    'Actual count of data pixels': [(25, 28), '1B4', 0],
    'Actual count of right-fill pixels': [(29, 32), '1B4', 0],
    # PREFIX DATA-SENSOR/PROCESSING PARAMETERS
    'Sensor parameters update flag': [(33, 36), '1B4', 0],
    'Sensor acquisition year (UT)': [(37, 40), '1B4', 0],
    'Sensor acquisition day of year (UT)': [(41, 44), '1B4', 0],
    'Sensor acquisition milliseconds of day (UT)': [(45, 48), '1B4', 0],
    'SAR channel indicator (sequence number in multi-channel SAR data)': [(49, 50), '1B4', 0],
    'SAR channel code': [(51, 52), '1B4', 0],
    'Transmitted polarization': [(53, 54), '1B4', 0],
    'Received polarization': [(55, 56), '1B4', 0],
    'PRF (mHz)': [(57, 60), '1B4', 0],
    'Scan ID for SCAN SAR mode': [(61, 64), '1B4', 0],
    'Slant Range to 1st pixel (m)': [(65, 68), '1B4', 0],
    'Slant Range to mid-pixel (m)': [(69, 72), '1B4', 0],
    'Slant Range to last-pixel (m)': [(73, 76), '1B4', 0],
    'Doppler centroid value at 1st pixel (1/1,000 Hz)': [(77, 80), '1B4', 0],
    'Doppler centroid value at mid-pixel (1/1,000 Hz)': [(81, 84), '1B4', 0],
    'Doppler centroid value at last pixel (1/1,000 Hz)': [(85, 88), '1B4', 0],
    'Azimuth FM rate of 1st pixel (Hz/msec)': [(89, 92), '1B4', 0],
    'Azimuth FM rate of mid-pixel (Hz/msec)': [(93, 96), '1B4', 0],
    'Azimuth FM rate of last pixel (Hz/msec)': [(97, 100), '1B4', 0],
    'Look angle of nadir (millionths of degrees)': [(101, 104), '1B4', 0],
    'Azimuth squint angle (millionths of degrees)': [(105, 108), '1B4', 0],
    'Always blank (0) filled1': [(109, 128), '1B20', 0],
    # PREFIX DATA-GEOGRAPHIC REFERENCE INFO
    'Geographic ref. Parameter update flag': [(129, 132), '1B4', 0],
    'Latitude of 1st pixel (millionths of degrees)': [(133, 136), '1B4', 0],
    'Latitude of middle-pixel (millionths of degrees)': [(137, 140), '1B4', 0],
    'Latitude of last pixel (millionths of degrees)': [(141, 144), '1B4', 0],
    'Longitude of 1st pixel (millionths of degrees)': [(145, 148), '1B4', 0],
    'Longitude of middle-pixel (millionths of degrees)': [(149, 152), '1B4', 0],
    'Longitude of last pixel (millionths of degrees)': [(153, 156), '1B4', 0],
    'Northing of 1st pixel (m)': [(157, 160), '1B4', 0],
    'Always blank (0) filled2': [(161, 164), '1B4', 0],
    'Northing of last pixel (m)': [(165, 168), '1B4', 0],
    'Easting of 1st pixel (m)': [(169, 172), '1B4', 0],
    'Always blank (0) filled2': [(163, 176), '1B4', 0],
    'Easting of last pixel (m)': [(177, 180), '1B4', 0],
    'Line heading': [(181, 184), '1B4', 0],
    'Always blank (0) filled3': [(185, 192), '1B8', 0],
    # SAR PROCESSED DATA
    # 'Processed Data': [(13, 16), '2F2', 0],  # '2F2' for [real, imag], or '1C4' for real + 1j*imag
    'Processed Data': [(-1, -1), '2f1', 0],  # auto infer, (13, )
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


def read_alos_palsar_ldr_iip(filepath, verbose=False):
    r"""Read important imaging parameters from leader file

    Read important imaging parameters from leader file.

    Parameters
    ----------
    filepath : {str}
        Leader file path string.
    """

    logging.info("===In read_alos_palsar_ldr_iip...")

    LFIIPR = copy.deepcopy(LeaderFileImportantImagingParametersRecordALOS)

    offsLFIIPR = 0
    readrcd(filepath, decfmtfceos, LFIIPR, offset=offsLFIIPR, endian='>')
    if verbose:
        printrcd(LFIIPR)
    logging.info("---Done.")
    logging.info("===Out read_alos_palsar_ldr_iip.")
    return LFIIPR


def read_alos_palsar_raw(filepath, sl=1, el=-1, rmbp=False):
    r"""read ALOS PALSAR raw data

    read ALOS PALSAR raw data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly and do some post-process.


    Parameters
    ----------
    filepath : {string}
        ALOS PALSAR raw data file path string, ---> ``*.0__A``
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

    logging.info("===In read_alos_palsar_raw...")

    raise TypeError("Not opened yet!")
    logging.info("===Out read_alos_palsar_raw.")

    return S


def read_alos_palsar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read ALOS PALSAR SLC data

    read ALOS PALSAR SLC data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly.


    Parameters
    ----------
    filepath : {string}
        ALOS PALSAR raw data file path string, for ALOSPALSAR --> ``*.0__A``
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

    logging.info("===In read_alos_palsar_slc...")
    raise TypeError("Not opened yet!")

    logging.info("===Out read_alos_palsar_slc.")

    return S
