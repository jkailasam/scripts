#!/bin/bash

## This script takes snapshots
PREFIX=''                           # Default prefix

# FUNCTIONS
Help() {
    cat << EOF
${0##*/} v${VERSION}

Syntax:
${0##*/} snapshot [ options ] zpool/filesystem ...

OPTIONS:
  -a ttl       = How long the snapshot(s) should be kept (default: 1 month)
  -h           = Print this help and exit
  -n           = Dry-run. Perform a trial run with no actions actually performed
  -p prefix    = Prefix to use when naming snapshots for all ZFS file
                 systems that follow this option
  -P           = Dont apply any prefix when naming snapshots for all ZFS
                 file systems that follow this option
  -r           = Create recursive snapshots for all ZFS file systems that
                 follow this option
  -R           = Create non-recursive snapshots for all ZFS file systems that
                 follow this option
  -v           = Verbose output
  -z           = Round snapshot creation time down to 00 seconds

EOF

}

if [[ $# -lt 1 ]] ; then
    Help
fi

# main loop; get options, process snapshot creation
while [ "$1" ]; do
    OPTIND=1
    while getopts :a:hnp:PrRz OPT; do
        case "$OPT" in
            a) ValidTTL "$OPTARG" || Fatal "Invalid TTL: $OPTARG"
               TTL=$OPTARG
               ;;
            h) Help;;
            n) DRY_RUN='true';;
            p) PREFIX=$OPTARG;;
            P) PREFIX='';;
            r) ZOPT='-r';;
            R) ZOPT='';;
            z) TIME_FORMAT='%Y-%m-%d_%H.%M.00';;
            :) Fatal "Option -${OPTARG} requires an argument.";;
           \?) Fatal "Invalid option: -${OPTARG}.";;
        esac
    done

    # discard all arguments processed thus far
    shift $(($OPTIND - 1))

    # create snapshots
    if [ "$1" ]; then
        FSExists "$1" || Fatal "'$1' does not exist!"
        CURRENT_DATE=${CURRENT_DATE:-`date "+$TIME_FORMAT"`}
        ZFS_SNAPSHOT="$ZFS_CMD snapshot $ZOPT ${1}@${PREFIX}${CURRENT_DATE}--${TTL}"
        if IsFalse "$DRY_RUN"; then
            if $ZFS_SNAPSHOT >&2; then
                printf '%s ... DONE\n' "$ZFS_SNAPSHOT"
            else
                printf '%s ... FAIL\n' "$ZFS_SNAPSHOT"
            fi
        else
            printf '%s\n' "$ZFS_SNAPSHOT"
        fi

        shift
    fi
done
