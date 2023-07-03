#!/usr/bin/env bash
cd "${0%/*}"
source .v/bin/activate
while :; do
	python3 ./jarvis.py
	sleep .1
done
