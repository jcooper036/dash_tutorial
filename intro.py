import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#---------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv('intro_bees.csv')

df = df.groupby([
    'State',
    'ANSI',
    'Affected by',
    'Year',
    'state_code'
])['Pct of Colonies Impacted'].mean()
df = pd.DataFrame(df.reset_index())
print(df[:5])

#---------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(
        id="slct_year",
        options=[
            {'label':"2015", 'value':2015},
            {'label':"2016", 'value':2016},
            {'label':"2017", 'value':2017},
            {'label':"2018", 'value':2018},
        ],
        multi=False,
        value=2015,
        style={'width':"40%"}
    ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id="my_bee_map", figure={})
])


#---------------------------------------------------
# Call backs
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output('my_bee_map', 'figure'),],
    [Input('slct_year', 'value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = f"The year chosen by the user was: {option_slctd}"

    dff = df.copy()
    dff = dff.query(f"Year == {option_slctd}")
    dff = dff[dff["Affected by"] == 'Varroa_mites'] 

    fig = make_plot(dff)
    return container, fig

    #plotly express code

#---------------------------------------------------
# plotting code
def make_plot(dff):
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted' : '% of bee colonies'},
        template='plotly_dark'
    )
    return fig

#---------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)