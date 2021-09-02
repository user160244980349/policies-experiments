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

iot_tfidf = LDA(
    [p[1] for p in paragraphs_labeled],
    freq="tf-idf", topics_count=15, saved="models/iot_tfidf"
)

policies = []
fs = files("datasets/plain_policies", r".*")
for f in fs:
    with open(f, "r", encoding="utf-8") as fl:
        policies.append([("?", p) for p in fl.read().split("\n") if len(p) >= 100])

grouped = [aggregate_groups(iot_tfidf, p, groups)[1] for p in policies]
grouped = [Counter(g) for g in grouped]

keys = [g["name"] for g in groups]

s = Counter({})
for st in grouped:
    s += st


fig = go.Figure()

fig.add_pie(
    values=list(s.values()),
    text=list(s.keys()),
)

fig.update_annotations(
    font=dict(
        size=30,
    ),
)

fig.update_layout(
    title="Percentage relation of privacy policies` aspects",
    font=dict(
        size=24,
    ),
    width=1200,
    height=900,
    colorway=px.colors.qualitative.Dark24,
    showlegend=False,
    legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="left",
        x=1,
        y=1
    )
)
fig.show()
