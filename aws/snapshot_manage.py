#!/usr/bin/python
__author__ = "Jeeva Kailasam"
__version__ = "1.0"
__email__ = "jkailasam@netflix.com"
__status__ = "Development"

### Import modules
import sys
from datetime import datetime
import argparse
import time
import boto.ec2
import boto.sns

## Configuration section. Modify your Values here
region = 'us-west-2'
tag_name = 'tag:MakeSnapshot'
tag_value = 'True'
keep_daily = 6
keep_weekly = 4
Keep_monthly = 2
log_file = '/tmp/makesnapshots.log'
policy = 'daily'

### Define Functions

def get_resource_tags(resource_id):
    resource_tags = {}
    if resource_id:
        tags = conn.get_all_tags({'resource_id': resource_id})
        for tag in tags:
            if not tag.name.startswith('aws'):
                resource_tags[tag.name] = tag.value
    return resource_tags



def create_description(resource_id):
    desc = '%(policy)s_snapshot for %(vol_id)s taken on %(date)s' %{
    'policy' : policy, 'vol_id' : vol.id, 'date' : datetime.today().strftime('%d-%m-%Y at %H:%M:%S')
    }
    return desc

def create_delete_list(snap,policy):
    snapdesc = snap.description
    if (snapdesc.startswith(policy) and policy == policy):
        deletelist.append(snap)
    return deletelist



## Define AWS EC2 and SNS Connections
conn = boto.ec2.connect_to_region(region)
sns = boto.sns.connect_to_region(region)

# vols = conn.get_all_volumes(filters={ 'tag:' + config['tag_name']: config['tag_value'] })
vols = conn.get_all_volumes(filters={ 'tag:Snapshot': 'True' })


for vol in vols:
    description = create_description(vol)
    current_snap = vol.create_snapshot(description)
    print '%(snap_id)s created for %(volume)s' %{
    'snap_id' : current_snap, 'volume' : vol
    }


if policy == 'daily':
    snap_to_keep = 6
elif policy == weekly:
    snap_to_keep = 4
elif policy == monthly:
    snap_to_keep = 2



/// to delete the old snapshots

01. Get the delete list
def create_delete_list(snap,policy):
    snapdesc = snap.description
    if (snapdesc.startswith(policy) and policy == policy):
        deletelist[snap] = snap.start_time
    return deletelist

for snap in snaps:
    create_delete_list(snap,policy)

02. Sort it by value
    sorted_by_date = sorted(deletelist.values())

03. Find out the oldest snap
    for snap, start_time in deletelist.items():
        if start_time == sorted_by_date[0]:
            snap_to_delete = snap
    return snap_to_delete

///
