# Montage Installation Guide

Montage is a toolkit for building image mosaics. The tutorial and documentation can be found from the Montage website: [http://montage.ipac.caltech.edu](http://montage.ipac.caltech.edu/)

## **Part A: Building Montage**

1. Download the latest version of Montage (v5.0) tarball from <http://montage.ipac.caltech.edu/docs/download2.html> and untar the source file.

```
$ wget http://montage.ipac.caltech.edu/download/Montage_v5.0.tar.gz
```

```
$ tar -zxvf Montage_v5.0.tar.gz
```

2. This will create a new directory named *Montage*. Change working directory to the main Montage directory.

```
$ cd Montage
```

3. Next, run **make** to build all the libraries and executables needed, which will be placed automatically in *Montage/bin* directory. Run **sudo apt install make** if the package is not found. Run **sudo apt install gcc** as well if there is no C compiler installed previously.

Note: It is unnecessary to understand all of them, but you can find the description for any executable in <http://montage.ipac.caltech.edu/docs/components.html> whenever you need.

```
$ make
```

4. The build might take up to several minutes. After seeing continuous stream of output message, montage is successfully built.

Note: If there is a need to run executables from any directory, set the environment path by adding following line to */home/$username/.profile.*

```
PATH=$PATH:$HOME/Montage/bin
```

 Your PATH should look like this:

```
PATH="$HOME/bin:$HOME/.local/bin:$PATH:$HOME/Montage/bin"
```

Note: Remember to execute **source** to update the environment variables!

```
source .profile
```

## **Part B: Creating an m101 mosaic**

In this example, we will create a mosaic of 10 2MASS Atlas images.

1. Download the example source file and uncompress it.

```
$ wget http://montage.ipac.caltech.edu/docs/m101Example/tutorial-initial.tar.gz
```

```
$ tar -zxvf tutorial-initial.tar.gz
```

2. This will create a directory called m101 containing 5 subdirectories: rawdir, projdir, diffdir, corrdir and final. Change working directory to m101 to proceed.

```
$ cd m101
```

3. First, we will reproject the raw images, and add them up to generate a mosaic WITHOUT background matching. Along the process, we will create some metadata tables to describe the image. The final output is a JPEG image.

```
$ mImgtbl rawdir images-rawdir.tbl
Output: [struct stat="OK", count=10, badfits=0]
```

```
$ mProjExec -p rawdir images-rawdir.tbl template.hdr projdir stats.tbl
Output: [struct stat="OK", count=10, failed=0, nooverlap=0]
```

```
$ mImgtbl projdir images.tbl
Output: [struct stat="OK", count=10, badfits=0]'
```

```
$ mAdd -p projdir images.tbl template.hdr final/m101_uncorrected.fits
Output: [struct stat="OK", time=8]
```

```
$ mJPEG -gray final/m101_uncorrected.fits 20% 99.98% loglog -out final/m101_uncorrected.jpg
Output: [struct stat="OK", min=80.747, minpercent=20.00, max=180.914, maxpercent=99.98]
```

8. To open the image file, copy the JPEG file (found in m101/final) to local machine by using **scp**. In local machine terminal, run following command.

```
scp -i "[keyname].pem" [remote_user]@[remote_host]:[remote_file] [local_directory]
```

9. The result should be as follows:

![img](/images/m101_uncorrected.jpg)

10. The result image is not satisfying - few more steps need to be done for background modeling to smooth out the background levels between overlapping images.

```
$ mOverlaps images.tbl diffs.tbl
Output: [struct stat="OK", count=17]
```

```
$ mDiffExec -p projdir diffs.tbl template.hdr diffdir
Output: [struct stat="OK", count=17, failed=0]
```

```
$ mFitExec diffs.tbl fits.tbl diffdir
Output: [struct stat="OK", count=17, failed=0, warning=0, missing=0]
```

```
$ mBgModel images.tbl fits.tbl corrections.tbl
Output: [struct stat="OK"]
```

```
$ mBgExec -p projdir images.tbl corrections.tbl corrdir
Output: [struct stat="OK", count=10, nocorrection=0, failed=0]
```

```
$ mAdd -p corrdir images.tbl template.hdr final/m101_mosaic.fits
Output: [struct stat="OK", time=1]
```

```
$ mJPEG -gray final/m101_mosaic.fits 0s max gaussian-log -out final/m101_mosaic.jpg
Output: [struct stat="OK", min=82.7157, minpercent=50.00, max=9628.28, maxpercent=100.00]
```

11. Repeat step 8 to see the final image. The result should be as follows:

![img](/images/m101_mosaic.jpg)

 