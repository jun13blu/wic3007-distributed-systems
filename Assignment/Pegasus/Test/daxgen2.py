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

remotetblB = os.path.join(os.getcwd(), "output/remoteB.tbl")
remotetblR = os.path.join(os.getcwd(), "output/remoteR.tbl")
remotetblIR = os.path.join(os.getcwd(), "output/remoteIR.tbl")
f = open(remotetblB, 'r')
archive_file_listB = re.findall(r'(poss2ukstu_blue_.*\.fits\.gz)', f.read())
f = open(remotetblR, 'r')
archive_file_listR = re.findall(r'(poss2ukstu_red_.*\.fits\.gz)', f.read())
f = open(remotetblIR, 'r')
archive_file_listIR = re.findall(r'(poss2ukstu_ir_.*\.fits\.gz)', f.read())

# Create an abstract dag
dax = ADAG("pleiades")

# Add some workflow level metadata
dax.metadata("creator", "%s@%s" % (USER, os.uname()[1]))
dax.metadata("created", time.ctime())

mArchiveExecB = Job("mArchiveExec")
mArchiveExecB.addArguments("remoteB.tbl")
mArchiveExecB.uses("remoteB.tbl", link=Link.INPUT, transfer=True, register=True)
for f in archive_file_listB: mArchiveExecB.uses(f, link=Link.OUTPUT, register=True, transfer=True)
dax.addJob(mArchiveExecB)

mArchiveExecR = Job("mArchiveExec")
mArchiveExecR.addArguments("remoteR.tbl")
mArchiveExecR.uses("remoteR.tbl", link=Link.INPUT, transfer=True, register=True)
for f in archive_file_listR: mArchiveExecR.uses(f, link=Link.OUTPUT, register=True, transfer=True)
dax.addJob(mArchiveExecR)

mArchiveExecIR = Job("mArchiveExec")
mArchiveExecIR.addArguments("remoteIR.tbl")
mArchiveExecIR.uses("remoteIR.tbl", link=Link.INPUT, transfer=True, register=True)
for f in archive_file_listIR: mArchiveExecIR.uses(f, link=Link.OUTPUT, register=True, transfer=True)
dax.addJob(mArchiveExecIR)

mImgtbl_raw_input = "."
mImgtbl_raw_outputB = "rimagesB.tbl"
mImgtbl_raw_outputR = "rimagesR.tbl"
mImgtbl_raw_outputIR = "rimagesIR.tbl"

mImgtblB = Job("mImgtbl")
mImgtblB.addArguments(mImgtbl_raw_input, mImgtbl_raw_outputB)
for f in archive_file_listB:	mImgtblB.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtblB.uses(mImgtbl_raw_outputB, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mImgtblB)

mImgtblR = Job("mImgtbl")
mImgtblR.addArguments(mImgtbl_raw_input, mImgtbl_raw_outputR)
for f in archive_file_listR:	mImgtblR.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtblR.uses(mImgtbl_raw_outputR, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mImgtblR)

mImgtblIR = Job("mImgtbl")
mImgtblIR.addArguments(mImgtbl_raw_input, mImgtbl_raw_outputIR)
for f in archive_file_listIR:	mImgtblIR.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtblIR.uses(mImgtbl_raw_outputIR, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mImgtblIR)

header_template = "pleiades.hdr"
mProjExec_output = "."

new_file_namesB = [("hdu0_" + f + ".fits") for f in archive_file_listB]
new_file_names_areaB = [("hdu0_" + f + "_area.fits") for f in archive_file_listB]
stats_tableB = "statsB.tbl"

new_file_namesR = [("hdu0_" + f + ".fits") for f in archive_file_listR]
new_file_names_areaR = [("hdu0_" + f + "_area.fits") for f in archive_file_listR]
stats_tableR = "statsR.tbl"

new_file_namesIR = [("hdu0_" + f + ".fits") for f in archive_file_listIR]
new_file_names_areaIR = [("hdu0_" + f + "_area.fits") for f in archive_file_listIR]
stats_tableIR = "statsIR.tbl"

