#!/bin/bash

DELETE_ALL_SNAPSHOTS='false'        # Should all snapshots be deleted, regardless of TTL
RM_SNAPSHOTS=''                     # List of specific snapshots to delete
FORCE_DELETE_BY_AGE='false'         # Ignore TTL expiration and delete if older than "AGE" (in TTL format).
FORCE_AGE_TTL=''                    # Used to store "age" TTL if FORCE_DELETE_BY_AGE is set.
RECURSIVE='false'
PREFIXES=''                         # List of prefixes

# FUNCTIONS
Help() {
    cat << EOF
${0##*/} v${VERSION}

Syntax:
${0##*/} destroy [ options ] zpool/filesystem ...

OPTIONS:
  -D           = Delete *all* zfsnap snapshots — regardless of their TTL
                 expiration — on all ZFS file systems that follow this option
  -F age       = Force delete all snapshots exceeding "age" — regardless
                 of their TTL expiration — on all ZFS file systems that
                 follow this option
  -h           = Print this help and exit
  -n           = Dry-run. Perform a trial run with no actions actually performed
  -p prefix    = Enable filtering to only consider snapshots with "prefix";
                 it can be specified multiple times to build a list.
  -P           = Disable filtering for prefixes.
  -r           = Operate recursively on all ZFS file systems after this option
  -R           = Do not operate recursively on all ZFS file systems after this option
  -v           = Verbose output


EOF
    exit 20
}

if [[ $# -lt 1 ]] ; then
    Help
fi

# main loop; get options, process snapshot expiration/deletion
OPTIND=1
while getopts :DF:hnp:PrRz OPT; do
    case "$OPT" in
        D) DELETE_ALL_SNAPSHOTS='true';;
        F) ValidTTL "$OPTARG" || Fatal "Invalid TTL: $OPTARG"
           [ "$OPTARG" = 'forever' ] && Fatal '-F does not accept the "forever" TTL'
           FORCE_AGE_TTL=$OPTARG
           FORCE_DELETE_BY_AGE='true'
           ;;
        h) Help;;
        n) DRY_RUN='true';;
        p) PREFIX=$OPTARG; PREFIXES="${PREFIXES:+$PREFIXES }$PREFIX";;
        P) PREFIX=''; PREFIXES='';;
        r) RECURSIVE='true';;
        R) RECURSIVE='false';;
        :) Fatal "Option -${OPTARG} requires an argument.";;
       \?) Fatal "Invalid option: -${OPTARG}.";;
    esac
done

# discard all arguments processed thus far
shift $(($OPTIND - 1))

if [ -n "$1" ]; then
    FileSystem=$1
    ZFS_SNAPSHOTS=$($ZFS list -H -o name -s name -t snapshot -r $1) >&2 || Fatal "'$1' does not exist!"
    for SNAPSHOT in $ZFS_SNAPSHOTS; do
        Info "Now processing $SNAPSHOT"
        FileSystem=${SNAPSHOT%%@*}
        SnapShotName=${SNAPSHOT##*@}
        TTL=${SnapShotName##*--}
        TTL_TYPE=$(echo -n $TTL | tail -c 1)
        TTL_VALUE=$(echo -n $TTL | sed -e '$s/\(.\{1\}\)$//' -e 's/^0*//')

        case $TTL_TYPE in
            m) SecToKeep=$(expr $TTL_VALUE \* 60);;
            h) SecToKeep=$(expr $TTL_VALUE \* 3600);;
            d) SecToKeep=$(expr $TTL_VALUE \* 86400);;
            w) SecToKeep=$(expr $TTL_VALUE \* 86400 \* 7);;
            M) SecToKeep=$(expr $TTL_VALUE \* 86400 \* 30);;
            y) SecToKeep=$(expr $TTL_VALUE \* 86400 \* 365);;
            *) Warn "TTL is not valid; Skipping to next snapshot"
               continue;;
        esac

        # convert the snapshot time in epoch seconds
        pre_date="${SnapShotName%$DATE_PATTERN*}"
        post_date="${SnapShotName##*$DATE_PATTERN}"
        snapshot_date="${SnapShotName##$pre_date}"
        snapshot_date=${snapshot_date%%$post_date}
        # Confirm date in the snapshot name is in the right format
        if ! [ -z "${snapshot_date##$DATE_PATTERN}" ] ; then
            Warn "Date is not in the Valid format. Skipping to the next snapshot"
            continue
        fi
        # Find out if the snapshot TTL has expired, delete it if expired
        date_formated=$(echo $snapshot_date|sed -e s'/_/ /' -e s'/\./:/g')
        snapshot_creaed_sec=$(date -d "$date_formated" +%s)
        snap_expire_sec=$(expr $snapshot_creaed_sec + $SecToKeep)
        cur_date_in_sec=$(date +%s)
        if [[ $cur_date_in_sec -gt $snap_expire_sec ]] ; then
            Info "Snapshot Expired.. Deleting it now"
        else
            Info "Snapshot not expired yet... Skipping"
        fi
        echo -e "\n\n\n"
    done
fi
