#!/usr/bin/python
import boto.ec2
import argparse
#import boto.utils



def create_snapshot(conn, instance_id, name):
	response = conn.create_image(instance_id,name,no_reboot=True)

def parsed_args():
	parser = argparse.ArgumentParser(description='Create and and copy AMI Image.')
	parser.add_argument('-r', '--region',required=True)
	parser.add_argument('-i', '--instance',required=True)
	parser.add_argument('-n', '--name',required=True)
	#parser.add_argument('-d', '--device',)
	return parser.parse_args()

def main():
	args = parsed_args()
	print args.region
	print args.instance
	print args.name
	#print args.device
	conn = boto.ec2.connect_to_region(args.region)
	ImageId = create_snapshot(conn, args.instance, args.name)


if __name__ == '__main__':
	main()

    # Create Snapshot
    #ImageId = create_snapshot(conn, args.instance, args.name)
    #print ImageId
