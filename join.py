import click
import csv
import re
from nltk.corpus import wordnet
from more_itertools import peekable


PRED_MAT = 'PredicateMatrix.v1.3/PredicateMatrix.v1.3.txt'
PROPBANK_DEFNS = 'Finnish_PropBank/gen_lemmas/pb-defs.tsv'
OUT = 'joined.tsv'
MODEL_RE = re.compile(r".*\(tags: model:([^, \)]+)\).*")


@click.command()
@click.option('--pred-matrix', default=PRED_MAT,
              help='Path to PredicateMatrix.v?.?.txt TSV file')
@click.option('--pb-defns', default=PROPBANK_DEFNS,
              help='Path to Finnish PropBank pb-defs.tsv file')
@click.option('--out', default=OUT,
              help='Path to output joined TSV')
@click.option('--reject-non-english/--accept-non-english', default=False,
              help='Accept or reject non-English based mappings')
@click.option('--use-model/--use-link-original', default=True,
              help='Link via the model tag or via the link_original field')
@click.option('--synset/--english-lemmas', default=False,
              help='Map to synset IDs rather than English lemmas')
def main(pred_matrix, pb_defns, out, reject_non_english, use_model, synset):
    # Load mapping from English PropBank senses to English WordNet senses
    mapping = {}
    with open(pred_matrix, 'r') as matrix:
        matrix = csv.DictReader(matrix, delimiter='\t')
        for row in matrix:
            if reject_non_english and row['1_ID_LANG'] != 'id:eng':
                continue
            if row['11_WN_SENSE'] != 'wn:NULL':
                pb = row['16_PB_ROLESET'].split(':', 1)[1]
                wn = row['11_WN_SENSE'].split(':', 1)[1]
                mapping.setdefault(pb, set()).add(wn)

    # Join with mapping from Finnish to English PropBank
    with open(pb_defns, 'r') as propbank, open(out, 'w') as csvout:
        propbank = csv.DictReader(propbank, delimiter='\t')
        csvout = csv.writer(csvout)
        csvout.writerow(['pb', 'wn'])
        propbank = peekable(propbank)
        for row in propbank:
            pb_finn = "{}.{:0>2}".format(row['base'], row['number'])
            if use_model:
                match = MODEL_RE.match(row['note'])
                if match:
                    pb = match.group(1)
                else:
                    pb = None
            else:
                pb = row['link_original']
            if pb == 'none.01':
                pb = None
            if pb is not None and pb in mapping:
                for wn in mapping[pb]:
                    if synset:
                        csvout.writerow((pb_finn, wordnet.ss2of(wordnet.lemma_from_key(wn + "::").synset())))
                    else:
                        csvout.writerow((pb_finn, wn))


if __name__ == '__main__':
    main()
