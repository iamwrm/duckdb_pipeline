git init
git add .
git commit -m "Initial commit with all files"
git format-patch --root -o .
rm -rf .git
