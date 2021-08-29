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
