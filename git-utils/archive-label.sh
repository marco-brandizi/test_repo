#!/usr/bin/env bash
#
# Archive a tag or branch into a tag like $archive_prefix/$label
#
# Adapted from:
#   http://stackoverflow.com/questions/10242924/how-to-close-a-branch-without-removing-it-from-history-in-git
# 

set -e # at the first error, you might want to disable, but it's dangerous 

is_tag=false
is_local_only=false
archive_prefix=archive

# Parse the CLI options
# 
while [[ $# -gt 0 ]]
do
	opt_name="$1"
  case $opt_name in
  	# WARNING: these '--:' special markers are used by --help to generate explanations about the available
  	# options.

  	#--: The label parameter refers to a tag, rather than a branch.
  	--tag)
  		is_tag=true; shift 1;;
  	#--: Doesn't push the archive tag upstream, keeps it in the local clone only.
  	--local)
  		is_local_only=true; shift 1;;
		#--: The prefix to use for the archive tag (default: 'archive').
		--archive-prefix)
			archive_prefix="$2"; shift 2;;
  	#--: yields this help output and then exits with 1
  	--help|-h)
  		echo -e "\n"
  		# Report the options
  		cat <<EOT


==== Branch/Tag Archiver ====
 
Usage: $0 [options] <branch|tag> [archive_prefix]

	<branch|tag>      The branch or tag to archive
	[archive_prefix]  (optional) The prefix to use for the archive tag (default: 'archive')

=== Options:
	
EOT

			egrep -i '(#\-\-:|\-\-[a-z,0-9,-,_].+\))' "$0" | sed s/'^\s*#\-\-:/#/g' | sed -E s/'^\s+(\-\-.+)\)'/'\1\n'/g
  		exit 2;;
  	--*)
			echo -e "\n\n\tERROR: Invalid option '$1', try --help\n"
  		exit 1;;
  	*)
  		shift;;
	esac
done


label="$1"

git_cmd="git"
# git_cmd="echo git" # Debug


echo "Making the archive tag '$archive_prefix/$label'"
$git_cmd tag "$archive_prefix/$label" "$label"

`$is_tag` && target=tag || target=branch
echo "Deleting $target '$label'"
$git_cmd $target --delete "$label"
 
echo -e "Propagating everything upstream"
$git_cmd push origin --delete "$label"
`$is_local_only` || $git_cmd push --tags
echo -e "That's all!"
