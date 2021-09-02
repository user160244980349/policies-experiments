import json
import os

import plotly.graph_objects as go

import plotly.express as px
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


#################################################
#                                               #
#   Graph 1                                     #
#                                               #
#################################################

s, ss = 5, 15

lims = [(s * i, s * (i + 1)) for i in range(ss)]
ams = [f"{lim[0]}...{lim[1]}" for lim in lims]
vs = [0 for _ in range(ss)]

for i, lim in enumerate(lims):
    for stat in unique_stats:
        if lim[0] <= stat["headings"] < lim[1]:
            vs[i] += 1

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Headings")
    )
)

fig.add_bar(
    name="headings",
    x=ams,
    y=vs,
    showlegend=False
)

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="left",
        y=1,
        x=0
    ),
    colorway=[px.colors.qualitative.Dark24[0]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Presences')
fig.update_yaxes(showgrid=True, title_text='Number of policies')
fig.show()


#################################################
#                                               #
#   Graph 2                                     #
#                                               #
#################################################

s, ss = 5, 15

lims = [(s * i, s * (i + 1)) for i in range(ss)]
ams = [f"{lim[0]}...{lim[1]}" for lim in lims]
vs = [0 for _ in range(ss)]

for i, lim in enumerate(lims):
    for stat in unique_stats:
        if lim[0] <= stat["paragraphs"] < lim[1]:
            vs[i] += 1

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Paragraphs")
    )
)

fig.add_bar(
    name="paragraphs",
    x=ams,
    y=vs,
    showlegend=False
)

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="left",
        y=1,
        x=0
    ),
    colorway=[px.colors.qualitative.Dark24[1]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Presences')
fig.update_yaxes(showgrid=True, title_text='Number of policies')
fig.show()


#################################################
#                                               #
#   Graph 3                                     #
#                                               #
#################################################

s, ss = 1, 10

lims = [(s * i, s * (i + 1)) for i in range(ss)]
# ams = [f"{lim[0]}...{lim[1]}" for lim in lims]
ams = [f"{i}" for i in range(ss)]
vs = [0 for _ in range(ss)]

for i, lim in enumerate(lims):
    for stat in unique_stats:
        if lim[0] <= stat["tables"] < lim[1]:
            vs[i] += 1

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Tables")
    )
)

fig.add_bar(
    name="tables",
    x=ams,
    y=vs,
    showlegend=False
)

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="left",
        y=1,
        x=0
    ),
    colorway=[px.colors.qualitative.Dark24[2]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Presences')
fig.update_yaxes(showgrid=True, title_text='Number of policies')
fig.show()


#################################################
#                                               #
#   Graph 4                                     #
#                                               #
#################################################

s, ss = 1, 25

lims = [(s * i, s * (i + 1)) for i in range(ss)]
# ams = [f"{lim[0]}...{lim[1]}" for lim in lims]
ams = [f"{i}" for i in range(ss)]
vs = [0 for _ in range(ss)]

for i, lim in enumerate(lims):
    for stat in unique_stats:
        if lim[0] <= stat["unordered lists"] < lim[1]:
            vs[i] += 1

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Unordered lists")
    )
)

fig.add_bar(
    name="unordered lists",
    x=ams,
    y=vs,
    showlegend=False
)

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="left",
        y=1,
        x=0
    ),
    colorway=[px.colors.qualitative.Dark24[3]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Presences')
fig.update_yaxes(showgrid=True, title_text='Number of policies')
fig.show()


#################################################
#                                               #
#   Graph 5                                     #
#                                               #
#################################################

s, ss = 1, 10

lims = [(s * i, s * (i + 1)) for i in range(ss)]
# ams = [f"{lim[0]}...{lim[1]}" for lim in lims]
ams = [f"{i}" for i in range(ss)]
vs = [0 for _ in range(ss)]

for i, lim in enumerate(lims):
    for stat in unique_stats:
        if lim[0] <= stat["ordered lists"] < lim[1]:
            vs[i] += 1

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Ordered lists")
    )
)

fig.add_bar(
    name="ordered lists",
    x=ams,
    y=vs,
    showlegend=False
)

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="left",
        y=1,
        x=0
    ),
    colorway=[px.colors.qualitative.Dark24[4]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Presences')
fig.update_yaxes(showgrid=True, title_text='Number of policies')
fig.show()


#################################################
#                                               #
#   Graph 6                                     #
#                                               #
#################################################

s, ss = 5, 15

lims = [(s * i, s * (i + 1)) for i in range(ss)]
ams = [f"{lim[0]}...{lim[1]}" for lim in lims]
vs = [0 for _ in range(ss)]

for i, lim in enumerate(lims):
    for stat in unique_stats:
        if lim[0] <= stat["list items"] < lim[1]:
            vs[i] += 1

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="List items")
    )
)

fig.add_bar(
    name="list items",
    x=ams,
    y=vs,
    showlegend=False
)

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="left",
        y=1,
        x=0
    ),
    colorway=[px.colors.qualitative.Dark24[5]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Presences')
fig.update_yaxes(showgrid=True, title_text='Number of policies')
fig.show()
