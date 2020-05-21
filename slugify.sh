#!/usr/bin/env sh
while read line
do
	SLUGIFIED="$(echo -n "${line}" | sed -e 's/[^[:alnum:]]/-/g' \
		| tr -s '-' | tr A-Z a-z)"
	echo $SLUGIFIED
done
