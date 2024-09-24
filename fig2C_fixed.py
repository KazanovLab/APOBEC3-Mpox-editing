from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import json, urllib
import pandas as pd


app = Dash(__name__)

outfile = "plots/fig2C_fixed.html"

df = pd.read_csv("data/grantham_score_article_pos_aa.csv", sep=',')
df = df.reset_index()
df['parent_aa_v2'] = [x+'_observed' for x in df.parent_aa.tolist()]
df['mutated_aa_v2'] = [x+'_editing' for x in df.mutated_aa.tolist()]
df1 = df.groupby(['parent_aa_v2','mutated_aa_v2', 'grantham_rank_color'])['index'].count().reset_index()
df1.columns = ['source','target', 'grantham_rank_color', 'value']
df1 = df1.sort_values(by='value', ascending=True)

unique_source_target = list(pd.unique(df1[['source','target']].values.ravel('k')))

unique_source_target_label = [list(x)[0] for x in unique_source_target]

mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
print(mapping_dict)

df1['source'] = df1['source'].map(mapping_dict)
df1['target'] = df1['target'].map(mapping_dict)
print(df1)

new_dict = df1.to_dict(orient='list')
print(new_dict)


fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 20,
        thickness=30,
        line=dict(color='black', width=0.5),
        label = unique_source_target_label,
        color='#81B29A'
    ),
    link = dict(
        source= new_dict['source'],
        target = new_dict['target'],
        value = new_dict['value'],
        color = new_dict['grantham_rank_color']
    )

)
])
#legend={"yellow": "conservative", "pink": "moderately conservative", "dark blue": "moderately radical", "brown": "radical", "green": "synonymous"}
fig.update_layout(
    font_family="Arial",
    font_color="black",
    font_size=18,
    width=700,
    height=1000
)

fig.write_html(outfile)
app.run_server(debug=False)
