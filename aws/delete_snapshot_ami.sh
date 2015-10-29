#!/bin/bash -x
# this script  deletes the  AMI and corresponding disk images

if [[ $# -ne 2 ]] ; then
   echo "Usage: $(basename $0) [Image-id] [region]"
   exit
fi

ImgId=$1
Region=$2
TmpFile=/tmp/snapfile

aws ec2 describe-images --region $Region --image-ids $ImgId | jq -r '.Images[].BlockDeviceMappings[].Ebs.SnapshotId' > $TmpFile

## de-register Image
aws ec2 deregister-image --image-id $ImgId

sleep 10
for i in $(cat $TmpFile|egrep -v null); do
	aws ec2 delete-snapshot --region $Region --snapshot-id $i
done

 
