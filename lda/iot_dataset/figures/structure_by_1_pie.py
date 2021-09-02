import json
import os

import plotly.express as px
import plotly.graph_objects as go

from config import resources


hashes = []
unique_stats = []

with open(os.path.join(resources, "datasets/plain.json"), "r", encoding="utf-8") as f:
    stats = json.load(f)

for st in stats:
    if st["policy_hash"] not in hashes and st["statistics"] is not None:
        hashes.append(st["policy_hash"])
        unique_stats.append(st["statistics"])

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

fig = go.Figure()

fig.add_pie(
    values=list(s.values()),
    text=[k.capitalize() for k in s.keys()],
)

fig.update_annotations(
    font=dict(
        size=30,
    ),
)

fig.update_layout(
    title="Percentage relation of privacy policies` structure elements",
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
