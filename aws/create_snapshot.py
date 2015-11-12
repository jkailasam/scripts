#!/usr/bin/python
import boto.ec2
import argparse


def create_snapshot(conn, instance_id, name):
    response = conn.create_image(instance_id,name,no_reboot=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create and and copy AMI Image.')
    parser.add_argument('--region',required=True)
    parser.add_argument('--instance',required=True)
    parser.add_argument('--name',required=True)
    args = parser.parse_args()
    
    print args.region
    print args.instance
    print args.name

    conn = boto.ec2.connect_to_region(args.region)

    # Create Snapshot
    ImageId = create_snapshot(conn, args.instance, args.name)
    print ImageId


