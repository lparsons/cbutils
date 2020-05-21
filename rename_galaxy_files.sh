#!/bin/sh

for f in Galaxy*; do
    echo "mv \"${f}\" \"${f/].*.gz/.gz}\";"
done
read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi
for f in Galaxy*; do
    mv "${f}" "${f/].*.gz/.gz}";
done

for f in Galaxy*; do
    echo "mv \"${f}\" \"${f/Galaxy*-[/}\";"
done
read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi
for f in Galaxy*; do
    mv "${f}" "${f/Galaxy*-[/}";
done

