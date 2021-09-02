import plotly.express as px
import plotly.graph_objects as go

from collections import Counter

from lda.iot_dataset.figures.dependency import aggregate_groups
from lda.iot_dataset.figures.groups import groups
from lda.lda import LDA
from tools.fsys import files


paragraphs_labeled = []
fs = files("datasets/plain_policies", r".*")
for f in fs:
    with open(f, "r", encoding="utf-8") as fl:
        paragraphs_labeled.extend([p for p in fl.read().split("\n") if len(p) >= 100])

iot_tfidf = LDA(paragraphs_labeled, freq="tf-idf", topics_count=15, saved="models/iot_tfidf")

policies = []
fs = files("datasets/plain_policies", r".*")
for f in fs:
    with open(f, "r", encoding="utf-8") as fl:
        policies.append([("?", p) for p in fl.read().split("\n") if len(p) >= 100])

grouped = [aggregate_groups(iot_tfidf, p, groups)[1] for p in policies]
grouped = [Counter(g) for g in grouped]

keys = [g["name"] for g in groups]


#################################################
#                                               #
#   Graph 1                                     #
#                                               #
#################################################

stats1 = grouped[:296]

fig = go.Figure()

for i, k in enumerate(keys):
    fig.add_bar(
        name=k,
        y=[v[k] for v in stats1],
        x=[i for i in range(296)]
    )

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    # margin=dict(l=0, r=0, t=300, b=0),
    title="Privacy policies` aspects for each document",
    barmode="stack",
    width=2100,
    height=900,
    # legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     xanchor="left",
    #     y=1,
    #     x=0
    # ),
    colorway=px.colors.qualitative.Dark24,
    font=dict(
        size=24,
    ),
)

fig.update_xaxes(showgrid=True, title_text='Privacy policies` documents')
fig.update_yaxes(showgrid=True, title_text='Aspects` presences')
fig.show()


#################################################
#                                               #
#   Graph 2                                     #
#                                               #
#################################################

stats2 = grouped[296:592]

fig = go.Figure()

for i, k in enumerate(keys):
    fig.add_bar(
        name=k,
        y=[v[k] for v in stats2],
        x=[i for i in range(296, 592)]
    )

fig.update_annotations(
    font=dict(
        size=30,
    ),
)

fig.update_layout(
    # margin=dict(l=0, r=0, t=300, b=0),
    title="Privacy policies` aspects for each document",
    barmode="stack",
    width=2100,
    height=900,
    # legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     xanchor="left",
    #     y=1,
    #     x=0
    # ),
    colorway=px.colors.qualitative.Dark24,
    font=dict(
        size=24,
    ),
)

fig.update_xaxes(showgrid=True, title_text='Privacy policies` documents')
fig.update_yaxes(showgrid=True, title_text='Aspects` presences')
fig.show()
