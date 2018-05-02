# Ceph Deploy Guide

## Terms

### Ceph Admin

You will install `ceph-deploy` on this host. It is used to setup all the other nodes. One of the clients or Ceph nodes can be used as admin node.

### Ceph Nodes

Actual host that is part of the ceph storage cluster. Must have at least an empty hard disk with storage larger than 5GB. The first 5GB will be taken up by the ceph journal, so only the remaining space will contribute to the storage size. Must not be the client.

### Ceph Client

Host that mount ceph cluster as a file system or block storage. Cannot be used as one of the ceph nodes.

## Admin Node Setup

Add the release key:

```bash
wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
```

Add the Ceph packages to your repository. Use the command below and replace `{ceph-stable-release}` with a stable Ceph release (e.g., `luminous`.) For example:

```bash
echo deb https://download.ceph.com/debian-{ceph-stable-release}/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
```

Update your repository and install `ceph-deploy`:

```bash
sudo apt update
sudo apt install ceph-deploy
```

## Ceph Node Setup

Install NTP:

```bash
sudo apt install ntp
```

### Create a Ceph Deploy user

Create a new user on each Ceph node:

```bash
ssh user@ceph-server
sudo useradd -d /home/{username} -m {username}
sudo passwd {username}
```

For the new user you added to each Ceph node, ensure that the user has sudo privileges.

```bash
echo "{username} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{username}
sudo chmod 0440 /etc/sudoers.d/{username}
```

Edit `/etc/ssh/sshd_config`

```bash
PasswordAuthentication no #uncomment this
```

## Enable Password-less ssh

### Ceph Admin Setup

Generate the SSH keys, but do not use sudo or the root user. Leave the passphrase empty:

```bash
ssh-keygen

Generating public/private key pair.
Enter file in which to save the key (/ceph-admin/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /ceph-admin/.ssh/id_rsa.
Your public key has been saved in /ceph-admin/.ssh/id_rsa.pub.
```

Copy the key to each Ceph Node, replacing {username} with the user name you created with Create a Ceph Deploy User.

```bash
ssh-copy-id {username}@node1
ssh-copy-id {username}@node2
ssh-copy-id {username}@node3
```

Modify the ~/.ssh/config file of your ceph-deploy admin node so that ceph-deploy can log in to Ceph nodes as the user you created without requiring you to specify --username {username} each time you execute ceph-deploy. This has the added benefit of streamlining ssh and scp usage. Replace {username} with the user name you created:

```bash
Host node1
   Hostname node1
   User {username}
Host node2
   Hostname node2
   User {username}
Host node3
   Hostname node3
   User {username}
```

## Storage Cluster Quick Start

Create a directory on your admin node for maintaining the configuration files and keys that `ceph-deploy` generates for your cluster.

```bash
mkdir my-cluster
cd my-cluster
```

Create the cluster.

```bash
ceph-deploy new {initial-monitor-node(s)}
```

For example:

```bash
ceph-deploy new node1
```

Edit `ceph.conf`

```bash
public network = {network address}/{network mask} #add this line
```

For example:

```bash
public network = 10.0.0.0/24
```

Install Ceph packages.:

```bash
ceph-deploy install {ceph-node} [...]
```

For example:

```bash
ceph-deploy install node1 node2 node3
```

The `ceph-deploy` utility will install Ceph on each node.

Deploy the initial monitor(s) and gather the keys:

```bash
ceph-deploy mon create-initial
```

Use `ceph-deploy` to copy the configuration file and admin key to your admin node and your Ceph Nodes.

```bash
ceph-deploy admin {ceph-node(s)}
```

For example:

```bash
ceph-deploy admin node1 node2 node3
```

Add three OSDs. For the purposes of these instructions, we assume you have an unused disk in each node called `/dev/xvdb`. Be sure that the device is not currently in use and does not contain any important data.

```bash
ceph-deploy disk zap {ceph-node}:{device}
ceph-deploy osd create {ceph-node}:{device}
```

For example:

```bash
ceph-deploy disk zap node1:xvdb
ceph-deploy osd create node1:xvdb

ceph-deploy disk zap node2:xvdb
ceph-deploy osd create node2:xvdb

ceph-deploy disk zap node3:xvdb
ceph-deploy osd create node3:xvdb
```

## Ceph FS Quick Start

On the admin node, use ceph-deploy to install Ceph on your ceph-client node.

```bash
ceph-deploy install ceph-client
```

On the monitor node, create a pool

```bash
sudo ceph osd pool create cephfs_data <pg_num>
sudo ceph osd pool create cephfs_metadata <pg_num>
sudo ceph fs new <fs_name> cephfs_metadata cephfs_data
```

For example:

```bash
sudo ceph osd pool create cephfs_data 64
sudo ceph osd pool create cephfs_metadata 64
sudo ceph fs new myclusterfs cephfs_metadata cephfs_data
```

On the client node, mount it in `/etc/fstab`

```bash
id=admin  {directory}  fuse.ceph _netdev,defaults  0 0
```

For example

```bash
id=admin  /mnt/ceph  fuse.ceph _netdev,defaults  0 0
```
