import os
import os.path
from os import listdir
from os.path import isfile, join
import pwd
import sys
import time
import re

from Pegasus.DAX3 import *

USER = pwd.getpwuid(os.getuid())[0]

# Generate the mDiffExec file names
diffs_tbl = os.path.join(os.getcwd(), "output/diffs.tbl")
f = open(diffs_tbl, 'r')
diff_file_list = re.findall(r'(diff\..*\.fits)', f.read())
new_diff_file_list = [f[:-5] + "_area.fits" for f in diff_file_list]

onlyfiles = [f for f in listdir("input/rawdir") if isfile(join("input/rawdir", f))]
new_file_names = [("hdu0_" + f) for f in onlyfiles]
new_file_names_area = [("hdu0_" + f[:-5] + "_area.fits") for f in onlyfiles]

# Create an abstract dag
dax = ADAG("m101_part2")

# Add some workflow level metadata
dax.metadata("creator", "%s@%s" % (USER, os.uname()[1]))
dax.metadata("created", time.ctime())

# Execution continues
mDiffExec = Job("mDiffExec")
mDiffExec.addArguments("-p", ".", "diffs.tbl", "template.hdr", ".")
for f in new_file_names: mDiffExec.uses(f, link=Link.INPUT, register=True, transfer=True)
for f in new_file_names_area: mDiffExec.uses(f, link=Link.INPUT, transfer=True, register=True)
mDiffExec.uses("diffs.tbl", link=Link.INPUT, transfer=True, register=True)
mDiffExec.uses("template.hdr", link=Link.INPUT, transfer=True, register=True)
for f in diff_file_list: mDiffExec.uses(f, link=Link.OUTPUT, register=True, transfer=False)
for f in new_diff_file_list: mDiffExec.uses(f, link=Link.OUTPUT, register=True, transfer=False)
dax.addJob(mDiffExec)

mFitExec = Job("mFitExec")
mFitExec.addArguments("diffs.tbl", "fits.tbl", ".")
mFitExec.uses("diffs.tbl", link=Link.INPUT, transfer=True, register=True)
for f in diff_file_list: mFitExec.uses(f, link=Link.INPUT, register=True, transfer=True)
mFitExec.uses("fits.tbl", link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mFitExec)

mBgModel = Job("mBgModel")
mBgModel.addArguments("images.tbl", "fits.tbl", "corrections.tbl")
mBgModel.uses("images.tbl", link=Link.INPUT, transfer=True, register=True)
mBgModel.uses("fits.tbl", link=Link.INPUT, transfer=True, register=True)
mBgModel.uses("corrections.tbl", link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mBgModel)

# Replaces mBgExec
jobs = []
for a,b in zip(new_file_names, new_file_names_area):
	mBackground = Job("mBackground")
	mBackground.uses(a, link=Link.INPUT, transfer=True, register=True)
	mBackground.uses(b, link=Link.INPUT, transfer=True, register=True)
	mBackground.uses("out_" + a, link=Link.OUTPUT, transfer=False, register=True)
	mBackground.uses("out_" + b, link=Link.OUTPUT, transfer=False, register=True)
	mBackground.uses("corrections.tbl", link=Link.INPUT, transfer=True, register=True)
	mBackground.uses("images.tbl", link=Link.INPUT, transfer=True, register=True)
	mBackground.addArguments("-t", a, "out_" + a, "images.tbl", "corrections.tbl")
	jobs.append(mBackground)
	dax.addJob(mBackground)

mImgtbl = Job("mImgtbl")
mImgtbl.addArguments(".", "updated_images.tbl")
for f in new_file_names: mImgtbl.uses("out_" + f, link=Link.INPUT, register=True, transfer=True)
for f in new_file_names_area: mImgtbl.uses("out_" + f, link=Link.INPUT, transfer=True, register=True)
mImgtbl.uses("updated_images.tbl", link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mImgtbl)

mAdd = Job("mAdd")
mAdd.addArguments("-p", ".", "updated_images.tbl", "template.hdr", "m101_mosaic.fits")
mAdd.uses("updated_images.tbl", link=Link.INPUT, transfer=True, register=True)
mAdd.uses("template.hdr", link=Link.INPUT, transfer=True, register=True)
for f in new_file_names: mAdd.uses("out_" + f, link=Link.INPUT, register=True, transfer=True)
for f in new_file_names_area: mAdd.uses("out_" + f, link=Link.INPUT, transfer=True, register=True)
mAdd.uses("m101_mosaic.fits", link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mAdd)

mJPEG = Job("mJPEG")
mJPEG.addArguments("-gray", "m101_mosaic.fits", "0s", "max", "gaussian-log", "-out", "m101_mosaic.jpg")
mJPEG.uses("m101_mosaic.fits", link=Link.INPUT, transfer=True, register=True)
mJPEG.uses("m101_mosaic.jpg", link=Link.OUTPUT, transfer=True, register=False)
dax.addJob(mJPEG)

dax.depends(parent=mDiffExec, child=mFitExec)
dax.depends(parent=mFitExec, child=mBgModel)
for j in jobs:
	dax.depends(parent=mBgModel, child=j)
	dax.depends(parent=j, child=mImgtbl)
dax.depends(parent=mImgtbl, child=mAdd)
dax.depends(parent=mAdd, child=mJPEG)

f = open("part2.dax", "w")
dax.writeXML(f)
f.close()
print "Generated part2.dax"

# End of m101 part 2