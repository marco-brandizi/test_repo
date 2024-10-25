# Some tricks and tips about git

## Creating a branch from local changes

```bash
git switch -c <new-branch>
```


## Downloading a branch

```bash
git checkout -b experimental origin/experimental
```

[Reference](http://stackoverflow.com/questions/67699/how-do-i-clone-all-remote-branches-with-git)

Might not work, when the branch is recent, so do this before:

```bash
git remote update
git fetch
```

## Creating a repo from an existing directory = 

```bash
git init
```

Then create it on github and it will tell you how to link the two (git remote).


## github forks

[Reference](http://help.github.com/fork-a-repo/)


## Push a branch upstream

```bash
git push -u origin branch
```

Name the branch you want to send up, else it will take master, even if you’re on a different branch.

[Reference](http://www.mariopareja.com/blog/archive/2010/01/11/how-to-push-a-new-local-branch-to-a-remote.aspx)


## Updating from upstream (aka pull from upstream)

```bash
git fetch upstream
git merge upstream/master
```

Which is more the fine-grained version of `git pull upstream`


## Changing the remote pointer == 

```bash
git remote set-url origin https://github.com/user/repo2.git
git remote -v # will show you the results
```

## Pulling a new branch

```bash
git fetch
git checkout <branch>
```


## Tags
  
[Reference](http://learn.github.com/p/tagging.html)

* List tags: `git tag`
* Add a tag: `git tag -a 'v1.3.1' -m 'Version 1.3.1'`
* Push all, tags included (not done by default): `git push --tags`

* Delete a tag on the remote repository
  * First delete it from the local repository: `git tag --delete xxx`
  * then issue: `git push --force origin :refs/tags/xxx`
 
* Checkout a given tag: `checkout tags/<tag_name>`


## Merge with "hard ours"

```bash
git merge --no-ff -s ours dev-branch
```
  
This is different than `-X ours`, cause it doesn't look at all at dev, and takes our version only.


## Merge with "hard theirs"

The option `git -s recursive -Xtheirs` isn't enough, you need the following ([reference](https://www.reddit.com/r/git/comments/bqx85v/how_do_i_overwrite_one_branch_with_another_branch/)

```bash
git checkout <branch to reset>
git reset --hard <branch to bring into this one>
```
  
At this point, it's likely you also need to pull without cancelling the above again (if you're rolling back changes coming from remote/upstream):

```bash
git merge -s ours origin/<branch to reset>
```

Now, push, and remember you'll lose the (remote) commits that changed the branch


## Closing a branch

There isn’t no such thing, but it can be simulated via conversion to tag.
[Reference](http://stackoverflow.com/questions/10242924/how-to-close-a-branch-without-removing-it-from-history-in-git)

```bash
git tag archive/<branchname> <branchname>
git branch -d <branchname>
git push origin --delete <branchname> # Propagate upstream
git push --tags # pushes archive/*
```

I've put the commands above in [this script](git-utils/archive-label.sh)

The branch will be deleted, and can be retrieved later by checking out the tag, and recreating the branch:

```bash
git checkout archive/<branchname>
git checkout -b new_branch_name
```

## Deleting a tag or branch locally, after remote deletion

Just do this for removing local branches that were deleted remotely: 

```bash
git fetch --prune
# 'git remote' has alternatives
```

## Amending a Commit ==

```bash
git commit --amend
```

and then edit the old message. If the commit is already pushed, do `git push --force [branch]`

If you need to amend an old (before the latest) message, use [this](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/changing-a-commit-message). If it's already pushed, do `git push --force` at the end, as they suggest. 

In both cases, you're rewriting the commit history when you push, so be careful and tell the collaborators.