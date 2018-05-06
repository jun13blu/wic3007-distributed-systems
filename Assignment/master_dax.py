import os
import os.path
from os import listdir
from os.path import isfile, join
import pwd
import sys
import time
import re
from Pegasus.DAX3 import *

# Download and extract file
os.system("curl http://montage.ipac.caltech.edu/docs/m101Example/tutorial-initial.tar.gz -o gg.zip")
os.system("tar -xvf gg.zip")

# Create directories and file preparation
os.system("mkdir m101pegasus")
os.system("cd m101pegasus && mkdir input")
os.system("cp -r ../m101/input/rawdir .")
os.system("cp ../m101/input/template.hdr .")

# Write transformation catalogue
def tc(dp):
	tmp = '''
	tr {} {{
		site condorpool {{
			pfn "/usr/bin/{}"
			arch "x86_64"
			os "LINUX"
			type "INSTALLED"
		}}
	}}	
	'''.format(dp,dp)
	return tmp

dependency = ["mImgTbl","mProjExec","mAdd","mBgModel","mFitExec","mJPEG","mBackground","mDiffExec"]

with open('tc.txt', 'w+') as f:
	for d in dependency:
		f.write(tc(d))

# Write Pegasus Properties 
def properties():
	tmp = '''
	# This tells Pegasus where to find the Site Catalog
	pegasus.catalog.site.file=sites.xml

	# This tells Pegasus where to find the Replica Catalog
	pegasus.catalog.replica=File
	pegasus.catalog.replica.file=rc.txt

	# This tells Pegasus where to find the Transformation Catalog
	pegasus.catalog.transformation=Text
	pegasus.catalog.transformation.file=tc.txt

	# Use condor to transfer workflow data
	pegasus.data.configuration=condorio

	# This is the name of the application for analytics
	pegasus.metrics.app=pegasus-tutorial
	'''
	return tmp

with open('pegasus.properties','w+') as f:
	f.write(properties)

# Write sites.xml
def sites():
	tmp = '''
	<?xml version="1.0" encoding="UTF-8"?>
	<sitecatalog xmlns="http://pegasus.isi.edu/schema/sitecatalog" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	    xsi:schemaLocation="http://pegasus.isi.edu/schema/sitecatalog http://pegasus.isi.edu/schema/sc-4.1.xsd" version="4.1">

	    <!-- The local site contains information about the submit host -->
	    <site handle="local" arch="x86_64" os="LINUX">
	        <!-- This is where intermediate data will be stored -->
	        <directory type="shared-scratch" path="/tmp/wf/scratch">
	            <file-server operation="all" url="file:///tmp/wf/scratch"/>
	        </directory>
	        <!-- This is where output data will be stored -->
	        <directory type="shared-storage" path="/tmp/wf/output">
	            <file-server operation="all" url="file:///tmp/wf/output"/>
	        </directory>
	    </site>

	    <site handle="condorpool" arch="x86_64" os="LINUX">
	        <!-- These profiles tell Pegasus that the site is a plain Condor pool -->
	        <profile namespace="pegasus" key="style">condor</profile>
	        <profile namespace="condor" key="universe">vanilla</profile>
	        <profile namespace="condor" key="should_transfer_files">True</profile>
	        <profile namespace="condor" key="when_to_transfer_output">ON_EXIT</profile>
	    </site>
	</sitecatalog>
	'''
	return tmp

with open('sites.xml', 'w+') as f:
	f.write(sites)

# Part one
os.system("python daxgen.py")
os.system("./plan_dax.sh part1.dax")

# Wait for trigger for part two execution
while True:
	f = open('rc.txt', 'r')
	if "diffs.tbl" in f.read():
		break		
	f.close()
	time.sleep(1)

# Part two
os.system("python daxgen2.py")
os.system("./plan_dax.sh part2.dax")
	
	