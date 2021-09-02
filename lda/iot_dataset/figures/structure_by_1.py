import json
import os

import plotly.express as px
import plotly.graph_objects as go

from config import resources


#################################################
#                                               #
#   Graph 1                                     #
#                                               #
#################################################

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


fig = go.Figure()

for i, k in enumerate(keys):
    fig.add_bar(
        name=k.capitalize(),
        y=[v[k] for v in stats1],
        x=[i for i in range(296)]
    )

fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    title="Privacy policies` structure elements for each document",
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
fig.update_yaxes(showgrid=True, title_text='Structure elements` presences')
fig.show()


#################################################
#                                               #
#   Graph 2                                     #
#                                               #
#################################################

fig = go.Figure()

for i, k in enumerate(keys):
    fig.add_bar(
        name=k.capitalize(),
        y=[v[k] for v in stats2],
        x=[i for i in range(296, 592)]
    )


fig.update_annotations(
    font=dict(
        size=40,
    ),
)

fig.update_layout(
    title="Privacy policies` structure elements for each document",
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
fig.update_yaxes(showgrid=True, title_text='Structure elements` presences')
fig.show()
