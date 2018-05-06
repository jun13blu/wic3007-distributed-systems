import os
from os import listdir
from os.path import isfile, join
import pwd
import sys
import time
from Pegasus.DAX3 import *

USER = pwd.getpwuid(os.getuid())[0]

# Register all the input files (INIT)
onlyfiles = [f for f in listdir("input/rawdir") if isfile(join("input/rawdir", f))]
fullpath = [os.path.join(os.getcwd(), "input/rawdir/" + f) for f in onlyfiles]
with open('rc.txt', 'w+') as f:
	for a,b in zip(onlyfiles, fullpath):
		f.write(a + ' file://' + b + ' site="local"\n')
	f.write("template.hdr file://"+os.path.join(os.getcwd(),"input/template.hdr")+ ' site="local"\n')

# Create an abstract dag
dax = ADAG("m101_part1")

# Add some workflow level metadata
dax.metadata("creator", "%s@%s" % (USER, os.uname()[1]))
dax.metadata("created", time.ctime())

# Job scheduling start
mImgtbl_rawdir_input = "."
mImgtbl_rawdir_output = "images-rawdir.tbl"

mImgtbl = Job("mImgtbl")
mImgtbl.addArguments(mImgtbl_rawdir_input, mImgtbl_rawdir_output)
for f in onlyfiles:	mImgtbl.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtbl.uses(mImgtbl_rawdir_output, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mImgtbl)

new_file_names = [("hdu0_" + f) for f in onlyfiles]
new_file_names_area = [("hdu0_" + f[:-5] + "_area.fits") for f in onlyfiles]

header_template = "template.hdr"
mProjExec_output = "."
stats_table = "stats.tbl"

# STEP 2
mProjExec = Job("mProjExec")
mProjExec.addArguments("-p", mImgtbl_rawdir_input, mImgtbl_rawdir_output, header_template, mProjExec_output, stats_table)
for f in onlyfiles:	mProjExec.uses(f, link=Link.INPUT, transfer=True, register=True)
mProjExec.uses(mImgtbl_rawdir_output, link=Link.INPUT, transfer=True, register=True)
mProjExec.uses(header_template, link=Link.INPUT, transfer=True, register=True)
for f in new_file_names:	mProjExec.uses(f, link=Link.OUTPUT, transfer=True, register=True)
for f in new_file_names_area: mProjExec.uses(f, link=Link.OUTPUT, transfer=True, register=True)
mProjExec.uses(stats_table, link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mProjExec)

mImgtbl_output = "images.tbl"
mImgtbl2 = Job("mImgtbl")
mImgtbl2.addArguments(mProjExec_output, mImgtbl_output)
for f in new_file_names:	mImgtbl2.uses(f, link=Link.INPUT, transfer=True, register=True)
for f in new_file_names_area: mImgtbl2.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtbl2.uses(mImgtbl_output, link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mImgtbl2)

diffs_tbl = "diffs.tbl"
mOverlaps = Job("mOverlaps")
mOverlaps.addArguments(mImgtbl_output, diffs_tbl)
mOverlaps.uses(mImgtbl_output, link=Link.INPUT, transfer=True, register=True)
mOverlaps.uses(diffs_tbl, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mOverlaps)

dax.depends(parent=mImgtbl, child=mProjExec)
dax.depends(parent=mProjExec, child=mImgtbl2)
dax.depends(parent=mImgtbl2, child=mOverlaps)

f = open("part1.dax", "w")
dax.writeXML(f)
f.close()
print "Generated part1.dax"

# End of m101 part one