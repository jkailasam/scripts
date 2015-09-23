#!/bin/bash 
# this script creates volume from AMI and attached it to an Instnace

if [[ $# -ne 2 ]] ; then 
   echo "Usage: $(basename $0) [Image-id] [instanceid]"
   exit
fi

ImgId=$1
InstanceId=$2
TmpFile=/tmp/snapfile


REGION=us-west-2
AZ=us-west-2c
type=gp2

aws ec2 describe-images --region us-west-2 --image-ids $ImgId | jq -r '.Images[].BlockDeviceMappings[]|.DeviceName+","+.Ebs.SnapshotId' > $TmpFile

for i in $(cat $TmpFile); do 
   DevId=$(echo $i | awk -F, '{print $1}')
   SnapId=$(echo $i | awk -F, '{print $2}')
   VolId=$(aws ec2 create-volume --region $REGION --availability-zone $AZ --snapshot $SnapId --volume-type $type  | jq -r .VolumeId)
   sed -ie "/$SnapId/s/$/,$VolId/" $TmpFile
done

sleep 20

for i in $(cat $TmpFile); do
   DevId=$(echo $i | awk -F, '{print $1}')
   VolId=$(echo $i | awk -F, '{print $3}')
   echo aws ec2 attach-volume --region $REGION --instance-id $InstanceId --device $DevId --volume-id $VolId
   aws ec2 delete-volume --region $REGION --volume-id $VolId
done
