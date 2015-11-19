SYNC1="/usr/bin/boto-rsync"
RSYNC2="/usr/bin/s3cmd"
RSYNC3="/usr/bin/aws"
SOURCE="/sherlockpool/sherlock"
DEST="s3://nflx-enterprise-platforms-us-west-2/sherlock_backup"
LOG=/root/s3backup.log

echo -e "Backup to s3 started at `date` \n\n\n\n" >$LOG
#$RSYNC1 -e $SOURCE $DEST >> $LOG 2>> $LOG
#$RSYNC2 sync --server-side-encryption --delete-removed -v --multipart-chunk-size-mb=15  ${SOURCE}/ ${DEST}/ >> $LOG 2>> $LOG
$RSYNC3 s3 sync ${SOURCE}/ ${DEST}/ --sse --delete >> $LOG 2>> $LOG
echo -e "\n\n\n\nBackup completed at `date`" \n\n\n >>$LOG 2>&1
