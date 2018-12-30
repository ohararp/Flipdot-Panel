#!/usr/bin/env bash

cd $(dirname $0)

if [[ -f python-time.service ]]; then
	echo "Stopping Service..."
	systemctl stop python-time.service

	echo "Disabling Service..."
	systemctl disable $(pwd)/python-time.service || exit -1
else
	echo "Could not find python-time.service. Please run make first"
	exit -1
fi
