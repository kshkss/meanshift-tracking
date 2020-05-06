import os
import logging
from ctypes import *
import numpy as np
import numpy.ctypeslib as npct

logger = logging.getLogger(__name__)

if os.name == 'posix':
    libcd = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "libmeanshift.so"))
elif os.name == 'nt':
    libcd = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "Meanshift.dll"))
else:
    logger.error("Unsupported OS.")
    raise Exception

freq = npct.ndpointer(dtype=np.float64, ndim=1, flags='CONTIGUOUS')
image = npct.ndpointer(dtype=np.uint8, ndim=2, flags='CONTIGUOUS')
dims = npct.ndpointer(dtype=np.uint8, ndim=2, flags='CONTIGUOUS')
offsets = npct.ndpointer(dtype=np.uint8, ndim=2, flags='CONTIGUOUS')
pitches = npct.ndpointer(dtype=np.uint32, ndim=2, flags='CONTIGUOUS')
args = [image, freq, offsets, dims, pitches]

libcd.histogram_epanechnikov.restype = None
libcd.histogram_epanechnikov.argtypes = args

libcd.histogram_gauss.restype = None
libcd.histogram_gauss.argtypes = args

libcd.meanshift_epanechnikov.restype = None
libcd.meanshift_epanechnikov.argtypes = args

libcd.meanshift_gauss.restype = None
libcd.meanshift_gauss.argtypes = args

class Point2d:
    x = 0
    y = 0
    def __init__(self, *, x, y):
        self.x = x
        self.y = y

def histogram(image, patch_size, offset0):
    assert image.ndim == 2
    freq = np.zeros(256, dtype=np.float64)

    embed = np.array([image.shape[1], image.shape[0]])
    size = np.array([patch_size[1], patch_size[0]])
    offset = np.array([offset0.x, offset0.y])

    histogram_gauss(image, freq, offset, size, embed)
    return freq

def mean(image, weight, patch_size, offset0):
    assert image.ndim == 2
    assert weight.ndim == 1

    embed = np.array([image.shape[1], image.shape[0]])
    size = np.array([patch_size[1], patch_size[0]])
    offset = np.array([offset0.x, offset0.y])

    meanshift_gauss(image, weight, offset, size, embed)
    return Point2d(x = offset[0], y = offset[1])

def meanshift(orig, target, offset):
    assert orig.ndim == 2 and orig.dtype == np.uint8, "Invalid function argument: input 2-dimensional array of uint8."
    assert target.ndim == 2 and target.dtype == np.uint8, "Invalid function argument: input 2-dimensional array of uint8."
    assert offset.x >= 0 and offset.y >= 0, "Invalid function argument:"
    assert offset.x < target.shape[1] and offset.y < target.shape[0], "Invalid function argument:"
    logger.debug( "({}, {})".format(offset.x, offset.y) )
    patch_size = orig.shape

    # compute histogram of orig
    freq0 = histogram(orig, patch_size, Point2d(x = 0, y = 0))

    # compute histogram of target
    freq = histogram(target, patch_size, offset) + 1e-16

    rho = np.sum( np.sqrt( freq0 * freq) )
    r = 1
    dr = 1
    while(dr > 1e-2):
        rho00 = rho
        offset_old = offset
        for i in range(100):
            # compute weight
            weight = np.sqrt(freq0 / freq)
            assert weight.dtype == np.float64, "weight is not 32-bit float"

            # compute mean shift
            offset = mean(target, weight, patch_size, offset)

            # compute histogram of target
            freq = histogram(target, patch_size, offset) + 1e-16

        rho = np.sum( np.sqrt( freq0 * freq) )
        r = (rho - rho00)/rho00
        dr = math.sqrt((offset.x - offset_old.x)**2 + (offset.y - offset_old.y)**2)
        logger.debug("{}, {}, {} {}".format(offset.x, offset.y, r, dr))
    return offset

