# Renames the local branch named `old`` to `new``, fetches the latest changes from `origin``, sets the upstream branch for the local branch to the remote branch , and sets the default branch for the remote to `new`.
git branch -m old new
git fetch origin
git branch -u origin/new new
git remote set-head origin -a # only needed if the old branch was the default branch for the remote