mProjExecB = Job("mProjExec")
mProjExecB.addArguments("-p", mImgtbl_raw_input, mImgtbl_raw_outputB, header_template, mProjExec_output, stats_tableB)
for f in archive_file_listB:	mProjExecB.uses(f, link=Link.INPUT, transfer=True, register=True)
mProjExecB.uses(mImgtbl_raw_outputB, link=Link.INPUT, transfer=True, register=True)
mProjExecB.uses(header_template, link=Link.INPUT, transfer=True, register=True)
for f in new_file_namesB:	mProjExecB.uses(f, link=Link.OUTPUT, transfer=True, register=True)
for f in new_file_names_areaB:	mProjExecB.uses(f, link=Link.OUTPUT, transfer=True, register=True)
mProjExecB.uses(stats_tableB, link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mProjExecB)

mProjExecR = Job("mProjExec")
mProjExecR.addArguments("-p", mImgtbl_raw_input, mImgtbl_raw_outputR, header_template, mProjExec_output, stats_tableR)
for f in archive_file_listR:	mProjExecR.uses(f, link=Link.INPUT, transfer=True, register=True)
mProjExecR.uses(mImgtbl_raw_outputR, link=Link.INPUT, transfer=True, register=True)
mProjExecR.uses(header_template, link=Link.INPUT, transfer=True, register=True)
for f in new_file_namesR:	mProjExecR.uses(f, link=Link.OUTPUT, transfer=True, register=True)
for f in new_file_names_areaR:	mProjExecR.uses(f, link=Link.OUTPUT, transfer=True, register=True)
mProjExecR.uses(stats_tableR, link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mProjExecR)

mProjExecIR = Job("mProjExec")
mProjExecIR.addArguments("-p", mImgtbl_raw_input, mImgtbl_raw_outputIR, header_template, mProjExec_output, stats_tableIR)
for f in archive_file_listIR:	mProjExecIR.uses(f, link=Link.INPUT, transfer=True, register=True)
mProjExecIR.uses(mImgtbl_raw_outputIR, link=Link.INPUT, transfer=True, register=True)
mProjExecIR.uses(header_template, link=Link.INPUT, transfer=True, register=True)
for f in new_file_namesIR:	mProjExecIR.uses(f, link=Link.OUTPUT, transfer=True, register=True)
for f in new_file_names_areaIR:	mProjExecIR.uses(f, link=Link.OUTPUT, transfer=True, register=True)
mProjExecIR.uses(stats_tableIR, link=Link.OUTPUT, transfer=False, register=True)
dax.addJob(mProjExecIR)

mImgtbl_outputB = "pimagesB.tbl"
mImgtbl_outputR = "pimagesR.tbl"
mImgtbl_outputIR = "pimagesIR.tbl"

mImgtbl2B = Job("mImgtbl")
mImgtbl2B.addArguments(mProjExec_output, mImgtbl_outputB)
for f in new_file_namesB:	mImgtbl2B.uses(f, link=Link.INPUT, transfer=True, register=True)
for f in new_file_names_areaB: mImgtbl2B.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtbl2B.uses(mImgtbl_outputB, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mImgtbl2B)

mImgtbl2R = Job("mImgtbl")
mImgtbl2R.addArguments(mProjExec_output, mImgtbl_outputR)
for f in new_file_namesR:	mImgtbl2R.uses(f, link=Link.INPUT, transfer=True, register=True)
for f in new_file_names_areaR: mImgtbl2R.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtbl2R.uses(mImgtbl_outputR, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mImgtbl2R)

mImgtbl2IR = Job("mImgtbl")
mImgtbl2IR.addArguments(mProjExec_output, mImgtbl_outputIR)
for f in new_file_namesIR:	mImgtbl2IR.uses(f, link=Link.INPUT, transfer=True, register=True)
for f in new_file_names_areaIR: mImgtbl2IR.uses(f, link=Link.INPUT, transfer=True, register=True)
mImgtbl2IR.uses(mImgtbl_outputIR, link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mImgtbl2IR)

