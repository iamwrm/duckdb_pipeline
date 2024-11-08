git init
git add .
git commit -m "Initial commit with all files"
# git diff --binary --full-index --no-prefix /dev/null > all_files.patch
git format-patch --root -o .
rm -rf .git
