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
keep_daily = 6
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
    snap_to_keep = keep_daily
elif policy == 'weekly':
    snap_to_keep = keep_weekly
elif policy == 'monthly':
    snap_to_keep = Keep_monthly

### Define Functions
def create_description():
    desc = '%(policy)s_snapshot for %(instance_id)s taken on %(date)s' %{
    'policy' : policy, 'instance_id' : instance.id, 'date' : datetime.today().strftime('%d-%m-%Y at %H:%M:%S')
    }
    return desc

def create_aminame(resource_id):
    crtime=datetime.today().strftime('%y-%m-%d_%H:%M')
    tags = conn.get_all_tags({'resource_id':resource_id})
    for tag in tags:
        if tag.name == 'Name':
            inst_name = tag.value
        else:
            inst_ame = ''
    name = '%(policy)s_%(instance_id)s_%(crtime)s_%(inst_name)s' %{
    'policy' : policy,'instance_id' :resource_id,'crtime': crtime, 'inst_name': inst_name}
    return name


def create_ami(instance_id, image_name):
    description = create_description()
    crtime=datetime.today().strftime('%y-%m-%d_%H:%M')

    ImageId = conn.create_image(instance_id,image_name,description=description,no_reboot=True)
    print "Image creation for instance {0} started. Image Id: {1}".format(instance_id,ImageId)
    return ImageId




def delete_snapshots():
    snaps = vol.snapshots()
    deletelist = {}
    for snap in snaps:
        snapdesc = snap.description
        if (snapdesc.startswith(policy) and policy == policy):
            deletelist[snap] = snap.start_time
    sorted_by_date = sorted(deletelist.values())
    count = len(deletelist)
    if count > snap_to_keep :
        delta = count - snap_to_keep
        for i in range(0,delta):
            for snap, start_time in deletelist.items():
                if start_time == sorted_by_date[i]:
                    try:
                        print "now deleting %(policy)s %(snap)s" %{'policy': policy, 'snap' : snap}
                        response = snap.delete()
                        print '%(policy)s %(snap)s deleted successully' %{'policy': policy, 'snap' : snap}
                    except:
                        print "Error deleing %(snap)s" %{'snap' : snap}

## Define AWS EC2 and SNS Connections
conn = boto.ec2.connect_to_region(region)
sns = boto.sns.connect_to_region(region)
instances=conn.get_only_instances(filters={ 'tag:CreateAMI': 'True' })

## Create a new snapshot
for instance in instances:
    create_ami()
    delete_ami()


'''
tags = conn.get_all_tags({'resource_id':instance_id})
for tag in tags:
    if tag.name == 'Name':
        name = tag.value
    else:
        name = ''




def get_resource_tags(resource_id):
    resource_tags = {}
    if resource_id:
        tags = conn.get_all_tags({'resource_id': resource_id})
        for tag in tags:
            if not tag.name.startswith('aws'):
                resource_tags[tag.name] = tag.value
    return resource_tags


def create_delete_list(snap,policy):
    snapdesc = snap.description
    if (snapdesc.startswith(policy) and policy == policy):
        deletelist[snap] = snap.start_time
    return deletelist


for vol in vols:
    snaps = vol.snapshots()
    deletelist = {}
    for snap in snaps:
        deletelist = create_delete_list(snap,policy)
        sorted_by_date = sorted(deletelist.values())
    count = len(deletelist)
    if count > snap_to_keep :
        delta = count - snap_to_keep
        for i in range(0,delta):
            for snap, start_time in deletelist.items():
                if start_time == sorted_by_date[i]:
                    try:
                        print "now deleting %(snap)s" %{'snap' : snap}
                        response = snap.delete()
                        print '%(snap)s deleted successully' %{'snap' : snap}
                    except:
                        print "Error deleing %(snap)s" %{'snap' : snap}
'''
