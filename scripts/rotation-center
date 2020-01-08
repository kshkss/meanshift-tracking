#!/usr/bin/python3

import os
import argparse
import numpy as np
import tifffile as tiff
from meanshift import meanshift

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--i0", help="file name for i0 iamge", default="i0.tif")
    parser.add_argument("--dark", help="file name for dark iamge", default="dark.tif")
    parser.add_argument("-n", "--num", help="use nth-file in the directory", default="0", type=int)
    parser.add_argument("base_sample", help="directory name for a base sample")
    parser.add_argument("opposite_sample", help="directory name for the next sample")
    args = parser.parse_args()

    base_dir = args.base_sample
    opposite_dir = args.opposite_sample
    i0_file = args.i0
    dark_file = args.dark
    k = atgs.num

    assert (os.path.exists(base_dir) and os.path.isdir(base_dir)), ("Input is expected as a directory: {}".format(base_dir))
    assert (os.path.exists(opposite_dir) and os.path.isdir(opposite_dir)), ("Input is expected as a directory: {}".format(opposite_dir))
    assert (os.path.exists(i0_file) ), ("File does not exist: {}".format(i0_file))
    assert (os.path.exists(dark_file) ), ("File does not exist: {}".format(dark_file))

    dark = tiff.imread(dark_file).astype(np.float32)
    i0 = np.log(tiff.imread(i0_file).astype(np.float32) - dark)

    files = os.listdir(base_dir)
    files.sort()
    base = np.log(tiff.imread(os.path.join(base_dir, files[k])).astype(np.float32) - dark)

    files = os.listdir(opposite_dir)
    files.sort()
    opposite = np.log(tiff.imread(os.path.join(opposite_dir, files[k])).astype(np.float32) - dark)

    height, width = base.shape
    w = int(width/10)
    h = int(height/10)

    base = base[4*h:5*h, 4*w:5*w].copy()
    opposite = np.fliplr(opposite).copy()

    maxv = np.max(base)
    minv = np.min(base)
    base = (255*(base - minv)/(maxv - minv)).astype(np.uint8)
    opposite = (255*(opposite - minv)/(maxv - minv)).astype(np.uint8)

    offset0 = (4*w, 4*h)
    #print(offset0)
    offset = meanshift(base, opposite, offset0)
    #print(offset)

    print( 0.5*(4*w + (width - offset[0])) )

main()

