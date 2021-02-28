import json
import os
import re
from math import sqrt
from pprint import pprint
from random import random

import plotly.graph_objects as go
from gensim.models import LdaModel

from config import resources
from initialization.initialization import initialize
from lsa.lsa import Lsa
from lsa.restore_segments import clear_segments, restore_segments
from tools.text import remove_newlines


def get_scatter_lda_p(model, name, aspect, t1=0, t2=1, t3=2):
    x = []
    y = []
    z = []
    for p in aspect:
        doc = model.dictionary.doc2bow(p[1].lower().split())
        similarity = model.lsa_model.get_document_topics(doc, minimum_probability=0)
        x.append(similarity[t1][1])
        y.append(similarity[t2][1])
        z.append(similarity[t3][1])
    return go.Scatter3d(x=x, y=y, z=z, name=name, mode="markers", marker=dict(sizemode='diameter', size=5))


def get_scatter2d_lda_p(model, name, aspect, t1=0, t2=1):
    x = []
    y = []
    for p in aspect:
        doc = model.dictionary.doc2bow(p[1].lower().split())
        similarity = model.lsa_model.get_document_topics(doc, minimum_probability=0)
        x.append(similarity[t1][1])
        y.append(similarity[t2][1])
    return go.Scatter(x=x, y=y, name=name, mode="markers", marker=dict(sizemode='diameter', size=5))


def get_low_affiliated_texts(model, aspect):
    with open(os.path.join(resources, "affiliations.txt"), "w", encoding="utf-8") as f:
        i = 0
        for p in aspect:
            doc = model.dictionary.doc2bow(p[1].lower().split())
            print("\n\n\n--------------------------------", file=f)
            print(f"\nId:\n{i}", file=f)
            print(f"\nData practice:\n{p[0]}", file=f)
            print(f"\nTopics & Affiliations:", file=f)
            pprint(model.lsa_model.get_document_topics(doc, minimum_probability=.0), stream=f)
            print("\nText:", file=f)
            pprint(p[1], stream=f)
            i += 1


def get_scatter_lda(model, name, aspect, t1=0, t2=1, t3=2):
    x = []
    y = []
    z = []
    for p in aspect:
        doc = model.dictionary.doc2bow(p[1].lower().split())
        similarity = model.lsa_model[doc]

        sdict = {k: v for k, v in similarity}
        new_s = []

        for i in range(model.topics_count):
            try:
                new_s.append((i, sdict[i]))
            except KeyError:
                new_s.append((i, 0))

        x.append(new_s[t1][1])
        y.append(new_s[t2][1])
        z.append(new_s[t3][1])
    return go.Scatter3d(x=x, y=y, z=z, name=name, mode="markers", marker=dict(sizemode='diameter', size=5))


def get_scatter2d_lda(model, name, aspect, t1=0, t2=1):
    x = []
    y = []
    for p in aspect:
        doc = model.dictionary.doc2bow(p[1].lower().split())
        similarity = model.lsa_model[doc]

        sdict = {k: v for k, v in similarity}
        new_s = []

        for i in range(model.topics_count):
            try:
                new_s.append((i, sdict[i]))
            except KeyError:
                new_s.append((i, 0))

        x.append(new_s[t1][1])
        y.append(new_s[t2][1])
    return go.Scatter(x=x, y=y, name=name, mode="markers", marker=dict(sizemode='diameter', size=5))


def get_scatter_lsi(model, name, aspect, t1=0, t2=1, t3=2):
    x = []
    y = []
    z = []
    for p in aspect:
        doc = model.dictionary.doc2bow(p[1].lower().split())
        similarity = model.lsa_model[doc]

        sdict = {k: v for k, v in similarity}
        new_s = []

        for i in range(model.topics_count):
            try:
                new_s.append((i, sdict[i]))
            except KeyError:
                new_s.append((i, 0))

        x.append(new_s[t1][1])
        y.append(new_s[t2][1])
        z.append(new_s[t3][1])

    return go.Scatter3d(x=x, y=y, z=z, name=name, mode="markers", marker=dict(sizemode='diameter', size=5))


