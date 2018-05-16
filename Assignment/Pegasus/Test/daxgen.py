import os
from os import listdir
from os.path import isfile, join
import pwd
import sys
import time
from Pegasus.DAX3 import *

USER = pwd.getpwuid(os.getuid())[0]

with open('rc.txt', 'w+') as f:
	f.write("pleiades.hdr file://"+os.path.join(os.getcwd(),"input/pleiades.hdr")+ ' site="local"\n')

# Create an abstract dag
dax = ADAG("pleiades")

# Add some workflow level metadata
dax.metadata("creator", "%s@%s" % (USER, os.uname()[1]))
dax.metadata("created", time.ctime())

# Job scheduling start
mArchiveListB = Job("mArchiveList")
mArchiveListB.addArguments("dss", "DSS2B", "\"56.5 23.75\"", "3", "3", "remoteB.tbl")
mArchiveListB.uses("remoteB.tbl", link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mArchiveListB)

mArchiveListR = Job("mArchiveList")
mArchiveListR.addArguments("dss", "DSS2R", "\"56.5 23.75\"", "3", "3", "remoteR.tbl")
mArchiveListR.uses("remoteR.tbl", link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mArchiveListR)

mArchiveListIR = Job("mArchiveList")
mArchiveListIR.addArguments("dss", "DSS2IR", "\"56.5 23.75\"", "3", "3", "remoteIR.tbl")
mArchiveListIR.uses("remoteIR.tbl", link=Link.OUTPUT, transfer=True, register=True)
dax.addJob(mArchiveListIR)

f = open("pleiades.dax", "w")
dax.writeXML(f)
f.close()
print "Generated pleiades.dax"

# End of pleiades part one