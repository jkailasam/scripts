#!/usr/bin/python
__author__ = "Jeeva Kailasam"
__version__ = "1.0"
__email__ = "jkailasam@netflix.com"
__status__ = "Beta"

### Import modules
import sys
from datetime import datetime
import argparse
import time
import boto.ec2
import boto.sns

## Configuration section. Modify your Values here
region = 'us-west-2'
tag_name = 'tag:CreateAMI'
tag_value = 'True'
Daily=['Mon','Tue','Wed','Thu','Fri']
Weekly = 'Sun'
keep_daily = 8
keep_weekly = 4
Keep_monthly = 2

#### Do not modify anything bellow this point####
## Set the policy
today=datetime.today().strftime('%a-%Y-%m-%d-%H:%M').split('-')
if today[0] in Daily:
    policy = 'daily'
elif today[0] in Weekly:
    policy = 'weekly'

## Set number of snaps to keep
if policy == 'daily':
    ami_to_keep = keep_daily
elif policy == 'weekly':
    ami_to_keep = keep_weekly
elif policy == 'monthly':
    ami_to_keep = Keep_monthly

### Define Functions
def create_description(instance_id):
    desc = '%(policy)s_AMI for %(instance_id)s taken on %(date)s' %{
    'policy' : policy, 'instance_id' : instance_id, 'date' : datetime.today().strftime('%d-%m-%Y at %H:%M:%S')
    }
    return desc

def create_aminame(resource_id):
    crtime=datetime.today().strftime('%y-%m-%d_%H-%M')
    tags = conn.get_all_tags({'resource_id':resource_id})
    for tag in tags:
        if tag.name == 'Name':
            inst_name = tag.value
        else:
            inst_ame = ''
    name = '%(policy)s_%(instance_id)s_%(crtime)s_%(inst_name)s' %{
    'policy' : policy,'instance_id' :resource_id,'crtime': crtime, 'inst_name': inst_name}
    return name


def create_ami(instance_id):
    description = create_description(instance_id)
    ami_name = create_aminame(instance_id)
    ImageId = conn.create_image(instance_id,ami_name,description=description,no_reboot=True)
    print "Image creation for instance {0} started. AMI Id: {1}".format(instance_id,ImageId)
    AMI=conn.get_all_images([ImageId])[0]
    AMI.add_tag('Name',ami_name)
    AMI.add_tag('InstanceID', instance_id)
    return AMI


def delete_ami(instance_id):
    images = conn.get_all_images(filters={'tag:InstanceID' :instance_id})
    deletelist = {}
    for ami in images:
        amidesc = ami.description
        if (amidesc.startswith(policy) and policy == policy):
            deletelist[ami] = ami.creationDate
    sorted_by_date = sorted(deletelist.values())
    count = len(deletelist)
    if count > ami_to_keep :
        delta = count - ami_to_keep
        for i in range(0,delta):
            for ami, creationDate in deletelist.items():
                ami_id=ami.id
                if creationDate == sorted_by_date[i]:
                    try:
                        print "now deleting %(ami)s" %{'ami' : ami}
                        response = conn.deregister_image(ami_id, delete_snapshot=True)
                        print '%(ami)s deleted successully' %{'ami' : ami}
                    except:
                        print "Error deleing %(ami)s" %{'ami' : ami}
                        print response

## Define AWS EC2 and SNS Connections
conn = boto.ec2.connect_to_region(region)
sns = boto.sns.connect_to_region(region)
instances=conn.get_only_instances(filters={ tag_name: tag_value })

## Create a new snapshot
for instance in instances:
    instance_id = instance.id
    create_ami(instance_id)
    delete_ami(instance_id)
