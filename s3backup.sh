#!/bin/bash
RSYNC1="/usr/bin/boto-rsync"
RSYNC2="/usr/bin/s3cmd"
SOURCE="/sherlockpool/sherlock"
DEST="s3://nflx-rsync-us-west-2/EnterprisePlatforms/sherlock_backup"
LOG=/root/s3backup.log

echo -e "Backup to s3 started at `date` \n\n\n\n" >$LOG
#$RSYNC1 -e $SOURCE $DEST >> $LOG 2>> $LOG
$RSYNC2 --server-side-encryption --delete-removed -v --multipart-chunk-size-mb=15  ${SOURCE}/ ${DEST}/ >> $LOG 2>> $LOG
echo -e "\n\n\n\nBackup completed at `date`" \n\n\n >>$LOG 2>&1
