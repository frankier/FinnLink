import csv
import sys
from finntk.wordnet.utils import fi2en_post

from join import PROPBANK_DEFNS 

with open(PROPBANK_DEFNS, 'r') as propbank:
    propbank = csv.DictReader(propbank, delimiter='\t')
    print("pb,wn")
    not_found = 0
    found = 0
    for row in propbank:
        pb_finn = "{}.{:0>2}".format(row['base'], row['number'])
        if row['synset_id'] in ("NULL", "666", ""):
            continue
        for raw_synset_id in row['synset_id'].split(","):
            stripped_synset_id = raw_synset_id.strip()
            if not stripped_synset_id:
                continue
            fi_synset_id = stripped_synset_id + "-v"
            try:
                en_synset_id = fi2en_post(fi_synset_id)
            except KeyError:
                print(f"Not found {fi_synset_id} (while processing {pb_finn})", file=sys.stderr)
                not_found += 1
            else:
                print(f"{pb_finn},{en_synset_id}")
                found += 1
    print(f"Found: {found}; Not found: {not_found}", file=sys.stderr)
