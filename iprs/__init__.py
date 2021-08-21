from __future__ import division, print_function, absolute_import
# from __future__ import absolute_import

# Utils
from . import utils
from .utils.const import *
from .utils.convert import str2list, str2num
from .utils.io import savemat, loadmat
from .utils.file import listxfile, pathjoin, fileparts


from .utils.image import imread, imsave, imadjust, imadjustlog, histeq, imresize

from .utils.transform import scale, db20

from .utils.typevalue import peakvalue

from .utils.geometry import linekb, isinpolygons, polygon


from .misc.baseops import dmka
from .misc.mathops import nextpow2, prevpow2, ebeo, real2imag, imag2real
from .misc.mapping_operation import mapping
from .misc.arrayops import cut
from .misc.data import sarread, sarstore, load_data, format_data
from .misc.observation import sparse_observation, gen_sample_mask, process_sarplat
from .misc.visual import show_targets, show_amplitude_phase, show_response, \
    showReImAmplitudePhase, sarshow, show_image, show_sarimage, show_sarimage3d, imshow

from .misc.sensing import bernoulli, gaussian
from .misc.dictionary import dctdic
from .misc.solvers import OMP
from .misc.entropy import natural_entropy, shannon_entropy
from .misc.plots import cplot
from .misc.sampling import dnsampling, upsampling
from .misc.image_converter import toimage

# evaluation
from .import evaluation
from .evaluation.error import ampphaerror, mse
from .evaluation.tbr import tbr1, tbr2
from .evaluation.snr import snr, psnr

from .evaluation.ent import ent

from .evaluation.tbed import tbed

from .evaluation.mlw import mlw


# Digital signal processing
from . import dsp
from .dsp.noise import imnoise, awgn, wgn, matnoise
from .dsp.normalsignals import hs, ihs, rect, chirp, pulse, pulse2
from .dsp.fft import padfft, fft, ifft, fftfreq, fft2, ifft2, fftx, ffty, ifftx, iffty
from .dsp.convolution import conv1, fftconv1, cutfftconv1
from .dsp.correlation import corr1, fftcorr1, cutfftcorr1, xcorr
from .dsp.interpolation import sinc, sinc_table, sinc_interp, interp

# SAR sensor platform
from . import sarcfg
from .sarcfg.sensors import *
from .sarcfg.acquis import *
from .sarcfg.selection import *
from .sarcfg.sarplat import *

# Sharing technology
from .sharing.chirp_tranrecv import chirp_tran, chirp_recv
from .sharing.matched_filter import chirp_mf_td, chirp_mf_fd
from .sharing.pulse_compression import mfpc_throwaway
from .sharing.equivalent_velocity_estimation import eve_npts_fit
from .sharing.doppler_centroid_estimation import bdce_sf, bdce_api, adce_wda, abdce_wda, dce_wda, fullfadc
from .sharing.doppler_rate_estimation import dre_geo
from .sharing.range_azimuth_beamwidth_footprint import compute_range_beamwidth, azimuth_beamwidth, antenna_pattern_azimuth, ar_footprint, cr_footprint, azimuth_footprint
from .sharing.slant_ground_range import slantr2groundr, slantt2groundr, groundr2slantr, groundr2slantt, min_slant_range, min_slant_range_with_migration

from . import modeling
from .modeling.phase_error import pe_identity, pe_polynomial

# simulation
from . import simulation
from .simulation.geometry import rectangle, disc
from .simulation.gentargets import gpts, grectangle, gdisc, img2tgs
from .simulation.sarsim import tgs2rawdata, img2rawdata, img2echo
from .simulation.sardata import *
from .simulation.sarsignal import sar_tran, sar_recv
from .simulation.sar_impulse_response import sarir
from .simulation.model import sarmodel, load_sarmodel, save_sarmodel, sarmodel_genecho


# SAR imaging tools
from . import imaging
from .imaging.range_dopplor import rda0, rda_adv, rda, rda_ls, rda_ss
from .imaging.chirp_scaling import csa, csa_adv
from .imaging.omega_k import wka
from .imaging.share import zeros_padding, range_matched_filtering, \
    range_compression, second_range_compression2, \
    range_migration_factor, rcmc_sinc, rcmc_interp, genRefPhase
from .imaging.cssar import cs1d_sar, cs2d_sar
from .imaging.regularizationsar import regular_sar
from .imaging.blind import blindsar_svd

from . import autofocus
from .autofocus.map_drift import mda_sm
from .autofocus.phase_gradient import pgaf_sm, pgaf_sm_1iter, spotlight_width
from .autofocus.minimum_entropy import entropyaf


from .calibration.sar_preprocess import iq_correction
from .calibration.multilook_process import multilook_spatial
from .calibration.radar_cross_section import intesity, power, sigma_naught, gamma_naught, beta_naught

from . import products
from .products.utils import getnumber, splitfmt
from .products.record import readrcd, readrcd1item, printrcd
from .products.vga import vga_gain_compensation
from .products.ceos import decfmtfceos, read_ceos_sar_raw, read_ceos_sar_slc, SarDataFileFileDescriptorRecordCEOS, SarDataFileSignalDataRecordCEOS
from .products.ers import read_ers_sar_ldr_iip, read_ers_sar_raw, read_ers_sar_slc, LeaderFileImportantImagingParametersRecordERS, SarDataFileFileDescriptorRecordERS, SarDataFileSignalDataRecordERS, SarDataFileProcessedDataRecordERS
from .products.radarsat import read_radarsat_sar_raw, SarDataFileFileDescriptorRecordRADARSAT, SarDataFileSignalDataRecordRADARSAT
from .products.uavsar import read_uavsar_mlc
from .products.alos import read_alos_palsar_ldr_iip, read_alos_palsar_raw, read_alos_palsar_slc, LeaderFileImportantImagingParametersRecordALOS, SarDataFileFileDescriptorRecordALOSPALSAR, SarDataFileSignalDataRecordALOSPALSAR, SarImageFileFileDescriptorRecordALOSPALSAR, SarImageFileSignalDataRecordALOSPALSAR, SarImageFileProcessedDataRecordALOSPALSAR
