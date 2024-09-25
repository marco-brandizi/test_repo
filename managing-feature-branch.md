# Notes about developing in a feature branch

An example of how to manage development in a feature branch, how to periodically re-align the feature branch and how to do a final merge back to the master.

This is based on a versioning modelling in which master is the dev branch and we open/close feature branches to develop disrupting features separately.

*See also: [my git cheat sheet](git-cheat-sheet.md)*

## Update your feature branch with most recent changes in master

```bash
# The dev branch
# 
$ git checkout 2024-test-branch

# We have committed and pushed changes in this branch and also
# other changes were pushed to master
# Let's align this branch to the latest master
# 
$ git merge --no-ff master
Merge made by the 'ort' strategy.
 test-new-file.txt | 2 ++
 1 file changed, 2 insertions(+)
```

`--no-ff` allows to record the operation with an actual merge, rather than re-basing. This is usefully visible in `git --log`.

The merge went fine, **but in real life you don't want to do it this way**: use an IDE, use their graphical comparison tool and check the difference **maually and carefully**.

You might want first to compare your branch with master, then make changes manually (for instance, the Eclipse egit tool allows me to overwrite a file in my dev branch with the version in master), ignore certain master changes cause they won't apply to the new feature anymore, and all that jazz.

**Important**: if you change your dev branch manually, you'll end up in a situation where the good version you want is the one in your branch, so you can merge master in it
via this variant:

```bash
$ git merge --no-ff -s ours master
```

This is "hard ours", it's different than `-X ours`, cause it doesn't look at all at the master branch (the merge source), and takes our version only. It just marks the commit history with a merge that is visible via `git log`, which can be useful to keep track of what happened.
 
 
Eventually, test, test, test, and test again your aligned dev branch (we're still under it). When you're happy with the master-aligned branch, push the alignment back to github:

```bash
$ git push
```

This re-alignment and test in the dev/feature branch could happen multiple times during the development of a feature (or alike) on the side.

Eventually, we'll be ready for merging the dev branch back to master.


## Merging a feature branch back to master

**Ensure no change happens on GH/master while you're doing the following**. If it happens, you'll have incoming changes to merge as soon as you do `git pull` (as usually, this might be split into: 1) `git fetch` 2) compare the local master to origin/master 3) merge). 

 
```bash
$ git checkout master

# Possibly, mark the pre-merge commit with a tag. If you don't do this, a date can usually
# be used to identify the last commit before merge

$ git tag 20240614-pre-merge-from-test-branch
$ git push --tag # pushes the tag to GH

# 'Hard theirs': this aligns master to the dev branch. This contains the new feature + the latest master version
# ==> WARNING: this OVERWRITES everything you had on master
#
$ git reset --hard 2024-test-branch

# Here, it might be worth to test it again
```

`git reset` doesn't make the reset stable, without the following merge, "git pull" would overwrite everything back again to the last github commit about master. So, do this:

```bash
# As said above, --no-ff is recommended, so that it creates a merge commit even when the master history could
# be rebased, it allows you to give a message to the merge commit, which remains in the commit
# history
# 
$ git merge --no-ff -s ours origin/master

# Finally, push upstream (to master)
$ git push
```

You can see what happened, your IDE is usually a much better GUI to inspect this:

```bash
# The trunk on the left is master, the one on the right is the dev branch, which diverged and then re-joined master
# during the last commit.
#

$ git log --graph

*   commit fe1b46ff2d635a541179d6ca3509f0a669040e13 (HEAD -> master, origin/master, origin/HEAD, origin/2024-test-branch, 2024-test-branch)
|\  Merge: 1708ba6 f629b4c
| | Author: Marco Brandizi <marco.brandizi@gmail.com>
| | Date:   Fri Jun 14 10:34:57 2024 +0100
| |
| |     Merge branch 'master' into 2024-test-branch
| |
| * commit f629b4c882b7d549434b105d087c481952be7262 (tag: 20240614-pre-merge-from-test-branch)
| | Author: Marco Brandizi <marco.brandizi@gmail.com>
| | Date:   Fri Jun 14 10:34:00 2024 +0100
| |
| |     Testing merge/back-merge.
| |
* | commit 1708ba63bbee55f5b24c0e9698dab98e24a60e22
|/  Author: Marco Brandizi <marco.brandizi@gmail.com>
|   Date:   Fri Jun 14 10:23:49 2024 +0100
|
|       Testing merge/back-merge.
|
```

**Ensure** your master still works! That is: CI builds and deploys correctly, test instances are fine.


## "Closing" a branch 

**Don't delete inactive branches**, archive them as described in the follow. This keeps track of the fact they existed, it's visible in the log tree and allows for reopening branches if it becomes necessary in future.

After a while, you might want to "archive" the feature branch. git hasn't such a feature, but it can be emulated as follow. **You can use [this script](git-utils/archive-label.sh)** for doing the same:

```bash
# Tag the to-be-archived branch, ie, a tag is attached to its last commit.
# The 'archive/' prefix is purely conventional, it doesn't have any particular
# meaning for git or github
$ git tag archive/2024-test-branch 2024-test-branch

# Now you can delete the branch and leave the tag in its place
git branch -d 2024-test-branch
git push origin --delete 2024-test-branch # Propagate upstream
git push --tags # pushes archive/* too
```

The branch will be deleted and "closed/archived". If needed, it can be "re-opened" later by checking out the tag, and recreating the branch:

```bash
$ git checkout archive/2024-test-branch
$ git checkout -b 2024-test-branch
```

Tags can be archived too (ie, renamed archive/xxx) with a similar technique).

