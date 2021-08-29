import plotly.express as px
import plotly.graph_objects as go

from collections import Counter
from lda.iot_dataset.figures.dependency import aggregate_groups
from lda.iot_dataset.figures.groups import groups
from lda.lda import LDA
from tools.fsys import files


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

groupped = [aggregate_groups(iot_tfidf, p, groups)[1] for p in policies]
groupped = [Counter(g) for g in groupped]

stats1 = groupped[:296]
stats2 = groupped[296:592]

keys = [g["name"] for g in groups]

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