mAddB = Job("mAdd")
mAddB.addArguments("-p", ".", mImgtbl_outputB, header_template, "DSS2B.fits")
mAddB.uses(mImgtbl_outputB, link=Link.INPUT, transfer=True, register=True)
mAddB.uses(header_template, link=Link.INPUT, transfer=True, register=True)
for f in new_file_namesB: mAddB.uses(f, link=Link.INPUT, register=True, transfer=True)
for f in new_file_names_areaB: mAddB.uses(f, link=Link.INPUT, transfer=True, register=True)
mAddB.uses("DSS2B.fits", link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mAddB)

mAddR = Job("mAdd")
mAddR.addArguments("-p", ".", mImgtbl_outputR, header_template, "DSS2R.fits")
mAddR.uses(mImgtbl_outputR, link=Link.INPUT, transfer=True, register=True)
mAddR.uses(header_template, link=Link.INPUT, transfer=True, register=True)
for f in new_file_namesR: mAddR.uses(f, link=Link.INPUT, register=True, transfer=True)
for f in new_file_names_areaR: mAddR.uses(f, link=Link.INPUT, transfer=True, register=True)
mAddR.uses("DSS2R.fits", link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mAddR)

mAddIR = Job("mAdd")
mAddIR.addArguments("-p", ".", mImgtbl_outputIR, header_template, "DSS2IR.fits")
mAddIR.uses(mImgtbl_outputIR, link=Link.INPUT, transfer=True, register=True)
mAddIR.uses(header_template, link=Link.INPUT, transfer=True, register=True)
for f in new_file_namesIR: mAddIR.uses(f, link=Link.INPUT, register=True, transfer=True)
for f in new_file_names_areaIR: mAddIR.uses(f, link=Link.INPUT, transfer=True, register=True)
mAddIR.uses("DSS2IR.fits", link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mAddIR)

mJPEG = Job("mJPEG")
mJPEG.addArguments("-blue", "DSS2B.fits", "-ls", "99.999%", "gaussian-log", "-green", "DSS2R.fits", "-ls", "99.999%", "gaussian-log", "-red", "DSS2IR.fits", "-ls", "99.999%", "gaussian-log", "-out", "DSS2_BRIR.jpg")
mJPEG.uses("DSS2B.fits", link=Link.INPUT, transfer=True, register=True)
mJPEG.uses("DSS2R.fits", link=Link.INPUT, transfer=True, register=True)
mJPEG.uses("DSS2IR.fits", link=Link.INPUT, transfer=True, register=True)
mJPEG.uses("DSS2_BRIR.jpg", link=Link.OUTPUT, transfer=True, register=False)
dax.addJob(mJPEG)

dax.depends(parent=mArchiveExecB, child=mImgtblB)
dax.depends(parent=mArchiveExecR, child=mImgtblR)
dax.depends(parent=mArchiveExecIR, child=mImgtblIR)
dax.depends(parent=mImgtblB, child=mProjExecB)
dax.depends(parent=mImgtblR, child=mProjExecR)
dax.depends(parent=mImgtblIR, child=mProjExecIR)
dax.depends(parent=mProjExecB, child=mImgtbl2B)
dax.depends(parent=mProjExecR, child=mImgtbl2R)
dax.depends(parent=mProjExecIR, child=mImgtbl2IR)
dax.depends(parent=mImgtbl2B, child=mAddB)
dax.depends(parent=mImgtbl2R, child=mAddR)
dax.depends(parent=mImgtbl2IR, child=mAddIR)
dax.depends(parent=mAddB, child=mJPEG)
dax.depends(parent=mAddR, child=mJPEG)
dax.depends(parent=mAddIR, child=mJPEG)

f = open("pleiades2.dax", "w")
dax.writeXML(f)
f.close()
print "Generated pleiades2.dax"