#!/usr/bin/env bash
#
# Archive a tag or branch into a tag like $archive_prefix/$label
#
# Adapted from:
#   http://stackoverflow.com/questions/10242924/how-to-close-a-branch-without-removing-it-from-history-in-git
# 

set -e # at the first error, you might want to disable, but it's dangerous 

if [[ -z "$1" ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
	echo -e "\n\n\t" $(basename $0) '[--tag|-t] <branch|tag> [<archive-prefix>]' "\n"
	exit 1
fi

is_tag=false
if [[ "$1" == '--tag' ]] || [[ "$1" == '-t' ]]; then
  is_tag=true
  shift
fi

label="$1"
archive_prefix=${2:-archive}

echo "Making the archive tag '$archive_prefix/$label'"
git tag "$archive_prefix/$label" "$label"

`$is_tag` && target=tag || target=branch
echo "Deleting $target '$label'"
git $target --delete "$label"
 
echo -e "Propagating everything upstream"
git push origin --delete "$label"
git push --tags 

echo -e "That's all!"
