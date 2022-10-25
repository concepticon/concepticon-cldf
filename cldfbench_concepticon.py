import re
import shutil
import decimal
import pathlib
import functools
import subprocess
import collections

from cldfbench import Dataset as BaseDataset, CLDFSpec
from pycldf.sources import Sources, Source
from clldutils.markup import MarkdownLink
from clldutils.jsonlib import load, dump
from pyconcepticon import Concepticon
from pyconcepticon.models import Languoid
from pybtex.database import parse_string
from rfc3986 import URIReference

# FIXME: The following should probably go into Glottolog.
COORDS = {
    'southafricanenglish': (-32.47, 25.39),
    'northamericanenglish': (39.10, -101.80),
    'lebanesearabic': (33.96, 35.49),
}


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "concepticon"

    def cldf_specs(self):
        return CLDFSpec(
            dir=self.cldf_dir,
            module='Wordlist',
            data_fnames=dict(
                ParameterTable='concepticon.csv',
                FormTable='glosses.csv',
                ContributionTable='conceptlists.csv',
            )
        )

    def cmd_download(self, args):
        subprocess.check_call(
            'git -C {} pull --recurse-submodules'.format(self.dir.resolve()), shell=True)

    def cmd_readme(self, args):
        desc = """
This CLDF dataset provides the data of the corresponding release of
[concepticon/concepticon-data](https://github.com/concepticon/concepticon-data) as CLDF Wordlist.
It is intended to replace the former method of accessing Concepticon data via `pyconcepticon`
with the various data access options available with [CLDF](https://github.com/cldf/cookbook/).
For some guidance on how to do that, see the examples in [doc](doc/).
"""
        pre, head, post = super().cmd_readme(args).partition('## CLDF ')
        return pre + desc + head + post

    def schema(self, cldf, api):
        t = cldf.add_component('LanguageTable')
        t.common_props['dc:description'] = \
            "Languages listed here are languages in which a concept list provides concept labels;" \
            " typically major scientific languages or major languages from the region in which " \
            "lexical data was collected."
        cldf.add_columns(
            'ParameterTable',
            {
                "name": "Semantic_Field",
                "dc:description": "A categorization of concept sets into the semantic fields defined"
                                 " in the Intercontinental Dictionary Series (IDS).",
                "datatype": {
                    "base": "string",
                    "format": "|".join(re.escape(s) for s in api.vocabularies['SEMANTICFIELD'])}
            },
            {
                "name": "Ontological_Category",
                "dc:description": "A rough ontological categorization to be used for navigating "
                                  "and filtering concept sets.",
                "datatype": {
                    "base": "string",
                    "format": "|".join(
                        re.escape(s) for s in api.vocabularies['ONTOLOGICAL_CATEGORY'])}
            },
            {
                "name": "Replacement_ID",
                "dc:description": "For superseded concept sets, this links to the concept set "
                                  "which replaces the one specified in this row.",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#parameterReference"
            }
        )
        cldf['ParameterTable', 'Name'].common_props['dc:description'] = \
            "A rough gloss for a concept set, serving as convenient abbreviation of its definition."
        cldf['ParameterTable', 'Description'].common_props['dc:description'] = \
            "A definition of the unifying aspect of the concepts grouped in the concept set."
        cldf['ParameterTable'].common_props['dc:description'] = \
            "The Concepticon - i.e. the list of concept sets to which individual concepts given " \
            "in concept lists are mapped."
        t = cldf.add_table(
            'relationtypes.csv',
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id"},
            {
                "name": "Description",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#description"},
            {
                "name": "Inverse_ID",
                "dc:description": "Inverse relation"},
        )
        t.common_props['dc:description'] = "Types of relations between concept sets."
        cldf.add_foreign_key('relationtypes.csv', 'Inverse_ID', 'relationtypes.csv', 'ID')
        t = cldf.add_table(
            'conceptrelations.csv',
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id"},
            {"name": "Source_ID"},
            {"name": "Relation_ID"},
            {"name": "Target_ID"},
        )
        t.common_props['dc:description'] = "Relations between concept sets."
        cldf.add_foreign_key('conceptrelations.csv', 'Source_ID', 'ParameterTable', 'ID')
        cldf.add_foreign_key('conceptrelations.csv', 'Relation_ID', 'relationtypes.csv', 'ID')
        cldf.add_foreign_key('conceptrelations.csv', 'Target_ID', 'ParameterTable', 'ID')
        cldf.add_columns(
            'ContributionTable',
            {
                "name": "Source",
                "separator": ";",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source"},
            {
                "name": "Related",
                "separator": " ",
                "dc:description": "Links to related conceptlists",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#contributionReference"},
            {
                "name": "PDF",
                "separator": " ",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#mediaReference"},
            {
                "name": "Tags",
                "separator": "; "},
            {"name": "Year", "datatype": "integer"},
            {"name": "Number_Of_Items", "datatype": "integer"},
            {
                "name": "Gloss_Language_IDs",
                "separator": " ",
                "dc:description": "Languages in which the conceptlist provides gloss labels",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#languageReference"},
            {
                "name": "Target_Language_ID",
                "dc:description": "Target language, i.e. language (grouo) from which lexical data "
                                  "was to be collected using the conceptlist as questionnaire",
            },
            {"name": "List_Suffix", "dc:description": "Name suffix for disambiguation"},
            {"name": "Source_URL", "datatype": "anyURI"},
            {"name": "Pages"},
            {"name": "Alias", "separator": " "},
            {
                "name": "Attributes",
                "separator": " ",
                "dc:description": "List of names of additional attributes supplied for each "
                                  "concept in the list"},
        )
        cldf['ContributionTable', 'Description'].common_props['dc:format'] = 'text/markdown'
        cldf['ContributionTable', 'Description'].common_props['dc:description'] = \
            'Conceptlist description formatted as CLDF markdown'
        cldf['ContributionTable', 'Contributor'].separator = ' and '
        cldf.add_component('MediaTable')
        cldf.add_columns(
            'FormTable',
            {
                "name": "Concept_ID",
                "dc:description": "Link to the concept for which this label is used as "
                                  "language specific gloss.",
            }
        )
        cldf.remove_columns('FormTable', 'Segments', 'Comment')
        cldf['FormTable'].common_props['dc:description'] = \
            "Glosses (aka concept labels) in particular languages given for concepts in a " \
            "concept list"
        t = cldf.add_table(
            'concepts.csv',
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id"},
            {
                "name": "Number",
                "dc:description": "Number of the concept within the concept list"},
            {
                "name": "Index",
                "datatype": "integer",
                "dc:description": "1-based index of the concept in its conceptlist"},
            {
                "name": "Conceptlist_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#contributionReference"},
            {
                "name": "Concepticon_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#parameterReference"},
            {
                "name": "Attributes",
                "datatype": "json"},
        )
        t.common_props['dc:description'] = \
            "This table lists concepts as they appear in published concept lists. Each " \
            "concept is linked to a concept list and a concept set (possibly the <NA> set)."
        cldf.add_foreign_key('FormTable', 'Concept_ID', 'concepts.csv', 'ID')
        cldf.add_table(
            'tags.csv',
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id"},
            {
                "name": "Description",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#description"},
        )
        cldf.add_foreign_key('ContributionTable', 'Tags', 'tags.csv', 'ID')
        cldf.add_table(
            'retired.csv',
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id"},
            {
                "name": "Comment",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#comment"},
            'Type',
            'Replacement_ID',
        )

    def cmd_makecldf(self, args):
        cdata = self.raw_dir / 'concepticon-data'
        api = Concepticon(cdata)
        self.schema(args.writer.cldf, api)

        for key, entry in parse_string(api.bibfile.read_text(encoding='utf8'), 'bibtex').entries.items():
            src = Source.from_entry(key, entry)
            src = Source(src.genre.lower(), src.id, **{k.lower(): v for k, v in src.items()})
            args.writer.cldf.sources.add(src)

        args.writer.cldf.properties.update({
            k: v for k, v in load(cdata / 'metadata.json').items()
            if not k.startswith('@')})
        src = args.writer.cldf.sources['List2016a']
        args.writer.cldf.properties['dc:description'] = str(src)
        args.writer.cldf.properties['dc:relation'] = src['url']

        shutil.copy(cdata / 'CONTRIBUTORS.md', self.cldf_dir)
        args.writer.cldf.properties['dc:contributor'] = {
            "dc:references": "CONTRIBUTORS.md", "dc:format": "text/markdown"}
        ref_in_note = collections.defaultdict(list)

        def biburl(clid, ml):
            if ml.url.startswith(':bib:'):
                rid = ml.url.replace(':bib:', '')
                return MarkdownLink(ml.label, 'sources.bib#cldf:{}'.format(rid))
            if ml.url.startswith(':ref:'):
                rid = ml.url.replace(':ref:', '')
                ref_in_note[clid].append(rid)
                return MarkdownLink(ml.label, 'conceptlists.csv#cldf:{}'.format(rid))
            return ml

        glangs = {lg.id: lg for lg in args.glottolog.api.languoids()}
        lids = set()
        for lg in api.vocabularies['COLUMN_TYPES'].values():
            if isinstance(lg, Languoid):
                glang = glangs[lg.glottocode] if lg.glottocode else None
                args.writer.objects['LanguageTable'].append(dict(
                    ID=lg.name,
                    Name=glang.name if glang else lg.name,
                    Latitude=glang.latitude if glang else COORDS.get(lg.name, (None, None))[0],
                    Longitude=glang.longitude if glang else COORDS.get(lg.name, (None, None))[1],
                ))
                lids.add(lg.name)
        for k, v in api.vocabularies['TAGS'].items():
            args.writer.objects['tags.csv'].append(dict(ID=k, Description=v))

        for ref in api.sources:
            args.writer.objects['MediaTable'].append(dict(
                ID=ref,
                Name=api.sources[ref]['original'],
                Media_Type=api.sources[ref]['mimetype'],
                Download_URL=api.sources[ref]['url'],
            ))

        args.writer.objects['ParameterTable'].append(dict(
            ID='0',
            Name='<NA>',
            Description='Set of all concepts not yet mapped to a meaningful concept set'))
        for cs in api.conceptsets.values():
            args.writer.objects['ParameterTable'].append(dict(
                ID=cs.id,
                Name=cs.gloss,
                Description=cs.definition,
                Semantic_Field=cs.semanticfield,
                Ontological_Category=cs.ontological_category,
                Replacement_ID=cs.replacement_id,
            ))

        inverses = {}
        for rid, spec in api.vocabularies['CONCEPTRELATIONS'].items():
            if 'inverseof' in spec:
                inverses[rid] = spec['inverseof']
                inverses[spec['inverseof']] = rid
            args.writer.objects['relationtypes.csv'].append(dict(
                ID=rid, Description=spec['definition'], Inverse_ID=spec.get('inverseof')))

        seen = set()
        for row in api.multirelations.raw:
            rid = '{}-{}-{}'.format(row['SOURCE'], row['RELATION'], row['TARGET'])
            if rid not in seen:
                args.writer.objects['conceptrelations.csv'].append(dict(
                    ID=rid,
                    Source_ID=row['SOURCE'],
                    Relation_ID=row['RELATION'],
                    Target_ID=row['TARGET'],
                ))
                seen.add(rid)
            if row['RELATION'] in inverses:
                rid = '{}-{}-{}'.format(row['TARGET'], inverses[row['RELATION']], row['SOURCE'])
                if rid not in seen:
                    args.writer.objects['conceptrelations.csv'].append(dict(
                        ID=rid,
                        Source_ID=row['TARGET'],
                        Relation_ID=inverses[row['RELATION']],
                        Target_ID=row['SOURCE'],
                    ))
                    seen.add(rid)

        def ckey(c):
            num = c.id.split('-')[-1]
            m = re.match('[0-9]+', num)
            assert m
            return int(num[:m.end()]), num[m.end():]

        for cl in api.conceptlists.values():
            slangs = [n.lower() for n in cl.source_language]
            assert all(n in lids for n in slangs), '{}'.format([n for n in slangs if n not in lids])

            desc = MarkdownLink.replace(cl.note, functools.partial(biburl, cl.id))
            args.writer.objects['ContributionTable'].append(dict(
                ID=cl.id,
                Name='{} {}{}'.format(cl.author, cl.year, cl.list_suffix or ''),
                Description=desc,
                Contributor=cl.author.replace('AND', 'and').split(' and '),
                Year=cl.year,
                List_Suffix=cl.list_suffix,
                Number_Of_Items=cl.items,
                Gloss_Language_IDs=slangs,
                Target_Language_ID=cl.target_language.lower(),
                Citation='\n'.join(str(api.bibliography[ref]) for ref in cl.refs),
                Source=cl.refs,
                Related=ref_in_note.get(cl.id, []),
                PDF=[ref for ref in cl.refs if ref in api.sources],
                Tags=cl.tags,
                Source_URL=cl.url,
                Pages=cl.pages,
                Alias=cl.alias,
            ))

            for i, c in enumerate(sorted(cl.concepts.values(), key=ckey), start=1):
                data = collections.OrderedDict(
                    [(k, v) for k, v in c.attributes.items() if v is not None])
                forms = {'english': c.english} if c.english and 'english' in slangs else {}
                for k, v in list(data.items()):
                    if k in slangs:
                        if v:
                            if k in forms:
                                assert v == forms[k]
                            forms[k] = v
                        del data[k]
                    elif isinstance(v, decimal.Decimal):
                        data[k] = str(v)
                    elif isinstance(v, URIReference):
                        data[k] = v.unsplit()
                if i == 1:
                    args.writer.objects['ContributionTable'][-1]['Attributes'] = sorted(data.keys())
                args.writer.objects['concepts.csv'].append(dict(
                    ID=c.id,
                    Concepticon_ID=c.concepticon_id or '0',
                    Conceptlist_ID=cl.id,
                    Number=c.number,
                    Index=i,
                    Attributes=data,
                ))
                for j, (lid, form) in enumerate(sorted(forms.items()), start=1):
                    args.writer.objects['FormTable'].append(dict(
                        ID='{}-{}'.format(c.id, j),
                        Form=form,
                        Parameter_ID=c.concepticon_id or '0',
                        Language_ID=lid,
                        Concept_ID=c.id,
                    ))

        for obj_type, retirements in api.retirements.items():
            for ret in retirements:
                args.writer.objects['retired.csv'].append(dict(
                    Type=obj_type,
                    ID=ret['id'],
                    Comment=ret['comment'],
                    Replacement_ID=ret['replacement'],
                ))
        zenodo = load(cdata / '.zenodo.json')
        zenodo['keywords'].append('cldf:Wordlist')
        zenodo['title'] = '{} as CLDF dataset'.format(zenodo['title'])
        dump(zenodo, self.dir / '.zenodo.json', indent=2)
