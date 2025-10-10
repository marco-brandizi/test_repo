# Some tricks and tips about git

*Note: git/GitHub used to create repositories with 'master' as the default branch, [now they choose 'main'](https://www.theserverside.com/feature/Why-GitHub-renamed-its-master-branch-to-main), in a questionable attempt to adopt a more inclusive terminology. I still haven't had time to update this document, so consider that where I mention 'master', you might need to use 'main' instead, or vice versa.*


## How to develop a new chunk from the main branch

* **Always, always update your clone as first step**. You don't want to make a change on code that is days, weeks, months old!
* Work locally, commit locally in a consistent way: every commit should be about one particular aspect that the commited changes are about, or at least about a small set of related changes. For example:
  * bugfix about orders not saved when product description is empty (#issueNumber)
  * introducing gene search
  * completing gene search with sequence matching
* Ideally, commit when your application builds, including that it passes the automatic tests. Although that's not as important as when you push
* When ready, push your local commits back to the main repo (eg, on github)
  * **do git pull before pushing**. If you know much might have changed, use the alignment procedure shown below, based on fetch/pull. Remember to **test again** after a merge between remote and local changes. Only do the actual push when your code is in a state of minimal working condition, ie, it builds, including automated tests.
    * Leave some comment or alike if you know some feature is still not working/incomplete. 

### How to align with your main branch

After I've made a few changes on my local clone, I usually align with the main repo (eg, on github) this way:

* If I'm sure the main repo hasn't changed or hasn't changed significantly since my last local update (via pull or alike), I do a git pull.
* Else, if I know I might have significant differences coming from the main repo, I do a git fetch, and then I compare the local version with the one marked with the branch `origin/*` (eg, `origin/main`). I recommend a visual tool to perform such comparison (eg, Eclipse Egit, Megit, SmartGit). I usually use Egit or Megit, which allow me to compare files one-by-one, side-by-side, and to merge remote changes onto local files, or even do manual edits.
* Once I'm happy with the alignment changes I've made this way on my local copy (ie, everything builds and passes the tests), I do a merge in 'hard ours' mode (see below) and finally, I commit and push such local changes.

## How I work on feature branches

General note: I usually work with small teams, We usually use a kind of [feature branch-based git workflow](https://nvie.com/posts/a-successful-git-branching-model/), that is, we normally commit/push on the main branch (we push when things are minimally working, see above), and we open feature branches for creating a new feature that will require some time before being ready for merging in the main code (some of my colleagues prefer pull request for this, even when they self-close them, the flow doesn't change much in this variant). Similarly, we open a branch for anything likely to break the main code (including deployments) for several days or longer. See [here](https://medium.com/@patrickporto/4-branching-workflows-for-git-30d0aaee7bf) for a summary about main git workflows.

For instance, when I create a new feature that I think requires a branch, I do:

* **First I update my local clone** with git pull or fetch+pull (see above)
* I open a branch, naming it YYYYMMDD-feature-summary or YYYMM-feature-summary (depending on how long I expect to work on it). The date (in that format) is important to see output from 'git branch' or 'git tag' in chronological order (and to not mess up with: when did I start that?).
* I work on the new branch for a while, filing one or more commits
* From time to time, I pull the main branch and align the feature branch with the code in main (in a way similar to 'How to align with your main branch' above).
* From time to time, I push my feature branch, mainly to let others check what I'm doing. It's not strictly necessary to push versions that work on a dev branch, but that might be useful (especially if the continuous integration system tries to build all branches).
* When I'm ready to align to 'main' (ie, I did updates and alignment with 'main' in my branch, everything works in my branch), I merge from the feature branch to 'main', using 'hard theirs' mode (see below). Eventually, I push everything upstream.
  * Beware of the impact that your new feature has on CI-deployed systems, eg, has the config format changed?
* After a while, when the feature is embedded in the code, I 'close' the branch (see below), leaving an archive tag for possibly reopening the branch.

See also: [merging and rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)


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

## Creating a repo from an existing directory

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

Name the branch you want to send up, else it will take 'master' or 'main', even if you’re on a different branch.

[Reference](http://www.mariopareja.com/blog/archive/2010/01/11/how-to-push-a-new-local-branch-to-a-remote.aspx)

See also:
  * [how to setup an upstream branch](https://devconnected.com/how-to-set-upstream-branch-on-git/)
  * [upstream tracking](https://mincong.io/2018/05/02/git-upstream-tracking/)


## Updating from upstream (aka pull from upstream)

```bash
git fetch upstream
git merge upstream/master
```

Which is more the fine-grained version of `git pull upstream`


## Changing the remote pointer

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

The option `git -s recursive -Xtheirs` isn't enough, you need the following ([reference](https://www.reddit.com/r/git/comments/bqx85v/how_do_i_overwrite_one_branch_with_another_branch/))

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

There is no such thing, but it can be emulated via conversion to tag ([reference](http://stackoverflow.com/questions/10242924/how-to-close-a-branch-without-removing-it-from-history-in-git))

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

## Amending a Commit

```bash
git commit --amend
```

and then edit the old message. If the commit is already pushed, do `git push --force [branch]`

If you need to amend an old (before the latest) message, use [this](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/changing-a-commit-message). If it's already pushed, do `git push --force` at the end, as they suggest. 

In both cases, you're rewriting the commit history when you push, so be careful and tell the collaborators.
