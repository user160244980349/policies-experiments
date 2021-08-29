import os

from pprint import pprint
from config import resources


def aggregate_groups(model, paragraphs, groups, file="aggregated_groups.txt"):
    labeled_paragraphs = []
    best = []

    with open(os.path.join(resources, file), "w", encoding="utf-8") as f:
        i = 0

        for p in paragraphs:
            print("\n\n\n--------------------------------", file=f)
            print(f"\nId:\n{i}", file=f)
            affs = model.get_document_topics(p[1].lower().split(), minimum_probability=.4)

            print(f"\nGroup:", file=f)

            alffs = []
            for g in groups:
                for a in affs:

                    if a[0] in g["topics"]:
                        labeled_paragraphs.append((g["name"], "?"))
                        alffs.append((a[1], g["name"]))

            for a in alffs:
                print(f"{a[0]:.2f} {a[1]}", file=f)

            best.extend([a[1] for a in alffs])

            print("\nText:", file=f)
            pprint(p[1], stream=f)
            i += 1

    return labeled_paragraphs, best
