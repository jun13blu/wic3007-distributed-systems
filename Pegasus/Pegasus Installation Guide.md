# Pegasus Installation Guide

***Last Updated by Xin Zhe & Suh Haw @ March 2018***

Software versions used in this guide:

> Ubuntu 16.04.3 LTS
>
> HT Condor Version 8.6.9
>
> Pegasus Version 4.8.1

*Note:*

*Before proceeding with this guide, you are expected to have HT Condor running on your machine/ instance. Pegasus must be installed on the HT Condor node which is running the scheduling daemon, SCHED.*

## Step One: Install Dependencies 

Pegasus requires Java 1.6 or higher, Python 2.6 or higher and HT Condor 8.4 or later.

**Java**

```bash
sudo apt-get install software-properties-common -y && \
sudo add-apt-repository ppa:webupd8team/java -y && \
sudo apt-get update && \
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections && \
sudo apt-get install oracle-java8-installer oracle-java8-set-default -y
```

**Python**

```bash
sudo apt-get install python
```

**HT Condor**

*Refer to the HT Condor Installation guide*

## Step Two: Adding Pegasus GPG Keys

```bash
sudo wget -O - http://download.pegasus.isi.edu/pegasus/gpg.txt | sudo apt-key add -
```

## Step Three: Adding Pegasus Repositories

```bash
sudo add-apt-repository "deb http://download.pegasus.isi.edu/pegasus/ubuntu trusty main"
sudo apt-get update
sudo apt-get install pegasus
```

If you are facing issues related to `libmysqlclient18`, you may need to install it via the following commands.

```bash
sudo wget http://launchpadlibrarian.net/212189159/libmysqlclient18_5.6.25-0ubuntu1_amd64.deb
sudo apt install ./libmysqlclient18_5.6.25-0ubuntu1_amd64.deb -y
```

## Step Four: Verifying HT Condor Status

Before proceeding with any further workflow, verify that HT Condor is running via `condor_q` or `condor_status` on your machine.

## Step Five: Pegasus Dashboard Setup

Pegasus relies on your UNIX user account and password as your credentials to login to the dashboard. Hence, if your current account uses a Public Key to login, you may need to create an additional user in order to use the dashboard.

In this case, we will be creating a user called `pegasus`, beyond that, follow the steps to complete your user account set up.

```bash
sudo adduser pegasus
```

Add your newly created user as a super user.

```bash
sudo usermod -aG sudo pegasus
```

Login to your newly created user.

```bash
sudo su pegasus
```

Initialize database for Pegasus. 

> Note: You may need to change the path for the `workflow.db` according to your username.

```bash
pegasus-db-admin update sqlite:////home/pegasus/.pegasus/workflow.db
```

## Step Six: Starting Up the Pegasus Dashboard Service

By default, Pegasus listens only to your `localhost` address. Hence, when starting your dashboard, you will need to enable it to listen to all requests to the dashboard.

> Note: The default port is 5000, you may change it using --port <PORT> based on your own preference.

```bash
sudo pegasus-service --host 0.0.0.0
```

Access the Pegasus Dashboard at `https://<IP>:5000` using your own internet browser and login with your newly created user credentials.

> Note: Remember to put HTTPS in front of your dashboard URL.

You should be able to see the Pegasus Dashboard, workflow listing with an empty chart and an empty table.

## Step Seven: Submitting an Example Workflow

We will generate a sample workflow called `split` by using `pegasus-init`. [Official Documentation Here](https://pegasus.isi.edu/documentation/tutorial_submitting_wf.php)

From your `pegasus` user, it will look like the following:

```bash
$ pegasus-init split
Do you want to generate a tutorial workflow? (y/n) [n]: y
1: Local Machine
2: USC HPCC Cluster
3: OSG from ISI submit node
4: XSEDE, with Bosco
5: Bluewaters, with Glite
What environment is tutorial to be setup for? (1-5) [1]: 1
1: Process
2: Pipeline
3: Split
4: Merge
5: EPA (requires R)
6: Diamond
What tutorial workflow do you want? (1-6) [1]: 3
Pegasus Tutorial setup for example workflow - split for execution on submit-host in directory /home/pegasus/split
```

After generating a sample workflow, navigate into the newly created directory and run the provided scripts to generate a DAX file for Pegasus to execute later, you should see the follow outcome.

```bash
$ cd split
$ ./generate_dax.sh split.dax
Generated dax split.dax
$ ./plan_dax.sh split.dax
2018.03.10 08:36:46.810 UTC:
2018.03.10 08:36:46.816 UTC:   -----------------------------------------------------------------------
2018.03.10 08:36:46.822 UTC:   File for submitting this DAG to HTCondor           : split-0.dag.condor.sub
2018.03.10 08:36:46.829 UTC:   Log of DAGMan debugging messages                 : split-0.dag.dagman.out
2018.03.10 08:36:46.836 UTC:   Log of HTCondor library output                     : split-0.dag.lib.out
2018.03.10 08:36:46.841 UTC:   Log of HTCondor library error messages             : split-0.dag.lib.err
2018.03.10 08:36:46.847 UTC:   Log of the life of condor_dagman itself          : split-0.dag.dagman.log
2018.03.10 08:36:46.852 UTC:
2018.03.10 08:36:46.857 UTC:   -no_submit given, not submitting DAG to HTCondor.  You can do this with:
2018.03.10 08:36:46.868 UTC:   -----------------------------------------------------------------------
2018.03.10 08:36:47.340 UTC:   Your database is compatible with Pegasus version: 4.8.1
2018.03.10 08:36:47.416 UTC:   Submitting to condor split-0.dag.condor.sub
2018.03.10 08:36:47.468 UTC:   Submitting job(s).
2018.03.10 08:36:47.475 UTC:   1 job(s) submitted to cluster 1.
2018.03.10 08:36:47.480 UTC:
2018.03.10 08:36:47.486 UTC:   Your workflow has been started and is running in the base directory:
2018.03.10 08:36:47.492 UTC:
2018.03.10 08:36:47.499 UTC:     /home/pegasus/split/submit/pegasus/pegasus/split/run0001
2018.03.10 08:36:47.504 UTC:
2018.03.10 08:36:47.511 UTC:   * To monitor the workflow you can run *
2018.03.10 08:36:47.519 UTC:
2018.03.10 08:36:47.527 UTC:     pegasus-status -l /home/pegasus/split/submit/pegasus/pegasus/split/run0001
2018.03.10 08:36:47.535 UTC:
2018.03.10 08:36:47.543 UTC:   * To remove your workflow run *
2018.03.10 08:36:47.551 UTC:
2018.03.10 08:36:47.559 UTC:     pegasus-remove /home/pegasus/split/submit/pegasus/pegasus/split/run0001
2018.03.10 08:36:47.567 UTC:
2018.03.10 08:36:51.850 UTC:   Time taken to execute is 1.981 seconds
```

Besides the outcome above, you may also observe more details on your Pegasus Dashboard.

## Optional: Environment Setup

In order to use the `DAX API`, you must have the following PATH set.

```bash
export PYTHONPATH=`pegasus-config --python`
export PERL5LIB=`pegasus-config --perl`
export CLASSPATH=`pegasus-config --classpath`
```

