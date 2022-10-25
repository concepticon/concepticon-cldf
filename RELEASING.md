# Releasing Concepticon as CLDF dataset

1. Make sure the corresponding release of (the submodule) `raw/concepticon-data` is checked out.
2. Re-create the CLDF data running
   ```shell
   cldfbench makecldf --with-cldfreadme cldfbench_concepticon.py --glottolog-version v4.6
   ```
3. Make sure the dataset is valid running
   ```shell
   pytest
   ```