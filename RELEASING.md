# Releasing Concepticon as CLDF dataset

- Make sure the corresponding release of (the submodule) `raw/concepticon-data` is checked out.
- Run
  ```shell
  cldfbench download cldfbench_concepticon.py
  ```
  to fetch source documents from CDSTAR.
- Re-create the CLDF data running
  ```shell
  cldfbench makecldf --with-cldfreadme cldfbench_concepticon.py --glottolog-version v5.1
  ```
- Make sure the dataset is valid running
  ```shell
  pytest
  ```
- Make sure examples in `doc/README.md` still work, in particular creation of a sqlite db.
- Recreate the README
  ```shell
  cldfbench readme cldfbench_concepticon.py 
  ```
- Create an ER diagram:
  ```shell
  cldferd --format compact.svg cldf > doc/erd.svg
  ```
- Create a map showing the gloss languages:
  ```shell
  cldfbench cldfviz.map --format svg --pacific-centered --no-legend cldf --with-ocean --padding-bottom 5 --padding-top 5 --width 20 --language-labels
  ```
- Adapt `CHANGELOG.md`.
- Commit the updates for this version and push updated data:
  ```shell
  git commit -a -m"<version> release"
  git tag -a v<version> -m"release <version>"
  git push origin
  git push origin --tags
  ```
- Create a release on GitHub.