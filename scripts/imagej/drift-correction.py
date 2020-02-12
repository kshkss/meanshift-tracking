import os
import shutil
import tempfile as tmp
import subprocess as sub
import logging
from ij import IJ
logger = logging.getLogger('drift_correction_in_Fiji')

img = IJ.getImage()
image_file = os.path.basename(img.getOriginalFileInfo().directory)
parent_dir = os.path.join(img.getOriginalFileInfo().directory, '..')
n_slices = img.getNSlices()
roi = img.getRoi()

logging.basicConfig(level=logging.INFO,
        filename=os.path.join(parent_dir, 'drift.log'),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

tmpdir = tmp.mkdtemp()
base_file = os.path.join(tmpdir, 'base.tif')
next_file = os.path.join(tmpdir, 'next.tif')

img.setSlice(1)
base_img = img.crop()
dx = []

logger.info('Start %s' % image_file)

for k in range(1, n_slices):
    img.setSlice(k+1)
    next_img = img.crop()
    IJ.saveAs(base_img, 'Tiff', base_file)
    IJ.saveAs(next_img, 'Tiff', next_file)

    pos = sub.check_output(('drift', base_file, next_file))
    #IJ.log(pos)
    logger.info(pos)
    dx.append(pos)

    base_img = next_img

shutil.rmtree(tmpdir)

img.setRoi(None)
img.setSlice(1)
img_c = img.crop()
stack = img_c.getStack()
x, y = 0.0, 0.0

for k, pos in enumerate(dx, 1):
    img.setSlice(k+1)
    img2 = img.crop()
    x += float(pos.split()[0])
    y += float(pos.split()[1])

    option = "x=%f y=%f interpolation=Bicubic" % (-x, -y)
    IJ.run(img2, "Translate...", option)
    stack.addSlice(img2.getProcessor())

img_c.setStack(stack)
img_c.show()
img.setRoi(roi)

