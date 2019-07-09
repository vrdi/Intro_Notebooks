---
title: Intro Git Lunch Session
author: 
- Parker Rule
- (Notes by Lee Hachadoorian)
date: July 9, 2019
---

# Some Definitions

Repository: "Repo" for short. Collection of files for a specific project.

Commit: Atomic unit of work. Delta is the difference between new files and old files. Project's commit history is almost a lab notebook, so write nice descriptive commit messages.

Branch: Pointer to a specific state after a commit.

Master Branch: Pointer to latest working version of your project.

# Git Sample Workflow

Begin by cloning a repo. Cloning will make a local copy of a remote repo. Run these commands in the terminal (command prompt on Windows).

```
git clone https://github.com/vrdi/git-lunch-session
```

List files in the current folder:

* Windows: `dir`
* Mac/Linux: `ls`

Set user name and email for the repo. If you are using GitHub, email must be address associated with your GitHub account.

```
git config user.name "Lee Hachadoorian"
git config user.email "Lee.Hachadoorian@gmail.com"
```

You will make your changes (adding, editing, or deleting files) in a **branch**. Begin by creating a branch using your name.

```
# Create branch
git branch <branch-name>

# View branches. Active branch has star (*) next to it
git branch

# Checkout the branch you want to work in.
git checkout <branch-name>
```

The example repo includes a Python script **names.py**. Open up **names.py** and add the line `print("Your name")`.


```
# What's the current state of the repo?
git status

# Add file to git for tracking:
git add .

# Or git add a specific file:
git add names.py
```

Now commit your changes. Commits *require* a message. Message is given in quotes after -m flag.

> TIP: It is a best practice to start commit messages with a present tense verb.

```
git commit -m "Add my print statement"
```

Push changes to centralized repo. `origin` is a label for the remote repo. The name is arbitrary, but `origin` is conventional, and was created by default when you cloned the repo. `<branch-name>` is the name of the branch to push to on the remote, and should match the branch that you have checked out. In this case, you have been asked to create a branch with your name.


```
git push origin <branch-name>
```

Once pushed, you can go to GitHub and you will see the new branch. In order to merge this branch, you will create a pull request (PR). When you create a PR, the **base** branch is the one you want to merge your work into (usually `master`). The **compare** branch is the one with the new work.

When creating a PR, you may change the message so that it makes sense within the broader project (i.e., don't have to keep the commit message), and you should add a detailed comment. Do not merge your own PRs! PRs should be reviewed by at one other developer on your team.

When the remote has been updated, you will need to pull the changes to your local repo. You usually only want to pull changes that have been committed to `master`. On your local, you first need to check out master, then pull changes.

```
git checkout master
git pull origin master
```

