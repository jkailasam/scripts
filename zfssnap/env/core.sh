#!/bin/bash
#All the environment variables are functions are defined here
readonly VERSION='2.0.0.beta2'
ZFS='/sbin/zfs'
ZPOOL='/sbin/zpool'


## HELPER FUNCTIONS
Err() {
    printf '%s\n' "ERROR: $*" >&2
}

Fatal() {
    printf '%s\n' "FATAL: $*" >&2
    exit 1
}

Info() {
    printf '%s\n' "INFO: $*" >&2
}

Warn() {
    printf '%s\n' "WARNING: $*" >&2
}
