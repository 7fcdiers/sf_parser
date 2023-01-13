rm -f .git/index.lock
git rm -r --cached .
git add .
git commit -m ".gitignore is now working"