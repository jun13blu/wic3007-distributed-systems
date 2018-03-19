# HT Condor Installation Quick Guide

Software versions used in this guide:

> Ubuntu 16.04.3 LTS
>
> HT Condor Version 8.6.9

## Step One: Add HT Condor Repositories

```bash
sudo add-apt-repository "deb http://htcondor.org/debian/stable/ wheezy contrib"
sudo add-apt-repository "deb http://htcondor.org/debian/development/ wheezy contrib"
sudo add-apt-repository "deb http://htcondor.org/debian/stable/ jessie contrib"
sudo add-apt-repository "deb http://htcondor.org/debian/development/ jessie contrib"
```

## Step Two: Add HT Condor Repository GPG Keys

```bash
wget -qO - http://research.cs.wisc.edu/htcondor/debian/HTCondor-Release.gpg.key | sudo apt-key add -
```

## Step Three: Install HT Condor 

```bash
sudo apt update
sudo apt install condor
```

## Step Four: Configuring the Master Node

1. For this example, the master node allows job submission and job execution.
2. Update the configuration files for the master node at `/etc/condor/condor_config`.
3. Add `ALLOW_READ = *` and `ALLOW_WRITE = *` to the configuration file and save it.
4. Start Condor on your master node.

```bash
sudo /etc/init.d/condor start
```

4. Verify that Condor is running, you should see a few of the condor services running such as `condor_sched`, `condor_startd`, `condor_collector`, `condor_negotiator` and `condor_procd`.

```
ps -ef | grep condor
```

## Step Five: Configuration the Worker Nodes

1. For this example, the worker nodes only perform job execution only.

2. Update the configuration files for the worker nodes at `/etc/condor/condor_config`.

3. Add `ALLOW_READ = *` and `ALLOW_WRITE = *` to the configuration file.

4. Change the **CONDOR_HOST** to the IP address of your *master* node. 

   ```
   # Example
   CONDOR_HOST = 192.168.1.1
   ```

5. Leave only the daemons `MASTER` and `STARTD`, and remove the other daemons.

   ```
   DAEMON_LIST = MASTER, STARTD
   ```

6. Save the configuration file and start Condor on your worker node.

   ```bash
   sudo /etc/init.d/condor start
   ```

## Step Six: Verify Condor Pool Information

You can verify the total number of nodes available in the pool by executing the command `condor_status`. Like the example below:

```bash
Name               OpSys      Arch   State     Activity LoadAv Mem   ActvtyTime

slot3@vulture.cs.w LINUX      INTEL  Unclaimed Idle     0.070   512  1+11:10:32
slot4@vulture.cs.w LINUX      INTEL  Unclaimed Idle     0.070   512  1+11:10:32

                     Total Owner Claimed Unclaimed Matched Preempting Backfill

         INTEL/LINUX     2     0       0         2       0          0        0

               Total     2     0       0         2       0          0        0
```

