#!/bin/bash
if [[ $# -lt 2 ]] ; then 
   echo "Usage: $(basename $0) [crmap|delete|detach] [region] [instanceid]"
   exit
fi

REGION=$2
InstanceId=$3
TmpFile=/tmp/tmpfile

detach_ebs () {
  for i in $(cat $TmpFile | grep -v da1); do 
    VolID=$(echo $i | awk -F, '{print $1}')
#    Device=$(echo $i | awk -F, '{print $2}')
    SInstID=$(echo $i | awk -F, '{print $3}')
    echo -e  "$VolID\t$Device\t$SInstID"
    aws ec2 detach-volume --region $REGION --instance-id $InstanceId --volume-id $VolID  --force
  done
}

delete_ebs () {
for i in $(cat $TmpFile | grep -v da1 | awk -F, '{print $1}'); do aws ec2 delete-volume --region $REGION --volume-id $i ; done
}

create_mapfile () {
aws ec2 describe-volumes --region $REGION --filters Name=attachment.instance-id,Values=$InstanceId | jq -r '.Volumes[].Attachments[]|.VolumeId+","+.Device+","+.InstanceId' > $TmpFile
}

case $1 in 
  detach) detach_ebs ;;
  delete) delete_ebs ;;
  attach) attach_ebs ;;
  crmap) create_mapfile ;;
esac
