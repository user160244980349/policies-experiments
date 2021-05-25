import json
import os
import re
from math import sqrt
from pprint import pprint
from random import random
from collections import Counter
import plotly.express as px

import plotly.graph_objects as go
from gensim.models import LdaModel

from tools.fsys import files
from config import resources
from initialization.initialization import initialize
from lsa.lsa import Lsa
from lsa.restore_segments import clear_segments, restore_segments


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


def get_affiliation(model, aspect, file="affiliations.txt"):
    with open(os.path.join(resources, file), "w", encoding="utf-8") as f:

        print("\n\n\nTopics:", file=f)
        pprint(model.lsa_model.print_topics(num_topics=model.lsa_model.num_topics,
                                            num_words=10), stream=f)
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


def render_affiliations(model, segments):

    topic_x = 0
    topic_y = 1
    topic_x = int(input())
    topic_y = int(input())

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
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
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

    values = [(len(extract_class(segments, classes[i])),) for i in range(len(classes))]
    pprint(values)
    data = [
        go.Bar(
            name=classes[i],
            y=values[i],
            x=("",))
        for i in range(len(classes))
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="left",
            x=1,
            y=1
        )
    )
    fig2.show()


def render_volumes(model, segments, threshold=.5, file=f"volumes.txt"):

    classes = list(set([p[0].strip() for p in segments]))
    topics = [f"Topic {i}" for i in range(model.lsa_model.num_topics)]

    y = []
    for i in range(len(classes)):
        y.append([volume(model, t, extract_class(segments, classes[i]), threshold=threshold) if volume(model, t, extract_class(segments, classes[i]), threshold=threshold) > 3 else 0
                  for t in range(model.lsa_model.num_topics)])

    mx = max([len(c) for c in classes])

    with open(os.path.join(resources, file), "w", encoding="utf-8") as f:
        print(f"{''.join([' ' for _ in range(mx)])} {'   '.join([f'T{j:3}' for j in range(len(y[0]))])}", file=f)
        for i in range(len(y)):
            print(f"{''.join([' ' for _ in range(mx - len(classes[i]))])}{classes[i]} {'   '.join([f'{y[i][j]:4}' for j in range(len(y[0]))])}", file=f)

        print(f"{''.join([' ' for _ in range(mx - 3)])}SUM {'   '.join([f'{j:4}' for j in [sum(row[c] for row in y) for c in range(len(y[0]))]])}", file=f)

    data = [
        go.Bar(
            name=classes[i],
            x=topics,
            y=y[i])
        for i in range(len(classes))
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig2.show()


def render_groups(model, paragraphs, file="to_groups.txt"):

    groups = [
        {
            "name": "First party collection Opt-in, opt-out messages and notifications to end user",
            "topics": [0],
        },
        {
            "name": "Third parties sharing for marketing purposes",
            "topics": [1],
        },
        {
            "name": "Contact information: company",
            "topics": [2],
        },
        {
            "name": "First party collection: browser and device information",
            "topics": [3],
        },
        {
            "name": "Special audience: children",
            "topics": [4],
        },
        {
            "name": "First-party collection: device and service specific information",
            "topics": [5],
        },
        {
            "name": "Other",
            "topics": [6, 8],
        },
        {
            "name": "First-party collection: right to edit, access, with specified (legal) basis of data processing",
            "topics": [7],
        },
        {
            "name": "Third-party sharing in case of company acquisition and merging",
            "topics": [9],
        },
        {
            "name": "Right to erase",
            "topics": [10],
        },
        {
            "name": "First party collection: personal and account information",
            "topics": [11],
        },
        {
            "name": "Data security",
            "topics": [12],
        },
        {
            "name": "Special audience: California residents",
            "topics": [13],
        },
        {
            "name": "Privacy policy changes",
            "topics": [14],
        }
    ]

    labeled_paragraphs = []
    best = []

    with open(os.path.join(resources, file), "w", encoding="utf-8") as f:
        i = 0

        for p in paragraphs:
            doc = model.dictionary.doc2bow(p[1].lower().split())
            print("\n\n\n--------------------------------", file=f)
            print(f"\nId:\n{i}", file=f)
            affs = model.lsa_model.get_document_topics(doc, minimum_probability=.4)
            
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

    return labeled_paragraphs, best, groups


def render_groups_opp(model, paragraphs, file="to_groups.txt"):

    groups = [
        {
            "name": "Сбор от 1-х лиц (куки, эл.почта), Особая аудитория (дети)",
            "topics": [0],
        },
        {
            "name": "Сбор от 1-х лиц (идентификационные данные)",
            "topics": [1],
        },
        {
            "name": "Сбор от 1-х лиц (платежные данные)",
            "topics": [2],
        },
        {
            "name": "Распространение 3-м лицам",
            "topics": [3],
        },
        {
            "name": "Безопасность данных (вкл. распространение 3-м лицам)",
            "topics": [4],
        },
        {
            "name": "Распространение 3-м лицам (использование куки)",
            "topics": [5],
        },
        {
            "name": "Сбор от 1-х лиц и Распростр. 3-м лицам (услуги, данные сайта)",
            "topics": [6],
        },
        {
            "name": "Сбор от 1-х лиц (информация об аккаунте)",
            "topics": [7],
        },
        {
            "name": "Другое",
            "topics": [8, 12],
        },
        {
            "name": "Сбор от 1-х лиц и подписка/отписка",
            "topics": [9],
        },
        {
            "name": "Обновление политики, включая механизм уведомления",
            "topics": [10],
        },
        {
            "name": "Сбор от 1-х лиц (информация об устройстве и местоположении)",
            "topics": [11],
        },
        {
            "name": "Распространение 3-м лицам и Особая аудитория (Калифорнийцы)",
            "topics": [13],
        },
        {
            "name": "Особая аудитория (дети)",
            "topics": [14],
        }
    ]

    labeled_paragraphs = []

    with open(os.path.join(resources, file), "w", encoding="utf-8") as f:
        i = 0
        for p in paragraphs:
            doc = model.dictionary.doc2bow(p[1].lower().split())
            print("\n\n\n--------------------------------", file=f)
            print(f"\nId:\n{i}", file=f)
            affs = model.lsa_model.get_document_topics(doc, minimum_probability=.4)
            
            print(f"\nGroups:", file=f)

            alffs = []
            for g in groups:
                for a in affs:
                    if a[0] in g["topics"]:
                        labeled_paragraphs.append((g["name"], "?"))
                        alffs.append((a[1], g["name"]))

            for a in alffs:
                print(f"{a[0]:.2f} {a[1]}", file=f)

            print("\nText:", file=f)
            pprint(p[1], stream=f)
            i += 1

    return labeled_paragraphs


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


def render_heatmap(topics, render=False, file="ranges.txt"):
    points = extract_coordinates(topics)
    m = [[calculate_range(p1, p2) for p2 in points] for p1 in points]

    with open(os.path.join(resources, file), "w", encoding="utf-8") as f:
        print(f"     {''.join([f'     T{j:5}' for j in range(len(m))])}", file=f)
        for i in range(len(m)):
            print(f"T{i:3}\t{'   '.join([f'  {m[i][j]:.4f}' for j in range(len(m))])}", file=f)

    if render:
        ts = [f"Topic {i}" for i in range(len(topics))]
        fig = go.Figure(
            data=go.Heatmap(
            z=m,
            x=ts,
            y=ts,
            hoverongaps=False))
        fig.update_layout(
            colorway=px.colors.qualitative.Dark24,
            font=dict(
                family="Times New Roman",
                color="#000",
                size=20,
            ),
        )
        fig.show()


def calculate_lengths(paragraphs_labeled):
    below_100 = 0
    below_200 = 0
    below_300 = 0
    below_400 = 0
    below_500 = 0
    below_600 = 0
    below_700 = 0
    below_800 = 0
    below_1600 = 0
    more_800 = 0
    
    for p in paragraphs_labeled:
    
        if 100 > len(p[1]) > 70:
            below_100 += 1
    
        if 200 > len(p[1]) >= 100:
            below_200 += 1
    
        if 300 > len(p[1]) >= 200:
            below_300 += 1
    
        if 400 > len(p[1]) >= 300:
            below_400 += 1
    
        if 500 > len(p[1]) >= 400:
            below_500 += 1
    
        if 600 > len(p[1]) >= 500:
            below_600 += 1
    
        if 700 > len(p[1]) >= 600:
            below_700 += 1
    
        if 800 > len(p[1]) >= 700:
            below_800 += 1
    
        if 1600 > len(p[1]) >= 800:
            below_1600 += 1
    
        if len(p[1]) >= 1600:
            more_800 += 1

    ams = ["0 .. 200", "200 .. 300", "300 .. 400", "400 .. 500", 
           "500 .. 600", "600 .. 700", "700 .. 800", "800 .. 1600", "1600 .. +oo"]

    vs = [below_200, below_300, below_400, below_500, 
          below_600, below_700, below_800, below_1600, more_800]

    data = [
        go.Bar(
            x=ams,
            y=vs)
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig2.show()


def calculate_policies_lengths(paragraphs_labeled):
    below_100 = 0
    below_200 = 0
    below_300 = 0
    below_400 = 0
    below_500 = 0
    below_600 = 0
    below_700 = 0
    below_800 = 0
    more_800 = 0
    
    for p in paragraphs_labeled:
    
        if 3000 > len(p[1]) >= 0:
            below_100 += 1
    
        if 6000 > len(p[1]) >= 3000:
            below_200 += 1
    
        if 10000 > len(p[1]) >= 6000:
            below_300 += 1
    
        if 15000 > len(p[1]) >= 10000:
            below_400 += 1
    
        if 25000 > len(p[1]) >= 15000:
            below_500 += 1
    
        if 35000 > len(p[1]) >= 25000:
            below_600 += 1
    
        if 45000 > len(p[1]) >= 35000:
            below_700 += 1
    
        if 60000 > len(p[1]) >= 45000:
            below_800 += 1
    
        if len(p[1]) >= 60000:
            more_800 += 1

    with open(os.path.join(resources, "short_paragraphs.txt"), "w", encoding="utf-8") as f:
        paragraphs_small = [p for p in paragraphs_labeled if len(p[1]) < 100]
        for p in paragraphs_small:
            print(f"{p[1]}\n", file=f)

    ams = ["0 .. 3000", "3000 .. 6000", "6000 .. 10000", "10000 .. 15000", "15000 .. 25000", 
           "25000 .. 35000", "35000 .. 45000", "45000 .. 60000", "60000 .. +oo"]

    vs = [below_100, below_200, below_300, below_400, below_500, 
          below_600, below_700, below_800, more_800]

    data = [
        go.Bar(
            x=ams,
            y=vs)
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig2.show()


def get_opp_paragraphs(paragraphs_labeled):
    
    with open(os.path.join(resources, "datasets/all_segments.json"), "r", encoding="utf-8") as f:
        segments = json.load(f)
    
    paragraphs_labeled.extend([(s["category"], p)
                               for s in segments
                               for p in s["paragraphs"]])
                               
    # with open(os.path.join(resources, "datasets/plain_policies/mi.com-global-about-privacy.html.txt"), 
    #           "r", encoding="utf-8") as fl:
    #     paragraphs_labeled.extend([("?", p) for p in fl.read().split("\n")])

    return paragraphs_labeled


def get_iot_paragraphs(paragraphs_labeled):

    fs = files("datasets/plain_policies", r".*")
    for f in fs:
        with open(f, "r", encoding="utf-8") as fl:
            paragraphs_labeled.extend([("?", p) for p in fl.read().split("\n")])

    return paragraphs_labeled


def get_iot_fulltexts(paragraphs_labeled):

    fs = files("datasets/plain_policies", r".*")
    for f in fs:
        with open(f, "r", encoding="utf-8") as fl:
            paragraphs_labeled.extend([("?", fl.read())])

    return paragraphs_labeled


def make_model(corpus, model, load=True, file="models/some_model"):

    lsa = Lsa(corpus, freq=model, model="lda")

    # lsa.best_coherence(stop=30, start=2, step=3)
    lsa.topics_count = 15

    lsa.preprocess_data()
    lsa.prepare_corpus()

    if not load:
        lsa.create_lsa_model()
        lsa.lsa_model.save(os.path.join(resources, file))
    else:
        lsa.lsa_model = LdaModel.load(os.path.join(resources, file))

    return lsa


def print_topics(topics, file="topics.txt"):
    with open(os.path.join(resources, file), "w", encoding="utf-8") as f:
        pprint(topics, stream=f)


def clean_iot():
    fs = files("datasets/iot", r".*")
    for f in fs:
        Converter.plain_webpage(f)


def calculate_structure_elements():
    with open(os.path.join(resources, "datasets/plain.json"), "r", encoding="utf-8") as f:
        stats = json.load(f)

    hashes = []
    unique_stats = []
    for s in stats:
        if s["policy_hash"] not in hashes and s["statistics"] is not None:
            hashes.append(s["policy_hash"])
            unique_stats.append(s["statistics"])

    stats1 = unique_stats[:296]
    stats2 = unique_stats[296:592]
    
    keys = ["list items", "ordered lists", "unordered lists", "tables", "paragraphs", "headings"]

    _map = {
        "list items": "Элемент списка", 
        "ordered lists": "Нумерованный список", 
        "unordered lists": "Ненумерованный список", 
        "tables": "Таблица", 
        "paragraphs": "Абзац", 
        "headings": "Заголовок"
    }

    data = [
        go.Bar(
            name=_map[k],
            y=[v[k] for v in stats1])
        for k in keys
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig2.show()

    data = [
        go.Bar(
            name=_map[k],
            y=[v[k] for v in stats2])
        for k in keys
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig2.show()

    
def calculate_structure_elements_small():
    with open(os.path.join(resources, "datasets/plain.json"), "r", encoding="utf-8") as f:
        stats = json.load(f)

    hashes = []
    unique_stats = []
    for s in stats:
        if s["policy_hash"] not in hashes and s["statistics"] is not None:
            hashes.append(s["policy_hash"])
            unique_stats.append(s["statistics"])
    
    s = {
        "list items": 0, 
        "ordered lists": 0, 
        "unordered lists": 0, 
        "tables": 0, 
        "paragraphs": 0, 
        "headings": 0
    }

    for st in unique_stats:
        for k in s.keys():
            s[k] += st[k]

    keys = ["list items", "ordered lists", "unordered lists", "tables", "paragraphs", "headings"]
    _map = {
        "list items": "Элемент списка", 
        "ordered lists": "Нумерованный список", 
        "unordered lists": "Ненумерованный список", 
        "tables": "Таблица", 
        "paragraphs": "Абзац", 
        "headings": "Заголовок"
    }

    data = [
        go.Bar(
            name=_map[k],
            y=(s[k],),
            x=("",))
        for k in keys
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="left",
            x=1,
            y=1
        )
    )
    fig2.show()


def clusterize_by_1():

    paragraphs_labeled = []

    with open(os.path.join(resources, "datasets/plain_policies/mi.com-global-about-privacy.html.txt"), 
              "r", encoding="utf-8") as fl:
        paragraphs_labeled.extend([("?", p) for p in fl.read().split("\n")])

    paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 100]
    paragraphs = [p[1] for p in paragraphs_labeled]

    iot_tfidf = make_model(paragraphs, model="tf-idf", load=True, file="models/iot_tfidf")
    topics = iot_tfidf.lsa_model.print_topics(num_topics=iot_tfidf.lsa_model.num_topics, num_words=10)

    policies = []

    fs = files("datasets/plain_policies", r".*")
    for f in fs:
        with open(f, "r", encoding="utf-8") as fl:
            policies.append([("?", p) for p in fl.read().split("\n") if len(p) >= 100])

    groupped = [render_groups(iot_tfidf, p)[1] for p in policies]
    groupped = [Counter(g) for g in groupped]
    
    stats1 = groupped[:296]
    stats2 = groupped[296:592]
    
    keys = [n["name"] for n in render_groups(iot_tfidf, [])[2]]

    data = [
        go.Bar(
            name=k,
            y=[v[k] for v in stats1])
        for k in keys
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig2.show()

    data = [
        go.Bar(
            name=k,
            y=[v[k] for v in stats2])
        for k in keys
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig2.show()

    
def clusterize_by_1_small():

    paragraphs_labeled = []

    with open(os.path.join(resources, "datasets/plain_policies/mi.com-global-about-privacy.html.txt"), 
              "r", encoding="utf-8") as fl:
        paragraphs_labeled.extend([("?", p) for p in fl.read().split("\n")])

    paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 100]
    paragraphs = [p[1] for p in paragraphs_labeled]

    iot_tfidf = make_model(paragraphs, model="tf-idf", load=True, file="models/iot_tfidf")
    topics = iot_tfidf.lsa_model.print_topics(num_topics=iot_tfidf.lsa_model.num_topics, num_words=10)

    policies = []

    fs = files("datasets/plain_policies", r".*")
    for f in fs:
        with open(f, "r", encoding="utf-8") as fl:
            policies.append([("?", p) for p in fl.read().split("\n") if len(p) >= 100])

    groupped = [render_groups(iot_tfidf, p)[1] for p in policies]
    groupped = [Counter(g) for g in groupped]
    
    keys = [n["name"] for n in render_groups(iot_tfidf, [])[2]]

    s = Counter({})
    for st in groupped:
        s += st

    _map = {
        "Privacy policy changes": "Обновление политики",
        "Special audience: California residents": "Особая аудитория (калифорнийцы)",
        "Data security": "Защита данных",
        "First party collection: personal and account information": "Сбор от 1-х лиц (песональные данные и аккаунт)",
        "Right to erase": "Право пользователя на удаление",
        "Third-party sharing in case of company acquisition and merging": "Распространение 3-м лицам в случае поглощения компании",
        "First-party collection: right to edit, access, with specified (legal) basis of data processing": "Пользовательский доступ, изменение и удаление",
        "Other": "Другое",
        "First-party collection: device and service specific information": "Сбор от 1-х лиц (данные об устройстве и приложении)",
        "Special audience: children": "Особая аудитория (дети)",
        "First party collection: browser and device information": "Сбор от 1-х лиц (данные о браузере)",
        "Contact information: company": "Контактная информация компании",
        "Third parties sharing for marketing purposes": "Распространение 3-м лицам в рекламных целях",
        "First party collection Opt-in, opt-out messages and notifications to end user": "Сбор от 1-х лиц, подписка/отписка и уведомления для пользователя"
    }

    data = [
        go.Bar(
            name=_map[k],
            y=[s[k]],
            x=[""])
        for k in keys
    ]

    fig2 = go.Figure(data=data)
    fig2.update_yaxes(tickformat="т")
    fig2.update_layout(
        barmode="stack",
        font=dict(
            family="Times New Roman",
            color="#000",
            size=20,
        ),
        colorway=px.colors.qualitative.Dark24,
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="left",
            y=1,
            x=1
        )
    )
    fig2.show()

    
def work_opp(load=True):

    paragraphs_labeled = []

    get_opp_paragraphs(paragraphs_labeled)

    paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 100]
    paragraphs = [p[1] for p in paragraphs_labeled]

    _map = {
        "User Access, Edit and Deletion": "Пользовательский доступ, изменение и удаление",
        "Other": "Другое",
        "Third Party Sharing/Collection": "Распространение и сбор от 3-х лиц",
        "First Party Collection/Use": "Сбор от 1-х лиц и использование",
        "Do Not Track": "Не отслеживать",
        "User Choice/Control": "Выбор пользователя",
        "Data Retention": "Удержание данных",
        "Policy Change": "Обновление политики",
        "International and Specific Audiences": "Международная и особая аудитории",
        "Data Security": "Безопасность данных"
    }

    paragraphs_translated = []
    for p in paragraphs_labeled:
        if _map[p[0].strip()] is not None:
            paragraphs_translated.append((_map[p[0].strip()], p[1]))

    opp_tfidf = make_model(paragraphs, model="tf-idf", load=load, file="models/opp_tfidf")
    topics = opp_tfidf.lsa_model.print_topics(num_topics=opp_tfidf.lsa_model.num_topics, num_words=10)

    render_amounts(paragraphs_translated)

    paragraphs_labeled = []

    get_opp_paragraphs(paragraphs_labeled)
    # with open(os.path.join(resources, "datasets/plain_policies/mi.com-global-about-privacy.html.txt"), 
    #           "r", encoding="utf-8") as fl:
    #     paragraphs_labeled.extend([("?", p) for p in fl.read().split("\n")])

    paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 100]
    paragraphs = [p[1] for p in paragraphs_labeled]

    paragraphs_labeled = render_groups_opp(opp_tfidf, paragraphs_labeled)
    render_amounts(paragraphs_labeled)

    # render_volumes(opp_tfidf, paragraphs_labeled, threshold=.15)


def work_iot(load=False):

    paragraphs_labeled = []

    # get_iot_paragraphs(paragraphs_labeled)

    # paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 100]
    # paragraphs = [p[1] for p in paragraphs_labeled]

    # iot_tfidf = make_model(paragraphs, model="tf-idf", load=load, file="models/iot_tfidf")
    # topics = iot_tfidf.lsa_model.print_topics(num_topics=iot_tfidf.lsa_model.num_topics, num_words=10)

    # print_topics(topics)

    # paragraphs_labeled = []
    # with open(os.path.join(resources, "datasets/plain_policies/mi.com-global-about-privacy.html.txt"), 
    #           "r", encoding="utf-8") as fl:
    #     paragraphs_labeled.extend([("?", p) for p in fl.read().split("\n")])

    # paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) > 0]

    # render_heatmap(topics)
    
    # render_affiliations(iot_tfidf, paragraphs_labeled)
    # render_volumes(iot_tfidf, paragraphs_labeled, threshold=.3)

    #  FIGURE
    # paragraphs_labeled = []
    # get_iot_paragraphs(paragraphs_labeled)
    # paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 100]
    # paragraphs = [p[1] for p in paragraphs_labeled]
    # iot_tfidf = make_model(paragraphs, model="tf-idf", load=load, file="models/iot_tfidf")
    # paragraphs_labeled, _, _ = render_groups(iot_tfidf, paragraphs_labeled)
    # render_amounts(paragraphs_labeled)

    #  FIGURE
    # paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 100]
    # paragraphs = [p[1] for p in paragraphs_labeled]
    # render_volumes(iot_tfidf, paragraphs_labeled, threshold=.2)
    # get_affiliation(iot_tfidf, paragraphs_labeled)
    # render_groups(iot_tfidf, paragraphs_labeled)

    #  FIGURE
    paragraphs_labeled = []
    paragraphs_labeled = get_iot_fulltexts(paragraphs_labeled)
    calculate_policies_lengths(paragraphs_labeled)

    #  FIGURE
    paragraphs_labeled = []
    get_iot_paragraphs(paragraphs_labeled)
    paragraphs_labeled = [p for p in paragraphs_labeled if len(p[1]) >= 1]
    calculate_lengths(paragraphs_labeled)


def main():

    # initialize()
    # restore_segments()
    # clean_iot()

    work_opp(load=True)
    # work_iot(load=True)

    # calculate_structure_elements_small()
    # clusterize_by_1_small()