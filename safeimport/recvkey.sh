#!/usr/bin/env sh
# A small shell-script to receive keys from a keyserver reasonably safely.
# Author: David Leon Gil
# License: CC0, attribution kindly requested
fp="$(printf ${1} | tr -d \ )"&&
touch ./${fp}.pubring.tmp&&
touch ./${fp}.secring.tmp&&
2>&1 gpg --keyserver pool.sks-keyservers.net --keyring ./${fp}.pubring.tmp --secret-keyring ./${fp}.secring.tmp --recv-keys ${fp}|tee -a ./${fp}.recvlog&&
gpg --keyring ./${fp}.pubring.tmp --export ${fp} > ./${fp}.pubkey&&
2>&1 gpg --import ./${fp}.pubkey|tee -a ./${fp}.importlog&&
touch ./${fp}.pubring&&
2>&1 gpg --keyring ./${fp}.pubring --import ./${fp}.pubkey&&
tar -czvf ./${fp}_log.tgz ./${fp}.*&&
rm ./${fp}.*
