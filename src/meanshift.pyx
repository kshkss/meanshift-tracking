from meanshift_version import *
from libc.stdint cimport uint8_t

cdef extern from "histogram.h":
    cdef void histogram_epanechnikov(uint8_t *vs, double *freq, double *offset, double *size, int *embed)
    cdef void histogram_gauss(uint8_t *vs, double *freq, double *offset, double *size, int *embed)
    cdef void meanshift_epanechnikov(uint8_t *vs, double *freq, double *offset, double *size, int *embed)
    cdef void meanshift_gauss(uint8_t *vs, double *freq, double *offset, double *size, int *embed)

import numpy as np
import os
import math
import logging

logger = logging.getLogger(__name__)

class Point2d:
    x = 0
    y = 0
    def __init__(self, *, x, y):
        self.x = x
        self.y = y

def histogram(image, patch_size, offset0):
    freq = np.zeros(256, dtype=np.float64)
    cdef uint8_t[:,:] image_v = image
    cdef double[:] freq_v = freq

    cdef int embed[2]
    cdef double size[2]
    cdef double offset[2]
    for i in range(2):
        embed[i] = image.shape[1-i]
        size[i] = patch_size[1-i]
    offset[0] = offset0.x
    offset[1] = offset0.y

    histogram_gauss(&image_v[0,0], &freq_v[0], offset, size, embed)
    return freq

def mean(image, weight, patch_size, offset0):
    cdef uint8_t[:,:] image_v = image
    cdef double[:] weight_v = weight

    cdef int embed[2]
    cdef double size[2]
    cdef double offset[2]
    for i in range(2):
        embed[i] = image.shape[1-i]
        size[i] = patch_size[1-i]
    offset[0] = offset0.x
    offset[1] = offset0.y

    meanshift_gauss(&image_v[0,0], &weight_v[0], offset, size, embed)
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

