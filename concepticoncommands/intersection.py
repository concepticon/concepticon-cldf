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
        help="Conceptsets related via a instanceof/isa relation will be treated as equal.",
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--output-union',
        help="Print the shared concepts as well as the unique, non-shared concepts from each list.",
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--verbose',
        help="Print matching concepts in each list for each 'fuzzy' shared concept",
        action='store_true',
        default=False,
    )
    parser.add_argument(
        'clists',
        metavar='CLIST',
        help="Conceptlist identifier (or '-' to read the concepts of one list from stdin).",
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
                            rel[kk] = vv + level
            if args.equate_instanceof:
                # We assue that there are no chains of "instanceof" relations.
                rel.update(fetch_related(cu, cid[0], maxdist=1, inv='instanceof', rel='isa'))
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
    for item in res:
        if isinstance(item, list):
            # Output the broadest concept: Sort matching concepts by distance from first concept.
            items = sorted(item, key=lambda i: (i[1], i[0]))
            if all(i[1] == 0 for i in items):
                # The (ROAD, 0), (PATH, 0) case.
                # There must be a common broader concept.
                it = (fetch_broader(cu, [i[0][0] for i in items]), 1)
            else:
                it = items[0]
            if args.verbose:
                print(it[0][0], it[0][1], item)
            else:
                print(it[0][0], it[0][1])
        else:
            print(item[0], item[1])

    if args.output_union:
        seen = set()
        for k, v in concepts.items():
            for item in v:
                if item[0] not in seen:
                    print(item[0], item[1])
                seen.add(item[0])


def fetch_broader(cu, cids):
    cu.execute(
        " UNION ".join([
            "SELECT cldf_targetParameterReference FROM ParameterNetwork WHERE cldf_sourceParameterReference = ?" for _ in cids]),
        cids)
    res = cu.fetchall()
    assert len(res) == 1
    cu.execute("SELECT cldf_id, cldf_name FROM parametertable WHERE cldf_id = ?", (res[0][0],))
    return cu.fetchone()


def fetch_concepts(cu, clid):
    if clid == '-':
        return {tuple(l.split(' ', maxsplit=1)) for l in sys.stdin.read().split('\n') if l.strip()}

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
            cldf_sourceParameterReference, rel.level + 1
        FROM
            ParameterNetwork, rel
        WHERE
            ParameterNetwork.cldf_targetParameterReference = rel.n AND ParameterNetwork.relation = ?
    ),
    inv(n, level) AS (
        SELECT ?, 0
        UNION ALL
        SELECT
            cldf_sourceParameterReference, inv.level - 1
        FROM
            ParameterNetwork, inv
        WHERE
            ParameterNetwork.cldf_targetParameterReference = inv.n AND ParameterNetwork.relation = ?
    )
SELECT DISTINCT n.level AS l, n.n, p.cldf_name FROM rel as n, ParameterTable as p WHERE n.n = p.cldf_id AND n.level <= ?
UNION
SELECT DISTINCT n.level AS l, n.n, p.cldf_name FROM inv as n, ParameterTable as p WHERE n.n = p.cldf_id AND ABS(n.level) <= ?
ORDER BY l
    """, (cid, rel, cid, inv, maxdist, maxdist))
    return {(row[1], row[2]): row[0] for row in cu.fetchall()}
