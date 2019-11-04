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

def meanshift(orig, target, offset0):
    assert orig.ndim == 2 and orig.dtype == np.uint8, "Invalid function argument: input 2-dimensional array of uint8."
    assert target.ndim == 2 and target.dtype == np.uint8, "Invalid function argument: input 2-dimensional array of uint8."
    assert offset0[0] >= 0 and offset0[1] >= 0, "Invalid function argument:"
    assert offset0[0] < target.shape[1] and offset0[1] < target.shape[0], "Invalid function argument:"

    cdef uint8_t[:,:] orig_v = orig
    cdef uint8_t[:,:] tgt_v = target

    # compute histogram of orig
    cdef int embed[2]
    cdef double size[2]
    cdef double offset[2]
    for i in range(2):
        embed[i] = orig.shape[1-i]
        size[i] = orig.shape[1-i]
        offset[i] = 0
    freq0 = np.zeros(256, dtype=np.float64)
    cdef double[:] freq0_v = freq0
    histogram_gauss(&orig_v[0,0], &freq0_v[0], offset, size, embed)
    #print(freq0)

    # compute histogram of target
    for i in range(2):
        embed[i] = target.shape[1-i]
        size[i] = orig.shape[1-i]
        offset[i] = offset0[i]
    logger.debug( "({}, {})".format(offset[0], offset[1]) )
    freq = np.zeros(256, dtype=np.float64) + 1e-16
    cdef double[:] freq_v = freq
    histogram_gauss(&tgt_v[0,0], &freq_v[0], offset, size, embed)
    rho = np.sum( np.sqrt( freq0 * freq) )
    r = 1
    dr = 1

    weight = np.empty(freq.shape, dtype=np.float64)
    cdef double[:] weight_v = weight

    #cdef double offset_old[2]
    while(dr > 1e-2):
        rho00 = rho
        offset_old = (offset[0], offset[1])
        for i in range(100):
            # compute weight
            np.copyto(weight, np.sqrt(freq0 / freq, dtype=np.float64))
            #assert weight.dtype == np.float64, "weight is not 32-bit float"

            # compute mean shift
            meanshift_gauss(&tgt_v[0,0], &weight_v[0], offset, size, embed)

            # compute histogram of target
            np.copyto(freq, np.zeros(256, dtype=np.float64) + 1e-16)
            histogram_gauss(&tgt_v[0,0], &freq_v[0], offset, size, embed)

        rho = np.sum( np.sqrt( freq0 * freq) )
        r = (rho - rho00)/rho00
        dr = math.sqrt((offset[0] - offset_old[0])**2 + (offset[1] - offset_old[1])**2)
        logger.debug("{}, {}, {} {}".format(offset[0], offset[1], r, dr))

    return (offset[0], offset[1])

