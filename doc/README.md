# Using Concepticon data from the CLDF dataset

[CLDF](https://cldf.clld.org) is package format for linguistic data, bundling a set of tables as CSV files
with JSON metadata, describing - among other things - relations between these tables.

First, familiarize yourself with the data model by looking through [cldf/README.md](../cldf/README.md).


## It's all just text files!

The files in a CLDF dataset are just text files (even though the text may comply with "higher-level" formatting
rules like CSV or JSON). Thus, basic exploration of the data can easily be done with the tools available in the
[Unix Shell](https://swcarpentry.github.io/shell-novice/).

```shell
$ ls -1 cldf
concepticon.csv
conceptlists.csv
conceptrelations.csv
concepts.csv
CONTRIBUTORS.md
glosses.csv
languages.csv
media.csv
README.md
relationtypes.csv
requirements.txt
retired.csv
sources.bib
tags.csv
Wordlist-metadata.json
```

```shell
$ wc -l cldf/languages.csv 
59 cldf/languages.csv
```

```shell
$ head -n 2 cldf/languages.csv 
ID,Name,Macroarea,Latitude,Longitude,Glottocode,ISO639P3code
afrikaans,Afrikaans,,-22.0,30.0,,
```


## Most of these are tables, though!

While the standard Unix tools can get you a long way towards parsing tabular data formatted as CSV, tools like the
ones provided by [csvkit](https://csvkit.readthedocs.io/en/latest/) will make this a lot easier.

E.g. you could list all english glosses mapped to [FIRE](https://concepticon.clld.org/parameters/221) running
```shell
$ csvgrep -c Parameter_ID -r "^221$" cldf/glosses.csv | csvcut -c Language_ID,Form | sort | uniq -i | grep english
english,*fire
english,fire
english,fire 
english,fire*
english,fire-
english,Fire
english,"FIRE, (FIREWOOD)"
english,fire (for cooking)/heat
english,fire (n.)
english,the fire
```

Note that the gloss `FIRE, (FIREWOOD)` contains a comma, hence naively trying to split columns by splitting text lines
at commas would have failed.


## Related tables, that is.

If we wanted to list concepts of a conceptlist with gloss and mapped Concepticon gloss, we'd have to join data from
two tables: `glosses.csv` and `concepticon.csv` (and exploit the fact that gloss identifiers are based on the 
conceptlist identifiers):

```shell
$ csvjoin cldf/glosses.csv cldf/concepticon.csv -c Parameter_ID,ID | csvcut -c Form,Concept_ID,Name | csvgrep -c Concept_ID -m"Swadesh-1955-100"
Form,Concept_ID,Name
all,Swadesh-1955-100-1,ALL
bone,Swadesh-1955-100-10,BONE
yellow,Swadesh-1955-100-100,YELLOW
*breast,Swadesh-1955-100-11,BREAST
burn,Swadesh-1955-100-12,BURN
*claw,Swadesh-1955-100-13,CLAW
cloud,Swadesh-1955-100-14,CLOUD
...
```

Now, if we wanted to do this "properly", i.e. use only the conceptlist identifier `Swadesh-1955-100` as input, we'd
have to join data from `concepts.csv`, too, which gets a bit cumbersome on the shell. But CLDF contains all the
information necessary to load a dataset into a relational database - and the [pycldf](https://github.com/cldf/pycldf)
package can turn any CLDF dataset into a [SQLite](https://sqlite.com/index.html) database, which can be queried
more comfortably using SQL.

```shell
$ cldf createdb cldf/Wordlist-metadata.json concepticon.sqlite
INFO    <cldf:v1.0:Wordlist at cldf> loaded in concepticon.sqlite
```

Now we can list the concepts of a conceptlist much like the web app does 
(e.g. at https://concepticon.clld.org/contributions/Swadesh-1955-100), running a query like
```sql
SELECT c.cldf_id, ft.cldf_form, pt.cldf_name FROM
  ContributionTable as ct,
  `concepts.csv` as c,
  FormTable as ft,
  ParameterTable as pt
WHERE
  ct.cldf_id = c.cldf_contributionReference AND
  ft.Concept_ID = c.cldf_id AND
  pt.cldf_id = ft.cldf_parameterReference AND
  ct.cldf_id = 'Swadesh-1955-100'
ORDER BY
  c.`Index`
```
via
```shell
$ sqlite3 concepticon.sqlite -header < query.sql
```
to get

cldf_id|cldf_form|cldf_name
--- | --- | ---
Swadesh-1955-100-1|all|ALL
Swadesh-1955-100-2|ashes|ASH
Swadesh-1955-100-3|bark|BARK
Swadesh-1955-100-4|belly|BELLY
Swadesh-1955-100-5|big|BIG
... | ... | ...
