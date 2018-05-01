# Ceph Deploy Guide

## Ceph-Deploy Setup
Add the release key:
```
wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
```

Add the Ceph packages to your repository. Use the command below and replace {ceph-stable-release} with a stable Ceph release (e.g., luminous.) For example:
```
echo deb https://download.ceph.com/debian-{ceph-stable-release}/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
```

Update your repository and install ceph-deploy:
```
sudo apt update
sudo apt install ceph-deploy
```

## Ceph Node Setup
Install NTP:
```
sudo apt install ntp
```

### Create a Ceph Deploy user
Create a new user on each Ceph node:
```
ssh user@ceph-server
sudo useradd -d /home/{username} -m {username}
sudo passwd {username}
```

For the new user you added to each Ceph node, ensure that the user has sudo privileges.
```
echo "{username} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{username}
sudo chmod 0440 /etc/sudoers.d/{username}
```

Edit `/etc/ssh/sshd_config`
```
PasswordAuthentication yes
```

### Enable Password-less ssh
Generate the SSH keys, but do not use sudo or the root user. Leave the passphrase empty:

```
ssh-keygen

Generating public/private key pair.
Enter file in which to save the key (/ceph-admin/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /ceph-admin/.ssh/id_rsa.
Your public key has been saved in /ceph-admin/.ssh/id_rsa.pub.
```

Copy the key to each Ceph Node, replacing {username} with the user name you created with Create a Ceph Deploy User.
```
ssh-copy-id {username}@node1
ssh-copy-id {username}@node2
ssh-copy-id {username}@node3
```

Modify the ~/.ssh/config file of your ceph-deploy admin node so that ceph-deploy can log in to Ceph nodes as the user you created without requiring you to specify --username {username} each time you execute ceph-deploy. This has the added benefit of streamlining ssh and scp usage. Replace {username} with the user name you created:
```
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
```
mkdir my-cluster
cd my-cluster
```

Create the cluster.
```
ceph-deploy new {initial-monitor-node(s)}
```
For example:
```
ceph-deploy new node1
```

Install Ceph packages.:
```
ceph-deploy install {ceph-node} [...]
```
For example:
```
ceph-deploy install node1 node2 node3
```
The ceph-deploy utility will install Ceph on each node.

Deploy the initial monitor(s) and gather the keys:
```
ceph-deploy mon create-initial
```

Use ceph-deploy to copy the configuration file and admin key to your admin node and your Ceph Nodes.
```
ceph-deploy admin {ceph-node(s)}
```
For example:
```
ceph-deploy admin node1 node2 node3
```

Add three OSDs. For the purposes of these instructions, we assume you have an unused disk in each node called /dev/vdb. Be sure that the device is not currently in use and does not contain any important data.
```
ceph-deploy osd create –data {device} {ceph-node}
```
For example:
```
ceph-deploy osd create --data /dev/vdb node1
ceph-deploy osd create --data /dev/vdb node2
ceph-deploy osd create --data /dev/vdb node3
```

## Ceph FS Quick Start
On the admin node, use ceph-deploy to install Ceph on your ceph-client node.
```
ceph-deploy install ceph-client
```

Create a filesystem
```
ceph osd pool create cephfs_data <pg_num>
ceph osd pool create cephfs_metadata <pg_num>
ceph fs new <fs_name> cephfs_metadata cephfs_data
```

Mount it in `fstab`
```
none    /mnt/ceph  fuse.ceph ceph.id=myuser,_netdev,defaults  0 0
```
