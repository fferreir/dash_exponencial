import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.integrate import odeint
from numpy import heaviside
from textwrap import dedent
import plotly.graph_objects as go


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN, dbc.icons.FONT_AWESOME], requests_pathname_prefix='/dash_sli/' )
server = app.server

cabecalho = html.H1("Modelo SLI",className="bg-primary text-white p-2 mb-4")

descricao = dcc.Markdown(
    '''
    É apresentado o modelo exponenciald de crescimento populacional. No exercício a sugestão é que sejam consideradas taxas de variação por ano. Por exemplo, $$a=0.05 \\text{ ano}^{-1}$$ equivale a uma taxa de natalidade de 5% por ano.

.
    ''', mathjax=True
)

parametros = dcc.Markdown(
    '''
    * taxa de natalidade: $$a=0.05 \\text{ ano}^{-1}$$
    * taxa de mortalidade: natural $$b=0.01 \\text{ ano}^{-1}$$
    * mortalidade adicional gerada por algum fenômeno (p.ex. caça): $$c=0 \\text{ ano}^{-1}$$
    ''', mathjax=True
)
cond_inicial = dcc.Markdown(
    '''
    * condição inicial: $$N(0)=1$$
    ''', mathjax=True
)

perguntas = dcc.Markdown(
    '''
    1. Considere uma população com taxa de natalidade superior à de mortalidade. Por exemplo, $$a=0.10$$ e $$b=0.05$$ (com $$c=0$$). Estime qual o tempo necessário (em anos) para que o tamanho desta população aumente duas, cinco ou dez vezes.Inicie com a população com um indivíduo

    2. Para uma situação em que a taxa de mortalidade seja maior que a taxa de natalidade, calcule qual o tempo até a extinção da população. Por exemplo, para uma população com 1000 indivíduos e taxa de natalidade de $$10\\%$$ por ano, estime o tempo até a extinção, variando a taxa de mortalidade entre $$15\\%$$ e $$50\\%$$ por ano.

    3. Supondo uma situação em que a taxa de natalidade e a de mortalidade sejam iguais (população em equilíbrio), verifique em quanto tempo pode se extinguir uma população com 10000 animais quando sujeita à caça predatória com taxa $$c=0.10$$ por ano.
    ''', mathjax=True
)

textos_descricao = html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    descricao, title="Descrição do modelo"
                ),
                dbc.AccordionItem(
                    parametros, title="Parâmetros do modelo"
                ),
                dbc.AccordionItem(
                    cond_inicial, title="Condições iniciais"
                ),
                dbc.AccordionItem(
                    perguntas, title="Perguntas"
                ),
            ],
            start_collapsed=True,
        )
    )

ajuste_condicoes_iniciais = html.Div(
        [
            html.P("Ajuste das condições iniciais", className="card-header border-dark mb-3"),
            html.Div(
                [
                    dbc.Label(dcc.Markdown('''$$N$$ população inicial''', mathjax=True), html_for="n_init"),
                    dcc.Dropdown([1, 10, 100, 1000, 10000], 1, id="n_init"),
                ],
                className="m-2",
            ),

        ],
        className="card border-dark mb-3",
    )

ajuste_parametros = html.Div(
        [
            html.P("Ajuste dos parâmetros", className="card-header border-dark mb-3"),
            html.Div(
                [
                    dbc.Label(dcc.Markdown('''Taxa de natalidade ($$a$$)''', mathjax=True), html_for="a"),
                    dcc.Slider(id="a", min=0.05, max=0.5, value=0.1, tooltip={"placement": "bottom", "always_visible": False}),
                ],
                className="m-2",
            ),
            html.Div(
                [
                    dbc.Label(dcc.Markdown('''Taxa de mortalidade ($$b$$): ''', mathjax=True), html_for="b"),
                    dcc.Slider(id="b", min=0.01, max=0.5, value=0.05, tooltip={"placement": "bottom", "always_visible": False}, className="card-text"),
                ],
                className="m-1",
            ),
            html.Div(
                [
                    dbc.Label(dcc.Markdown('''Taxa de mortalidade adicional ($$c$$):''', mathjax=True), html_for="c"),
                    dcc.Slider(id="c", min=0.0, max=0.2, value=0.0, tooltip={"placement": "bottom", "always_visible": False}, className="card-text"),
                ],
                className="m-1",
            ),

        ],
        className="card border-dark mb-3",
    )

def ode_sys(state, t, a, b, c):
    n=state
    dn_dt=(a-b-c)*n
    return dn_dt

@app.callback(Output('population_chart', 'figure'),
              [Input('n_init', 'value'),
              Input('a', 'value'),
              Input('b', 'value'),
              Input('c', 'value')])
def gera_grafico(n_init, a, b, c):
    t_begin = 0.
    t_end = 70.
    t_nsamples = 10000
    t_eval = np.linspace(t_begin, t_end, t_nsamples)
    sol = odeint(func=ode_sys,
                    y0=[n_init],
                    t=t_eval,
                    args=( a, b, c))
    n = sol.flatten()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_eval, y=n, name='População',
                             line=dict(color='#00b400', width=4)))

    fig.update_layout(title='Crescimento Exponencial',
                       xaxis_title='Tempo (anos)',
                       yaxis_title='Número de indivíduos')
    return fig

app.layout = dbc.Container([
                cabecalho,
                dbc.Row([
                        dbc.Col(html.Div(ajuste_parametros), width=3),
                        dbc.Col(html.Div([ajuste_condicoes_iniciais,html.Div(textos_descricao)]), width=3),
                        dbc.Col(dcc.Graph(id='population_chart', className="shadow-sm rounded-3 border-primary",
                                style={'height': '500px'}), width=6),
                ]),
              ], fluid=True),


if __name__ == '__main__':
    app.run(debug=False)
