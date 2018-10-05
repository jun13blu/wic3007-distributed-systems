# HT Condor AWS Instance Setup

This file is a guide for setting the AWS instances to be used with HT Condor. This will make two/more instances to work in a cluster.

## Step One: Setting Up Security Group

Open up your AWS Console and, scroll down the sidebar, and click "Security Groups" under "Network & Security".
Create a new security group or edit an existing one.

### Create a new security group

1. Click on "Create Security Group" button.
2. Fill in "Security group name" (e.g. condor_pool) and "Description" (e.g. for HT Condor).
3. On "Inbound" tab, click "Add rule" button.
4. For "Type" pick "SSH", and for "Source", pick "Anywhere" (or any ip address that you want).
5. Click on "Create button".

Now we are going to add two more rules to be included. These two rules cannot be added during creating a new security group since for sources for both rules, we need to enter the name of an existing security group (in this case, condor_pool, which doesn't exist yet).

### Edit the newly created security group/existing security group

1. Right click on the newly created security group, and pick "Edit inbound rules".
2. Click on "Add rule" button.
3. For "Type" pick "All TCP", and for "Source", type the name of the newly created security group. There will be a suggestion under the space which is the group ID of that security group. Click on that suggestion.
4. Repeat no. 2 and no. 3, and the type is "All UDP" with the same source.
5. Click on "Save" button.

Now at this point, your "Edit inbound rules" setting should look like this:

![Image of Edit inboudn rules](https://github.com/AzriDelta/wic3007-distributed-systems/blob/master/HTCondor/Security%20Group%20-%20Inbound%20Rule.png)

## Step Two: Adding Instances to the Security Group

1. Click on "EC2 Dashbord" on the sidebar, and click on Running Instances.
2. Click on an instance, right click, and go to Networking -> Change Security Groups.
3. Tick the newly created security group, and click on "Assign Security Groups" button.
4. Repeat no. 2 and no. 3 on other instances.
