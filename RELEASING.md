# Releasing Concepticon as CLDF dataset

- Make sure the corresponding release of (the submodule) `raw/concepticon-data` is checked out.
- Re-create the CLDF data running
  ```shell
  cldfbench makecldf --with-cldfreadme cldfbench_concepticon.py --glottolog-version v4.7
  ```
- Make sure the dataset is valid running
  ```shell
  pytest
  ```
- Make sure examples in `doc/README.md` still work, in particular creation of a sqlite db.
- Adapt `CHANGELOG.md`.
- Commit the updates for this version and push updated data:
  ```shell script
  git commit -a -m"<version> release"
  git tag -a v<version> -m"release <version>"
  git push origin
  git push origin --tags
  ```
- Create a release on GitHub.