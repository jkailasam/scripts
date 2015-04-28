#!/bin/bash
RSYNC="/usr/bin/boto-rsync"
SOURCE="/pool01/test"
DEST="s3://bucketname/dirname"
LOG=/root/s3backup.log

echo -e "Backup to s3 started at `date` \n\n\n\n" >$LOG
$RSYNC $SOURCE $DEST >> $LOG 2>> $LOG
echo -e "\n\n\n\nBackup completed at `date`" \n\n\n >>$LOG 2>&1
#boto-rsync  /pool01/csinternalkb s3://csknowledgebase/internalkb
