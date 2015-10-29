#!/bin/bash -x
# this script  deletes the  AMI and corresponding disk images

if [[ $# -ne 3 ]] ; then
   echo "Usage: $(basename $0) [Image-id] [instanceid] [region]"
   exit
fi

ImgId=$1
InstanceId=$2
Region=$3
TmpFile=/tmp/snapfile

AZ=$3
REGION="${AZ%?}"
type=gp2

aws ec2 describe-images --region $Region --image-ids $ImgId | jq -r '.Images[].BlockDeviceMappings[].Ebs.SnapshotId' > $TmpFile

## de-register Image
aws ec2 deregister-image --image-id ImgId

for i in $(cat $TmpFile|egrep -v null); do
	aws ec2 delete-snapshot --region $Region --snapshot-id $i
done

 
