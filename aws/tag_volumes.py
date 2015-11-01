#!/usr/bin/python

import boto.ec2
region = 'us-west-2'
tag_name = 'MakeSnapshot'
tag_value = 'True'
instance_ids = ['i-328091f7','i-fa81e621']

#instance = conn.get_only_instances(instance_ids=instance_id)[0]
conn = boto.ec2.connect_to_region(region)

for instance_id in instance_ids:
    volumes = conn.get_all_volumes(filters={'attachment.instance-id': instance_id})
    for vol in volumes:
        vol.add_tag(tag_name,tag_value)
        
