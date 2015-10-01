#!/usr/bin/python
import boto.ec2
import argparse
import time
#import boto.utils


def create_ami(conn,instance_id, name):
	ImageId = conn.create_image(instance_id,name,no_reboot=True)
	print "Image creation for instance {0} started. Image Id: {1}".format(instance_id,ImageId)
	return ImageId

def parsed_args():
	parser = argparse.ArgumentParser(description='Create and and copy AMI Image.')
	parser.add_argument('-r', '--region',required=True)
	parser.add_argument('-i', '--instance',required=True)
	parser.add_argument('-n', '--name',required=True)
	#parser.add_argument('-d', '--device',)
	return parser.parse_args()

def get_image_status(conn,ImageId):
	image = conn.get_all_images([ImageId])[0]
	return image.state

def main():
	args = parsed_args()
	print args.region
	print args.instance
	print args.name
	#print args.device
	conn = boto.ec2.connect_to_region(args.region)
	image_id = create_ami(conn,args.instance, args.name)
	status = get_image_status(conn,image_id)
	print status
	while status == 'pending':
		time.sleep(5)
		status = get_image_status(conn,image_id)
	if status == 'available':
		print "success: Image creation completed"


if __name__ == '__main__':
	main()


'''
    # Create Snapshot
    #ImageId = create_snapshot(conn, args.instance, args.name)
    #print ImageId

import time
image_id = ec2_conn.create_image(instance.id, ...)
image = ec2_conn.get_all_images(image_ids=[image_id])[0]
while image.state == 'pending':
    time.sleep(5)
    image.update()
if image.state == 'available':
     success, do something here
else:
     handle failure here
'''
