import json
import os

import plotly.express as px
import plotly.graph_objects as go

from config import resources


_map = {
    "list items": "Элемент списка",
    "ordered lists": "Нумерованный список",
    "unordered lists": "Ненумерованный список",
    "tables": "Таблица",
    "paragraphs": "Абзац",
    "headings": "Заголовок"
}

hashes = []
unique_stats = []

with open(os.path.join(resources, "datasets/plain.json"), "r", encoding="utf-8") as f:
    stats = json.load(f)

for s in stats:
    if s["policy_hash"] not in hashes and s["statistics"] is not None:
        hashes.append(s["policy_hash"])
        unique_stats.append(s["statistics"])

stats1 = unique_stats[:296]
stats2 = unique_stats[296:592]

keys = ["list items", "ordered lists", "unordered lists", "tables", "paragraphs", "headings"]

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