def get_scatter2d_lsi(model, name, aspect, t1=0, t2=1):
    x = []
    y = []
    for p in aspect:
        doc = model.dictionary.doc2bow(p[1].lower().split())
        similarity = model.lsa_model[doc]

        sdict = {k: v for k, v in similarity}
        new_s = []

        for i in range(model.topics_count):
            try:
                new_s.append((i, sdict[i]))
            except KeyError:
                new_s.append((i, 0))

        x.append(new_s[t1][1])
        y.append(new_s[t2][1])

    return go.Scatter(x=x, y=y, name=name, mode="markers", marker=dict(sizemode='diameter', size=5))


def volume(model, topic, aspects, threshold=0.9):
    v = 0
    for p in aspects:
        doc = model.dictionary.doc2bow(p[1].lower().split())
        similarity = model.lsa_model.get_document_topics(doc, minimum_probability=0)
        if similarity[topic][1] > threshold:
            v += 1
    return v


def extract_class(paragraphs: list, category: str):
    return [p for p in paragraphs if p[0] == category]


def render_affiliations(model, segments, topic_x, topic_y):

    classes = list(set([p[0].strip() for p in segments]))
    paragraphs = [extract_class(segments, c) for c in classes]

    fig = go.Figure(data=[
        get_scatter2d_lda_p(model, classes[i], paragraphs[i], topic_x, topic_y) for i in range(len(classes))
    ])
    fig.update_layout(
        xaxis_title=f'Topic {topic_x} Affiliation',
        yaxis_title=f'Topic {topic_y} Affiliation',
        font=dict(
            family="Times New Roman",
            size=25,
        ),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.98
        )
    )
    fig.show()


