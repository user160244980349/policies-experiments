import os

import plotly.express as px
import plotly.graph_objects as go

from config import resources
from tools.fsys import files


#################################################
#                                               #
#   Graph 1                                     #
#                                               #
#################################################

paragraphs_labeled = []

fs = files("datasets/plain_policies", r".*")
for f in fs:
    with open(f, "r", encoding="utf-8") as fl:
        paragraphs_labeled.extend([("?", fl.read())])

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

ams = ["0...3000", "3000...6000", "6000...10000", "10000...15000", "15000...25000",
       "25000...35000", "35000...45000", "45000...60000", "60000...+oo"]

vs = [below_100, below_200, below_300, below_400, below_500,
      below_600, below_700, below_800, more_800]

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Distribution of documents by length")
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
    colorway=[px.colors.qualitative.Dark24[0]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Length in symbols')
fig.update_yaxes(showgrid=True, title_text='Number of paragraphs')
fig.show()


#################################################
#                                               #
#   Graph 2                                     #
#                                               #
#################################################

paragraphs_labeled = []

fs = files("datasets/plain_policies", r".*")
for f in fs:
    with open(f, "r", encoding="utf-8") as fl:
        paragraphs_labeled.extend([("?", p) for p in fl.read().split("\n")])

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

ams = ["0...200", "200...300", "300...400", "400...500",
       "500...600", "600...700", "700...800", "800...1600", "1600...+oo"]

vs = [below_200, below_300, below_400, below_500,
      below_600, below_700, below_800, below_1600, more_800]

fig = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Distribution of paragraphs by length")
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
    colorway=[px.colors.qualitative.Dark24[1]],
    font=dict(
        size=30,
    ),
    width=900,
    height=900,
)

fig.update_xaxes(showgrid=True, title_text='Length in symbols')
fig.update_yaxes(showgrid=True, title_text='Number of policies')
fig.show()
