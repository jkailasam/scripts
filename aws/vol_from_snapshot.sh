#!/bin/bash
# this script creates volume from AMI and attach it to an existing Instnace

if [[ $# -ne 3 ]] ; then
   echo "Usage: $(basename $0) [Image-id] [instanceid] [availability-zone]"
   exit
fi

ImgId=$1
InstanceId=$2
TmpFile=/tmp/snapfile

AZ=$3
REGION="${AZ%?}"
type=gp2

aws ec2 describe-images --region us-west-2 --image-ids $ImgId | jq -r '.Images[].BlockDeviceMappings[]|.DeviceName+","+.Ebs.SnapshotId' > $TmpFile

for i in $(cat $TmpFile|grep -v da1); do
   DevId=$(echo $i | awk -F, '{print $1}')
   SnapId=$(echo $i | awk -F, '{print $2}')
   VolId=$(aws ec2 create-volume --region $REGION --availability-zone $AZ --snapshot $SnapId --volume-type $type  | jq -r .VolumeId) \
   && echo "$VolId created"
   sed -ie "/$SnapId/s/$/,$VolId/" $TmpFile
done

sleep 30

for i in $(cat $TmpFile | grep -v da1); do
   DevId=$(echo $i | awk -F, '{print $1}')
   VolId=$(echo $i | awk -F, '{print $3}')
   aws ec2 attach-volume --region $REGION --instance-id $InstanceId --device $DevId --volume-id $VolId
   #aws ec2 delete-volume --region $REGION --volume-id $VolId
done
