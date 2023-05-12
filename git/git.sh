# un-commit last commit
git reset --soft HEAD~

git remote set-url origin https://github.com/ultratesting/great-expectations-utilities.git

# push repo to different remote: https://stackoverflow.com/questions/5181845/git-push-existing-repo-to-a-new-and-different-remote-repo-server
# Create a new repo at github.
# Clone the repo from fedorahosted to your local machine.
git remote rename origin upstream
git remote add origin URL_TO_GITHUB_REPO
git push origin master

# list remotes
git remote -v
