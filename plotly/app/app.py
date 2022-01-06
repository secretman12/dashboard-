import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from sqlalchemy import create_engine
from plotly.validator_cache import ValidatorCache
from plotly.graph_objects import Layout




#kalispera se opoion diavazei to kwdika
#yparxoun polla  pandas mesa

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


def getData():
    mmydb = create_engine("mysql://user:pass@db:3306/test_db")

    df = pd.read_sql('select * from arxeia ', con=mmydb)
    print(df)

    df['yyyy-mm'] = pd.to_datetime(df['eos']).dt.to_period('M')
    df['yyyy-mm'] = df['yyyy-mm'].dt.strftime('%b-%Y')#afto edo pera to kano giati thelw to mina kai tin xronologia gia pio meta 
    df=df.drop_duplicates(subset=['eos'], keep='last')
    df = df.drop(['apo', 'eos', 'id', 'arithmos_prosorinon_ao'], axis=1)# ta kano drop the den ta thelw pote aplos yparxoun stin vasi 
    return df.to_dict()


cards = {
    dbc.Card(
        [

            html.H2(className="card-title", id='output1'),
            html.P("ο Μεσος ορος ειναι των 7 ημερων",
                   className="card-text"),   #einai ta cards tou bootsrap   color ktl 
        ],
        body=True,
        color="light",),
    dbc.Card(
        [
            html.H2(className="card-title", id='output2'),
            html.P("Το συνολικο αθροισμα", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,),
    dbc.Card(
        [
            html.H2(className="card-title", id='output3'),
            html.P("Το τελευταιο 24ωρο βγηκανε", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),


}


app.layout = html.Div([
    html.Hr(),
    dcc.Interval('graph-update', interval=100000, n_intervals=0),# afto einai to proto simantiko einai kathe pote tha kanei update ta dedomena se milisecond
    dbc.Row([dbc.Col(card) for card in cards]), 
    dcc.Store(id="table"), #afto apothikevi tha dedomena tou update
    html.Br(),
    html.H3("ΤΟ ΑΘΡΟΙΣΜΑ ΓΙΑ 7 ΜΕΡΕΣ", className="text-success text-center"),
    dcc.Graph(id="bar-chart"),
    html.H3("ΣΥΝΟΛΙΚΟ ΑΔΕΙΩΝ ΓΙΑ ΚΑΘΕ ΜΗΝΑ", className="text-info text-center"),
    dcc.Graph(id="line-chart"),
])


@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('graph-update', 'n_intervals')])
def updateTable(n_intervals):
    x = getData() #afto einai i enimerosi ton dedomena apo to interval vlepoume oti epistefei to table kai  ta data
    return x


@app.callback(Output("bar-chart", "figure"),
              Input("table", "data"),
              )
def update_bar_chart(data): #to barchart diagramma 
    dff = data 
    df1 = pd.DataFrame(dff) # afto tha to deite  kai pio kato gia to exo parei san json apo to return tis fuction einai anagkastika etsi  
    df1 = df1.drop(['yyyy-mm'], axis=1)
    df1=df1.rename(columns={"anatolikis_makedonias_tharkis": "Ανατολικής Μακεδονίας και Θράκης", "attikis": "Αττικής", "voreio_agaio": "Βορείου Αιγαίου","dytikis_elladas": "Δυτικής Ελλάδας","dytikis_makedonias": "Δυτικής Μακεδονίας", \
     "ipeiros": "Ήπειρος","thessalias": "Θεσσαλίας","ionion_nision": "Ιονίων Νήσων","kentrikis_makedonias": "Κεντρική Μακεδονία","kritis": "Κρήτης","notio_aigaio": "Νοτίου Αιγαίου","pelloponisos": "Πελοποννήσου","stereas_elladas": "Στερεάς Ελλάδας"})
    df1 = df1.iloc[-7:] # perno tis telefteies 7 grammes
    df1 = df1.sum(numeric_only=True).reset_index(name='ΣΥΝΟΛΟ 7 ΗΜΕΡΩΝ')
    df1 = df1.rename(columns={"index": "Περιφερειες"})
    df1 = df1.sort_values(by='ΣΥΝΟΛΟ 7 ΗΜΕΡΩΝ', ascending=False) # kanei sort gia na einai pio oraio :D
    barchart = px.bar(
        data_frame=df1,
        x=df1['Περιφερειες'],
        y=df1['ΣΥΝΟΛΟ 7 ΗΜΕΡΩΝ'],
        color='Περιφερειες',
        height=800,
        text=df1['ΣΥΝΟΛΟ 7 ΗΜΕΡΩΝ'],
    )
    return (barchart)


# linecart
@app.callback(Output("line-chart", "figure"), Input("table", "data"))
def update_line_chart(data):
    df4 = data
    df4 = pd.DataFrame(df4)
    df4['yyyy-mm'] = pd.to_datetime(df4['yyyy-mm']).dt.to_period('M')
    df4 = df4.groupby([df4['yyyy-mm'].dt.strftime('%b-%Y')]
                      ).sum().reset_index() # afto  kanei group tis imerominies oles mazi  gia na pane se mia 
    df4 = df4.T.reset_index().reindex()
    df4 = df4.rename(columns=df4.iloc[0])
    df4 = df4.drop(df4.index[0])
    df4 = df4.rename(columns={"yyyy-mm": "nomoi"})
    df4 = df4.sum(axis=0).reset_index(name='Total Amount1') # to reset index einai aparaitito 
    df4 = df4.rename(columns={"index": "imerominies"})
    df4 = df4.drop([0]) 
    df4['imerominies'] = pd.to_datetime(df4['imerominies'])
    # print(df4)
    df4 = df4.sort_values("imerominies")
    df4['imerominies'] = df4['imerominies'].dt.strftime('%b-%Y')
    fig = px.line(df4, x='imerominies', y="Total Amount1",
                  height=600, markers=True)
    return (fig)


@app.callback(
    [
        Output('output1', 'children'),
        Output('output2', 'children'), 
        Output('output3', 'children'),

    ],
    Input('table', 'data')
)
#ola afta ta kato einai gia tis  cards
def update_cards(data):
    dff = data
    df1 = pd.DataFrame(dff)
    df1 = df1.drop(['yyyy-mm'], axis=1)
    df1 = df1.iloc[-7:]
    df1 = df1.sum(numeric_only=True).reset_index(name='Total Amount')
    df1 = df1.sort_values(by='Total Amount', ascending=False)
    output1 = df1['Total Amount'].mean().astype('int64')

    df2 = pd.DataFrame(dff)
    df2 = df2.drop(['yyyy-mm'], axis=1)
    df2 = df2.sum(numeric_only=True).reset_index(name='Total Amount')
    df2 = df2.sort_values(by='Total Amount', ascending=False)
    output2 = df2['Total Amount'].sum()

    df3 = pd.DataFrame(dff)
    df3 = df3.drop(['yyyy-mm'], axis=1)
    df3 = df3.iloc[-1:]
    df3 = df3.sum(numeric_only=True).reset_index(name='Total Amount')
    df3 = df3.sort_values(by='Total Amount', ascending=False)
    output3 = df3['Total Amount'].sum()

    return output1, output2, output3


if __name__ == '__main__':
    app.run_server()