def render_amounts(segments):

    classes = list(set([p[0].strip() for p in segments]))
    print(classes)
    data = [
        go.Bar(
            name=classes[i],
            x=[""],
            y=[len(extract_class(segments, classes[i]))])
        for i in range(len(classes))
    ]

    fig2 = go.Figure(data=data)
    fig2.update_layout(
        font=dict(
            family="Times New Roman",
            size=25,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig2.show()


def render_volumes(model, segments):

    classes = list(set([p[0].strip() for p in segments]))
    topics = [f"Topic {i}" for i in range(model.lsa_model.num_topics)]

    data = [
        go.Bar(
            name=classes[i],
            x=topics,
            y=[volume(model, t, extract_class(segments, classes[i]), threshold=.9)
               for t in range(model.lsa_model.num_topics)])
        for i in range(len(classes))
    ]

    fig2 = go.Figure(data=data)
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            size=25,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig2.show()


def render_groups(model, paragraphs):

    groups = [
        {
            "name": "Browser, cookies, device, location data",
            "topics": [0, 2, 7],
        },
        {
            "name": "Contacts and reference information",
            "topics": [1, 13, 14],
        },
        {
            "name": "Policy changes",
            "topics": [2],
        },
        {
            "name": "Data collection, services usage, consents",
            "topics": [3],
        },
        {
            "name": "Disclosure, third-party sources and social nets, advertisement with cookies and cookies tracking",
            "topics": [4, 5, 9, 11, 12],
        },
        {
            "name": "User control and data retention",
            "topics": [6],
        },
        {
            "name": "Payment information and credentials",
            "topics": [8],
        },
        {
            "name": "Notifications and children",
            "topics": [10],
        }
    ]

    with open(os.path.join(resources, "to_groups.txt"), "w", encoding="utf-8") as f:
        i = 0
        for p in paragraphs:
            doc = model.dictionary.doc2bow(p[1].lower().split())
            print("\n\n\n--------------------------------", file=f)
            print(f"\nId:\n{i}", file=f)
            affs = model.lsa_model.get_document_topics(doc, minimum_probability=.2)
            max_aff_t = 0
            max_aff_p = 0
            for a in affs:
                if max_aff_p < a[1]:
                    max_aff_t = a[0]
                    max_aff_p = a[1]
            print(f"\nGroup:", file=f)
            for g in groups:
                if max_aff_t in g["topics"]:
                    pprint(f"{g['name']}", stream=f)
                    break
            print("\nText:", file=f)
            pprint(p[1], stream=f)
            i += 1


def extract_coordinates(topics):

    points = []

    for t in topics:

        coordinates = re.sub(r" ", "", t[1]).split("+")
        coordinates_pairs = []
        for c in coordinates:
            m = re.match(r"(0\.\d+)\*\"([\d\w]+)\"", c)
            coordinates_pairs.append((float(m.group(1)), m.group(2)))

        points.append(coordinates_pairs)

    coordinates = list(set([c[1] for p in points for c in p]))

    new_points = []

    for p in points:
        c = dict()
        for coord in p:
            c[coord[1]] = coord[0]
        new_points.append(c)

    for p in new_points:
        for c in coordinates:
            if c not in p.keys():
                p[c] = 0.

    return new_points


def calculate_range(p1, p2):
    s = []
    n = len(p1.keys())
    c1 = list(p1.values())
    c2 = list(p2.values())

    for i in range(n):
        s.append((c1[i] - c2[i]) ** 2)

    return sqrt(sum(s))


def render_heatmap(topics):
    points = extract_coordinates(topics)
    m = [[calculate_range(p1, p2) for p2 in points] for p1 in points]

    with open(os.path.join(resources, "ranges.txt"), "w", encoding="utf-8") as f:
        print(f"     {''.join([f'     T{j:5}' for j in range(len(m))])}", file=f)
        for i in range(len(m)):
            print(f"T{i:3}\t{'   '.join(['  {:.4f}'.format(m[i][j]) for j in range(len(m))])}", file=f)

    ts = [f"Topic {i}" for i in range(len(topics))]

    fig = go.Figure(
        data=go.Heatmap(
           z=m,
           x=ts,
           y=ts,
           hoverongaps=False))
    fig.update_layout(
        font=dict(
            family="Times New Roman",
            size=25,
        ),
    )
    fig.show()


def main():
    initialize()
    # restore_segments()

    paragraphs_labeled = []

    with open(os.path.join(resources, "all_segments.json"), "r", encoding="utf-8") as f:
        segments = json.load(f)

    paragraphs_labeled.extend([(s["category"], p)
                               for s in segments
                               for p in s["paragraphs"]])

    # with open(os.path.join(resources, "POLICIES.txt"), "r", encoding="utf-8") as f:
    #     paragraphs = remove_newlines(f.read())
    #
    # paragraphs_labeled.extend([("?", p)
    #                            for p in paragraphs.split("\n")])

    lsa = Lsa([p[1] for p in paragraphs_labeled], freq="bow", model="lda")
    # lsa = Lsa([p[1] for p in paragraphs_labeled], freq="tf-idf", model="lda")

    lsa.preprocess_data()
    lsa.prepare_corpus()

    # lsa.best_coherence(stop=30, start=2, step=3)
    lsa.topics_count = 15

    # lsa.create_lsa_model()
    # lsa.lsa_model.save(os.path.join(resources, "models/lda_model"))

    lsa.lsa_model = LdaModel.load(os.path.join(resources, "models/lda_model_opp"))

    topics = lsa.lsa_model.print_topics(num_topics=lsa.lsa_model.num_topics, num_words=10)

    with open(os.path.join(resources, "topics.txt"), "w", encoding="utf-8") as f:
        pprint(topics, stream=f)

    # get_low_affiliated_texts(lsa, paragraphs_labeled)
    # render_amounts(paragraphs_labeled)
    # render_heatmap(topics)

    # topic_x = 0
    # topic_y = 1
    # topic_x = int(input())
    # topic_y = int(input())
    # render_affiliations(lsa, paragraphs_labeled, topic_x, topic_y)

    render_groups(lsa, paragraphs_labeled)
    # render_volumes(lsa, paragraphs_labeled)

