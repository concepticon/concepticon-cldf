<a name="ds-wordlistmetadatajson"> </a>

# Wordlist Concepticon

**CLDF Metadata**: [Wordlist-metadata.json](./Wordlist-metadata.json)

**Sources**: [sources.bib](./sources.bib)

List, Johann-Mattis and Cysouw, Michael and Forkel, Robert. 2016. Concepticon. A resource for the linking of concept lists. In Chair), Nicoletta Calzolari (Conference and Choukri, Khalid and Declerck, Thierry and Grobelnik, Marko and Maegaard, Bente and Mariani, Joseph and Moreno, Asuncion and Odijk, Jan and Piperidis, Stelios (eds.), Proceedings of the Tenth International Conference on Language Resources and Evaluation, 2393-2400. European Language Resources Association (ELRA).

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF Wordlist](http://cldf.clld.org/v1.0/terms.rdf#Wordlist)
[dc:contributor](http://purl.org/dc/terms/contributor) | <dl><dt><a href="http://purl.org/dc/terms/references">dc:references</a></dt><dd>CONTRIBUTORS.md</dd><dt><a href="http://purl.org/dc/terms/format">dc:format</a></dt><dd>text/markdown</dd></dl>
[dc:license](http://purl.org/dc/terms/license) | <dl><dt>url</dt><dd>https://creativecommons.org/licenses/by/4.0/</dd><dt>icon</dt><dd>cc-by.png</dd><dt>name</dt><dd>Creative Commons Attribution 4.0 International License</dd></dl>
[dc:publisher](http://purl.org/dc/terms/publisher) | <dl><dt>http://xmlns.com/foaf/0.1/name</dt><dd>Max Planck Institute for Evolutionary Anthropology</dd><dt><a href="http://purl.org/dc/terms/Location">dc:Location</a></dt><dd>Leipzig</dd><dt>http://xmlns.com/foaf/0.1/homepage</dt><dd>https://www.eva.mpg.de</dd><dt>http://xmlns.com/foaf/0.1/mbox</dt><dd>concepticon@eva.mpg.de</dd></dl>
[dc:relation](http://purl.org/dc/terms/relation) | http://www.lrec-conf.org/proceedings/lrec2016/summaries/127.html
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://concepticon.clld.org
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/concepticon/concepticon-cldf/tree/7bbae99">concepticon/concepticon-cldf 7bbae99</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v4.6">Glottolog v4.6</a></li><li><a href="https://github.com/concepticon/concepticon-data/tree/d7e9a39f">concepticon/concepticon-data v2.6.0-179-gd7e9a39f</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>python</strong>: 3.8.10</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | concepticon
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-glossescsv"></a>Table [glosses.csv](./glosses.csv)

Glosses (aka concept labels) in particular languages given for concepts in a concept list

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF FormTable](http://cldf.clld.org/v1.0/terms.rdf#FormTable)
[dc:extent](http://purl.org/dc/terms/extent) | 190457


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | A reference to a language (or variety) the form belongs to<br>References [languages.csv::ID](#table-languagescsv)
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | A reference to the meaning denoted by the form<br>References [concepticon.csv::ID](#table-concepticoncsv)
[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | The written expression of the form. If possible the transcription system used for the written form should be described in CLDF metadata (e.g. via adding a common property `dc:conformsTo` to the column description using concept URLs of the GOLD Ontology (such as [phonemicRep](http://linguistics-ontology.org/gold/2010/phonemicRep) or [phoneticRep](http://linguistics-ontology.org/gold/2010/phoneticRep)) as values).
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Concept_ID` | `string` | Link to the concept for which this label is used as language specific gloss.<br>References [concepts.csv::ID](#table-conceptscsv)

## <a name="table-concepticoncsv"></a>Table [concepticon.csv](./concepticon.csv)

The Concepticon - i.e. the list of concept sets to which individual concepts given in concept lists are mapped.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 3961


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | A rough gloss for a concept set, serving as convenient abbreviation of its definition.
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | A definition of the unifying aspect of the concepts grouped in the concept set.
`Semantic_Field` | `string` | A categorization of concept sets into the semantic fields defined in the Intercontinental Dictionary Series (IDS).
`Ontological_Category` | `string` | A rough ontological categorization to be used for navigating and filtering concept sets.
[Replacement_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | For superseded concept sets, this links to the concept set which replaces the one specified in this row.<br>References [concepticon.csv::ID](#table-concepticoncsv)

## <a name="table-conceptlistscsv"></a>Table [conceptlists.csv](./conceptlists.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ContributionTable](http://cldf.clld.org/v1.0/terms.rdf#ContributionTable)
[dc:extent](http://purl.org/dc/terms/extent) | 410


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | Conceptlist description formatted as CLDF markdown
[Contributor](http://cldf.clld.org/v1.0/terms.rdf#contributor) | list of `string` (separated by ` and `) | 
[Citation](http://cldf.clld.org/v1.0/terms.rdf#citation) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
[Related](http://cldf.clld.org/v1.0/terms.rdf#contributionReference) | list of `string` (separated by ` `) | Links to related conceptlists<br>References [conceptlists.csv::ID](#table-conceptlistscsv)
[PDF](http://cldf.clld.org/v1.0/terms.rdf#mediaReference) | list of `string` (separated by ` `) | References [media.csv::ID](#table-mediacsv)
`Tags` | list of `string` (separated by `; `) | References [tags.csv::ID](#table-tagscsv)
`Year` | `integer` | 
`Number_Of_Items` | `integer` | 
[Gloss_Language_IDs](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | list of `string` (separated by ` `) | Languages in which the conceptlist provides gloss labels<br>References [languages.csv::ID](#table-languagescsv)
`Target_Language` | `string` | Target language(s), i.e. language (group) from which lexical data was to be collected using the conceptlist as questionnaire
`List_Suffix` | `string` | Name suffix for disambiguation
`Source_URL` | `anyURI` | 
`Pages` | `string` | 
`Alias` | list of `string` (separated by ` `) | 
`Attributes` | list of `string` (separated by ` `) | List of names of additional attributes supplied for each concept in the list

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

Languages listed here are languages in which a concept list provides concept labels; typically major scientific languages or major languages from the region in which lexical data was collected.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 58


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal` | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal` | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string` | 

## <a name="table-relationtypescsv"></a>Table [relationtypes.csv](./relationtypes.csv)

Types of relations between concept sets.

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 14


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
`Inverse_ID` | `string` | Inverse relation<br>References [relationtypes.csv::ID](#table-relationtypescsv)

## <a name="table-conceptrelationscsv"></a>Table [conceptrelations.csv](./conceptrelations.csv)

Relations between concept sets.

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 1552


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
`Source_ID` | `string` | References [concepticon.csv::ID](#table-concepticoncsv)
`Relation_ID` | `string` | References [relationtypes.csv::ID](#table-relationtypescsv)
`Target_ID` | `string` | References [concepticon.csv::ID](#table-concepticoncsv)

## <a name="table-mediacsv"></a>Table [media.csv](./media.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF MediaTable](http://cldf.clld.org/v1.0/terms.rdf#MediaTable)
[dc:extent](http://purl.org/dc/terms/extent) | 164


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
[Media_Type](http://cldf.clld.org/v1.0/terms.rdf#mediaType) | `string` | 
[Download_URL](http://cldf.clld.org/v1.0/terms.rdf#downloadUrl) | `anyURI` | 

## <a name="table-conceptscsv"></a>Table [concepts.csv](./concepts.csv)

This table lists concepts as they appear in published concept lists. Each concept is linked to a concept list and a concept set (possibly the <NA> set).

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 115612


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
`Number` | `string` | Number of the concept within the concept list
`Index` | `integer` | 1-based index of the concept in its conceptlist
[Conceptlist_ID](http://cldf.clld.org/v1.0/terms.rdf#contributionReference) | `string` | References [conceptlists.csv::ID](#table-conceptlistscsv)
[Concepticon_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [concepticon.csv::ID](#table-concepticoncsv)
`Attributes` | `json` | 

## <a name="table-tagscsv"></a>Table [tags.csv](./tags.csv)

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 22


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 

## <a name="table-retiredcsv"></a>Table [retired.csv](./retired.csv)

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 6018


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
`Type` | `string` | 
`Replacement_ID` | `string` | 

