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
region = 'us-west-1'
tag_name = 'tag:MakeSnapshot'
tag_value = 'True'
keep_day = 6
keep_week = 4
Keep_month = 2
log_file = '/tmp/makesnapshots.log'


### Define Functions

def get_resource_tags(resource_id):
    resource_tags = {}
    if resource_id:
        tags = conn.get_all_tags({'resource_id': resource_id})
        for tag in tags:
            if not tag.name.startswith('aws'):
                resource_tags[tag.name] = tag.value
    return resource_tags





## Define AWS EC2 and SNS Connections
conn = boto.ec2.connect_to_region(region)
sns = boto.sns.connect_to_region(region)

# vols = conn.get_all_volumes(filters={ 'tag:' + config['tag_name']: config['tag_value'] })
vols = conn.get_all_volumes(filters={ 'tag:Snapshot': 'True' })



for vol in vols:
    current_snap=vol.create_snapshot(description)