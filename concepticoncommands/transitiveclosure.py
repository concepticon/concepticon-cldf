"""
Compute the transitive closure of a concept given a relation.
"""
from networkx import DiGraph
from networkx.algorithms import transitive_closure

from cldfbench_concepticon import Dataset


def register(parser):
    #cldf = Dataset().cldf_reader()
    parser.add_argument('gloss_or_id')
    parser.add_argument(
        '--relation',
        help="Relation for which to investigate the network.",
        #choices=[r['ID'] for r in cldf['relationtypes.csv']],
        default='broader')


def run(args):
    cldf = Dataset().cldf_reader()
    csets_by_id, csets_by_name = {}, {}
    for r in cldf['ParameterTable']:
        csets_by_id[int(r['ID'])] = r
        csets_by_name[r['Name']] = int(r['ID'])
    g = DiGraph()
    nodes = set()
    for row in cldf['conceptrelations.csv']:
        if row['Relation_ID'] == args.relation:
            for key in ['Source_ID', 'Target_ID']:
                if row[key] not in nodes:
                    nodes.add(row[key])
                    g.add_node(int(row[key]))
            g.add_edge(int(row['Source_ID']), int(row['Target_ID']))
    nid = csets_by_name[args.gloss_or_id] \
        if args.gloss_or_id in csets_by_name else int(args.gloss_or_id)
    for e in transitive_closure(g).edges(nid):
        print(e[1], csets_by_id[e[1]]['Name'])
