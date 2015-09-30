#!/usr/bin/python
import boto.ec2
import argparse
import time
#import boto.utils

def create_ami(conn, instance_id, name):
	response = conn.create_image(instance_id,name,no_reboot=True)
	print "Image {image} creation started".format(image=response.id)
	return response.id

def parsed_args():
	parser = argparse.ArgumentParser(description='Create and and copy AMI Image.')
	parser.add_argument('-r', '--region',required=True)
	parser.add_argument('-i', '--instance',required=True)
	parser.add_argument('-n', '--name',required=True)
	#parser.add_argument('-d', '--device',)
	return parser.parse_args()

def get_image_status(conn, ImageId):
	image = conn.get_all_images(image_ids=[ImageId])[0]
	return image.state

def main():
	args = parsed_args()
	print args.region
	print args.instance
	print args.name
	#print args.device
	conn = boto.ec2.connect_to_region(args.region)
	Image_id = create_snapshot(conn, args.instance, args.name)
	print Image_id



#	#ImageId = create_snapshot(conn, args.instance, args.name)
#	images = conn.get_all_images()
#	image = images[0]
#	#image = conn.get_all_images(image_ids=[ImageId])[0]
#	while image.state == 'pending':
#		time.sleep(10)
#		image.update()
#	if image.state == 'available':
#		print "Image is ready and available"
#		print (time.strftime("%H:%M:%S"))
#	else:
#		print "Something Wrong... Please check"




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
