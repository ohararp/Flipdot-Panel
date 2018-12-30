#!/usr/bin/env bash

cd $(dirname $0)

if [[ -f python-time.service ]]; then
	echo "Enabling Service..."
	systemctl enable $(pwd)/python-time.service || exit -1

	echo "Starting Service..."
	systemctl start python-time.service
	systemctl status python-time.service
else
	echo "Could not find python-time.service. Please run make first"
	exit -1
fi
