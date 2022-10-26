"""
Compute conceptsets shared between a set of conceptlists.

Note: This functionality accesses the Concepticon data in a SQLite database. If such a database
is already available (created via 'cldf createdb'), pass the name of the db file as `db`
argument. Otherwise, an in-memory SQLite database is created on the fly, adding about ~20 seconds
to the processing time.
"""
import sys
import sqlite3

from clldutils.clilib import PathType
from pycldf import Database
from cldfbench_concepticon import Dataset


def register(parser):
    parser.add_argument(
        '--db',
        help="SQLite database created from the CLDF dataset via 'cldf createdb'",
        type=PathType(type='file'),
        default=None)
    parser.add_argument(
        '--maxdist',
        help="Conceptsets related via broader or narrower relations will be treated as equal, "
             "if they are only MAXDIST nodes apart in the relation graph.",
        type=int,
        default=0)
    parser.add_argument(
        '--equate-instanceof',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--output-union',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        'clists',
        metavar='CLIST',
        help="Conceptlist identifier",
        nargs='+')


def run(args):
    if args.db is None:
        db = Database(Dataset().cldf_reader())
        db.write_from_tg()
        conn = db.connection()
    else:
        conn = sqlite3.connect(str(args.db))
    cu = conn.cursor()

    concepts = {clist: fetch_concepts(cu, clist) for clist in args.clists}
    # First we compute the exact matches:
    res = list(set.intersection(*concepts.values()))
    if args.maxdist:
        # If "fuzzy" matches are acceptable, we first prune the concepts to what has not been
        # matched.
        concepts = {k: v - set(res) for k, v in concepts.items()}
        # Then loop through leftover concepts of the first list.
        for cid in list(concepts[args.clists[0]])[:]:
            # Compute all concepts which are (not too distantly) related.
            rel = fetch_related(cu, cid[0], args.maxdist)
            for k, level in list(rel.items()):
                # FIXME: We'd need to do this recursively, also for the newly added concepts below.
                # This would be necessary, if there were concepts being part of more than one
                # broader concept, e.g. FINGER and ARM in FINGER_OR_HAND and ARM_OR_HAND.
                if 0 < abs(level) < args.maxdist:
                    # Add related concepts of related concepts - thus catering to the cases where
                    # lists have different constituent concepts of a "A OR B"-type concept.
                    for kk, vv in fetch_related(cu, k[0], args.maxdist - abs(level)).items():
                        if kk not in rel:
                            rel[kk] = abs(vv) + abs(level)
            if args.equate_instanceof:
                rel.update(fetch_related(cu, cid[0], maxdist=1, rel='instanceof', inv='isa'))
            relset = set(rel.keys())
            # Intersect remaining concepts of the other lists with the related concepts.
            matches = [relset.intersection(concepts[clid]) for clid in args.clists[1:]]
            if all(matches):
                # If matches with any of the related concepts are found, we add this concept to
                # the resultset ...
                fuzzymatch = [(cid, 0)]
                # ... and remove matching concepts from the remaining, to-be-matched concepts.
                concepts[args.clists[0]].remove(cid)
                for i, matched in enumerate(matches, start=1):
                    othercid = matched.pop()
                    fuzzymatch.append((othercid, rel[othercid]))
                    concepts[args.clists[i]].remove(othercid)
                res.append(fuzzymatch)
    if args.output_union:
        for item in res:
            if isinstance(item, list):
                print(item[0][0][0])
            else:
                print(item[0])
        for k, v in concepts.items():
            for item in v:
                print(item[0])
        return
    print("The lists have {} concepts in common:".format(len(res)))
    for i in res:
        print(i)
    print("Remaining, not shared concepts:")
    for k, v in concepts.items():
        print(k, v)


def fetch_concepts(cu, clid):
    if clid == '-':
        stdin = sys.stdin.read()
        #print(stdin[:40], stdin[-40:])
        cids = stdin.split()
        cu.execute("""
SELECT
    pt.cldf_id, pt.cldf_name
FROM
    ParameterTable as pt
WHERE
    pt.cldf_id IN {}
    """.format(tuple(cids)))
        return set(cu.fetchall())

    cu.execute("""
SELECT
  pt.cldf_id, pt.cldf_name
FROM
  ContributionTable as ct,
  `concepts.csv` as c,
  ParameterTable as pt
WHERE
  ct.cldf_id = c.cldf_contributionReference AND
  pt.cldf_id = c.cldf_parameterReference AND
  ct.cldf_id = ?
""", (clid,))
    return set(cu.fetchall())


def fetch_related(cu, cid, maxdist=3, rel='broader', inv='narrower'):
    cu.execute("""
WITH RECURSIVE
    rel(n, level) AS (
        SELECT ?, 0
        UNION ALL
        SELECT
            Source_ID, rel.level + 1
        FROM
            `conceptrelations.csv`, rel
        WHERE
            `conceptrelations.csv`.Target_ID = rel.n AND `conceptrelations.csv`.Relation_ID = ?
    ),
    inv(n, level) AS (
        SELECT ?, 0
        UNION ALL
        SELECT
            Source_ID, inv.level - 1
        FROM
            `conceptrelations.csv`, inv
        WHERE
            `conceptrelations.csv`.Target_ID = inv.n AND `conceptrelations.csv`.Relation_ID = ?
    )
SELECT DISTINCT n.level AS l, n.n, p.cldf_name FROM rel as n, ParameterTable as p WHERE n.n = p.cldf_id AND n.level <= ?
UNION
SELECT DISTINCT n.level AS l, n.n, p.cldf_name FROM inv as n, ParameterTable as p WHERE n.n = p.cldf_id AND ABS(n.level) <= ?
ORDER BY l
    """, (cid, rel, cid, inv, maxdist, maxdist))
    return {(row[1], row[2]): row[0] for row in cu.fetchall()}
