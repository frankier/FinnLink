import fileinput
from nltk.corpus import wordnet


def main():
    inf = fileinput.input()
    next(inf)
    for line in inf:
        frame, ssof = line.strip().split(",", 1)
        ss = wordnet.of2ss(ssof)
        print(frame, " ".join((l.name() for l in ss.lemmas(lang="fin"))))


if __name__ == "__main__":
    main()
