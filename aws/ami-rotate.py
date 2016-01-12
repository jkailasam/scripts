#!/usr/bin/python
__author__ = "Jeeva Kailasam"
__version__ = "1.01"
__email__ = "jkailasam@netflix.com"
__status__ = "Beta"

### Import modules
import sys
from datetime import datetime
import argparse
import time
import boto.ec2
import boto.sns

## Configuration section. Modify your f here
#regions = ['us-west-2', 'us-west-1']
regions = ['us-west-1','us-west-2','us-east-1']
tag_name = 'tag:autobackup'
tag_value = 'true'
Weekly = 'Sun'
keep_daily = 6
keep_weekly = 4
keep_monthly = 2

#### Do not modify anything bellow this point####
## Set the policy
today=datetime.today().strftime('%a-%Y-%m-%d-%H:%M').split('-')

if today[3] == '01':
    policy = 'monthly'
elif today[0] in Weekly:
    policy = 'weekly'
else:
    policy = 'daily'

## Set number of snaps to keep
if policy == 'daily':
    ami_to_keep = keep_daily
elif policy == 'weekly':
    ami_to_keep = keep_weekly
elif policy == 'monthly':
    ami_to_keep = keep_monthly

###### conn = boto.ec2.connect_to_region(region)
###### sns = boto.sns.connect_to_region(region)

### Define Functions
def create_description(instance_id):
    desc = '%(policy)s_AMI for %(instance_id)s taken on %(date)s' %{
    'policy' : policy, 'instance_id' : instance_id, 'date' : datetime.today().strftime('%d-%m-%Y at %H:%M:%S')
    }
    return desc

def create_aminame(conn, resource_id):
    crtime=datetime.today().strftime('%y-%m-%d_%H-%M')
    tags = conn.get_all_tags({'resource_id':resource_id})
    for tag in tags:
        if tag.name == 'Name':
            inst_name = tag.value
            break
        else:
            inst_name = ''
    name = '%(policy)s_%(instance_id)s_%(crtime)s_%(inst_name)s' %{
    'policy' : policy,'instance_id' :resource_id,'crtime': crtime, 'inst_name': inst_name}
    return name


def create_ami(conn, instance_id):
    print "==============================="
    print "Creating {0} AMI for instance {1}...".format(policy, instance_id)

    description = create_description(instance_id)
    ami_name = create_aminame(conn, instance_id)

    ImageId=""
    try:
        ImageId = conn.create_image(instance_id,ami_name,description=description,no_reboot=True)
        AMI=conn.get_all_images([ImageId])[0]
        AMI.add_tag('Name',ami_name)
        AMI.add_tag('InstanceID', instance_id)
        print "Successfully created AMI Id: {1}".format(instance_id,ImageId)
    except:
        print "Failed to create AMI"

    return ImageId


def delete_ami(conn, instance_id):
    print "==============================="
    print "Reviewing AMI inventory for instance {0}...".format(instance_id)
    images = conn.get_all_images(filters={'tag:InstanceID' :instance_id})
    deletelist = {}
    for ami in images:
        amidesc = ami.description
        if (amidesc.startswith(policy)):
            deletelist[ami] = ami.creationDate
    sorted_by_date = sorted(deletelist.values())
    count = len(deletelist)
    print "Found {0} images.".format(count)
    if count > ami_to_keep :
        delta = count - ami_to_keep
        print "Found {0} images to delete.".format(delta)
        for i in range(0,delta):
            for ami, creationDate in deletelist.items():
                ami_id=ami.id
                if creationDate == sorted_by_date[i]:
                    try:
                        print "Now deleting %(ami)s" %{'ami' : ami}
                        response = conn.deregister_image(ami_id, delete_snapshot=True)
                        print '%(ami)s deleted successully' %{'ami' : ami}
                    except:
                        print "Error deleting %(ami)s" %{'ami' : ami}
                        print response

def lambda_handler(event, context):
    for region in regions:
        conn = boto.ec2.connect_to_region(region)
        sns = boto.sns.connect_to_region(region)
        instances=conn.get_only_instances(filters={ tag_name: tag_value })
        print ("===================================")
        print ("Now processing {0} region......".format(region))

        ## Create a new snapshot
        for instance in instances:
            instance_id = instance.id
            # create_ami(conn,instance_id)
            #time.sleep(10)
            delete_ami(conn, instance_id)
        print ("===================================")
        print "\n\n\ncompleted processing all instances in {0}... \n\n".format(region)
    return

if __name__ == '__main__':
    lambda_handler('a','b')
